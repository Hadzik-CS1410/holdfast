"""
Holdfast -- weekly sync

Run this at the start of every Holdfast session to get this week's work:

    python sync.py

It is safe to run any time, and safe to run twice. If something needs your
attention it will say exactly what to do.

You do not need to understand this file. Do not edit it -- it arrives again
every week, and your changes would be overwritten.
"""
import datetime
import json
import os
import subprocess
import sys

# The env var lets the course build point this at a throwaway repo, so the
# delivery harness exercises this exact file rather than a copy of it.
UPSTREAM_URL = os.environ.get(
    "HOLDFAST_UPSTREAM", "https://github.com/Hadzik-CS1410/holdfast.git")
UPSTREAM_BRANCH = "weeks"
REF = "upstream/" + UPSTREAM_BRANCH

REPO = os.path.dirname(os.path.abspath(__file__))
MANIFEST = "weeks.json"

# Fetched before anything else, so a sync always runs against the current
# calendar and the current scripts.
SELF_PATHS = (MANIFEST, "sync.py", "catchup.py")

GREEN, YELLOW, RED, DIM, BOLD, OFF = (
    "\033[92m", "\033[93m", "\033[91m", "\033[2m", "\033[1m", "\033[0m")


def say(msg="", color=""):
    print(f"{color}{msg}{OFF}" if color else msg)


def rule():
    say("-" * 64, DIM)


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO,
                          capture_output=True, text=True)


def out(*args):
    return git(*args).stdout.strip()


def stop(title, *lines):
    say()
    rule()
    say("  " + title, RED + BOLD)
    rule()
    for line in lines:
        say("  " + line)
    say()
    sys.exit(1)


# --------------------------------------------------------------- the calendar


def load_weeks():
    path = os.path.join(REPO, MANIFEST)
    if not os.path.exists(path):
        stop("weeks.json is missing.",
             "That file is mine and should always be here. Tell your",
             "instructor -- do not try to recreate it.")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh).get("weeks", [])


def unlocked(weeks, forced):
    """Weeks the calendar has reached, oldest first."""
    if forced is not None:
        return [w for w in weeks if int(w["week"]) <= forced]

    now = datetime.datetime.now(datetime.timezone.utc)
    open_weeks = []
    for week in weeks:
        try:
            when = datetime.datetime.fromisoformat(week["unlock"])
        except (KeyError, ValueError):
            continue
        if when.tzinfo is None:                     # treat a bare time as UTC
            when = when.replace(tzinfo=datetime.timezone.utc)
        if when <= now:
            open_weeks.append(week)
    return open_weeks


def next_locked(weeks, open_weeks):
    numbers = {w["week"] for w in open_weeks}
    for week in weeks:
        if week["week"] not in numbers:
            return week
    return None


# ------------------------------------------------------------------ delivery


def deliver(paths):
    """Check out paths from upstream. Not a merge: a week that is not listed
    stays out of your repository even though it exists upstream."""
    wanted = [p for p in paths if p]
    if not wanted:
        return False
    result = git("checkout", REF, "--", *wanted)
    if result.returncode != 0:
        # A path in the manifest that upstream does not have yet is a mistake
        # on my side, not yours -- say so plainly rather than failing silently.
        stop("A file this week needs is missing upstream.",
             "This is my mistake, not yours. Show your instructor:",
             "",
             *result.stderr.strip().splitlines()[:5])
    return True


def remove(paths):
    gone = []
    for path in paths or []:
        if os.path.exists(os.path.join(REPO, path)):
            git("rm", "-q", "--", path)
            gone.append(path)
    return gone


def changes_staged():
    """{path: 'A'|'M'} for what the delivery actually changed."""
    text = out("diff", "--cached", "--name-status", "HEAD")
    changed = {}
    for line in text.splitlines():
        bits = line.split("\t")
        if len(bits) >= 2:
            changed[bits[-1]] = bits[0][0]
    return changed


# ---------------------------------------------------------------------- main


