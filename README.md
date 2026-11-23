# Holdfast

A real-time tower defense game, in C++. You build it one feature a week, for twelve weeks, in this repository. By the end it has two class hierarchies, loads its levels from files, and is about 1,500 lines of your own code.

This file is written once and never grows. **Each week's instructions arrive in `weeks/`** — this week's is the newest file there.

---

## Every session starts the same way

```bash
python sync.py
```

That fetches this week's instructions, tests and scaffolding. It will tell you which file to open first and the exact command to score yourself. It never touches code you wrote.

Then, and only then, start a branch for the week:

```bash
git switch -c week-03
```

**Sync first, then branch.** `sync.py` refuses to run on a week branch, because pulling my files into your branch would make your pull request look like you changed eleven files when you changed three.

---

## The three commands

| Command | What it does |
|---|---|
| `python sync.py` | get this week's work. Run it at the start of every session |
| `python tests/scorecard.py 2` | score one week. The number it prints is what you submit |
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

\* `include/` is mine until Week 7, when you write your first header and it becomes yours.

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
python tests/scorecard.py 2      # score Week 2
```

Always name the week. Run it with no number and it will list the weeks you have.

Sections are all-or-nothing — every test in a section must pass to earn its points. Four sections, 5 points each, 20 points a week.

---

## Submitting a week

1. Score it and **screenshot the scorecard**
2. Tag the commit: `git tag week-03 && git push origin week-03`
3. Upload the screenshot to Canvas

The screenshot has your name, your repository and your commit stamped on it by the scorecard — none of which you type. Your repository gets re-scored from the tag, so the tag has to point at the work the screenshot shows.

---

## The log

`CHANGELOG.md` has one row a week and two numbers in it:

- **Touch count** — how many separate *places in the code* you had to edit to make this week's change. You count these by hand.
- **Changed files** — the "N changed files" figure from your pull request header. Free; just read it off.

They are different numbers and the difference is the point. Adding a tower in Week 4 will cost you six to eight touches. Adding one in Week 13 will cost you one new file. Same game, much bigger, far less work — and you will have your own data proving it. The final project asks you to explain the curve, so fill the log in every week or you will have nothing to explain.

---

## Falling behind

It happens, and it is recoverable. The rule is simple: **you score 0 for a week you skipped, and full marks on everything after it.** Falling one week behind is nothing. Falling three weeks behind is the end of the game for you, so do not let it get there.

Each week's solution is published one week after that week was due:

```bash
python catchup.py 05          # read Week 5's solution beside your own code
python catchup.py --checkpoint  # badly behind: get a working game back
```

`catchup.py 05` puts the solution in a `catchup/` folder that git ignores, so you read it and copy across what you are missing. Your own code, your colours and your numbers stay.

`--checkpoint` is the bigger hammer: it saves everything you have to a branch first, then replaces your game logic with the last published week so you have something that runs again. Your `CHANGELOG.md` is kept. Nothing is deleted — your work is on a branch and the command tells you its name.

---

## Getting help

Bring the error message. If the build fails, the first error is the one that matters; the rest are usually its children. `undefined reference to 'something(int, int)'` almost always means a function in `src/core/` is named or shaped differently from what `include/rules.h` promised.
