# Solution to https://adventofcode.com/2024/day/19

import os
import time

INPUT_FILE_NUMBER = 2

# The recursion takes too long with a large dataset, so we cache our known findings so far in the known_combos dictionary.
# The keys of the dict are the towel patterns (e.g. "rrbgbr") and the values are the # of ways to make that pattern (e.g. 6).
# This speeds up the time it takes to run with the input provided from hours to < 1s.
known_combos = {}


def parse_input():
    script_path = os.path.dirname(os.path.realpath(__file__))
    input_file = open(os.path.join(script_path, f"input_{INPUT_FILE_NUMBER}.txt"))
    available_cloths = input_file.readline()
    available_cloths = [cloth.strip() for cloth in available_cloths.split(", ")]
    desired_towels = []
    while towel_design := input_file.readline():
        if clean_towel_design := towel_design.strip():
            desired_towels.append(clean_towel_design)
    return available_cloths, desired_towels


def can_make_towel(available_cloths, desired_towel):
    for cloth in available_cloths:
        if len(desired_towel) == 0:
            return True
        if desired_towel.startswith(cloth):
            remaining_desired_towel = desired_towel[len(cloth) :]
            if can_make_towel(available_cloths, remaining_desired_towel):
                return True
    return False


def ways_to_make_towel(available_cloths, desired_towel, depth=0):
    global known_combos

    ways = 0
    if not desired_towel:
        return 1

    if desired_towel in known_combos:
        return known_combos[desired_towel]

    for i, cloth in enumerate(available_cloths):
        if desired_towel.startswith(cloth):
            remaining_desired_towel = desired_towel[len(cloth) :]
            ways += ways_to_make_towel(
                available_cloths, remaining_desired_towel, depth + 1
            )
    if ways > 0:
        known_combos[desired_towel] = ways
    return ways


def part1(available_cloths, desired_towels):
    answer = 0
    for desired_towel in desired_towels:
        if can_make_towel(available_cloths, desired_towel):
            answer += 1
    print(answer)


def part2(available_cloths, desired_towels):
    t1 = time.time()
    answer = 0
    print(f"# of available cloths: {len(available_cloths)}")
    total_desired_towels = len(desired_towels)
    for i, desired_towel in enumerate(desired_towels):
        t2 = time.time()
        if i == 0 or (i + 1) % 50 == 0:
            print(
                f"{int(t2-t1)}s: Working on desired towel #{i+1}/{total_desired_towels}"
            )
        ways = ways_to_make_towel(available_cloths, desired_towel)
        answer += ways
    print(answer)


if __name__ == "__main__":
    available_cloths, desired_towels = parse_input()
    part2(available_cloths, desired_towels)
