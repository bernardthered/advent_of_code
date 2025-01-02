# Solution to
# https://adventofcode.com/2024/day/11


from functools import cache
import os


@cache
def blink_one_stone_once(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    stonestr = str(stone)
    if len(stonestr) % 2 == 0:
        first = int(stonestr[: int(len(stonestr) / 2)])
        second = int(stonestr[int(len(stonestr) / 2) :])
        return [first, second]
    return [stone * 2024]


@cache
def recursive_blink(stone, depth=0, maxdepth=75) -> int:
    count = 0
    if depth == maxdepth:
        return 1
    new_stones = blink_one_stone_once(stone)
    for new_stone in new_stones:
        count = count + recursive_blink(new_stone, depth + 1, maxdepth)
    return count


def blink_multiple_stones(stones: list, iterations: int = 5) -> int:
    stone_count = 0
    for stone in stones:
        stone_count += recursive_blink(stone, 0, iterations)
    return stone_count


if __name__ == "__main__":
    script_path = os.path.dirname(os.path.realpath(__file__))
    input = open(os.path.join(script_path, "input_2.txt"))
    line = input.readline()
    stones = [int(stone) for stone in line.split()]
    print(blink_multiple_stones(stones, 75))
