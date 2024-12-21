# Solution to https://adventofcode.com/2024/day/NN

import os

INPUT_FILE_NUMBER = 1


def parse_input():
    script_path = os.path.dirname(os.path.realpath(__file__))
    input_file = open(os.path.join(script_path, f"input_{INPUT_FILE_NUMBER}.txt"))
    l1 = []
    l2 = []
    for line in input_file.readlines():
        n1, n2 = line.split("   ")
        l1.append(int(n1))
        l2.append(int(n2))
    return l1, l2


def compute_distance_between_lists(l1, l2):
    answer = 0
    l1.sort()
    l2.sort()
    for i in range(len(l1)):
        answer += abs(l1[i] - l2[i])
    return answer


def compute_similarity_of_lists(l1, l2):
    answer = 0
    for n1 in l1:
        answer += n1 * l2.count(n1)
    return answer


if __name__ == "__main__":
    l1, l2 = parse_input()
    # print(compute_distance_between_lists(l1, l2))
    print(compute_similarity_of_lists(l1, l2))
