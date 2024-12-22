# Solution to https://adventofcode.com/2024/day/2

import copy
import os

INPUT_FILE_NUMBER = 1

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
}

directional_pad = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}


def parse_input():
    script_path = os.path.dirname(os.path.realpath(__file__))
    input_file = open(os.path.join(script_path, f"input_{INPUT_FILE_NUMBER}.txt"))
    return input_file.readlines()


def get_sequence_of_button_presses_for_single_move(char1, char2, pad):
    sequence = ""
    l1 = pad[char1]
    l2 = pad[char2]

    Δx = l2[1] - l1[1]
    Δy = l2[0] - l1[0]

    if Δx < 0:
        sequence += "<" * abs(Δx)
    elif Δx > 0:
        sequence += ">" * abs(Δx)
    if Δy < 0:
        sequence += "^" * abs(Δy)
    elif Δy > 0:
        sequence += "v" * abs(Δy)
    return sequence + "A"


def get_sequence_of_button_presses_for_code(code):
    sequence = ""
    startingchar = "A"
    for char in code:
        sequence += get_sequence_of_button_presses_for_single_move(
            startingchar, char, keypad
        )
        startingchar = char
        # sequence += get_sequence_of_button_presses_for_single_move(char, "A", keypad)
    print(f"Code: {code}, seq: {sequence}")
    return sequence


def get_code_complexity(code):
    return len(get_sequence_of_button_presses_for_code(code.strip()))


def get_code_complexities(codes):
    answer = 0
    for code in codes:
        answer += get_code_complexity(code)
        break
    return answer


if __name__ == "__main__":
    codes = parse_input()
    print(get_code_complexities(codes))
