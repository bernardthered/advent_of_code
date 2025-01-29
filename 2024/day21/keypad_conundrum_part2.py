# Solution to https://adventofcode.com/2024/day/21 part 2
# This would technically work to solve part 1, this algorithm yields the same result, it
# is just much more efficient and can handle the scale of part 2 (depth = 25 instead of 2)

import functools
import re


from keypad_conundrum import *


@functools.cache
def get_length_of_sequence(sequence, levels_deep):
    """
    Depth-first traversal of the keypresses at the next level up in order to achieve sequence at this level.

    Returning the length of the series of keypresses at the next level up.
    """
    sequence = get_button_presses_for_code(sequence, "directional_pad", quiet=True)
    if levels_deep == 1:
        return len(sequence)

    sequence_length = 0
    for subsequence in sequence.split("A")[:-1]:
        sequence_length += get_length_of_sequence(subsequence + "A", levels_deep - 1)
    return sequence_length


def get_length_of_outer_sequence(code, levels_deep):
    length_of_outer_sequence = 0
    sequence = get_button_presses_for_code(code, "num_pad", quiet=True)
    for subsequence in sequence.split("A")[:-1]:
        length_of_outer_sequence += get_length_of_sequence(
            subsequence + "A", levels_deep
        )
    return length_of_outer_sequence


def get_outer_code_complexity(code):
    depth = 25
    outer_sequence_len = get_length_of_outer_sequence(code, depth)
    print(f"Code: {code} -> {outer_sequence_len}")
    numeric_part_of_code = re.sub("^0*", "", code)
    numeric_part_of_code = re.sub("A", "", numeric_part_of_code)
    complexity = outer_sequence_len * int(numeric_part_of_code)
    return complexity


def get_code_complexities(codes):
    answer = 0
    for code in codes:
        answer += get_outer_code_complexity(code.strip())
    return answer


if __name__ == "__main__":
    codes = parse_input()
    print(get_code_complexities(codes))
