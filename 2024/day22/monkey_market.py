# Solution to https://adventofcode.com/2024/day/22

import collections
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


def cache_sequences_of_changes(secret, depth=2000):
    cache = collections.OrderedDict()
    last_four_changes = collections.deque()
    previous_price = secret % 10
    for i in range(depth - 1):
        next_secret = calculate_next_secret(secret)
        price = next_secret % 10
        change = price - previous_price
        last_four_changes.append(change)
        if len(last_four_changes) > 4:
            last_four_changes.popleft()
        if len(last_four_changes) == 4:
            if tuple(last_four_changes) not in cache:
                # only the first occurence of each sequence counts
                cache[tuple(last_four_changes)] = price
        secret = next_secret
        previous_price = price
    return cache


def part1(initial_secrets):
    answer = 0
    for initial_secret in initial_secrets:
        initial_secret = int(initial_secret)
        nth_secret = calculate_nth_secret(initial_secret)
        print(f"{initial_secret}: {nth_secret}")
        answer += nth_secret
    print(f"Answer: {answer}")
    return answer


def calculate_sum_of_prices_for_sequence(list_of_changes, caches):
    sum = 0
    for cache in caches:
        sum += cache.get(list_of_changes, 0)
    return sum


def find_optimal_sequence(caches):
    best_price = 0
    best_sequence = None
    already_seen = set()

    for cache in caches:
        for list_of_changes in cache:
            if list_of_changes in already_seen:
                continue
            already_seen.add(list_of_changes)

            total_price_for_sequence = calculate_sum_of_prices_for_sequence(
                list_of_changes, caches
            )
            if total_price_for_sequence > best_price:
                best_price = total_price_for_sequence
                best_sequence = list_of_changes
    print(f"best_sequence: {best_sequence}, best_price: {best_price}")
    return best_price


def part2(initial_secrets):
    caches = []
    for initial_secret in initial_secrets:
        caches.append(cache_sequences_of_changes(int(initial_secret), 2000))
    print(f"{len(caches)} caches complete")
    answer = find_optimal_sequence(caches)
    print(answer)


if __name__ == "__main__":
    initial_secrets = parse_input()
    part2(initial_secrets)
