cmake_minimum_required(VERSION 3.13)
project(snake_cmd)

set(CMAKE_CXX_STANDARD 14)

add_executable(snake_cmd main.cpp Snake.cpp Snake.h)