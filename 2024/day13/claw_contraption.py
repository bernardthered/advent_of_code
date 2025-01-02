# Solution to
# https://adventofcode.com/2024/day/13

from sympy import symbols, Eq, solve
from functools import cache

import re
import os

A_COST = 3
B_COST = 1


def solve_equation(
    a_x_additive, a_y_additive, b_x_additive, b_y_additive, prize: tuple[int, int]
) -> int:
    """
    Return the # of tokens requried, or 0 if the equation doesn't solve to integer values.
    """
    # Define the variables
    a_presses, b_presses = symbols("a_presses b_presses")

    # Define the equations
    eq1 = Eq(
        a_presses * a_x_additive + b_presses * b_x_additive, prize[0] + 10000000000000
    )
    eq2 = Eq(
        a_presses * a_y_additive + b_presses * b_y_additive, prize[1] + 10000000000000
    )

    # Solve the system of equations
    solution = solve((eq1, eq2), (a_presses, b_presses))
    if not solution:
        return 0
    if solution[a_presses] != int(solution[a_presses]):
        return 0
    if solution[b_presses] != int(solution[b_presses]):
        return 0
    return solution[a_presses] * A_COST + solution[b_presses] * B_COST


def read_equation_from_file(file):
    button_a = file.readline()
    if not button_a:
        return None

    a_mo = re.match(r"Button .: X\+([0-9]+), Y\+([0-9]+)", button_a)
    if not a_mo:
        return None
    button_b = file.readline()
    b_mo = re.match(r"Button .: X\+([0-9]+), Y\+([0-9]+)", button_b)
    prize = file.readline()
    prize_mo = re.match(r"Prize: X=([0-9]+), Y=([0-9]+)", prize)
    _ = file.readline()  # blank line

    return (
        int(a_mo.groups()[0]),
        int(a_mo.groups()[1]),
        int(b_mo.groups()[0]),
        int(b_mo.groups()[1]),
        (int(prize_mo.groups()[0]), int(prize_mo.groups()[1])),
    )


def read_equations_from_file():
    equations = []
    script_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_path, "input_2.txt")) as inputfile:
        while True:
            equation = read_equation_from_file(inputfile)
            if not equation:
                break
            equations.append(equation)
    return equations


def count_tokens_for_equations(equations):
    tokens = 0
    for equation in equations:
        tokens += solve_equation(*equation)
    return tokens


if __name__ == "__main__":
    equations = read_equations_from_file()
    print(count_tokens_for_equations(equations))
