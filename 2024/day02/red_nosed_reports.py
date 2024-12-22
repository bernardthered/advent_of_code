# Solution to https://adventofcode.com/2024/day/2

import copy
import os

INPUT_FILE_NUMBER = 2


def parse_input():
    script_path = os.path.dirname(os.path.realpath(__file__))
    input_file = open(os.path.join(script_path, f"input_{INPUT_FILE_NUMBER}.txt"))
    return input_file


def is_report_safe(levels):
    increasing = False
    if levels[1] > levels[0]:
        increasing = True
    for i in range(1, len(levels)):
        diff = levels[i] - levels[i - 1]
        if increasing:
            if diff > 3 or diff < 1:
                # This report is unsafe, no further processing needed
                return False
        else:
            if diff < -3 or diff > -1:
                # This report is unsafe, no further processing needed
                return False
    return True


def count_safe_reports(input_file):
    safe_count = 0
    for report in input_file.readlines():
        levels = [int(level) for level in report.split()]
        if is_report_safe(levels):
            safe_count += 1
        else:
            for i in range(len(levels)):
                revised_levels = copy.copy(levels)
                del revised_levels[i]
                if is_report_safe(revised_levels):
                    safe_count += 1
                    break
    return safe_count


if __name__ == "__main__":
    input_file = parse_input()
    print(count_safe_reports(input_file))
