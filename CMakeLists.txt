cmake_minimum_required(VERSION 3.15)
project(yogapy LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(pybind11 REQUIRED)

# Logical path resolution for CI and Local
if(NOT YOGA_SRC_DIR)
    set(YOGA_SRC_DIR "${CMAKE_SOURCE_DIR}/yoga_src")
endif()

message(STATUS "Looking for Yoga in: ${YOGA_SRC_DIR}")

# Recursive globbing ensures all Yoga sub-components are found
file(GLOB_RECURSE YOGA_SOURCES
    "${YOGA_SRC_DIR}/yoga/*.cpp"
    "${YOGA_SRC_DIR}/yoga/*.c"
)

if(NOT YOGA_SOURCES)
    message(FATAL_ERROR "Yoga sources not found at ${YOGA_SRC_DIR}. Build cannot continue.")
endif()

# Create the Python module
pybind11_add_module(_yogapy src/main.cpp ${YOGA_SOURCES})

# Platform-agnostic include directories
target_include_directories(_yogapy PRIVATE
    "${YOGA_SRC_DIR}"
    "src"
)

# Fix for MSVC symbol export issues on Windows
if(WIN32)
    target_compile_definitions(_yogapy PRIVATE YOGA_EXPORT_SYMBOLS=0)
    target_compile_options(_yogapy PRIVATE /W4) # Higher warning level for Windows
else()
    target_compile_options(_yogapy PRIVATE -Wall -Wextra)
endif()

install(TARGETS _yogapy DESTINATION .)