# Solution to
# https://adventofcode.com/2024/day/14


import math
import os
import re

input_line_re = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")


def parse_input_line(line):
    """
    p=0,4 v=3,-3
    """
    mo = input_line_re.match(line)
    return [int(var) for var in mo.groups()]


def compute_final_position(x, y, vx, vy, width, height, seconds):
    x += vx * seconds
    y += vy * seconds
    return x % width, y % height


def add_to_quadrant_count(x, y, width, height, quadrants):
    quadrant = None
    if y < int(height / 2):
        if x < int(width / 2):
            quadrant = 0
        elif x >= int(width / 2 + 0.5):
            quadrant = 1
    elif y >= int(height / 2 + 0.5):
        if x < int(width / 2):
            quadrant = 2
        elif x >= int(width / 2 + 0.5):
            quadrant = 3
    if quadrant is not None:
        quadrants[quadrant] += 1
    return quadrants


if __name__ == "__main__":
    # width = 11
    # height = 7
    width = 101
    height = 103
    seconds = 100
    quadrants = [0, 0, 0, 0]
    script_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_path, "input_2.txt")) as inputfile:
        for line in inputfile.readlines():
            x, y, vx, vy = parse_input_line(line)
            x, y = compute_final_position(x, y, vx, vy, width, height, seconds)
            quadrants = add_to_quadrant_count(x, y, width, height, quadrants)
    print(quadrants)
    print(math.prod(quadrants))
