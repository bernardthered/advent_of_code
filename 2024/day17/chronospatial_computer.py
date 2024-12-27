# Solution to
# https://adventofcode.com/2024/day/17

import os

register = {}
instruction_pointer = 0
INPUT_FILENUMBER = 2


def combo(operand):
    match operand:
        case 0 | 1 | 2 | 3:
            return operand
        case 4:
            return register["A"]
        case 5:
            return register["B"]
        case 6:
            return register["C"]
    raise Exception(f"Unexpected combo operand '{operand}'")


def adv(operand):
    """
    The adv instruction (opcode 0) performs division. The numerator is the value in the A register.
    The denominator is found by raising 2 to the power of the instruction's combo operand.
    (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.)
    The result of the division operation is truncated to an integer and then written to the A register.
    """
    register["A"] = int(register["A"] / 2 ** combo(operand))


def bdv(operand):
    register["B"] = int(register["A"] / 2 ** combo(operand))


def cdv(operand):
    register["C"] = int(register["A"] / 2 ** combo(operand))


def bxl(operand):
    """
    The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal
    operand, then stores the result in register B.
    """
    register["B"] ^= operand


def bst(operand):
    """
    The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its
    lowest 3 bits), then writes that value to the B register.
    """
    register["B"] = combo(operand) % 8


def jnz(operand):
    """
    The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero,
    it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps,
    the instruction pointer is not increased by 2 after this instruction.
    """
    global instruction_pointer
    if not register["A"]:
        return
    # The caller always increments the pointer by 2, so we'll set it to 2 less than we want
    instruction_pointer = operand - 2


def bxc(operand):
    """
    The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the
    result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
    """
    register["B"] ^= register["C"]


def out(operand):
    """
    The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that
    value. (If a program outputs multiple values, they are separated by commas.)
    """
    return combo(operand) % 8


OPERATION = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv,
}


def set_registers(a=None, b=None, c=None):
    if a:
        register["A"] = a
    if b:
        register["B"] = b
    if c:
        register["C"] = c


def get_register(register_letter: str):
    return register[register_letter.upper()]


def run_program(program_string: str):
    global instruction_pointer
    program_string = program_string.replace(",", "")
    instruction_pointer = 0
    outputs = []
    # instructions = program_string.split(",")

    while instruction_pointer < len(program_string):
        instruction = int(program_string[instruction_pointer])
        operand = int(program_string[instruction_pointer + 1])
        operation_method = OPERATION[instruction]
        print(f"Running {operation_method}({operand})")
        ret = operation_method(operand)
        if ret is not None:
            outputs.append(str(ret))
        instruction_pointer += 2
    return ",".join(outputs)


def parse_input():
    global register
    script_path = os.path.dirname(os.path.realpath(__file__))
    input = open(os.path.join(script_path, f"input_{INPUT_FILENUMBER}.txt"))
    register["A"] = int(input.readline().split(": ")[1])
    register["B"] = int(input.readline().split(": ")[1])
    register["C"] = int(input.readline().split(": ")[1])
    input.readline()
    return input.readline().split(": ")[1].strip()


def part1():
    program = parse_input()
    outputs = run_program(program)
    print(f"Registers = {register}")
    print()
    print(f"Outputs: {outputs}")


if __name__ == "__main__":
    part1()
