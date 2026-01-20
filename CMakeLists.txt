cmake_minimum_required(VERSION 3.15)
project(yogapy LANGUAGES CXX)

# Yoga 3.x needs C++17 or C++20
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(pybind11 REQUIRED)

# This directory points to the 'yoga' subfolder within the fetched source
set(YOGA_DIR "${CMAKE_SOURCE_DIR}/yoga_src/yoga")

# We only need the .cpp files for core layout logic
file(GLOB_RECURSE YOGA_SOURCES
    "${YOGA_DIR}/*.cpp"
)

pybind11_add_module(_yogapy src/main.cpp ${YOGA_SOURCES})

target_include_directories(_yogapy PRIVATE
    "${CMAKE_SOURCE_DIR}/yoga_src" # For #include "yoga/Yoga.h"
)

# Crucial for Windows: avoid trying to export internal Yoga symbols
target_compile_definitions(_yogapy PRIVATE YOGA_EXPORT_SYMBOLS=0)
