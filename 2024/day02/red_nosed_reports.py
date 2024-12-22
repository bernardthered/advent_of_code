# Solution to https://adventofcode.com/2024/day/2

import os

INPUT_FILE_NUMBER = 1


def parse_input():
    script_path = os.path.dirname(os.path.realpath(__file__))
    input_file = open(os.path.join(script_path, f"input_{INPUT_FILE_NUMBER}.txt"))
    return input_file


def is_report_safe(report):
    levels = [int(level) for level in report.split()]
    increasing = False
    if levels[1] > levels[0]:
        increasing = True
    for i in range(1, len(levels)):
        diff = levels[i] - levels[i - 1]
        if increasing:
            if diff > 3 or diff < 1:
                # This report is unsafe, no further processing needed
                # print(
                #     f"Unsafe increasing report: {levels} ({levels[i]} - {levels[i - 1]} = {diff})"
                # )
                return False
        else:
            if diff < -3 or diff > -1:
                # This report is unsafe, no further processing needed
                # print(
                #     f"Unsafe decreasing report: {levels} ({levels[i]} - {levels[i - 1]} = {diff})"
                # )
                return False
    # print(f"Safe: {levels}")
    return True


def count_safe_reports(input_file):
    safe_count = 0
    for report in input_file.readlines():
        if is_report_safe(report):
            safe_count += 1
    return safe_count


if __name__ == "__main__":
    input_file = parse_input()
    # print(compute_distance_between_lists(l1, l2))
    print(count_safe_reports(input_file))
