# Holdfast

A real-time tower defense game, in C++. You build it one feature a week, for twelve weeks, in this repository. By the end it has two class hierarchies, loads its levels from files, and is about 1,500 lines of your own code.

**One repository, all semester.** You created it once, in class, through the GitHub Repo Creator. You never make another — each week `python sync.py` brings the new week's files into this same repo, so its history is the whole story of the game being built.

This file is written once and never grows. **Each week's instructions arrive in `weeks/`** — this week's is the newest file there.

---

## Every session starts the same way

```bash
python sync.py
```

That fetches this week's instructions, tests and scaffolding. It will tell you which file to open first and the exact command to score yourself. It never touches code you wrote.

Then, and only then, start a branch for the week:

```bash
git switch -c functions-debugging
```

**Sync first, then branch.** `sync.py` refuses to run on a week branch, because pulling my files into your branch would make your pull request look like you changed eleven files when you changed three.

---

## The three commands

| Command | What it does |
|---|---|
| `python sync.py` | get this week's work. Run it at the start of every session |
| `python tests/scorecard.py cpp-basics` | score one session. The number it prints is what you submit |
| `python catchup.py --help` | behind? This is the way back. See *Falling behind* below |

---

## What's yours and what's mine

| | Who | |
|---|---|---|
| `src/core/`, `include/`* | **yours** | every game rule you write. Once a file arrives here it is yours permanently — I never change it again |
| `tests/student/` | **yours** | tests you write. Never overwritten, never graded |
| `CHANGELOG.md` | **yours** | your weekly log. See *The log* below |
| `src/game/main.cpp`, `src/game/render.cpp` | mine | the window, the loop, the pixels. Re-delivered every week |
| `tests/`, `weeks/`, `CMakeLists.txt`, `sync.py` | mine | re-delivered every week |

\* `include/` is mine until the **Multi-file & Recursion** session, when you write your first header and it becomes yours.

**Editing one of my files is the one way to make a sync go wrong.** It will be overwritten and your change will be gone. If you want something in there to be different, ask — sometimes the answer is yes and it changes for everybody.

---

## Running the game

```bash
cmake --build build --target holdfast
./build/holdfast
```

The game window appears on the Linux desktop in your browser: **http://localhost:6080**. The first build takes a few minutes while raylib and Google Test download; after that it is seconds.

Press `ESC` to close the window.

---

## Scoring yourself

```bash
python tests/scorecard.py cpp-basics      # score the C++ Basics session
```

Always name the session. Run it with no number and it will list the sessions you have.

Sections are all-or-nothing — every test in a section must pass to earn its points. **Four sections of 4 = 16**, and the other **4 points** of the week come from the rubric: committing, pushing, branching, and opening a pull request. Check the scorecard header says `Pushed  yes` and shows a the session slug branch before you screenshot it.

---

## Submitting a week

1. Score it and **screenshot the scorecard**
2. Tag the commit: `git tag cpp-basics && git push origin cpp-basics`
3. Upload the screenshot to Canvas

The screenshot has your name, your repository and your commit stamped on it by the scorecard — none of which you type. Your repository gets re-scored from the tag, so the tag has to point at the work the screenshot shows.

---

## The log

`CHANGELOG.md` gets **one line per session**: what you added, and anything that
surprised you.

It takes thirty seconds and it is the only record of how the game grew. By April
you will have twelve lines describing a program you could not have written in
January, which is the point — and the final project asks you **what got easier,
and why**. You answer that from your own repository, so the log is where you
find your evidence.
---

## Falling behind

It happens, and it is recoverable. **One date to remember: everything from a
session is due the night before the next one.** Both halves — what we wrote
together in class and the sibling you write alone.

**You do not have to ask for the answers.** The next time you run
`python sync.py`, the previous session's full solution arrives in `catchup/`,
because that session has closed. Read it beside your own code; git ignores the
folder, so nothing of yours is touched.

```bash
python catchup.py arrays        # an older session, out of order
python catchup.py --checkpoint  # badly behind: get a working game back
```

`catchup.py` is for when you are *several* sessions behind. For the one you
just missed, syncing is enough.

`--checkpoint` is the bigger hammer: it saves everything you have to a branch
first, then replaces your game logic with the last published session so you
have something that runs again. Your `CHANGELOG.md` is kept. Nothing is
deleted — your work is on a branch and the command tells you its name.
---

## Getting help

Bring the error message. If the build fails, the first error is the one that matters; the rest are usually its children. `undefined reference to 'something(int, int)'` almost always means a function in `src/core/` is named or shaped differently from what `include/rules.h` promised.
