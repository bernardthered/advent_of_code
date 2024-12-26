# Solution to
# https://adventofcode.com/2024/day/18

import copy
from functools import cache
import math
import os

LOGLEVEL = 100

DIRECTIONS = {0: "up", 1: "right", 2: "down", 3: "left"}
NUM_ROWS_AND_COLS = 71


map = []
min_steps_to_exit_from_location = {}


class InfiniteLoop(Exception):
    pass


def log(msg, level=10):
    if level >= LOGLEVEL:
        print(msg)


def construct_map(max_bytes=1024):
    global map
    map = [[0 for i in range(NUM_ROWS_AND_COLS)] for j in range(NUM_ROWS_AND_COLS)]

    script_path = os.path.dirname(os.path.realpath(__file__))
    input = open(os.path.join(script_path, "input_2.txt"))
    lines = input.readlines()
    for i, line in enumerate(lines):
        if i >= max_bytes:
            break

        x, y = line.strip().split(",")
        map[int(x)][int(y)] = 1
    return map


def print_map(previously_visited=None):
    global map
    for y in range(NUM_ROWS_AND_COLS):
        for x in range(NUM_ROWS_AND_COLS):
            if previously_visited and (x, y) in previously_visited:
                print("O", end="")
            elif map[x][y] == 0:
                print(".", end="")
            else:
                print("#", end="")
        print()


def is_off_the_map(col_num, row_num):
    return (
        row_num < 0
        or col_num < 0
        or row_num >= NUM_ROWS_AND_COLS
        or col_num >= NUM_ROWS_AND_COLS
    )


def next_square(location: tuple[int, int], direction: int) -> tuple[int, int]:
    match direction:
        case 0:
            return location[0], location[1] - 1
        case 1:
            return location[0] + 1, location[1]
        case 2:
            return location[0], location[1] + 1
        case 3:
            return location[0] - 1, location[1]


def find_path_to_exit(location=(0, 0), steps_so_far=0, previously_visited=None) -> list:
    global map

    if location in min_steps_to_exit_from_location:
        return min_steps_to_exit_from_location[location]

    if location == (NUM_ROWS_AND_COLS - 1, NUM_ROWS_AND_COLS - 1):
        min_steps_to_exit_from_location[location] = steps_so_far
        return steps_so_far

    min_steps_to_exit = math.inf
    if previously_visited is None:
        previously_visited = set()

    for direction in DIRECTIONS:
        next_location = next_square(location, direction)
        if next_location in previously_visited or is_off_the_map(*next_location):
            continue
        next_terrain = map[next_location[0]][next_location[1]]
        match next_terrain:
            case 0:
                previously_visited.add(location)
                steps_to_exit = find_path_to_exit(
                    next_location, steps_so_far + 1, previously_visited.copy()
                )
                if steps_to_exit < min_steps_to_exit:
                    min_steps_to_exit = steps_to_exit
            case 1:
                continue
    return min_steps_to_exit


if __name__ == "__main__":
    construct_map()
    print_map()
    print(find_path_to_exit())
