# Solution to
# https://adventofcode.com/2024/day/15 part 2


from collections import deque
from warehouse_woes_lib import print_map, read_input, calculate_gps_sum, DIRECTIONS


def build_block_of_barrels(map, spots_to_check, direction) -> list[tuple[int, int]]:
    """
    Return a list of all coordinates that will move in 'direction'.

    If there are any blockers, return an empty list.
    """
    spots_to_move = []

    spots_to_check = deque(spots_to_check)
    while spots_to_check:
        spot_to_check = spots_to_check.popleft()
        spot = map[spot_to_check[0]][spot_to_check[1]]

        if spot in "[]@":
            spots_to_move.append((spot_to_check[0], spot_to_check[1]))
            if direction in "^v" and spot in "[]":
                # Add the other half of the barrel to the spots to check
                if spot == "[":
                    other_half = (spot_to_check[0], spot_to_check[1] + 1)
                elif spot == "]":
                    other_half = (spot_to_check[0], spot_to_check[1] - 1)
                if other_half not in spots_to_check and other_half not in spots_to_move:
                    spots_to_check.append(other_half)
            next_spot = (
                spot_to_check[0] + DIRECTIONS[direction][0],
                spot_to_check[1] + DIRECTIONS[direction][1],
            )
            if next_spot not in spots_to_check and next_spot not in spots_to_move:
                spots_to_check.append(next_spot)
        if spot == ".":
            pass
        if spot == "#":
            return []
    return spots_to_move


def move_spots(map, spots_to_move, direction):
    for coordinates in reversed(spots_to_move):
        char = map[coordinates[0]][coordinates[1]]
        map[coordinates[0] + DIRECTIONS[direction][0]][
            coordinates[1] + DIRECTIONS[direction][1]
        ] = char
        map[coordinates[0]][coordinates[1]] = "."
    return map


def process_move(move, map, robot):
    all_spots_to_move = build_block_of_barrels(map, [robot], move)
    if all_spots_to_move:
        map = move_spots(map, all_spots_to_move, move)
        robot = (robot[0] + DIRECTIONS[move][0], robot[1] + DIRECTIONS[move][1])
    return robot


def expand_map(map):
    expanded_map = []
    current_row = 0
    for i in range(len(map)):
        expanded_map.append([])
        for j in range(len(map[0])):
            if map[i][j] in ["#", "."]:
                expanded_map[current_row] += [map[i][j]] * 2
            if map[i][j] == "O":
                expanded_map[current_row] += ["[", "]"]
            if map[i][j] == "@":
                expanded_map[current_row] += ["@", "."]
        current_row += 1
    return expanded_map


def part2():
    map, robot, moves = read_input(2)
    map = expand_map(map)
    robot = (robot[0], robot[1] * 2)
    for move in moves:
        robot = process_move(move, map, robot)
    print(calculate_gps_sum(map))


if __name__ == "__main__":
    part2()
