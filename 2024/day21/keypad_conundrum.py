# Solution to https://adventofcode.com/2024/day/2

import copy
import os
import re

INPUT_FILE_NUMBER = 2

keypad = {
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
}

directional_pad = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
    "verboten": (0, 0),
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


def get_sequence_of_button_presses_for_single_move(char1, char2, pad):
    # This approach is insufficient for 1+ reasons:
    #   1) the robot cannot move its finger over the blank space on the keypad
    #   2) to optimize for shortest path, we may need to strategically end the intermediary
    #      robot arms over one button instead of another. Perhaps this doesn't matter, since
    #      they need to move to the A after every set of moves. Needs further consideration.
    sequence = ""
    l1 = pad[char1]
    l2 = pad[char2]

    move_horizontally_first = True

    if l2[1] - l1[1] > 0:
        # We are moving to the right
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


def get_sequence_of_button_presses_for_code(code, pad):
    sequence = ""
    startingchar = "A"
    for char in code:
        sequence += get_sequence_of_button_presses_for_single_move(
            startingchar, char, pad
        )
        startingchar = char
        # sequence += get_sequence_of_button_presses_for_single_move(char, "A", keypad)
    # print(f"Code: {code}, seq: {sequence}")
    return sequence


def get_code_complexity(code):
    first_directional_pad_sequence = get_sequence_of_button_presses_for_code(
        code, keypad
    )
    second_directional_pad_sequence = get_sequence_of_button_presses_for_code(
        first_directional_pad_sequence, directional_pad
    )
    third_directional_pad_sequence = get_sequence_of_button_presses_for_code(
        second_directional_pad_sequence, directional_pad
    )
    numeric_part_of_code = re.sub("^0*", "", code)
    numeric_part_of_code = re.sub("A", "", numeric_part_of_code)
    complexity = len(third_directional_pad_sequence) * int(numeric_part_of_code)
    print(
        f"Code: {code}, {len(third_directional_pad_sequence)} * {int(numeric_part_of_code)}, {third_directional_pad_sequence}"
    )
    return complexity


def get_code_complexities(codes):
    answer = 0
    for code in codes:
        answer += get_code_complexity(code.strip())
    return answer


if __name__ == "__main__":
    codes = parse_input()
    print(get_code_complexities(codes))
