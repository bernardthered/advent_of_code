# Solution to
# https://adventofcode.com/2024/day/15


import math
import os
import re

input_line_re = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")

DIRECTIONS = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}


def read_input(filenum):
    map = []
    script_path = os.path.dirname(os.path.realpath(__file__))
    reading_map = True
    moves = ""
    with open(os.path.join(script_path, f"input_{filenum}.txt")) as inputfile:
        for y, line in enumerate(inputfile.readlines()):
            line = line.strip()
            if line == "":
                reading_map = False
            if reading_map:
                map.append([])
                for x, char in enumerate(line):
                    if char == "@":
                        char = "."
                        robot = (y, x)
                    map[y].append(char)
            else:
                moves += line
    return map, robot, moves


def process_move(move, map, robot):
    next = (robot[0] + DIRECTIONS[move][0], robot[1] + DIRECTIONS[move][1])

    if map[next[0]][next[1]] == ".":
        map[robot[0]][robot[1]] = "."
        robot = next
        map[robot[0]][robot[1]] = "@"
        return robot
    elif map[next[0]][next[1]] == "#":
        return robot
    elif map[next[0]][next[1]] == "O":
        barrel_line_spot = (next[0], next[1])
        while map[barrel_line_spot[0]][barrel_line_spot[1]] == "O":
            barrel_line_spot = (
                barrel_line_spot[0] + DIRECTIONS[move][0],
                barrel_line_spot[1] + DIRECTIONS[move][1],
            )
        if map[barrel_line_spot[0]][barrel_line_spot[1]] == "#":
            # Nothing moves!
            return robot
        elif map[barrel_line_spot[0]][barrel_line_spot[1]] == ".":
            # the first barrel moves to the empty spot
            map[barrel_line_spot[0]][barrel_line_spot[1]] = "O"
            # the robot moves to the spot it was originally trying to move to
            map[robot[0]][robot[1]] = "."
            robot = next
            map[robot[0]][robot[1]] = "@"
            return robot
        else:
            raise Exception(
                f"Shouldn't get here. map[{barrel_line_spot}] = {map[barrel_line_spot[0]][barrel_line_spot[1]]}"
            )


def calculate_gps_sum(map):
    total = 0
    for y, line in enumerate(map):
        for x, char in enumerate(line):
            if char == "O":
                total += (y * 100) + x
    return total


def part1():
    map, robot, moves = read_input(2)
    for move in moves:
        robot = process_move(move, map, robot)
    print_map(map)
    print(calculate_gps_sum(map))


def print_map(map):
    for line in map:
        for char in line:
            print(char, end="")
        print()


if __name__ == "__main__":
    part1()
