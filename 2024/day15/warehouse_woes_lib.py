import os


DIRECTIONS = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}


def print_map(map):
    for line in map:
        for char in line:
            print(char, end="")
        print()


def calculate_gps_sum(map):
    total = 0
    for y, line in enumerate(map):
        for x, char in enumerate(line):
            if char == "O":
                total += (y * 100) + x
    return total


def read_input(filenum):
    map = []
    script_path = os.path.dirname(os.path.realpath(__file__))
    reading_map = True
    moves = ""
    with open(os.path.join(script_path, f"input_{filenum}.txt")) as inputfile:
        for y, line in enumerate(inputfile.readlines()):
            line = line.strip()
            if line == "":
                reading_map = False
            if reading_map:
                map.append([])
                for x, char in enumerate(line):
                    if char == "@":
                        # char = "."
                        robot = (y, x)
                    map[y].append(char)
            else:
                moves += line
    return map, robot, moves
