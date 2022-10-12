cmake_minimum_required(VERSION 3.5)

# set the project name
project(pymdstresslab VERSION 1.0)

set(CMAKE_CXX_STANDARD 17)
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}  -std=c++14")

# find the kim api package
find_package(KIM-API 2.2 REQUIRED CONFIG)
SET(CMAKE_BUILD_RPATH_USE_ORIGIN TRUE)
# Include directories
#include_directories(${PROJECT_SOURCE_DIR}/include/MDStressLab++)

#add_subdirectory(src)
#add_subdirectory(tests)
#add_subdirectory(unit_tests)
#SET(CMAKE_SKIP_BUILD_RPATH  FALSE)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(PythonInterp REQUIRED)
# Without explicitly finding PythonLibs, Build fails in env with no explicit LD_LIBRARY_PATH
find_package(PythonLibs REQUIRED)

include_directories(${PYTHON_INCLUDE_DIRS})
include_directories(pybind11/include)
include_directories("mdstresslab/include/MDStressLab++/Eigen")
include_directories("mdstresslab/include/MDStressLab++")

add_subdirectory(pybind11)
add_subdirectory(mdstresslab/src "./mdstresslab")

pybind11_add_module(pymdstresslab src/python_bindings.cpp)
target_link_libraries(pymdstresslab PUBLIC MDStressLab++)

#set_target_properties(pymdstresslab PROPERTIES BUILD_WITH_INSTALL_RPATH FALSE LINK_FLAGS "-Wl,-rpath,$ORIGIN/")