# Solution to https://adventofcode.com/2024/day/21

import functools
import os
import re
import time

INPUT_FILE_NUMBER = 2

PADS = {
    "num_pad": {
        "7": (0, 0),
        "8": (0, 1),
        "9": (0, 2),
        "4": (1, 0),
        "5": (1, 1),
        "6": (1, 2),
        "1": (2, 0),
        "2": (2, 1),
        "3": (2, 2),
        "0": (3, 1),
        "A": (3, 2),
        "verboten": (3, 0),
    },
    "directional_pad": {
        "^": (0, 1),
        "A": (0, 2),
        "<": (1, 0),
        "v": (1, 1),
        ">": (1, 2),
        "verboten": (0, 0),
    },
}


def parse_input():
    script_path = os.path.dirname(os.path.realpath(__file__))
    input_file = open(os.path.join(script_path, f"input_{INPUT_FILE_NUMBER}.txt"))
    return input_file.readlines()


def move_horizontally(l1, l2):
    Δx = l2[1] - l1[1]
    if Δx < 0:
        return "<" * abs(Δx)
    return ">" * abs(Δx)


def move_vertically(l1, l2):
    Δy = l2[0] - l1[0]
    if Δy < 0:
        return "^" * abs(Δy)
    return "v" * abs(Δy)


@functools.cache
def get_button_presses_for_move(char1, char2, padname) -> str:
    pad = PADS[padname]

    sequence = ""
    l1 = pad[char1]
    l2 = pad[char2]

    # Move horizontally first by default
    move_horizontally_first = True

    if l2[1] - l1[1] > 0:
        # We are moving to the right. When moving right, it's most efficient to
        # move vertically first, if it's safe
        if not (l2[0], l1[1]) == pad["verboten"]:
            # moving vertically first is safe
            move_horizontally_first = False

    if (l1[0], l2[1]) == pad["verboten"]:
        # moving horizontally first is not safe, we need to move vertically first
        move_horizontally_first = False

    if move_horizontally_first:
        sequence += move_horizontally(l1, l2)
        sequence += move_vertically(l1, l2)
    else:
        sequence += move_vertically(l1, l2)
        sequence += move_horizontally(l1, l2)

    return sequence + "A"


@functools.cache
def get_button_presses_for_code(code, pad, quiet=False):
    sequence = ""
    startingchar = "A"
    for char in code:
        sequence += get_button_presses_for_move(startingchar, char, pad)
        startingchar = char
    if not quiet:
        print(f"Code: {code}, seq: {sequence}")
    return sequence


def get_outer_sequence(code, levels_deep):
    t1 = time.time()
    current_pad_sequence = get_button_presses_for_code(code, "num_pad")
    for i in range(levels_deep - 1):
        td = int(time.time() - t1)
        # print(
        #     f"{i+1}/{levels_deep - 1}, {td}s: current length = {len(current_pad_sequence)}"
        # )
        current_pad_sequence = get_button_presses_for_code(
            current_pad_sequence, "directional_pad", quiet=True
        )
    return current_pad_sequence


def get_outer_code_complexity(code):
    # For part 1, this should be 3, for part 2, it would be 26
    depth_of_robots = 3
    outer_sequence = get_outer_sequence(code, depth_of_robots)
    numeric_part_of_code = re.sub("^0*", "", code)
    numeric_part_of_code = re.sub("A", "", numeric_part_of_code)
    complexity = len(outer_sequence) * int(numeric_part_of_code)
    print(outer_sequence)
    print(
        f"For code: {code}, complexity = {len(outer_sequence)} * {int(numeric_part_of_code)}"
    )
    return complexity


def get_code_complexities(codes):
    answer = 0
    for code in codes:
        answer += get_outer_code_complexity(code.strip())
    return answer


if __name__ == "__main__":
    codes = parse_input()
    print(get_code_complexities(codes))
