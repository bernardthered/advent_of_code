# Solution to
# https://adventofcode.com/2024/day/15


from collections import deque
from warehouse_woes_lib import print_map, read_input, calculate_gps_sum, DIRECTIONS


def build_block_of_barrels(map, spots_to_check, direction) -> list[tuple]:
    spots_to_move = []
    # spots_to_check = [(starting_spot[0] + DIRECTIONS[direction][0], starting_spot[1] + DIRECTIONS[direction][1])]
    spots_to_check = deque(spots_to_check)
    while spots_to_check:
        spot_to_check = spots_to_check.pop()
        spot = map[spot_to_check[0]][spot_to_check[1]]
        if direction in (">", "<"):
            if spot in ("[", "]"):
                spots_to_move.append((spot_to_check[0], spot_to_check[1]))
                spots_to_check.append(
                    (
                        spot_to_check[0] + DIRECTIONS[direction][0],
                        spot_to_check[1] + DIRECTIONS[direction][1],
                    )
                )
            if spot == ".":
                spots_to_move.append((spot_to_check[0], spot_to_check[1]))
                return spots_to_move
            if spot == "#":
                return []
    return []


def move_spots(map, spots_to_move, direction):
    for coordinates in reversed(spots_to_move):
        char = map[coordinates[0]][coordinates[1]]
        map[coordinates[0] + DIRECTIONS[direction][0]][
            coordinates[1] + DIRECTIONS[direction][1]
        ] = char
    return map


def process_move(move, map, robot):
    next = (robot[0] + DIRECTIONS[move][0], robot[1] + DIRECTIONS[move][1])

    next_char = map[next[0]][next[1]]
    if next_char == ".":
        map[robot[0]][robot[1]] = "."
        robot = next
        map[robot[0]][robot[1]] = "@"
        return robot
    elif next_char == "#":
        return robot
    elif next_char in ("[", "]"):
        all_spots_to_move = build_block_of_barrels(map, [(next[0], next[1])], move)
        if all_spots_to_move:
            map = move_spots(map, all_spots_to_move, move)
            robot = next
            map[robot[0]][robot[1]] = "@"
        return robot
    else:
        raise Exception(f"Shouldn't get here. map[{next}] = {next_char}")


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
    map, robot, moves = read_input(1)
    map = expand_map(map)
    robot = (robot[0] * 2, robot[1])
    print(robot)
    for move in moves:
        robot = process_move(move, map, robot)
    print_map(map)
    # print(calculate_gps_sum(map))


if __name__ == "__main__":
    part2()
