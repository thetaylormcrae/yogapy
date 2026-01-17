cmake_minimum_required(VERSION 3.15)
project(yogapy LANGUAGES CXX)

# 1. Force C++20 - This fixes the 'bit_cast' error on Linux
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# 2. Fetch Yoga Source
include(FetchContent)
FetchContent_Declare(
  yoga_src
  GIT_REPOSITORY https://github.com/facebook/yoga.git
  GIT_TAG        v3.1.0
)
# Force Yoga to build its C API but skip its internal tests/tools
set(YOGA_BUILD_C ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(yoga_src)

# 3. Setup Pybind11
find_package(pybind11 REQUIRED)

# 4. Create the Extension
pybind11_add_module(_native src/wrapper.cpp)

# 5. Linking and Includes
target_link_libraries(_native PRIVATE yogacore)
target_include_directories(_native PRIVATE ${yoga_src_SOURCE_DIR})
