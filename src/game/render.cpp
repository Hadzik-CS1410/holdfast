// =============================================================================
// render.cpp -- turns your game logic into pixels. MINE, not yours.
// =============================================================================
// Read it if you are curious. Do not edit it -- it arrives again every week,
// and your changes would be overwritten.
//
// Notice what this file does NOT decide: which tiles are dark, or what a tower
// costs. It asks your code and draws the answer. Change isDarkTile and the
// screen changes. That is the whole arrangement for the next five weeks.
// =============================================================================
#include "render.h"

#include <raylib.h>

#include <string>

#include "rules.h"

namespace {

constexpr int MAP_HEIGHT{ROWS * TILE_SIZE};
constexpr int HUD_HEIGHT{120};

constexpr Color LIGHT_GRASS{126, 170, 90, 255};
constexpr Color DARK_GRASS{104, 148, 74, 255};
constexpr Color HUD_BACK{38, 42, 52, 255};
constexpr Color HUD_TEXT{225, 230, 238, 255};
constexpr Color HUD_DIM{140, 150, 165, 255};
constexpr Color GOLD_TEXT{235, 200, 90, 255};
constexpr Color LIVES_TEXT{226, 120, 120, 255};

// The board. Two nested loops, and one question per tile -- asked of YOUR code.
void drawBoard()
{
    for (int row{0}; row < ROWS; row++) {
        for (int col{0}; col < COLS; col++) {
            DrawRectangle(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE,
                          isDarkTile(row, col) ? DARK_GRASS : LIGHT_GRASS);
        }
    }
}

// One shop entry in the bottom bar. The price comes from your towerCost().
void drawShopSlot(int slot, const char* name, int type)
{
    int x{24 + slot * 210};
    int y{MAP_HEIGHT + 46};
    DrawRectangleLines(x - 10, y - 12, 190, 56, HUD_DIM);
    DrawText(TextFormat("%d  %s", slot + 1, name), x, y, 20, HUD_TEXT);
    DrawText(TextFormat("%d gold", towerCost(type)), x, y + 24, 18, GOLD_TEXT);
}

void drawHud(int gold, int lives)
{
    DrawRectangle(0, MAP_HEIGHT, COLS * TILE_SIZE, HUD_HEIGHT, HUD_BACK);
    DrawText("HOLDFAST", 24, MAP_HEIGHT + 12, 24, HUD_TEXT);
    DrawText(TextFormat("Gold %d", gold), 220, MAP_HEIGHT + 14, 22, GOLD_TEXT);
    DrawText(TextFormat("Lives %d", lives), 360, MAP_HEIGHT + 14, 22, LIVES_TEXT);
    DrawText("week 2 -- the board appears", 520, MAP_HEIGHT + 18, 16, HUD_DIM);

    drawShopSlot(0, "Arrow", 1);
    drawShopSlot(1, "Cannon", 2);
    drawShopSlot(2, "Mortar", 3);
}

}  // namespace

void drawFrame(int gold, int lives)
{
    drawBoard();
    drawHud(gold, lives);
}
