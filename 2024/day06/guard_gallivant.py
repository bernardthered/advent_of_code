# Solution to
# https://adventofcode.com/2024/day/6

import os


LOGLEVEL = 100

DIRECTIONS = {0: "up", 1: "right", 2: "down", 3: "left"}


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


def part1(map, guard_location):
    squares_visited = 1  # The starting square counts
    direction = 0
    while True:
        moving_to_location = next_square(guard_location, direction)
        if is_off_the_map(*moving_to_location):
            print(f"Exited the map at {moving_to_location}")
            return squares_visited
        next_terrain = map[moving_to_location[0]][moving_to_location[1]]
        match next_terrain:
            case ".":
                guard_location = moving_to_location
                map[moving_to_location[0]][moving_to_location[1]] = "X"
                squares_visited += 1
            case "X":
                guard_location = moving_to_location
            case "#":
                direction += 1
                direction %= 4


if __name__ == "__main__":
    script_path = os.path.dirname(os.path.realpath(__file__))
    input = open(os.path.join(script_path, "input_2.txt"))
    lines = input.readlines()
    map, guard_location = input_lines_to_map(lines)
    print(part1(map, guard_location))