def main():
    forced = None
    if "--week" in sys.argv:
        try:
            forced = int(sys.argv[sys.argv.index("--week") + 1])
        except (IndexError, ValueError):
            sys.exit("Usage: python sync.py [--week N]")

    say()
    say("  Holdfast -- weekly sync", BOLD)
    rule()

    # --- 0. git, and are we in the repository? ------------------------------
    if git("rev-parse", "--git-dir").returncode != 0:
        stop("This folder isn't a git repository.",
             "Run this from inside your holdfast folder -- the one with",
             "README.md in it.")

    # --- 1. main only -------------------------------------------------------
    # Delivering my files into your week branch would make your pull request
    # claim you changed eleven files when you changed three -- and that number
    # is the one you log every week.
    branch = out("rev-parse", "--abbrev-ref", "HEAD")
    if branch != "main":
        stop(f"You're on the '{branch}' branch.",
             "Sync onto main, then branch for the week:",
             "",
             "    git switch main",
             "    python sync.py",
             f"    git switch -c {branch}" if branch != "HEAD" else
             "    git switch -c week-NN",
             "",
             "Sync first, then branch. Nothing is lost -- your branch is",
             "still there and you'll switch straight back to it.")

    # --- 2. uncommitted work blocks a delivery ------------------------------
    dirty = out("status", "--porcelain")
    if dirty:
        say()
        rule()
        say("  Commit your work first", YELLOW + BOLD)
        rule()
        say("  You have changes that aren't committed. Save them before this")
        say("  week's files arrive, so nothing can be overwritten:")
        say()
        say("    git add -A", BOLD)
        say('    git commit -m "my work so far"', BOLD)
        say()
        say("  Then run  python sync.py  again.")
        say()
        say("  Not committed yet:", DIM)
        for line in dirty.splitlines()[:10]:
            say("    " + line, DIM)
        say()
        sys.exit(1)

    # --- 3. connect to the class repo ---------------------------------------
    if "upstream" not in out("remote").split():
        say("  Connecting to the class repo for the first time...")
        if git("remote", "add", "upstream", UPSTREAM_URL).returncode != 0:
            stop("Couldn't connect to the class repo.",
                 "Ask your instructor for help.")
        say("  Connected.", GREEN)

    # --- 4. fetch -----------------------------------------------------------
    say("  Checking for new files...")
    if git("fetch", "-q", "upstream", UPSTREAM_BRANCH).returncode != 0:
        stop("Couldn't reach GitHub.",
             "Check your internet connection and try again.",
             "",
             "If you're on campus wifi and it still fails, tell your",
             "instructor -- it may be a GitHub sign-in problem.")

    # --- 5. update the calendar and these scripts, before using them --------
    deliver([p for p in SELF_PATHS
             if git("cat-file", "-e", f"{REF}:{p}").returncode == 0])
    script_changed = "sync.py" in changes_staged()

    weeks = load_weeks()
    open_weeks = unlocked(weeks, forced)
    if not open_weeks:
        git("reset", "-q")
        say()
        say("  Nothing has opened yet. Come back on the day of the first", GREEN)
        say("  session and run this again.", GREEN)
        say()
        return

    # --- 6. deliver every unlocked week ------------------------------------
    # Re-running costs nothing: an unchanged file produces no change.
    tracked = set(out("ls-files").split())
    paths, removes = [], []
    for week in open_weeks:
        for path in week.get("delivers", []):
            # A handed-over file is yours the moment it arrives. I never send
            # it again -- so if you already have it, it is skipped here even
            # though the manifest still lists it.
            if path in week.get("hands_over", []) and path in tracked:
                continue
            paths.append(path)
        removes += week.get("removes", [])

    deliver(paths)
    dropped = remove(removes)
    changed = changes_staged()

    latest = open_weeks[-1]

    # Nothing new is the normal case for a second run in the same week -- and
    # it still has to answer "what am I doing and how do I score it", because
    # that is why a student runs this.
    if not changed and not dropped:
        git("reset", "-q")
        say()
        say("  You already have everything. Nothing new this week yet.", GREEN)
        report_week(latest)
        report_next(weeks, open_weeks)
        return

    git("commit", "-q", "-m",
        f"sync: week {latest['week']:02d} -- {latest.get('title', '')}".strip())

    # --- 7. say what arrived ------------------------------------------------
    new = sorted(p for p, kind in changed.items() if kind == "A")
    updated = sorted(p for p, kind in changed.items() if kind == "M")

    if new:
        say()
        say("  New:", GREEN + BOLD)
        for path in new:
            say("    " + path, GREEN)
    if updated:
        say()
        say("  Updated -- worth another look:", BOLD)
        for path in updated:
            say("    " + path, BOLD)
        say("  You already had these. Something changed in them, so open", DIM)
        say("  them again even if you finished that week.", DIM)
    if dropped:
        say()
        say("  Retired (you don't need these any more):", DIM)
        for path in dropped:
            say("    " + path, DIM)

    report_week(latest)
    report_next(weeks, open_weeks)

    if script_changed:
        say()
        say("  Note: sync.py itself was updated. Run it once more so the new", YELLOW)
        say("  version is the one that runs.", YELLOW)


def report_week(latest):
    week_no = latest["week"]
    briefing = f"weeks/week{week_no:02d}.md"
    say()
    rule()
    say(f"  Week {week_no} -- {latest.get('title', '')}".rstrip(), BOLD)
    rule()
    if os.path.exists(os.path.join(REPO, briefing)):
        say(f"  Start here:  {briefing}", BOLD)
    say(f"  Score it:    python tests/scorecard.py {week_no}")
    say(f"               (the {week_no} matters -- without it the scorecard", DIM)
    say("               will ask you which week you meant)", DIM)
    say()
    say("  Now branch for the week, work, then open a pull request:")
    say(f"    git switch -c week-{week_no:02d}", BOLD)


def report_next(weeks, open_weeks):
    upcoming = next_locked(weeks, open_weeks)
    if upcoming:
        say()
        say(f"  Week {upcoming['week']} opens {upcoming['unlock'][:10]}.", DIM)
    released = open_weeks[-1]["week"] - 1
    if released >= 2:
        say(f"  Behind? Week {released}'s solution is published:", DIM)
        say(f"    python catchup.py {released:02d}", DIM)


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError:
        say()
        say("  git isn't installed, or isn't on your PATH.", RED + BOLD)
        say("  Open this folder in the dev container and try again.")
        sys.exit(1)
    say()
