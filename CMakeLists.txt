cmake_minimum_required(VERSION 3.20)
project(holdfast LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# =============================================================================
# core -- every game rule. No raylib, no window. This is what the tests test.
# =============================================================================
# Globbed, so the files you add in later weeks are picked up without anyone
# editing this file.
file(GLOB CORE_SOURCES CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/src/core/*.cpp)
add_library(core STATIC ${CORE_SOURCES})
target_include_directories(core PUBLIC include)
target_compile_options(core PRIVATE -Wall -Wextra -Wno-unused-parameter)

include(FetchContent)

# =============================================================================
# holdfast -- the playable game: core + raylib
# =============================================================================
option(HOLDFAST_BUILD_GAME "Build the raylib game (needs the dev container)" ON)
if(HOLDFAST_BUILD_GAME)
    set(BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
    set(BUILD_GAMES OFF CACHE BOOL "" FORCE)
    FetchContent_Declare(
        raylib
        URL https://github.com/raysan5/raylib/archive/refs/tags/5.5.tar.gz
        DOWNLOAD_EXTRACT_TIMESTAMP TRUE
    )
    FetchContent_MakeAvailable(raylib)
    target_compile_options(raylib PRIVATE -w)   # third-party warnings aren't ours to fix

    add_executable(holdfast src/game/main.cpp src/game/render.cpp)
    target_link_libraries(holdfast PRIVATE core raylib)
    target_compile_options(holdfast PRIVATE -Wall -Wextra -Wno-unused-parameter)
endif()

# =============================================================================
# One test program per session -- cpp_basics_tests, functions_debugging_tests, ...
# =============================================================================
# EXCLUDE_FROM_ALL matters: a week whose code you have not written yet does not
# compile, and an excluded target is only built when something asks for it. So
# `cmake --build build` always works, and the game always runs, no matter which
# session you are on. scorecard.py asks for exactly one session.
FetchContent_Declare(
    googletest
    URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
    DOWNLOAD_EXTRACT_TIMESTAMP TRUE
)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

# Globbed, not listed: a session that has not unlocked yet has no test file,
# and naming them would break the build before they arrive.
file(GLOB SESSION_TESTS CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/tests/test_*.cpp)
foreach(test_file ${SESSION_TESTS})
    get_filename_component(stem ${test_file} NAME_WE)       # test_cpp_basics
    string(REPLACE "test_" "" session ${stem})              # cpp_basics
    add_executable(${session}_tests EXCLUDE_FROM_ALL ${test_file})
    target_link_libraries(${session}_tests PRIVATE core GTest::gtest_main)
    target_compile_options(${session}_tests PRIVATE -Wall -Wextra -Wno-unused-parameter)
endforeach()

# Tests you write yourself live in tests/student/ and are yours alone -- a sync
# never overwrites them, and they are never graded.
file(GLOB STUDENT_TESTS CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/tests/student/*.cpp)
if(STUDENT_TESTS)
    add_executable(student_tests EXCLUDE_FROM_ALL ${STUDENT_TESTS})
    target_link_libraries(student_tests PRIVATE core GTest::gtest_main)
    target_compile_options(student_tests PRIVATE -Wall -Wextra -Wno-unused-parameter)
endif()
