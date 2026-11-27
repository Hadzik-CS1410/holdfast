// =============================================================================
// rules.cpp -- C++ Basics session, your game logic
// =============================================================================
// This file is YOURS. Once it arrives it is never overwritten -- fix a typo
// here and it stays fixed.
//
// Four pairs. The LIVE half is written with the class; the FINISH half is the
// student's, alone, and is deliberately the same shape (ADR 0004).
// =============================================================================
#include "rules.h"

#include <iomanip>
#include <iostream>

// --- Pair 1 ------------------------------------------------------------------
int towerCost(int type)
{
    // TODO (LIVE -- we write this together in class):
    //   switch on type and return ARROW_COST / CANNON_COST / MORTAR_COST.
    //   Anything else returns 0.
    return 0;
}

int towerDamage(int type)
{
    // TODO (FINISH -- yours, alone. Sibling of towerCost):
    //   the same switch, over ARROW_DAMAGE / CANNON_DAMAGE / MORTAR_DAMAGE.
    return 0;
}

// --- Pair 2 ------------------------------------------------------------------
int sellValue(int cost)
{
    // TODO (LIVE): 70% of cost, rounded down.
    //   Multiply BEFORE you divide -- 7 / 10 is 0 in int arithmetic.
    return 0;
}

int upgradeCost(int cost)
{
    // TODO (FINISH -- sibling of sellValue): 150% of cost, rounded down.
    return 0;
}

// --- Pair 3 ------------------------------------------------------------------
bool isDarkTile(int row, int col)
{
    // TODO (LIVE): a checkerboard -- true when (row + col) is odd.
    return false;
}

bool isEdgeTile(int row, int col)
{
    // TODO (FINISH -- sibling of isDarkTile):
    //   true when the tile is on the outer border. Off-board counts as edge.
    return false;
}

// --- Pair 4 ------------------------------------------------------------------
void printShopTable()
{
    // TODO (LIVE): three rows, aligned. std::left << std::setw(18) for the
    //   name, std::right << std::setw(4) for the number, then the word
    //   gold and a newline.

}

void printTowerTable()
{
    // TODO (FINISH -- sibling of printShopTable):
    //   the same three rows and the SAME column widths, showing damage
    //   instead of gold, ending in dmg and a newline.

}
