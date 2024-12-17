# Solution to
# https://adventofcode.com/2024/day/12

import curses
import time


DIRECTIONS = {0: "up", 1: "right", 2: "down", 3: "left"}
LOGLEVEL = 15

# garden_map = open("day_11_input.txt").read()
garden_map = """AAAA
BBCD
BBCC
EEEC"""
highest_row_num = 0
highest_col_num = 0
message_row = 0
screen = None
letter_colors = {}


def log(msg, level=10):
    global message_row, screen
    if level >= LOGLEVEL:
        if screen:
            screen.addstr(message_row, 0, msg)
            message_row += 1
            screen.refresh()
        else:
            print(msg)


class GardenSquare(str):

    def __init__(self, _):
        # The 4 elements represent whether there is a known side above, right, below, left of this square
        self.sides = [False, False, False, False]


def convert_map_to_array(garden):
    global highest_row_num, highest_col_num, message_row

    garden_rows = []
    garden = garden.strip()
    for row_num, row in enumerate(garden.split("\n")):
        garden_rows.append([])
        for letter in row:
            garden_rows[row_num].append(GardenSquare(letter))
    highest_row_num = row_num
    highest_col_num = len(garden_rows[0]) - 1
    message_row = highest_row_num + 6
    return garden_rows


def get_adjacent_squares(row_num, col_num):
    # Return the squares up, right, down, and left
    # (starting at north and going clockwise)
    return [
        (row_num - 1, col_num),
        (row_num, col_num + 1),
        (row_num + 1, col_num),
        (row_num, col_num - 1),
    ]


def is_off_the_map(square):
    row_num, col_num = square
    return (
        row_num < 0
        or col_num < 0
        or row_num > highest_row_num
        or col_num > highest_col_num
    )


def is_new_side(garden_rows, adjacent_squares, direction, this_veggie):
    orthogonal_direction = (direction - 1) % 4
    orthogonal_square = adjacent_squares[orthogonal_direction]

    if not (is_off_the_map(orthogonal_square)):
        orthogonal_veggie = garden_rows[orthogonal_square[0]][orthogonal_square[1]]
        if orthogonal_veggie == this_veggie and orthogonal_veggie.sides[direction]:
            return False

    orthogonal_direction = (direction + 1) % 4
    orthogonal_square = adjacent_squares[orthogonal_direction]
    if not (is_off_the_map(orthogonal_square)):
        orthogonal_veggie = garden_rows[orthogonal_square[0]][orthogonal_square[1]]
        if orthogonal_veggie == this_veggie and orthogonal_veggie.sides[direction]:
            return False
    return True


def addstr(*args, **kwargs):
    if screen:
        screen.addstr(*args, **kwargs)
        screen.refresh()


def addch(*args, **kwargs):
    if screen:
        if len(args) > 3:
            screen.addch(*args[:3], curses.color_pair(args[3]), **kwargs)
        else:
            screen.addch(*args, **kwargs)
        screen.refresh()


def map_region(
    garden_rows, visited, row_num, col_num, area=0, perimeter=0, sides=0
) -> tuple[int, int]:
    """
    Return the area and perimeter of this region.

    Add each consitutent location in the garden to the visited set.
    """
    log(f"  Processing square at {col_num}, {row_num}")
    area += 1  # This square
    this_veggie = garden_rows[row_num][col_num]
    # perimeter = 0
    # sides = 0
    visited.add((row_num, col_num))

    color_pair = letter_colors.get(this_veggie.upper(), 0)
    addch(row_num, col_num, this_veggie, color_pair)
    addstr(highest_row_num + 2, 0, f"Area: {area}            ")
    if screen:
        time.sleep(0.5)

    adjacent_squares = get_adjacent_squares(row_num, col_num)

    for direction in DIRECTIONS:
        adjacent_square = adjacent_squares[direction]
        adjacent_row_num, adjacent_col_num = adjacent_square
        # if it's off the map or a different veggie, add one to the perimeter and continue
        if (
            is_off_the_map(adjacent_square)
            or (adjacent_veggie := garden_rows[adjacent_row_num][adjacent_col_num])
            != this_veggie
        ):
            perimeter += 1
            this_veggie.sides[direction] = True
            addstr(highest_row_num + 3, 0, f"Perimeter: {perimeter}                ")
            # check if this is a new side that we are starting
            if is_new_side(garden_rows, adjacent_squares, direction, this_veggie):
                sides += 1
                addstr(highest_row_num + 4, 0, f"Sides: {sides}                   ")
            continue
        log(
            f"    Looking at adjacent square of {adjacent_veggie} ({adjacent_col_num}, {adjacent_row_num})"
        )
        # If it's already been visited, continue w/o adding to perimeter or area
        if (adjacent_row_num, adjacent_col_num) in visited:
            continue

        # It's the same veggie! Recurse, adding the adjacent square's area & perimeter to our own
        area, perimeter, sides = map_region(
            garden_rows,
            visited,
            adjacent_row_num,
            adjacent_col_num,
            area,
            perimeter,
            sides,
        )
    return area, perimeter, sides


def compute_cost_of_garden(garden, style=1):
    """
    If parameter 'part' is 1, the cost of each region will be area x perimeter.
    If parameter 'part' is 2, the cost of each region will be area x # of sides.
    """

    global highest_row_num
    global highest_col_num
    visited = set()

    garden_rows = convert_map_to_array(garden)
    draw_garden(garden_rows)
    total_area = 0
    total_cost = 0
    for row_num in range(highest_row_num + 1):
        for col_num in range(highest_col_num + 1):
            if (row_num, col_num) in visited:
                continue

            veggie = garden_rows[row_num][col_num]
            log(f"Processing region of {veggie} starting at {col_num}, {row_num}")
            area, perimeter, sides = map_region(garden_rows, visited, row_num, col_num)
            if style == 1:
                cost = area * perimeter
            else:
                cost = area * sides
            log(
                f"Found a region of {veggie} of area {area}, perimeter {perimeter}, and {sides} sides, making its fencing cost ${cost}.",
                20,
            )
            total_area += area
            total_cost += cost

    garden = garden.replace("\n", "")
    if total_area != len(garden):
        log(
            f"WARNING: the total area ({total_area}) does not equal the size of the garden map ({len(garden)}) ",
            30,
        )
    log(f"Total cost: {total_cost}", 20)
    return total_cost


def draw_garden(array):
    """Draws the initial 2D array on the screen with colors."""
    for row_idx, row in enumerate(array):
        for col_idx, char in enumerate(row):
            addch(row_idx, col_idx, char)


def main(stdscr):
    global screen, letter_colors
    screen = stdscr

    # Hide the cursor
    curses.curs_set(0)

    # Initialize color pairs
    curses.start_color()
    curses.use_default_colors()

    for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        curses.init_pair(
            i + 1,
            min(i * 10, 255),
            -1,
        )
        letter_colors[letter] = i + 1

    compute_cost_of_garden(garden_map, 2)

    # Wait for user input
    log("(Press any key to continue)", 30)
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
