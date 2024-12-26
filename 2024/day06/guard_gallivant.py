# Solution to
# https://adventofcode.com/2024/day/6

import copy
import os


LOGLEVEL = 100

DIRECTIONS = {0: "up", 1: "right", 2: "down", 3: "left"}


class InfiniteLoop(Exception):
    pass


highest_row_num = 0
highest_col_num = 0


def log(msg, level=10):
    if level >= LOGLEVEL:
        print(msg)


def input_lines_to_map(lines):
    global highest_col_num
    global highest_row_num

    map = []
    for y, line in enumerate(lines):
        line = line.strip()
        map.append([])
        for x, char in enumerate(line):
            map[y].append(char)
            if char == "^":
                guard_location = (y, x)
                map[y][x] = "X"  # mark the starting square as visited
    highest_row_num = y
    highest_col_num = x
    return map, guard_location


def is_off_the_map(row_num, col_num):
    return (
        row_num < 0
        or col_num < 0
        or row_num > highest_row_num
        or col_num > highest_col_num
    )


def next_square(location: tuple[int, int], direction: int) -> tuple[int, int]:
    match direction:
        case 0:
            return location[0] - 1, location[1]
        case 1:
            return location[0], location[1] + 1
        case 2:
            return location[0] + 1, location[1]
        case 3:
            return location[0], location[1] - 1


def trace_path(map, guard_location) -> list:
    direction = 0
    # Each item in visited_locations also tracks the direction: ((y, x), direction).
    # This enables us to quickly detect if we are in a loop.
    visited_locations = set()
    while True:
        moving_to_location = next_square(guard_location, direction)
        if is_off_the_map(*moving_to_location):
            return visited_locations
        next_terrain = map[moving_to_location[0]][moving_to_location[1]]
        match next_terrain:
            case ".":
                guard_location = moving_to_location
                visited_locations.add((guard_location, direction))
                map[moving_to_location[0]][moving_to_location[1]] = "X"
                # squares_visited += 1
            case "X":
                guard_location = moving_to_location
                # We've been here before. Check if we're in a loop.
                if (guard_location, direction) in visited_locations:
                    # We're stuck in a loop!
                    raise InfiniteLoop()
            case "#":
                direction += 1
                direction %= 4


def count_obstacle_possibilities(map, visited_locations, guard_location):
    obstacle_possibilities = 0
    for possible_obstactle_location, _ in enumerate(visited_locations):
        try:
            newmap = copy.deepcopy(map)
            newmap[possible_obstactle_location[0]][possible_obstactle_location[1]] = "#"
            trace_path(newmap, guard_location)
        except InfiniteLoop:
            obstacle_possibilities += 1
    return obstacle_possibilities


if __name__ == "__main__":
    script_path = os.path.dirname(os.path.realpath(__file__))
    input = open(os.path.join(script_path, "input_2.txt"))
    lines = input.readlines()
    map, guard_location = input_lines_to_map(lines)
    visited_locations = trace_path(copy.deepcopy(map), guard_location)
    print(
        f"Part 1: {len(visited_locations) + 1}"
    )  # The +1 is to account for the guard's original position
    print(
        f"Part 2: {count_obstacle_possibilities(map, visited_locations, guard_location)}"
    )
