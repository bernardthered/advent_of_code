# Solution to
# https://adventofcode.com/2024/day/11


from functools import cache
import os
import time


@cache
def blink_one_stone(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    stonestr = str(stone)
    if len(stonestr) % 2 == 0:
        first = int(stonestr[: int(len(stonestr) / 2)])
        second = int(stonestr[int(len(stonestr) / 2) :])
        return [first, second]
    return [stone * 2024]


def blink(stones: list, iterations: int = 5) -> list[int]:
    t1 = time.time()
    for i in range(iterations):
        if i == 1 or i % 5 == 0:
            print(
                f"{int(time.time() - t1)}s: {i}/{iterations} blinks, {len(stones)} stones."
            )
        new_stones = []
        for stone in stones:
            new_stones += blink_one_stone(stone)
        # print(new_stones)
        stones = new_stones
    return new_stones


if __name__ == "__main__":
    script_path = os.path.dirname(os.path.realpath(__file__))
    input = open(os.path.join(script_path, "input_2.txt"))
    line = input.readline()
    stones = [int(stone) for stone in line.split()]
    print(len(blink(stones, 25)))
