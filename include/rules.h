// =============================================================================
// rules.h -- DECLARATIONS: what your game logic promises to provide
// =============================================================================
// This file is MINE, not yours. It arrives again every week, so do not edit it
// -- your changes would be overwritten on your next sync.
//
// What it does is promise the compiler that four functions exist. The renderer
// calls them. You write their bodies in src/core/rules.cpp.
//
// If you name a function differently, the build fails with
//     undefined reference to `isDarkTile(int, int)'
// which is the linker telling you the exact signature it was promised.
// =============================================================================
#pragma once

// --- The board ---------------------------------------------------------------
// 20 columns x 12 rows of 48-pixel tiles. The whole course uses these numbers.
inline constexpr int ROWS{12};
inline constexpr int COLS{20};
inline constexpr int TILE_SIZE{48};

// --- The shop ----------------------------------------------------------------
// Tower types are plain ints this week. Week 4 turns them into an enum class.
//   1 = Arrow     2 = Cannon     3 = Mortar
inline constexpr int ARROW_COST{50};
inline constexpr int CANNON_COST{90};
inline constexpr int MORTAR_COST{70};

// Gold it costs to build a tower. Returns 0 for a type that does not exist.
int towerCost(int type);

// Gold you get back for selling a tower that cost `cost`. 70%, rounded down.
int sellValue(int cost);

// true if the tile at (row, col) should be drawn in the darker colour.
// This one is yours to make interesting -- see weeks/week02.md.
bool isDarkTile(int row, int col);

// Prints the shop's price list to the terminal, in aligned columns.
void printShopTable();
