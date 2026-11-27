// =============================================================================
// rules.h -- DECLARATIONS: what your game logic promises to provide
// =============================================================================
// This file is MINE, not yours. It arrives again every week, so do not edit it
// -- your changes would be overwritten on your next sync.
//
// What it does is promise the compiler that eight functions exist. The renderer
// calls them. You write their bodies in src/core/rules.cpp.
//
// If you name a function differently, the build fails with
//     undefined reference to `isDarkTile(int, int)'
// which is the linker telling you the exact signature it was promised.
// =============================================================================
#pragma once

// `const int`, not `constexpr`, on purpose: CT 1 teaches const and this course
// never teaches constexpr. You read this file every session, so it may only
// contain C++ you have already been shown.

// --- The board ---------------------------------------------------------------
// 20 columns x 12 rows of 48-pixel tiles. The whole course uses these numbers.
const int ROWS{12};
const int COLS{20};
const int TILE_SIZE{48};

// --- The shop ----------------------------------------------------------------
// Tower types are plain ints this week. Week 4 turns them into an enum class.
//   1 = Arrow     2 = Cannon     3 = Mortar
const int ARROW_COST{50};
const int CANNON_COST{90};
const int MORTAR_COST{70};

// Damage a tower deals per shot.
const int ARROW_DAMAGE{10};
const int CANNON_DAMAGE{35};
const int MORTAR_DAMAGE{25};

// =============================================================================
// FOUR PAIRS. In each pair the LIVE one is written together in class and the
// FINISH one is yours, alone -- and they are the SAME SHAPE. That is the whole
// design: by the time you write the second one you have written it twice
// already, once in Tuesday's Code-Together and once with the class.
// =============================================================================

// --- Pair 1: pick a value from a type ----------------------------------------
// LIVE    Gold it costs to build a tower. Returns 0 for a type that does not exist.
int towerCost(int type);
// FINISH  Damage that tower deals per shot. Same switch, different table.
int towerDamage(int type);

// --- Pair 2: integer arithmetic that looks right and is not ------------------
// LIVE    Gold back for selling a tower that cost `cost`. 70%, rounded down.
int sellValue(int cost);
// FINISH  Gold to upgrade a tower that cost `cost`. 150%, rounded down.
int upgradeCost(int cost);

// --- Pair 3: a question about a tile, answered true or false -----------------
// LIVE    true if (row, col) should be drawn in the darker colour.
bool isDarkTile(int row, int col);
// FINISH  true if (row, col) is on the outer border of the board.
bool isEdgeTile(int row, int col);

// --- Pair 4: a table in aligned columns --------------------------------------
// LIVE    The shop's price list.
void printShopTable();
// FINISH  The same table, showing damage instead of gold.
void printTowerTable();
