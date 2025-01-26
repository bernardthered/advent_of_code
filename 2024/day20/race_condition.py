# Solution to
# https://adventofcode.com/2024/day/20

import copy
from itertools import permutations
import math
import os
from typing import Counter

height = 0
width = 0


class NoRouteExists(Exception):
    pass


def construct_map(
    input_filenumber: int,
) -> tuple[list[list[str]], tuple[int, int], tuple[int, int]]:
    global width
    global height

    map = []
    walls = set()

    script_path = os.path.dirname(os.path.realpath(__file__))
    input = open(os.path.join(script_path, f"input_{input_filenumber}.txt"))
    lines = input.readlines()
    for y, line in enumerate(lines):
        map.append([])
        for x, char in enumerate(line):
            match char:
                case ".":
                    map[y].append(math.inf)
                case "#":
                    if x != 0 and y != 0:
                        walls.add((y, x))
                    map[y].append(-1)
                case "S":
                    map[y].append(math.inf)
                    start = (y, x)
                case "E":
                    map[y].append(math.inf)
                    end = (y, x)
    height = y + 1
    width = x + 1
    return map, start, end, walls


def print_map(map, special_spots=None):
    global height
    global width
    for y in range(height):
        for x in range(width):
            if special_spots and (y, x) in special_spots:
                print("≈", end="")
            elif map[y][x] == -1:
                print("#", end="")
            else:
                print(".", end="")
        print()


def get_adjacent_empty_squares(map, location) -> set:
    global height
    global width

    adjacent_empty_squares = set()
    y, x = location
    if y > 0:
        if map[y - 1][x] == math.inf:
            adjacent_empty_squares.add((y - 1, x))
    if y < height - 2:
        if map[y + 1][x] == math.inf:
            adjacent_empty_squares.add((y + 1, x))
    if x > 0:
        if map[y][x - 1] == math.inf:
            adjacent_empty_squares.add((y, x - 1))
    if x < width - 2:
        if map[y][x + 1] == math.inf:
            adjacent_empty_squares.add((y, x + 1))
    return adjacent_empty_squares


def get_adjacent_squares_with_annotations(map, location) -> set:
    global height
    global width

    adjacent_empty_squares = set()
    y, x = location
    if y > 0:
        if map[y - 1][x] >= 0:
            adjacent_empty_squares.add((y - 1, x))
    if y < height - 2:
        if map[y + 1][x] >= 0:
            adjacent_empty_squares.add((y + 1, x))
    if x > 0:
        if map[y][x - 1] >= 0:
            adjacent_empty_squares.add((y, x - 1))
    if x < width - 2:
        if map[y][x + 1] >= 0:
            adjacent_empty_squares.add((y, x + 1))
    return adjacent_empty_squares


def annotate_map_with_distances_from_point(map, start) -> int:
    """
    A breadth-first search of the map, taking one step at a time and then
    adding all the unvisited adjacent open squares to the list of squares to
    process after taking the following step.

    Return the map with all the empty locations changed to the distance from the start.
    """
    next_step_locations = set([start])
    steps_from_start = 0

    while True:
        if not next_step_locations:
            return map

        locations = next_step_locations.copy()
        next_step_locations = set()
        for location in locations:
            map[location[0]][location[1]] = steps_from_start
            next_step_locations |= get_adjacent_empty_squares(map, location)

        steps_from_start += 1


def find_one_wall_cheats(
    distances_from_start, distances_from_end, walls, original_solution, min_savings=100
):
    # for each wall in the map:
    # if there's an empty spot on two sides of it:
    #   and the distance from the start to one adjacent square + 2 + the distance from the
    #   end to the other adjacent square < OG solution, it's a valid cheat.
    #   if the diff is > 100, it's a big cheat.

    cheat_count = 0
    for wall in walls:
        if wall[0] in [0, width] or wall[1] in [0, height]:
            continue
        adjacent_squares = get_adjacent_squares_with_annotations(
            distances_from_start, wall
        )
        # usually we just care about the spots directly across from each other, but there may be some weird diagonal
        # use case where we turn inside the wall and this will take care of that
        for location1, location2 in permutations(adjacent_squares, 2):
            dist_from_start = distances_from_start[location1[0]][location1[1]]
            dist_from_end = distances_from_end[location2[0]][location2[1]]
            if dist_from_end == math.inf:
                raise Exception
            if dist_from_start == math.inf:
                raise Exception
            cost_with_cheat = dist_from_start + 2 + dist_from_end
            if cost_with_cheat + min_savings <= original_solution:
                cheat_count += 1
    return cheat_count


def part1():
    map, start, end, walls = construct_map(2)
    print(f"Going from {start} to {end}")
    distances_from_start = copy.deepcopy(map)
    distances_from_end = copy.deepcopy(map)
    annotate_map_with_distances_from_point(distances_from_start, start)
    original_solution = distances_from_start[end[0]][end[1]]
    print(f"Solution with no cheats: {original_solution}")
    annotate_map_with_distances_from_point(distances_from_end, end)
    print("Number of cheats: ", end="")
    print(
        find_one_wall_cheats(
            distances_from_start,
            distances_from_end,
            walls,
            original_solution,
            min_savings=100,
        )
    )


def count_multi_step_cheats(
    location,
    distances_from_start,
    distances_from_end,
    original_solution,
    min_savings=100,
):
    """
    Return the # of cheats starting from `location` that save at least 100ns and end within 20 spaces of location.
    """
    cheat_count = 0
    min_y = max(location[0] - 20, 0)
    max_y = min(location[0] + 20, height - 1)
    dist_from_start = distances_from_start[location[0]][location[1]]

    for y in range(min_y, max_y + 1):
        delta_y = abs(location[0] - y)
        max_delta_x = 20 - delta_y
        min_x = max(location[1] - max_delta_x, 0)
        max_x = min(location[1] + max_delta_x, width - 2)
        for x in range(min_x, max_x + 1):

            dist_from_end = distances_from_end[y][x]
            if dist_from_end == -1:
                continue

            dist_from_start_to_end_of_cheat = abs(location[0] - y) + abs(
                location[1] - x
            )
            cost_with_cheat = (
                dist_from_start + dist_from_start_to_end_of_cheat + dist_from_end
            )
            if cost_with_cheat <= original_solution - min_savings:
                cheat_count += 1
    return cheat_count


def find_multi_wall_cheats(
    start,
    map,
    distances_from_start,
    distances_from_end,
    original_solution,
    min_savings=100,
):
    cheat_count = 0

    next_step_locations = set([start])
    steps_from_start = 0

    while True:
        if not next_step_locations:
            return cheat_count

        locations = next_step_locations.copy()
        next_step_locations = set()
        for location in locations:
            next_step_locations |= get_adjacent_empty_squares(map, location)
            # only needed to prevent get_adjacent_empty_squares() from returning this one again later:
            map[location[0]][location[1]] = steps_from_start
            cheat_count += count_multi_step_cheats(
                location,
                distances_from_start,
                distances_from_end,
                original_solution,
                min_savings,
            )
        steps_from_start += 1


def part2():
    map, start, end, _ = construct_map(2)
    distances_from_start = copy.deepcopy(map)
    distances_from_end = copy.deepcopy(map)
    annotate_map_with_distances_from_point(distances_from_start, start)
    original_solution = distances_from_start[end[0]][end[1]]
    print(f"Solution with no cheats: {original_solution}")
    annotate_map_with_distances_from_point(distances_from_end, end)
    print(
        find_multi_wall_cheats(
            start, map, distances_from_start, distances_from_end, original_solution, 100
        )
    )


if __name__ == "__main__":
    part2()
