# Solution to
# https://adventofcode.com/2024/day/4

import os


DIRECTIONS = {0: "N", 1: "NE", 2: "E", 3: "SE", 4: "S", 5: "SW", 6: "W", 7: "NW"}
LOGLEVEL = 100
WORD_TO_FIND = "XMAS"

script_path = os.path.dirname(os.path.realpath(__file__))
grid_map = open(os.path.join(script_path, "input_1.txt")).read()

# grid_map = """
# MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX
# """


highest_row_num = 0
highest_col_num = 0


def log(msg, level=10):
    if level >= LOGLEVEL:
        print(msg)


class gridSquare(str):

    def __init__(self, _):
        # The 4 elements represent whether there is a known side above, right, below, left of this square
        self.sides = [False, False, False, False]


def convert_map_to_array(grid):
    global highest_row_num, highest_col_num

    grid_rows = []
    grid = grid.strip()
    for row_num, row in enumerate(grid.split("\n")):
        grid_rows.append([])
        for letter in row:
            grid_rows[row_num].append(gridSquare(letter))
    highest_row_num = row_num
    highest_col_num = len(grid_rows[0]) - 1
    return grid_rows


def adjacent_square(row_num, col_num, direction):
    # Return the squares up, right, down, and left
    # (starting at north and going clockwise)
    direction_letters = DIRECTIONS[direction]
    if "N" in direction_letters:
        row_num -= 1
    if "E" in direction_letters:
        col_num += 1
    if "S" in direction_letters:
        row_num += 1
    if "W" in direction_letters:
        col_num -= 1
    return row_num, col_num


def is_off_the_map(row_num, col_num):
    return (
        row_num < 0
        or col_num < 0
        or row_num > highest_row_num
        or col_num > highest_col_num
    )


def does_word_exist_starting_from_location_and_direction(
    grid_rows, row_num, col_num, direction, remaining_letters
) -> int:
    """
    Return True if so
    """
    if len(remaining_letters) == 0:
        return True
    # If it's off the map or the incorrect letter, give up
    if (
        is_off_the_map(row_num, col_num)
        or grid_rows[row_num][col_num] != remaining_letters[0]
    ):
        return False

    adjacent_row_num, adjacent_col_num = adjacent_square(row_num, col_num, direction)
    return does_word_exist_starting_from_location_and_direction(
        grid_rows, adjacent_row_num, adjacent_col_num, direction, remaining_letters[1:]
    )


def is_x_mas_centered_at_location(
    grid_rows,
    row_num,
    col_num,
) -> int:
    if grid_rows[row_num][col_num] != "A":
        return False
    nw_se_diagonal = [
        grid_rows[row_num + 1][col_num + 1],
        grid_rows[row_num - 1][col_num - 1],
    ]
    nw_se_diagonal.sort()
    if nw_se_diagonal != ["M", "S"]:
        return False

    sw_ne_diagonal = [
        grid_rows[row_num + 1][col_num - 1],
        grid_rows[row_num - 1][col_num + 1],
    ]
    sw_ne_diagonal.sort()
    if sw_ne_diagonal != ["M", "S"]:
        return False
    return True


def word_count_starting_from_location(
    grid_rows,
    row_num,
    col_num,
) -> int:
    """
    Return the # of occurrences (0-8) of WORD_TO_FIND that originate at col_num, row_num.
    """

    log(f"  Processing square at {row_num}, {col_num}")
    count = 0

    for direction in DIRECTIONS:
        if does_word_exist_starting_from_location_and_direction(
            grid_rows, row_num, col_num, direction, remaining_letters=WORD_TO_FIND
        ):
            log(
                f"Found {WORD_TO_FIND} going {DIRECTIONS[direction]} from {row_num}, {col_num}"
            )
            count += 1

    return count


def count_words(grid, style=1):
    global highest_row_num
    global highest_col_num
    count = 0

    grid_rows = convert_map_to_array(grid)
    for row_num in range(highest_row_num + 1):
        for col_num in range(highest_col_num + 1):
            count += word_count_starting_from_location(grid_rows, row_num, col_num)

    log(f"Total {WORD_TO_FIND} count: {count}", 100)
    return count


def count_x_mases(grid):

    global highest_row_num
    global highest_col_num
    count = 0

    grid_rows = convert_map_to_array(grid)
    for row_num in range(1, highest_row_num):
        for col_num in range(1, highest_col_num):
            count += (
                1 if is_x_mas_centered_at_location(grid_rows, row_num, col_num) else 0
            )

    log(f"Total X-MAS count: {count}", 100)
    return count


if __name__ == "__main__":
    count_words(grid_map)
    count_x_mases(grid_map)
