cmake_minimum_required(VERSION 3.15)
project(yogapy LANGUAGES CXX)

# CRITICAL: Yoga v3+ requires C++20 for std::bit_cast
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)
FetchContent_Declare(
  yoga_src
  GIT_REPOSITORY https://github.com/facebook/yoga.git
  GIT_TAG        v3.2.1
)
FetchContent_MakeAvailable(yoga_src)

find_package(pybind11 REQUIRED)

pybind11_add_module(_native src/wrapper.cpp)

target_link_libraries(_native PRIVATE yogacore)
target_include_directories(_native PRIVATE ${yoga_src_SOURCE_DIR})
