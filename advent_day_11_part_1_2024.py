import os
from typing import List

# script_path = os.path.dirname(os.path.realpath(__file__))
garden_map = open("day_11_input.txt").read()

highest_row_num = 0
highest_col_num = 0


def log(msg):
    if False:
        print(msg)


def convert_map_to_array(garden):
    global highest_row_num
    global highest_col_num

    garden_rows = []
    garden = garden.strip()
    for row_num, row in enumerate(garden.split("\n")):
        garden_rows.append([])
        for letter in row:
            garden_rows[row_num].append(letter)
    highest_row_num = row_num
    highest_col_num = len(garden_rows[0]) - 1
    if highest_col_num > 4:
        print("hmm")
    print(f"highest_col_num = {highest_col_num}, highest_row_num = {highest_row_num}")
    return garden_rows


def get_adjacent_squares(row_num, col_num):
    return [
        (row_num + 1, col_num),
        (row_num - 1, col_num),
        (row_num, col_num + 1),
        (row_num, col_num - 1),
    ]


def map_region(garden_rows, visited, row_num, col_num) -> tuple[int, int]:
    """
    Return the area and perimeter of this region.

    Add each consitutent location in the garden to the visited set.
    """
    log(f"  Processing square at {col_num}, {row_num}")
    area = 1  # This square
    this_veggie = garden_rows[row_num][col_num]
    perimeter = 0
    visited.add((row_num, col_num))

    for adjacent_row_num, adjacent_col_num in get_adjacent_squares(row_num, col_num):
        # if it's off the map, add one to the perimeter and continue
        if (
            adjacent_row_num < 0
            or adjacent_col_num < 0
            or adjacent_row_num > highest_row_num
            or adjacent_col_num > highest_col_num
        ):
            perimeter += 1
            continue

        adjacent_veggie = garden_rows[adjacent_row_num][adjacent_col_num]
        log(
            f"    Looking at adjacent square of {adjacent_veggie} ({adjacent_col_num}, {adjacent_row_num})"
        )
        # if it's a diff veggie, add one to the perimeter and continue
        if adjacent_veggie != this_veggie:
            perimeter += 1
            continue

        # If it's already been visited, continue w/o adding to perimeter or area
        if (adjacent_row_num, adjacent_col_num) in visited:
            continue

        # It's the same veggie! Recurse, adding the adjacent square's area & perimeter to our own
        adjacent_area, adjacent_perimeter = map_region(
            garden_rows, visited, adjacent_row_num, adjacent_col_num
        )
        area += adjacent_area
        perimeter += adjacent_perimeter

    return area, perimeter


def compute_cost_of_garden(garden):
    global highest_row_num
    global highest_col_num
    visited = set()

    garden_rows = convert_map_to_array(garden)
    total_area = 0
    total_cost = 0
    for row_num in range(highest_row_num + 1):
        for col_num in range(highest_col_num + 1):
            if (row_num, col_num) in visited:
                continue

            veggie = garden_rows[row_num][col_num]
            print(f"Processing region of {veggie} starting at {col_num}, {row_num}")
            area, perimeter = map_region(garden_rows, visited, row_num, col_num)
            print(
                f"Found a region of {veggie} of area {area} and perimeter {perimeter}, making its fencing cost {area * perimeter}."
            )
            total_area += area
            total_cost += area * perimeter

    garden = garden.replace("\n", "")
    if total_area != len(garden):
        print(
            f"WARNING: the total area ({total_area}) does not equal the size of the garden map ({len(garden)}) "
        )
    print(f"Total cost: ", total_cost)
    return total_cost


if __name__ == "__main__":
    compute_cost_of_garden(garden_map)
