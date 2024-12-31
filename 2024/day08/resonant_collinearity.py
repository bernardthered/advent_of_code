# Solution to
# https://adventofcode.com/2024/day/8


from itertools import combinations, permutations, product
import math
import os
import time

width = 0
height = 0


def input_lines_to_antenna_locations(lines):
    """
    Return a dict with keys representing the antennas' characters, and the values a list of 2-tuple
    locations of those antennas.

    E.g. {
        "a": [(0,4), (5,2), (7,1)],
        "0": [(1,3), (8,2)],
    }
    """

    global width
    global height

    antennas = {}

    for y, line in enumerate(lines):
        line = line.strip()
        for x, char in enumerate(line):
            if char != ".":
                if char in antennas:
                    antennas[char].append((x, y))
                else:
                    antennas[char] = [(x, y)]
    height = y + 1
    width = x + 1
    return antennas


def find_all_antinodes_for_one_direction(
    position, x_increment, y_increment, limit=math.inf
):
    # For part 1, set the limit to 1
    antinodes = set()
    position = (position[0] + x_increment, position[1] + y_increment)
    while (
        0 <= position[0] < width
        and 0 <= position[1] < height
        and len(antinodes) < limit
    ):
        antinodes.add(position)
        position = (position[0] + x_increment, position[1] + y_increment)
    return antinodes


def determine_antinode_locations(antennas, part1=False):
    limit = math.inf
    if part1:
        limit = 1
    antinodes = set()
    for char in antennas:
        for a1, a2 in combinations(antennas[char], 2):
            if not part1:
                antinodes.add(a1)
                antinodes.add(a2)
            distance_x = a2[0] - a1[0]
            distance_y = a2[1] - a1[1]
            antinodes |= find_all_antinodes_for_one_direction(
                a2, distance_x, distance_y, limit
            )
            antinodes |= find_all_antinodes_for_one_direction(
                a1, -distance_x, -distance_y, limit
            )
    return antinodes


if __name__ == "__main__":
    script_path = os.path.dirname(os.path.realpath(__file__))
    input = open(os.path.join(script_path, "input_3.txt"))
    lines = input.readlines()
    antennas = input_lines_to_antenna_locations(lines)
    print(len(determine_antinode_locations(antennas, part1=False)))
