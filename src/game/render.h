// =============================================================================
// render.h -- the ONLY part of Holdfast that knows what a pixel is
// =============================================================================
// MINE, not yours. Re-delivered every week; do not edit.
//
// Everything above this line in the architecture -- every rule, every number,
// every decision -- lives in src/core/ and never includes raylib. That is why
// your code can be tested with no window, no display and no graphics card.
// =============================================================================
#pragma once

// Draws one frame: the board, then the HUD on top.
void drawFrame(int gold, int lives);
