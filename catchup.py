"""
Holdfast -- catching up

Two ways back, for when a week got away from you.

    python catchup.py 05            read Week 5's finished code beside your own
    python catchup.py --checkpoint  get a working game back, keeping your work
    python catchup.py --list        which weeks are published

The deal: you score 0 for a week you skipped, and full marks on everything
after it. Falling one week behind is nothing. Falling three weeks behind is
the end of the game for you -- so use this before it gets there.

Each week's solution is published one week after that week was due, so nothing
you can still earn points for is ever available here.

You do not need to understand this file. Do not edit it.
"""
import os
import shutil
import subprocess
import sys
import tempfile

SOLUTIONS_URL = os.environ.get(
    "HOLDFAST_SOLUTIONS",
    "https://github.com/Hadzik-CS1410/holdfast-solutions.git")
REPO = os.path.dirname(os.path.abspath(__file__))
CATCHUP_DIR = os.path.join(REPO, "catchup")

# Never replaced by a checkpoint:
#   CHANGELOG.md   your touch-count log -- your record of the weeks you DID do,
#                  and the data the final project asks you to explain
#   tests/student/ tests you wrote
KEEP = ("CHANGELOG.md", "tests/student")

GREEN, YELLOW, RED, DIM, BOLD, OFF = (
    "\033[92m", "\033[93m", "\033[91m", "\033[2m", "\033[1m", "\033[0m")


def say(msg="", color=""):
    print(f"{color}{msg}{OFF}" if color else msg)


def rule():
    say("-" * 64, DIM)


def git(*args, cwd=None):
    return subprocess.run(["git", *args], cwd=cwd or REPO,
                          capture_output=True, text=True)


def out(*args, cwd=None):
    return git(*args, cwd=cwd).stdout.strip()


def stop(title, *lines):
    say()
    rule()
    say("  " + title, RED + BOLD)
    rule()
    for line in lines:
        say("  " + line)
    say()
    sys.exit(1)


def fetch_solutions():
    """Shallow clone into a temp folder. No remote is added to your repository,
    so a solution can never ride into your history or your pull request."""
    temp = tempfile.mkdtemp(prefix="holdfast_catchup_")
    say("  Fetching published solutions...")
    result = subprocess.run(
        ["git", "clone", "--depth", "1", "-q", SOLUTIONS_URL, temp],
        capture_output=True, text=True)
    if result.returncode != 0:
        shutil.rmtree(temp, ignore_errors=True)
        stop("Couldn't reach the solutions repo.",
             "Check your internet connection and try again. If it keeps",
             "failing, ask your instructor -- it may not be published yet.",
             "",
             *result.stderr.strip().splitlines()[:4])
    return temp


