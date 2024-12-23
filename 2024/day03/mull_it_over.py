# Solution to https://adventofcode.com/2024/day/3

import os
import re

INPUT_FILE_NUMBER = 2

dont_re = re.compile("don't\(\)")
do_re = re.compile("do\(\)")
mul_re = re.compile("mul\((\d+),(\d+)\)")


def parse_input():
    script_path = os.path.dirname(os.path.realpath(__file__))
    input_file = open(os.path.join(script_path, f"input_{INPUT_FILE_NUMBER}.txt"))
    return input_file.read().strip()


def multiply_the_things(input):
    sum = 0
    matches = mul_re.findall(input)
    for match in matches:
        if not match:
            continue
        sum += int(match[0]) * int(match[1])
    return sum


def remove_the_cruft(input):
    removed = True
    while removed:
        mo = dont_re.search(input)
        if not mo:
            break
        dont_location = mo.start()
        mo = do_re.search(input, pos=dont_location)
        if mo:
            do_location = mo.start()
        else:
            do_location = len(input)
        if dont_location and do_location:
            input = input[:dont_location] + input[do_location:]
    return input


if __name__ == "__main__":
    input = parse_input()
    input = remove_the_cruft(input)
    print(multiply_the_things(input))
