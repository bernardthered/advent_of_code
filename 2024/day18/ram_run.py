# Solution to
# https://adventofcode.com/2024/day/18

import os

# part 1
INPUT_FILENUMBER = NUM_ROWS_AND_COLS = 7
MAX_BYTES = 12
# part 2
INPUT_FILENUMBER = NUM_ROWS_AND_COLS = 71
MAX_BYTES = 1024

map = []


class NoRouteExists(Exception):
    pass


def construct_map(max_bytes=MAX_BYTES) -> list[str]:
    global map
    map = [[0 for i in range(NUM_ROWS_AND_COLS)] for j in range(NUM_ROWS_AND_COLS)]

    script_path = os.path.dirname(os.path.realpath(__file__))
    input = open(os.path.join(script_path, f"input_{INPUT_FILENUMBER}.txt"))
    lines = input.readlines()
    for i, line in enumerate(lines):
        if i >= max_bytes:
            break

        x, y = line.strip().split(",")
        map[int(x)][int(y)] = 1
    return lines[i:]


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


def get_adjacent_empty_squares(location, visited: set) -> set:
    adjacent_empty_squares = set()
    x, y = location
    if x > 0:
        if map[x - 1][y] == 0:
            adjacent_empty_squares.add((x - 1, y))
    if x < NUM_ROWS_AND_COLS - 1:
        if map[x + 1][y] == 0:
            adjacent_empty_squares.add((x + 1, y))
    if y > 0:
        if map[x][y - 1] == 0:
            adjacent_empty_squares.add((x, y - 1))
    if y < NUM_ROWS_AND_COLS - 1:
        if map[x][y + 1] == 0:
            adjacent_empty_squares.add((x, y + 1))
    adjacent_empty_squares -= visited
    return adjacent_empty_squares


def find_min_distance_between_two_points(
    start=(0, 0), end=(NUM_ROWS_AND_COLS - 1, NUM_ROWS_AND_COLS - 1)
) -> int:
    """
    A breadth-first search of the map, taking one step at a time and then
    adding all the unvisited adjacent open squares to the list of squares to
    process after taking the following step.

    This avoids the cost of recursion and guarantees that we know the minimum
    number of steps to get to each square the first time we hit that square,
    so there is never a need to revisit any visited square. That in turn allows
    returning from this method as soon as we reach the end square, even if there
    are unprocessed paths and steps (because we know they won't get to the
    endpoint any sooner).

    Return the minimum number of steps to get from start to end.
    """
    next_step_locations = set([start])
    steps_from_start = 0
    visited = set()

    while True:
        if not next_step_locations:
            raise NoRouteExists(f"Couldn't find a path, after {steps_from_start} steps")
        steps_from_start += 1

        locations = next_step_locations.copy()
        next_step_locations = set()
        for location in locations:
            next_step_locations |= get_adjacent_empty_squares(location, visited)
            visited.add(location)

        if end in next_step_locations:
            return steps_from_start


def part1():
    construct_map()
    print(find_min_distance_between_two_points())


def part2():
    # Brute force approach, but it works and only takes a few seconds
    # with the large dataset
    remaining_bytes = construct_map()
    for byte in remaining_bytes:
        x, y = byte.strip().split(",")
        map[int(x)][int(y)] = 1
        try:
            find_min_distance_between_two_points()
        except NoRouteExists:
            print(f"{x},{y}")
            return


if __name__ == "__main__":
    part2()
