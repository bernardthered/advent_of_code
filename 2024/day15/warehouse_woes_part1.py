# Solution to
# https://adventofcode.com/2024/day/15 part 1


from warehouse_woes_lib import print_map, read_input, calculate_gps_sum, DIRECTIONS


def process_move(move, map, robot):
    next = (robot[0] + DIRECTIONS[move][0], robot[1] + DIRECTIONS[move][1])

    if map[next[0]][next[1]] == ".":
        map[robot[0]][robot[1]] = "."
        robot = next
        map[robot[0]][robot[1]] = "@"
        return robot
    elif map[next[0]][next[1]] == "#":
        return robot
    elif map[next[0]][next[1]] == "O":
        barrel_line_spot = (next[0], next[1])
        while map[barrel_line_spot[0]][barrel_line_spot[1]] == "O":
            barrel_line_spot = (
                barrel_line_spot[0] + DIRECTIONS[move][0],
                barrel_line_spot[1] + DIRECTIONS[move][1],
            )
        if map[barrel_line_spot[0]][barrel_line_spot[1]] == "#":
            # Nothing moves!
            return robot
        elif map[barrel_line_spot[0]][barrel_line_spot[1]] == ".":
            # the first barrel moves to the empty spot
            map[barrel_line_spot[0]][barrel_line_spot[1]] = "O"
            # the robot moves to the spot it was originally trying to move to
            map[robot[0]][robot[1]] = "."
            robot = next
            map[robot[0]][robot[1]] = "@"
            return robot
        else:
            raise Exception(
                f"Shouldn't get here. map[{barrel_line_spot}] = {map[barrel_line_spot[0]][barrel_line_spot[1]]}"
            )


def part1():
    map, robot, moves = read_input(2)
    for move in moves:
        robot = process_move(move, map, robot)
    print_map(map)
    print(calculate_gps_sum(map))


if __name__ == "__main__":
    part1()
