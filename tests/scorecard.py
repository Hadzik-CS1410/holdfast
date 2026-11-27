#!/usr/bin/env python3
"""Print your score. This is the output you screenshot when an assignment asks for one.

    python3 tests/scorecard.py            # the default for this repo
    python3 tests/scorecard.py arrays     # only that session (Holdfast)
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
        "pushed": pushed(),
        "branch": branch_line(),
    }


def branch_line():
    """Which branch, and a nudge if it is the wrong one.

    A pull request needs a branch to open from, and the most common way to end
    up without one is to never leave main. git can answer this for free; it
    cannot answer "is there a pull request", because a pull request is a GitHub
    object and not a git one. So the screenshot carries the branch, and the
    instructor's checker confirms the pull request.
    """
    name = _git("rev-parse", "--abbrev-ref", "HEAD")
    if not name:
        return "(no commits yet)"
    if name in ("main", "master"):
        return name + "   <- work belongs on its own branch: git switch -c week-NN"
    return name


def pushed():
    """Is the work that just scored actually on GitHub?

    The commit line already betrays a dirty tree or an empty repo, so a student
    who never commits is visible in their own screenshot. A student who commits
    and never PUSHES was not: the screenshot looked perfect and the repository
    was empty. CS 1400 had a run of exactly that.

    No network needed. Git already stores where origin was when you last
    cloned or pushed, so counting commits since then is a local question -- and
    for a student who has never pushed, that count is simply all of them.
    """
    branch = _git("rev-parse", "--abbrev-ref", "HEAD")
    if not branch:
        return "no -- nothing committed yet"
    # Prefer the branch's own upstream; fall back to origin/<branch>, then to
    # origin/main, so this reads sensibly on a week branch too.
    for ref in ("@{upstream}", "origin/" + branch, "origin/main"):
        if _git("rev-parse", "--verify", "--quiet", ref):
            ahead = _git("rev-list", "--count", ref + "..HEAD")
            if not ahead.isdigit():
                break
            n = int(ahead)
            if n == 0:
                return "yes"
            return ("NO -- %d commit%s not on GitHub. Run: git push"
                    % (n, "" if n == 1 else "s"))
    return "unknown -- no origin to compare against (did you clone?)"


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
        names = ", ".join(t["target"].replace("_tests", "").replace("_", "-")
                          for t in targets)
        sys.exit("Name the session you want to score, for example:\n"
                 "    python tests/scorecard.py cpp-basics\n\n"
                 "Available here: " + names)
    if arg == "all":
        return targets
    if arg == "latest":
        return targets[-1:]
    # Sessions are named for their module, not numbered: `scorecard.py
    # cpp-basics`. Targets spell that with underscores because a dash is not
    # legal in a CMake target name, so accept either.
    arg = arg.replace("-", "_")
    chosen = [t for t in targets if arg in t["target"]]
    if not chosen:
        sys.exit("Nothing in %s matches '%s'. Choices: %s, all" %
                 (CONFIG, arg, ", ".join(t["target"] for t in targets)))
    return chosen


def main():
    args = [a for a in sys.argv[1:] if a != "--json"]
    as_json = "--json" in sys.argv[1:]
    if not os.path.exists("CMakeLists.txt") or not os.path.exists(CONFIG):
        sys.exit("Run this from the top of your repository -- the folder that "
                 "holds CMakeLists.txt, not from inside tests/.")
    with open(CONFIG, encoding="utf-8") as fh:
        config = json.load(fh)

    targets = select(config["targets"], config.get("default", "all"),
                     args[0] if args else None)
    configure()
    color = use_color() and not as_json

    out = []                      # every printed line, for --json

    def line(text, ok=None):
        if color and ok is not None:
            text = (GREEN if ok else RED) + text + RESET
        if as_json:
            out.append(text)
        else:
            print(text)

    def say(text=""):
        if as_json:
            out.append(text)
        else:
            print(text)

    who = identity()
    say("")
    say("=" * WIDTH)
    say(("YOUR SCORE -- " + config["title"]).center(WIDTH))
    say("=" * WIDTH)
    say("  %-13s %s" % ("Repository", who["repo"]))
    say("  %-13s %s" % ("Committed by", who["who"]))
    say("  %-13s %s" % ("Commit", who["commit"]))
    # Printed in the header, not at the bottom, so it is inside any screenshot
    # that shows the score. Part of the submission, not a footnote to it.
    say("  %-13s %s" % ("Pushed", who["pushed"]))
    say("  %-13s %s" % ("Branch", who["branch"]))
    say("  %-13s %s" % ("Run at",
                          datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

    earned = possible = 0
    failed_builds = []
    detail = []
    for t in targets:
        say("-" * WIDTH)
        say("  " + t["label"])
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
            detail.append({"target": t["target"], "section": sec["name"].strip(),
                           "tests_passed": passed, "tests_total": total,
                           "points": sec["points"] if complete else 0,
                           "points_possible": sec["points"]})
            line("    %-36s %2d of %-2d  %2d/%-2d" %
                 (sec["name"], passed, total,
                  sec["points"] if complete else 0, sec["points"]), complete)

    say("=" * WIDTH)
    pct = (earned * 100.0 / possible) if possible else 0.0
    line("  %-40s %8s %3d/%-3d (%.0f%%)" % ("TOTAL", "", earned, possible, pct),
         earned == possible)
    say("=" * WIDTH)

    if as_json:
        json.dump({"title": config["title"], "repo": who["repo"],
                   "who": who["who"], "commit": who["commit"],
                   "pushed": who["pushed"], "branch": who["branch"],
                   "earned": earned, "possible": possible,
                   "sections": detail,
                   "report": "\n".join(out)},
                  sys.stdout, indent=2)
        print("")
        return 0 if earned == possible else 0

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

    # The tag, for a repo that holds more than one session.
    #
    # Nothing automates this. sync.py runs at the START of a session and
    # cannot know which commit you will finish on, and the scorecard will not
    # create tags behind your back. So it is yours to type -- and the script
    # that grades you looks for it, falling back to your merged pull request
    # if it is missing. This line exists because a step nobody is reminded of
    # is a step half the class skips.
    # "ask" is the marker for a repo that holds many sessions -- the same flag
    # that stops a bare run from guessing which one you meant. Counting
    # targets instead would stay silent all through the first session, when
    # only one is built, which is exactly when the habit has to form.
    if config.get("default") == "ask":
        name = targets[-1]["target"].replace("_tests", "").replace("_", "-")
        tagged = _git("tag", "--points-at", "HEAD")
        print("")
        if name in tagged.split():
            print("  Tagged        %s points at this commit" % name)
        else:
            print("  Tag this commit before you submit -- it is how your")
            print("  screenshot is matched to your code later:")
            print("")
            print("      git tag %s && git push origin %s" % (name, name))
    print("")

    # Exit 0 always. This is a report, not a gate; a non-zero exit here would
    # make it look like the script itself had broken.
    return 0


if __name__ == "__main__":
    sys.exit(main())
