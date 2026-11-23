// =============================================================================
// rules.cpp -- YOUR game logic. This file is yours for the rest of the semester.
// =============================================================================
// Four functions, four TODOs. The declarations are in include/rules.h -- read
// them first; they say exactly what each function must take and return.
//
// Score yourself at any time with:   python tests/scorecard.py 2
// =============================================================================
#include "rules.h"

#include <iomanip>
#include <iostream>

// TODO 1: return the gold cost of a tower type.
//   1 -> ARROW_COST, 2 -> CANNON_COST, 3 -> MORTAR_COST, anything else -> 0.
//   A switch is the natural shape here.
int towerCost(int type)
{
    return 0;
}

// TODO 2: return 70% of cost, rounded down.  sellValue(90) must be 63.
//   Careful: this is integer arithmetic, and the order you write it in matters.
int sellValue(int cost)
{
    return 0;
}

// TODO 3: decide which tiles are dark, and make the pattern YOURS.
//   A checkerboard is (row + col) % 2. Stripes, wide blocks, a diagonal -- all
//   fine. Two rules only: the same cell must always give the same answer, and
//   it must not be the same answer everywhere (or the board is one flat colour).
bool isDarkTile(int row, int col)
{
    return false;
}

// TODO 4: print the shop price list, with the columns lined up using std::setw.
//   Every line must come out the same width. Something like:
//
//     Arrow                  50 gold
//     Cannon                 90 gold
//     Mortar                 70 gold
void printShopTable()
{
}
