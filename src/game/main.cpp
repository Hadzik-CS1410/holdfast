// =============================================================================
// main.cpp -- the window and the game loop. MINE, not yours.
// =============================================================================
// Re-delivered every week; do not edit. In Week 7 you will own the file layout,
// and from Week 9 the type system -- but this file and render.cpp stay mine all
// semester, because they are the boundary where raylib lives. Keeping them
// sealed is what lets every rule you write be tested with no window.
//
// Run it:   cmake --build build --target holdfast && ./build/holdfast
//           (the window opens on the browser desktop at http://localhost:6080)
// =============================================================================
#include <raylib.h>

#include <iostream>

#include "render.h"
#include "rules.h"

namespace {

// GIVEN state. Globals, deliberately -- and that is worth noticing, because in
// Week 10 they move inside a Game object and stop being reachable from anywhere
// in the program. Compare them with the local variables in your own functions:
// these two live for the whole run, those live for one call.
int gold{120};
int lives{20};

}  // namespace

int main()
{
    // The terminal gets the shop table; the window gets the board. std::setw
    // has no meaning in a graphics window, so the price list earns a terminal.
    std::cout << "\n=== Holdfast -- Tower Shop ===\n";
    printShopTable();
    std::cout << std::endl;

    InitWindow(COLS * TILE_SIZE, ROWS * TILE_SIZE + 120, "Holdfast");
    SetTargetFPS(60);

    while (!WindowShouldClose()) {
        BeginDrawing();
        ClearBackground(BLACK);
        drawFrame(gold, lives);
        EndDrawing();
    }

    CloseWindow();
    return 0;
}
