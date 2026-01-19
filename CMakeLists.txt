cmake_minimum_required(VERSION 3.15)
project(yogapy LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(pybind11 REQUIRED)

# Use YOGA_SRC_DIR if provided by environment
if(NOT YOGA_SRC_DIR)
    set(YOGA_SRC_DIR "${CMAKE_SOURCE_DIR}/yoga_src")
endif()

set(YOGA_DIR "${YOGA_SRC_DIR}")

file(GLOB_RECURSE YOGA_SOURCES
    "${YOGA_DIR}/yoga/*.cpp"
)

pybind11_add_module(_yogapy src/main.cpp ${YOGA_SOURCES})

target_include_directories(_yogapy PRIVATE
    "${YOGA_DIR}"
)

target_compile_definitions(_yogapy PRIVATE YOGA_EXPORT_SYMBOLS=0)