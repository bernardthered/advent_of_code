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


def find_operators_for_operand(operand, operations):
    # This is innefficient using the data structure for operations that we are reusing from part 1,
    # but at this scale it shouldn't make a noticiable difference.
    matching_operators = set()
    for _, operation in operations.items():
        if operand in operation:
            matching_operators.add(operation[1])
    return matching_operators


def follows_rule_1(operation_assignee, operation, values, operations):
    """
    XOR only takes an input bit if a XOR follows it, unless the input bits are the first bits
    """
    if operation[0] not in values and operation[2] not in values:
        return True
    if "x00" in operation and "y00" in operation:
        return True
    # At this point it takes an input bit and the inputs are not the first bits
    next_operators = find_operators_for_operand(operation_assignee, operations)
    if "XOR" in next_operators:
        return True
    return False


def follows_rule_2(operation_assignee, operation, operations):
    """
    ANDs are only followed by ORs, unless the input bits are the first bits
    """
    if "x00" in operation and "y00" in operation:
        return True
    next_operators = find_operators_for_operand(operation_assignee, operations)
    if "AND" in next_operators or "XOR" in next_operators:
        return False
    return True


def follows_rule_3(operation_assignee, operation):
    """
    If the output of a gate is z, then the operation has to be XOR unless it is the last bit.
    """
    if not operation_assignee.startswith("z") or operation_assignee == "z45":
        return True
    if operation[1] == "XOR":
        return True
    return False


def follows_rule_4(operation_assignee, operation, values):
    """
    If the output of a gate is not z and the inputs are not x, y then it has to be AND / OR, but not XOR.
    """
    if operation_assignee.startswith("z"):
        return True
    if operation[0] in values and operation[2] in values:
        return True
    if operation[1] == "XOR":
        return False
    return True


def part2():
    bad_assignees = set()
    values, operations = read_input(2)
    for operation_assignee, operation in operations.items():
        operator = operation[1]
        if operator == "XOR":
            if not follows_rule_1(operation_assignee, operation, values, operations):
                print(f"{operation_assignee} = {" ".join(operation)} broke rule 1")
                bad_assignees.add(operation_assignee)
        elif operator == "AND":
            if not follows_rule_2(operation_assignee, operation, operations):
                print(f"{operation_assignee} = {" ".join(operation)} broke rule 2")
                bad_assignees.add(operation_assignee)
        if not follows_rule_3(operation_assignee, operation):
            print(f"{operation_assignee} = {" ".join(operation)} broke rule 3")
            bad_assignees.add(operation_assignee)
        if not follows_rule_4(operation_assignee, operation, values):
            print(f"{operation_assignee} = {" ".join(operation)} broke rule 4")
            bad_assignees.add(operation_assignee)

    bad_assignees = sorted(list(bad_assignees))
    print(len(bad_assignees))
    return ",".join(bad_assignees)


if __name__ == "__main__":
    print(part2())
