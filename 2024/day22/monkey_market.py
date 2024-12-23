# Solution to https://adventofcode.com/2024/day/22

import os

INPUT_FILE_NUMBER = 2


def parse_input():
    script_path = os.path.dirname(os.path.realpath(__file__))
    input_file = open(os.path.join(script_path, f"input_{INPUT_FILE_NUMBER}.txt"))
    initial_secrets = input_file.readlines()
    return initial_secrets


def mix(number1, number2):
    return number1 ^ number2


def prune(number):
    return number % 16777216


def calculate_next_secret(secret):
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, int(secret / 32)))
    secret = prune(mix(secret, secret * 2048))
    return secret


def calculate_nth_secret(secret, depth=2000):
    for i in range(depth):
        secret = calculate_next_secret(secret)
    return secret


def part1(initial_secrets):
    answer = 0
    for initial_secret in initial_secrets:
        initial_secret = int(initial_secret)
        nth_secret = calculate_nth_secret(initial_secret)
        print(f"{initial_secret}: {nth_secret}")
        answer += nth_secret
    print(f"Answer: {answer}")
    return answer


def part2(initial_secrets):
    answer = 0
    print(answer)


if __name__ == "__main__":
    initial_secrets = parse_input()
    part1(initial_secrets)
    # part1(
    #     [
    #         123,
    #     ]
    # )
