#!/usr/bin/env python3
"""Print your score. This is the output you screenshot when an assignment asks for one.

    python3 tests/scorecard.py            # the default for this repo
    python3 tests/scorecard.py 5          # only Week 5 (Holdfast)
    python3 tests/scorecard.py all        # every test target

Run it from the top of your repository -- the folder that holds CMakeLists.txt,
not from inside tests/. It configures and builds what it needs, runs the
Google Test suites, and prints a scorecard with your identity in the header.

What gets scored lives in tests/scorecard.json, never in this file, so the same
script ships unchanged in every CS 1410 repo. Do not edit either file.

Sections are all-or-nothing: every test in a section must pass to earn its
points. The "n of m" column is there so you can see how close you are, not to
award partial credit.

Each scored target is built on its own. A compile error in one target (say,
next week's tests that you haven't started) scores that target 0 but never
blocks the others.
"""

import datetime
import json
import os
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8")

WIDTH = 66
CONFIG = os.path.join("tests", "scorecard.json")
BUILD = "build"

GREEN, RED, DIM, RESET = "\033[32m", "\033[31m", "\033[2m", "\033[0m"


def use_color():
    return sys.stdout.isatty() and os.environ.get("TERM", "") != "dumb"


def _git(*args):
    try:
        out = subprocess.run(("git",) + args, capture_output=True, text=True)
        return out.stdout.strip() if out.returncode == 0 else ""
    except OSError:
        return ""


def identity():
    """Who ran this and where, for the header of the scorecard.

    Taken from the repository, never typed in: the remote says whose GitHub
    repo this is, and user.name / user.email are stamped on every commit.
    """
    remote = _git("remote", "get-url", "origin")
    repo = ""
    if remote:
        repo = remote.rstrip("/")
        if repo.endswith(".git"):
            repo = repo[:-4]
        # https://github.com/OWNER/REPO or git@github.com:OWNER/REPO
        repo = "/".join(repo.replace(":", "/").split("/")[-2:])

    who = " ".join(x for x in (_git("config", "--get", "user.name"),
                               _git("config", "--get", "user.email")) if x)
    commit = _git("rev-parse", "--short", "HEAD")
    dirty = " (uncommitted changes)" if _git("status", "--porcelain") else ""
    return {
        "repo": repo or "(no git remote -- did you clone, or download a ZIP?)",
        "who": who or "(git identity not set -- see Lab 0)",
        "commit": (commit + dirty) if commit else "(no commits yet)",
    }


def configure():
    if os.path.exists(os.path.join(BUILD, "CMakeCache.txt")):
        return
    print("No build folder yet -- configuring. This takes a minute the first "
          "time while Google Test downloads.\n")
    if subprocess.run(["cmake", "--preset", "default"]).returncode != 0:
        sys.exit("cmake configure failed. Fix the error above, then run this "
                 "again.")


def build(target):
    """Build one target quietly. Returns (ok, compiler output)."""
    proc = subprocess.run(["cmake", "--build", BUILD, "--target", target],
                          capture_output=True, text=True)
    return proc.returncode == 0, proc.stdout + proc.stderr


def run(target):
    """Run a gtest executable, return {suite: (passed, total)}."""
    exe = os.path.join(BUILD, target)
    out = os.path.join(tempfile.gettempdir(), "cs1410_%s.json" % target)
    if os.path.exists(out):
        os.remove(out)
    # A non-zero exit just means tests failed, which is expected while you are
    # still working -- so the return code is deliberately ignored. The timeout
    # catches an infinite loop or a test waiting on std::cin.
    try:
        subprocess.run([exe, "--gtest_output=json:" + out],
                       stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, timeout=30)
    except subprocess.TimeoutExpired:
        return None
    if not os.path.exists(out):
        return None  # crashed (segfault, abort) before gtest wrote results
    with open(out, encoding="utf-8") as fh:
        results = json.load(fh)

    counts = {}
    for suite in results.get("testsuites", []):
        # Parameterized suites are reported as "Prefix/SuiteName".
        name = suite.get("name", "").split("/")[-1]
        passed = total = 0
        for case in suite.get("testsuite", []):
            total += 1
            if not case.get("failures"):
                passed += 1
        prev = counts.get(name, (0, 0))
        counts[name] = (prev[0] + passed, prev[1] + total)
    return counts