def make_catchup_dir():
    """catchup/ ignores itself.

    The rule cannot live in .gitignore: that file is stamped from the course's
    canonical template by sync_tooling.py, so an addition there is overwritten
    on the next sync. A folder that carries its own .gitignore survives that,
    and survives a student deleting the folder and running this again.

    It matters because a solution inside the repository would be committed,
    ride into the week's pull request, and inflate the changed-files count --
    the one number that is supposed to be free and honest.
    """
    os.makedirs(CATCHUP_DIR, exist_ok=True)
    marker = os.path.join(CATCHUP_DIR, ".gitignore")
    if not os.path.exists(marker):
        with open(marker, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# Fetched solutions are never part of your repository.\n*\n")


def published(root):
    weeks = []
    for name in sorted(os.listdir(root)):
        if name.startswith("week") and os.path.isdir(os.path.join(root, name)):
            try:
                weeks.append(int(name[4:]))
            except ValueError:
                pass
    return weeks


def week_dir(root, number):
    return os.path.join(root, "week%02d" % number)


# ------------------------------------------------------------------ reading


def read_week(number):
    temp = fetch_solutions()
    try:
        source = week_dir(temp, number)
        if not os.path.isdir(source):
            weeks = published(temp)
            stop(f"Week {number} isn't published yet.",
                 "Solutions appear one week after that week was due.",
                 "",
                 "Published right now: " +
                 (", ".join(str(w) for w in weeks) if weeks else "none yet"))

        target = os.path.join(CATCHUP_DIR, "week%02d" % number)
        if os.path.exists(target):
            shutil.rmtree(target)
        make_catchup_dir()
        shutil.copytree(source, target)
    finally:
        shutil.rmtree(temp, ignore_errors=True)

    files = []
    for folder, _, names in os.walk(target):
        for name in sorted(names):
            files.append(os.path.relpath(os.path.join(folder, name), REPO))

    say()
    rule()
    say(f"  Week {number}'s solution is in catchup/week%02d/" % number,
        GREEN + BOLD)
    rule()
    for path in files:
        say("    " + path.replace("\\", "/"), GREEN)
    say()
    say("  Open it beside your own code and copy across what you're missing.")
    say("  Don't replace your whole file unless you have nothing -- you'd lose")
    say("  your own colours, numbers and pattern, and the solution is")
    say("  deliberately plain so that yours can be better than it.")
    say()
    say("  git ignores the catchup/ folder, so this never lands in your", DIM)
    say("  history or your next pull request.", DIM)


# --------------------------------------------------------------- checkpoint


def checkpoint():
    if git("rev-parse", "--git-dir").returncode != 0:
        stop("This folder isn't a git repository.",
             "Run this from inside your holdfast folder.")

    temp = fetch_solutions()
    try:
        weeks = published(temp)
        if not weeks:
            stop("No weeks are published yet.",
                 "There is nothing to check out to. Ask your instructor.")
        number = max(weeks)
        source = week_dir(temp, number)

        # Only the folders the solution actually carries are touched. For the
        # early weeks that is src/core/ alone; include/ joins it from Week 7,
        # when you start writing your own headers.
        folders = sorted(name for name in os.listdir(source)
                         if os.path.isdir(os.path.join(source, name)))

        say()
        rule()
        say(f"  Checkpoint: Week {number}, complete", YELLOW + BOLD)
        rule()
        say("  This will REPLACE these folders with Week %d's finished code:"
            % number)
        for name in folders:
            say("    " + name + "/", BOLD)
        say()
        say("  Kept exactly as it is:")
        for name in KEEP:
            say("    " + name, GREEN)
        say()
        say("  Your work is committed and saved to a branch FIRST, so nothing")
        say("  is deleted -- you can always get it back.")
        say()
        say("  You'll score 0 for the weeks you skipped, and full marks on")
        say("  everything after this one.")
        say()
        answer = input("  Type  checkpoint  to go ahead (anything else cancels): ")
        if answer.strip().lower() != "checkpoint":
            say()
            say("  Cancelled. Nothing was changed.", GREEN)
            return

        branch = f"my-work-before-week{number:02d}"
        if out("rev-parse", "--verify", "-q", branch):
            suffix = 2
            while out("rev-parse", "--verify", "-q", f"{branch}-{suffix}"):
                suffix += 1
            branch = f"{branch}-{suffix}"

        # 1. everything you have, committed
        if out("status", "--porcelain"):
            git("add", "-A")
            git("commit", "-q", "-m", "my work before taking a checkpoint")

        # 2. a branch pointing at it -- this is the undo
        if git("branch", branch).returncode != 0:
            stop("Couldn't save your work to a branch.",
                 "Nothing has been changed. Show your instructor this and",
                 "do not run any more git commands yet.")

        # 3. replace, wholesale, so the result is a game that actually builds
        for name in folders:
            target = os.path.join(REPO, name)
            if os.path.exists(target):
                shutil.rmtree(target)
            shutil.copytree(os.path.join(source, name), target)

        git("add", "-A")
        git("commit", "-q", "-m", f"checkpoint: week {number:02d} complete")
    finally:
        shutil.rmtree(temp, ignore_errors=True)

    say()
    rule()
    say(f"  Done. You have Week {number}'s game.", GREEN + BOLD)
    rule()
    say("  Build it and see:")
    say("    cmake --build build --target holdfast && ./build/holdfast", BOLD)
    say()
    say(f"  Your old work is on the branch  {branch}", BOLD)
    say("  To look at it:   git switch " + branch, DIM)
    say("  To come back:    git switch main", DIM)
    say()
    say("  Now do this week's work. python sync.py if you haven't yet.")


def list_weeks():
    temp = fetch_solutions()
    try:
        weeks = published(temp)
    finally:
        shutil.rmtree(temp, ignore_errors=True)
    say()
    if not weeks:
        say("  Nothing published yet.", DIM)
        return
    say("  Published solutions: " + ", ".join(str(w) for w in weeks), GREEN)
    say()
    say("    python catchup.py %02d          read one week" % weeks[-1], DIM)
    say("    python catchup.py --checkpoint  jump to Week %d complete" % weeks[-1], DIM)


def usage():
    say(__doc__.strip())
    sys.exit(0)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a]
    try:
        if not args or args[0] in ("-h", "--help", "help"):
            usage()
        elif args[0] == "--checkpoint":
            checkpoint()
        elif args[0] == "--list":
            list_weeks()
        elif args[0].lstrip("0").isdigit() or args[0] == "0":
            read_week(int(args[0]))
        else:
            say(f"  Don't know what '{args[0]}' means.", RED)
            say()
            usage()
    except FileNotFoundError:
        say()
        say("  git isn't installed, or isn't on your PATH.", RED + BOLD)
        sys.exit(1)
    except KeyboardInterrupt:
        say()
        say("  Cancelled. Nothing was changed.", GREEN)
    say()
