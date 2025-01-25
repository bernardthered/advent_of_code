# Solution to
# https://adventofcode.com/2024/day/25


import os


def read_key_or_lock(inputfile, line, stopchar):
    key_or_lock = [None] * 5
    row_num = 0
    while line:
        for col_num, char in enumerate(line):
            if char == stopchar and key_or_lock[col_num] is None:
                if stopchar == ".":
                    key_or_lock[col_num] = row_num - 1
                else:
                    key_or_lock[col_num] = 5 - (row_num - 1)

        line = inputfile.readline().strip()
        row_num += 1
    return key_or_lock


def read_input(filenum):
    keys = []
    locks = []

    script_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_path, f"input_{filenum}.txt")) as inputfile:
        line = inputfile.readline().strip()
        while line:
            if "." in line:
                keys.append(read_key_or_lock(inputfile, line, stopchar="#"))
            else:
                locks.append(read_key_or_lock(inputfile, line, stopchar="."))
            line = inputfile.readline().strip()
    return keys, locks


def fits(key, lock):
    for i in range(5):
        if key[i] + lock[i] > 5:
            return False
    return True


def count_combos_that_fit(keys, locks):
    count = 0
    for key in keys:
        for lock in locks:
            if fits(key, lock):
                count += 1
    return count


def part1():
    keys, locks = read_input(2)
    return count_combos_that_fit(keys, locks)


if __name__ == "__main__":
    print(part1())
