# Week 2 — The Board Appears

**Module 1: C++ Basics.** 20 points: four code sections of 4 (**16**), plus **4** for getting your work onto GitHub — committed and pushed. The scorecard prints `Pushed` in its header, so check it says `yes` before you screenshot.

By Thursday your game opens a window, draws a board with a pattern you invented, prints a price list in aligned columns, and knows what every tower costs. You will not write a single line of graphics code to do it.

---

## How this works

`src/game/main.cpp` and `src/game/render.cpp` are **mine**. They open the window, run the loop and draw the pixels. They arrive again every week and you never edit them.

`src/core/rules.cpp` is **yours**, for the rest of the semester.

The renderer doesn't decide anything. It asks your code and draws the answer:

```cpp
// in render.cpp -- mine
DrawRectangle(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE,
              isDarkTile(row, col) ? DARK_GRASS : LIGHT_GRASS);
```

`isDarkTile` is yours. Change it and the screen changes.

---

## The contract

These four declarations are in `include/rules.h`. **Do not change them, and do not edit that file** — it is mine and it arrives again next week. Write the bodies in `src/core/rules.cpp`.

```cpp
int  towerCost(int type);            // 1 = Arrow, 2 = Cannon, 3 = Mortar; 0 if unknown
int  sellValue(int cost);            // 70% of cost, rounded down
bool isDarkTile(int row, int col);   // true for the darker tile colour
void printShopTable();               // the price list, in aligned columns
```

If you rename one, the build stops with `undefined reference to 'isDarkTile(int, int)'`. That message is the linker telling you the exact signature it was promised.

Constants you already have, in `include/rules.h`: `ROWS`, `COLS`, `TILE_SIZE`, `ARROW_COST`, `CANNON_COST`, `MORTAR_COST`. Use the names, not the numbers.

---

## What you're finishing

**1. `towerCost`** — we wrote this together in class. Check it still does the right thing for 1, 2, 3 and for junk input.

**2. `sellValue`** — 70% of the cost, rounded down. `sellValue(90)` must be `63`.

> We wrote this as `cost * (7 / 10)` in class and watched every tower sell for 0 gold. If you have forgotten why: `7 / 10` is two integers, so C++ does integer division and the answer is `0`, and `cost * 0` is `0` for every tower in the game. Python would have said `0.7`.

**3. `isDarkTile`** — **make this one yours.** A checkerboard is `(row + col) % 2`, and you can do better: stripes, wide blocks, a diagonal, a border, a chequered band across the middle. Two rules only, and they are what the tests check:

- the same cell must always give the same answer
- it must not give the same answer everywhere, or the board is one flat colour

Nothing else about the pattern is graded. The person next to you should be able to tell your board from theirs across the room.

**4. `printShopTable`** — print the price list to the terminal with the columns lined up, using `std::setw` from `<iomanip>`. Every line must come out **the same width**. Aim for something like:

```
Arrow                  50 gold
Cannon                 90 gold
Mortar                 70 gold
```

---

## What's tested

| Section | 4 points for |
|---|---|
| Tower costs | `towerCost` returns the right constant for 1, 2, 3 and **0** for anything else |
| Selling a tower | `sellValue(90) == 63`, and selling never returns 0 gold for a real tower |
| The board's pattern | `isDarkTile` is deterministic and is not one flat colour — **your pattern, whatever it is, passes** |
| The shop table | every printed line is the same width, so `setw` was actually used |

Sections are all-or-nothing: both tests in a section must pass to earn its 4 points. The other **4 points** come from the Canvas rubric: 2 for committing and 2 for pushing. Check the scorecard says `Pushed  yes` before you screenshot it.

```bash
python tests/scorecard.py 2
```

Run it as often as you like. It prints your score with your name and repository on it — that screenshot is what you submit.

---

## Running the game

```bash
cmake --build build --target holdfast
./build/holdfast
```

The window opens on the browser desktop: **http://localhost:6080**. The price list prints in the terminal, because `std::setw` has no meaning in a graphics window — which is exactly why the shop earns a terminal and the board earns a window.

---

## Submitting

1. `python tests/scorecard.py 2` and screenshot the result
2. Tag it: `git tag week-02 && git push origin week-02`
3. Upload the screenshot to Canvas

The tag is how the score gets re-checked, so it has to point at the work the screenshot shows.

---

## Only Module 1 C++

No references, no structs, no arrays, no `enum`, no classes. Everything is `int`, `float`, `bool`, and passed by value. If you have seen something fancier elsewhere, it is coming — `enum class` in two weeks, and it replaces the `1 / 2 / 3` tower types you are using today.
