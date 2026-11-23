// =============================================================================
// test_week02.cpp -- Week 2, four sections, 5 points each. MINE, not yours.
// =============================================================================
// Sections are all-or-nothing: every test in a section must pass to earn it.
// Score yourself with:   python tests/scorecard.py 2
// =============================================================================
#include <gtest/gtest.h>

#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "rules.h"

namespace {

// Captures everything printed to std::cout while it is alive. This is how the
// shop table gets tested without changing the shape of printShopTable() --
// tests are allowed tools you have not been taught yet.
class CoutCapture {
public:
    CoutCapture() : old_{std::cout.rdbuf(buffer_.rdbuf())} {}
    ~CoutCapture() { std::cout.rdbuf(old_); }
    std::string text() const { return buffer_.str(); }

private:
    std::ostringstream buffer_;
    std::streambuf* old_;
};

std::vector<std::string> nonEmptyLines(const std::string& text)
{
    std::vector<std::string> lines;
    std::istringstream in{text};
    std::string line;
    while (std::getline(in, line)) {
        while (!line.empty() && (line.back() == ' ' || line.back() == '\r')) {
            line.pop_back();
        }
        if (!line.empty()) lines.push_back(line);
    }
    return lines;
}

}  // namespace

// --- Week02Costs -------------------------------------------------------------
TEST(Week02Costs, EachTowerTypeCostsItsConstant)
{
    EXPECT_EQ(towerCost(1), ARROW_COST);
    EXPECT_EQ(towerCost(2), CANNON_COST);
    EXPECT_EQ(towerCost(3), MORTAR_COST);
}

TEST(Week02Costs, UnknownTypesCostNothing)
{
    EXPECT_EQ(towerCost(0), 0);
    EXPECT_EQ(towerCost(4), 0);
    EXPECT_EQ(towerCost(-1), 0);
    EXPECT_EQ(towerCost(999), 0);
}

// --- Week02Refund ------------------------------------------------------------
TEST(Week02Refund, SellsForSeventyPercentRoundedDown)
{
    EXPECT_EQ(sellValue(90), 63);
    EXPECT_EQ(sellValue(50), 35);
    EXPECT_EQ(sellValue(70), 49);
}

TEST(Week02Refund, IsNotIntegerDivisionZero)
{
    // cost * (7 / 10) is 0 for every cost, because 7 / 10 is 0 in int maths.
    EXPECT_GT(sellValue(100), 0);
    EXPECT_EQ(sellValue(0), 0);
}

// --- Week02Board -------------------------------------------------------------
// Your pattern is yours. These two tests check only that it IS a pattern:
// the same cell always answers the same way, and not every cell answers alike.
TEST(Week02Board, IsDeterministic)
{
    for (int row{0}; row < ROWS; row++) {
        for (int col{0}; col < COLS; col++) {
            EXPECT_EQ(isDarkTile(row, col), isDarkTile(row, col))
                << "cell (" << row << ", " << col << ") changed its mind";
        }
    }
}

TEST(Week02Board, IsNotOneFlatColour)
{
    bool sawDark{false};
    bool sawLight{false};
    for (int row{0}; row < ROWS; row++) {
        for (int col{0}; col < COLS; col++) {
            if (isDarkTile(row, col)) {
                sawDark = true;
            } else {
                sawLight = true;
            }
        }
    }
    EXPECT_TRUE(sawDark) << "no dark tiles anywhere -- the board is one colour";
    EXPECT_TRUE(sawLight) << "every tile is dark -- the board is one colour";
}

// --- Week02Shop --------------------------------------------------------------
TEST(Week02Shop, PrintsOneLinePerTower)
{
    CoutCapture captured;
    printShopTable();
    EXPECT_GE(nonEmptyLines(captured.text()).size(), 3u)
        << "expected at least one line per tower type";
}

TEST(Week02Shop, EveryLineIsTheSameWidth)
{
    CoutCapture captured;
    printShopTable();
    std::vector<std::string> lines{nonEmptyLines(captured.text())};
    ASSERT_FALSE(lines.empty()) << "printShopTable printed nothing";
    for (const std::string& line : lines) {
        EXPECT_EQ(line.size(), lines.front().size())
            << "this line is a different width from the first:\n  " << line
            << "\nuse std::setw so the columns line up";
    }
}
