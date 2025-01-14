# Solution to
# https://adventofcode.com/2024/day/24


import os


def read_input(filenum):
    values = {}
    operations = {}
    script_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_path, f"input_{filenum}.txt")) as inputfile:
        line = inputfile.readline().strip()
        while line:
            var, val = line.strip().split(": ")
            values[var] = int(val)
            line = inputfile.readline().strip()

        line = inputfile.readline().strip()
        while line:
            operation, assignee = line.strip().split(" -> ")
            operations[assignee] = operation.split()
            line = inputfile.readline()

    return values, operations


def determine_all_values(values, operations):
    did_something = False
    first = True
    while did_something or first:
        first = False
        did_something = False
        for operation_assignee in operations:
            if operation_assignee in values:
                continue
            operation = operations[operation_assignee]
            if operation[0] not in values or operation[2] not in values:
                continue
            value1 = values[operation[0]]
            value2 = values[operation[2]]
            if operation[1] == "AND":
                values[operation_assignee] = value1 & value2
            elif operation[1] == "OR":
                values[operation_assignee] = value1 | value2
            elif operation[1] == "XOR":
                values[operation_assignee] = value1 ^ value2
            did_something = True
    return values


def determine_z_binary(values):
    str_bin_val = ""
    z_keys = [k for k in values if k.startswith("z")]
    z_keys.sort()
    z_keys.reverse()
    for z_key in z_keys:
        str_bin_val += str(values[z_key])
    print(str_bin_val)
    return int(str_bin_val, base=2)


def part1():
    values, operations = read_input(2)
    values = determine_all_values(values, operations)
    print(determine_z_binary(values))


if __name__ == "__main__":
    part1()
