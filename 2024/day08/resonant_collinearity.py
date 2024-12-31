# Solution to
# https://adventofcode.com/2024/day/8


from itertools import combinations, permutations, product
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


def determine_antinode_locations(antennas):
    antinodes = set()
    for char in antennas:
        print(f"{char}:")
        for a1, a2 in combinations(antennas[char], 2):
            print(f"  {a1} - {a2}")
            distance_x = a2[0] - a1[0]
            distance_y = a2[1] - a1[1]
            antinode1 = (a2[0] + distance_x, a2[1] + distance_y)
            antinode2 = (a1[0] - distance_x, a1[1] - distance_y)
            if 0 <= antinode1[0] < width and 0 <= antinode1[1] < height:
                antinodes.add(antinode1)
            if 0 <= antinode2[0] < width and 0 <= antinode2[1] < height:
                antinodes.add(antinode2)
    print(antinodes)
    return len(antinodes)


if __name__ == "__main__":
    script_path = os.path.dirname(os.path.realpath(__file__))
    input = open(os.path.join(script_path, "input_3.txt"))
    lines = input.readlines()
    antennas = input_lines_to_antenna_locations(lines)
    print(antennas)
    print()
    print(determine_antinode_locations(antennas))
