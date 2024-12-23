# Solution to https://adventofcode.com/2024/day/21

import functools
import os
import re
import time

INPUT_FILE_NUMBER = 1
# For part 1, this should be 3, for part 2, it should be 26
DEPTH_OF_ROBOTS = 1

PADS = {
    "keypad": {
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


def get_button_presses_for_code(code, pad):
    sequence = ""
    startingchar = "A"
    for char in code:
        sequence += get_button_presses_for_move(startingchar, char, pad)
        startingchar = char
    # print(f"Code: {code}, seq: {sequence}")
    return sequence


def get_outer_sequence(code, levels_deep):
    t1 = time.time()
    current_pad_sequence = get_button_presses_for_code(code, "keypad")
    for i in range(levels_deep - 1):
        td = int(time.time() - t1)
        print(
            f"{i+1}/{levels_deep - 1}, {td}s: current length = {len(current_pad_sequence)}"
        )
        current_pad_sequence = get_button_presses_for_code(
            current_pad_sequence, "directional_pad"
        )
    return current_pad_sequence


def get_outer_code_complexity(code):
    # outer_sequence = get_outer_sequence(code, DEPTH_OF_ROBOTS)

    move_length = 0
    for button in code:
        move_length += calculate_move_length(button, DEPTH_OF_ROBOTS)

    numeric_part_of_code = re.sub("^0*", "", code)
    numeric_part_of_code = re.sub("A", "", numeric_part_of_code)
    complexity = move_length * int(numeric_part_of_code)
    print(f"Code: {code}, {move_length} * {int(numeric_part_of_code)}")
    return complexity


def get_code_complexities(codes):
    answer = 0
    for code in codes:
        answer += get_outer_code_complexity(code.strip())
        break
    return answer


# @functools.cache
def calculate_move_length(button, depth):
    if depth == 0:
        print(button, end="")
        return 1  # just one button to press

    if depth == DEPTH_OF_ROBOTS:
        pad = "keypad"
    else:
        pad = "directional_pad"
    move_length = 0
    button_presses = get_button_presses_for_code(button, pad)
    for upper_button in button_presses:
        move_length += calculate_move_length(upper_button, depth - 1)

    if depth == DEPTH_OF_ROBOTS:
        print()
        print(
            f"Move lengths for '{button}' for depth {depth}: {move_length} ({button_presses})"
        )
    return move_length


def pre_cache_move_lengths():
    for depth in range(DEPTH_OF_ROBOTS):
        for key in PADS["directional_pad"]:
            if key == "verboten":
                continue
            calculate_move_length(key, depth)


if __name__ == "__main__":
    pre_cache_move_lengths()
    print("------------")
    codes = parse_input()
    print(get_code_complexities(codes))