def select(targets, default, arg):
    if arg is None:
        arg = default
    if arg == "ask":
        # A project with many targets (the semester game has one per week) must
        # not guess. CS 1400's check_week.py defaulted to the newest week it
        # could find, and a pile of Week 5 submissions came back 0 / 20 with
        # nothing wrong with the code. Here the screenshot IS the submission.
        names = ", ".join(t["target"].replace("_tests", "") for t in targets)
        sys.exit("Name the week you want to score, for example:\n"
                 "    python tests/scorecard.py 2\n\n"
                 "Available here: " + names)
    if arg == "all":
        return targets
    if arg == "latest":
        return targets[-1:]
    if arg.isdigit():
        arg = "week%02d" % int(arg)
    chosen = [t for t in targets if arg in t["target"]]
    if not chosen:
        sys.exit("Nothing in %s matches '%s'. Choices: %s, all" %
                 (CONFIG, arg, ", ".join(t["target"] for t in targets)))
    return chosen


def main():
    if not os.path.exists("CMakeLists.txt") or not os.path.exists(CONFIG):
        sys.exit("Run this from the top of your repository -- the folder that "
                 "holds CMakeLists.txt, not from inside tests/.")
    with open(CONFIG, encoding="utf-8") as fh:
        config = json.load(fh)

    targets = select(config["targets"], config.get("default", "all"),
                     sys.argv[1] if len(sys.argv) > 1 else None)
    configure()
    color = use_color()

    def line(text, ok=None):
        if color and ok is not None:
            text = (GREEN if ok else RED) + text + RESET
        print(text)

    who = identity()
    print("")
    print("=" * WIDTH)
    print(("YOUR SCORE -- " + config["title"]).center(WIDTH))
    print("=" * WIDTH)
    print("  %-13s %s" % ("Repository", who["repo"]))
    print("  %-13s %s" % ("Committed by", who["who"]))
    print("  %-13s %s" % ("Commit", who["commit"]))
    print("  %-13s %s" % ("Run at",
                          datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

    earned = possible = 0
    failed_builds = []
    for t in targets:
        print("-" * WIDTH)
        print("  " + t["label"])
        ok, log = build(t["target"])
        counts = run(t["target"]) if ok else None
        if not ok:
            failed_builds.append((t["target"], log))
            line("    does not compile yet -- see the errors below", False)
        elif counts is None:
            line("    crashed or timed out -- run ./build/%s to see why" %
                 t["target"], False)
        for sec in t["sections"]:
            possible += sec["points"]
            passed = total = 0
            if counts:
                passed = sum(counts.get(s, (0, 0))[0] for s in sec["suites"])
                total = sum(counts.get(s, (0, 0))[1] for s in sec["suites"])
            complete = total > 0 and passed == total
            if complete:
                earned += sec["points"]
            line("    %-36s %2d of %-2d  %2d/%-2d" %
                 (sec["name"], passed, total,
                  sec["points"] if complete else 0, sec["points"]), complete)

    print("=" * WIDTH)
    pct = (earned * 100.0 / possible) if possible else 0.0
    line("  %-40s %8s %3d/%-3d (%.0f%%)" % ("TOTAL", "", earned, possible, pct),
         earned == possible)
    print("=" * WIDTH)

    for target, log in failed_builds:
        errors = [l for l in log.splitlines() if "error" in l.lower()][:12]
        print("")
        print("  %s compile errors (first %d):" % (target, len(errors)))
        for e in errors:
            print("    " + e.strip())

    if earned < possible:
        print("")
        print("  Sections are all-or-nothing. To see exactly which tests fail:")
        print("")
        print("      ./build/%s --gtest_brief=1" % targets[-1]["target"])
    print("")

    # Exit 0 always. This is a report, not a gate; a non-zero exit here would
    # make it look like the script itself had broken.
    return 0


if __name__ == "__main__":
    sys.exit(main())
