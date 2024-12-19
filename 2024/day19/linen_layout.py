# Solution to https://adventofcode.com/2024/day/19

import os

INPUT_FILE_NUMBER = 2


def parse_input():
    script_path = os.path.dirname(os.path.realpath(__file__))
    input_file = open(os.path.join(script_path, f"input_{INPUT_FILE_NUMBER}.txt"))
    available_cloths = input_file.readline()
    available_cloths = [cloth.strip() for cloth in available_cloths.split(", ")]
    desired_towels = []
    while towel_design := input_file.readline():
        if clean_towel_design := towel_design.strip():
            desired_towels.append(clean_towel_design)

    # print(available_cloths, desired_towels)
    return available_cloths, desired_towels


def can_make_towel_from_available_cloths(available_cloths, desired_towel):
    for cloth in available_cloths:
        if len(desired_towel) == 0:
            return True
        if desired_towel.startswith(cloth):
            remaining_desired_towel = desired_towel[len(cloth) :]
            if can_make_towel_from_available_cloths(
                available_cloths, remaining_desired_towel
            ):
                return True
    return False


def main(available_cloths, desired_towels):
    answer = 0
    for desired_towel in desired_towels:
        if can_make_towel_from_available_cloths(available_cloths, desired_towel):
            answer += 1
    print(answer)


if __name__ == "__main__":
    available_cloths, desired_towels = parse_input()
    main(available_cloths, desired_towels)
