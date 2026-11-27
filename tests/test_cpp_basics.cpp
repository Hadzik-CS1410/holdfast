// Holdfast -- C++ Basics session.
//
// EIGHT suites: four for what the class wrote together (LIVE) and four for the
// siblings you wrote alone (FINISH). Each FINISH suite tests the same shape as
// the LIVE one directly above it.
#include "rules.h"

#include <gtest/gtest.h>

#include <sstream>
#include <string>

namespace {

// Capture std::cout so a printing function can be tested.
std::string capture(void (*fn)())
{
    std::ostringstream buffer;
    std::streambuf* old{std::cout.rdbuf(buffer.rdbuf())};
    fn();
    std::cout.rdbuf(old);
    return buffer.str();
}

int lineCount(const std::string& text)
{
    int n{0};
    for (char c : text) {
        if (c == '\n') { ++n; }
    }
    return n;
}

}  // namespace

// ===== Pair 1: pick a value from a type ======================================
TEST(LiveTowerCost, EachTypeCostsItsConstant)
{
    EXPECT_EQ(towerCost(1), ARROW_COST);
    EXPECT_EQ(towerCost(2), CANNON_COST);
    EXPECT_EQ(towerCost(3), MORTAR_COST);
}

TEST(LiveTowerCost, UnknownTypeIsFree)
{
    EXPECT_EQ(towerCost(0), 0);
    EXPECT_EQ(towerCost(9), 0);
    EXPECT_EQ(towerCost(-1), 0);
}

TEST(FinishTowerDamage, EachTypeDealsItsConstant)
{
    EXPECT_EQ(towerDamage(1), ARROW_DAMAGE);
    EXPECT_EQ(towerDamage(2), CANNON_DAMAGE);
    EXPECT_EQ(towerDamage(3), MORTAR_DAMAGE);
}

TEST(FinishTowerDamage, UnknownTypeDealsNothing)
{
    EXPECT_EQ(towerDamage(0), 0);
    EXPECT_EQ(towerDamage(9), 0);
    EXPECT_EQ(towerDamage(-1), 0);
}

// ===== Pair 2: integer arithmetic ============================================
TEST(LiveSellValue, SeventyPercentRoundedDown)
{
    EXPECT_EQ(sellValue(100), 70);
    EXPECT_EQ(sellValue(50), 35);
    EXPECT_EQ(sellValue(0), 0);
}

TEST(LiveSellValue, MultipliesBeforeDividing)
{
    // cost * (7 / 10) is 0 for every input. If these pass, the order is right.
    EXPECT_EQ(sellValue(ARROW_COST), 35);
    EXPECT_EQ(sellValue(1), 0);
    EXPECT_EQ(sellValue(3), 2);
}

TEST(FinishUpgradeCost, OneAndAHalfTimesRoundedDown)
{
    EXPECT_EQ(upgradeCost(100), 150);
    EXPECT_EQ(upgradeCost(50), 75);
    EXPECT_EQ(upgradeCost(0), 0);
}

TEST(FinishUpgradeCost, MultipliesBeforeDividing)
{
    // cost * (3 / 2) would be cost * 1. 3 and 5 are where that shows.
    EXPECT_EQ(upgradeCost(3), 4);
    EXPECT_EQ(upgradeCost(5), 7);
    EXPECT_EQ(upgradeCost(1), 1);
}

// ===== Pair 3: a question about a tile =======================================
TEST(LiveDarkTile, IsNotAllOneColour)
{
    int dark{0};
    for (int r = 0; r < ROWS; ++r) {
        for (int c = 0; c < COLS; ++c) {
            if (isDarkTile(r, c)) { ++dark; }
        }
    }
    EXPECT_GT(dark, 0);
    EXPECT_LT(dark, ROWS * COLS);
}

TEST(LiveDarkTile, GivesTheSameAnswerEveryTime)
{
    // A pattern that changes between calls would flicker on screen.
    for (int r = 0; r < ROWS; ++r) {
        for (int c = 0; c < COLS; ++c) {
            EXPECT_EQ(isDarkTile(r, c), isDarkTile(r, c));
        }
    }
}

TEST(FinishEdgeTile, BorderIsEdgeAndTheInteriorIsNot)
{
    EXPECT_TRUE(isEdgeTile(0, 0));
    EXPECT_TRUE(isEdgeTile(0, 5));
    EXPECT_TRUE(isEdgeTile(ROWS - 1, COLS - 1));
    EXPECT_TRUE(isEdgeTile(4, COLS - 1));

    EXPECT_FALSE(isEdgeTile(1, 1));
    EXPECT_FALSE(isEdgeTile(5, 10));
    EXPECT_FALSE(isEdgeTile(ROWS - 2, COLS - 2));
}

TEST(FinishEdgeTile, OffTheBoardCountsAsEdge)
{
    EXPECT_TRUE(isEdgeTile(-1, 5));
    EXPECT_TRUE(isEdgeTile(5, -1));
    EXPECT_TRUE(isEdgeTile(ROWS, 5));
    EXPECT_TRUE(isEdgeTile(5, COLS));
}

// ===== Pair 4: a table in aligned columns ====================================
TEST(LiveShopTable, ThreeRowsNamingEveryTower)
{
    const std::string out{capture(printShopTable)};
    EXPECT_EQ(lineCount(out), 3);
    EXPECT_NE(out.find("Arrow"), std::string::npos);
    EXPECT_NE(out.find("Cannon"), std::string::npos);
    EXPECT_NE(out.find("Mortar"), std::string::npos);
}

TEST(LiveShopTable, ColumnsLineUp)
{
    const std::string out{capture(printShopTable)};
    std::istringstream lines{out};
    std::string line;
    std::size_t width{0};
    while (std::getline(lines, line)) {
        if (width == 0) { width = line.size(); }
        EXPECT_EQ(line.size(), width);
        EXPECT_NE(line.find("gold"), std::string::npos);
    }
}

TEST(FinishTowerTable, ThreeRowsNamingEveryTower)
{
    const std::string out{capture(printTowerTable)};
    EXPECT_EQ(lineCount(out), 3);
    EXPECT_NE(out.find("Arrow"), std::string::npos);
    EXPECT_NE(out.find("Cannon"), std::string::npos);
    EXPECT_NE(out.find("Mortar"), std::string::npos);
}

TEST(FinishTowerTable, SameWidthsAsTheShopTable)
{
    // The sibling has to line up with the one written in class -- same name
    // column, same number column. The UNIT differs ("gold" vs "dmg"), so the
    // whole line is not the same length and comparing it would be wrong.
    const std::string shop{capture(printShopTable)};
    const std::string towers{capture(printTowerTable)};
    std::istringstream a{shop};
    std::istringstream b{towers};
    std::string x, y;
    while (std::getline(a, x) && std::getline(b, y)) {
        EXPECT_EQ(x.find(" gold"), y.find(" dmg"))
            << "the number column ends in a different place";
    }
    EXPECT_NE(towers.find("dmg"), std::string::npos);
}
