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


def part1():
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


def print_map(final_positions, width, height):
    for y in range(height):
        for x in range(width):
            if (x, y) in final_positions:
                print("O", end="")
            else:
                print(".", end="")
        print()


def is_horizontal_line_in_positions(final_positions, x, y, length):
    """
    Check from position x,y to see if there is a line that forms either direction of at least length 'length'
    """
    for i in range(length):
        if (x - i, y) not in final_positions:
            break
    # At this point, we have moved as far left as the line goes. We'll try moving right from the starting point next
    # if the total number of spaces that the line goes left (i) plus the number right it goes (j) gets to 'length',
    # then we found a line of that length.
    for j in range(i, length):
        if (x + j, y) not in final_positions:
            return False
    return True


def part2():
    width = 11
    height = 7
    width = 101
    height = 103
    ps_and_vs = []
    script_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_path, "input_2.txt")) as inputfile:
        for line in inputfile.readlines():
            x, y, vx, vy = parse_input_line(line)
            ps_and_vs.append((x, y, vx, vy))

    s = 0
    while True:
        s += 1
        final_positions = set()
        for x, y, vx, vy in ps_and_vs:
            x, y = compute_final_position(x, y, vx, vy, width, height, s)
            final_positions.add((x, y))
            if is_horizontal_line_in_positions(final_positions, x, y, 10):
                print_map(final_positions, width, height)
                input(f"{s}s elapsed. press enter to continue.")


if __name__ == "__main__":
    part2()
