# Solution to
# https://adventofcode.com/2024/day/7


from itertools import product
import os
import time


def input_lines_to_equations():
    equations = []
    script_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_path, "input_2.txt")) as inputfile:
        for line in inputfile.readlines():
            line = line.strip()
            if not line:
                continue
            answer, operands = line.split(": ")
            equations.append(
                {
                    "answer": int(answer),
                    "operands": [int(operand) for operand in operands.split(" ")],
                }
            )
    return equations


def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


def concatenate_digits(a, b):
    return int(f"{a}{b}")


def answer_if_true(equation):
    for operations in product(
        [add, multiply, concatenate_digits], repeat=len(equation["operands"]) - 1
    ):
        running_total = equation["operands"][0]
        for i, operation in enumerate(operations):
            running_total = operation(running_total, equation["operands"][i + 1])
        if running_total == equation["answer"]:
            return running_total
    return 0


def sum_of_true_equations(equations):
    sum = 0
    t1 = time.time()
    for i, equation in enumerate(equations):
        if i == 0 or (i + 1) % 50 == 0:
            print(f"{int(time.time()-t1)}s: Working on equation {i+1}/{len(equations)}")
        sum += answer_if_true(equation)
    return sum


if __name__ == "__main__":
    equations = input_lines_to_equations()

    print(sum_of_true_equations(equations))
