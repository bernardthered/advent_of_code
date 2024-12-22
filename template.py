# Solution to https://adventofcode.com/2024/day/N

import os

INPUT_FILE_NUMBER = 1


def parse_input():
    script_path = os.path.dirname(os.path.realpath(__file__))
    input = open(os.path.join(script_path, f"input_{INPUT_FILE_NUMBER}.txt")).read()
    return input


def main(input):
    answer = 0
    return answer


if __name__ == "__main__":
    input = parse_input()
    print(main(input))
