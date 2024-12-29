# Solution to
# https://adventofcode.com/2024/day/16

from heapq import heappop, heappush
import os

DIRECTIONS = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
height = 0
width = 0


class NoRouteExists(Exception):
    pass


def construct_map(input_filenumber: int) -> list[list[str]]:
    global height
    global width

    script_path = os.path.dirname(os.path.realpath(__file__))
    input = open(os.path.join(script_path, f"input_{input_filenumber}.txt"))
    map = [list(line.strip()) for line in input.readlines() if line]

    height = len(map)
    width = len(map[0])

    return map


def print_map(map, previously_visited=None):
    for y in range(height):
        for x in range(width):
            if previously_visited and (x, y) in previously_visited:
                print("O", end="")
            elif isinstance(map[x][y], int):
                print(".", end="")
            else:
                print(map[x][y], end="")
        print()


def get_adjacent_squares_costs_and_new_directions(
    score: int, location: tuple[int, int], dir: int
) -> list[tuple[int, tuple[int, int], int]]:
    """
    Return a set of 3 adjacent squares. Each is a tuple with the new (score, location, direction).
    """
    adjacent_squares = []

    # straight:
    newloc = location[0] + DIRECTIONS[dir][0], location[1] + DIRECTIONS[dir][1]
    adjacent_squares.append((score + 1, newloc, dir))

    # turn and move right:
    newdir = (dir + 1) % 4
    newloc = location[0] + DIRECTIONS[newdir][0], location[1] + DIRECTIONS[newdir][1]
    adjacent_squares.append((score + 1001, newloc, newdir))

    # turn and move left:
    newdir = (dir - 1) % 4
    newloc = location[0] + DIRECTIONS[newdir][0], location[1] + DIRECTIONS[newdir][1]
    adjacent_squares.append((score + 1001, newloc, newdir))

    return adjacent_squares


def find_min_score_between_two_points(map) -> int:
    """
    Modified Dijkstra's algorithm. It does not keep track of the path taken, as that
    isn't needed for this problem (just the score to get to the end node).

    Keeps the set of next locations to process as a heapq sorted list so we can cheaply get
    the item with the least score by popping it off the left hand side.

    Return the minimum number of steps to get from start to end.
    """
    next_step_locations = []

    # Starting score always 0
    # The start is always in the lower left corner (with # walls inbetween it and the sides of the map)
    # Starting direction always east (1)
    heappush(next_step_locations, (0, (height - 2, 1), 1))
    previous_locations = {}

    while True:
        if not next_step_locations:
            break
            # raise NoRouteExists(f"Couldn't find a path")
        bad = False
        score, location, dir = heappop(next_step_locations)
        if score < 0:
            bad = True
            # two chances
        score = abs(int(score))

        map[location[0]][location[1]] = score
        # if location == (9, 3):
        #     print(score)

        # print(f"{score}, {location}, {dir}")
        # visited.add((location[0], location[1], dir))

        # The end point is always in the upper right corner
        # if location == (1, width - 2):
        #     return score
        for newscore, newloc, newdir in get_adjacent_squares_costs_and_new_directions(
            score, location, dir
        ):
            y, x = newloc
            if map[y][x] == "#":
                continue

            oldscore = map[y][x]

            if isinstance(oldscore, int) and oldscore == newscore:
                print(f"Tie at {y},{x} ({newscore})!")
            if isinstance(oldscore, int) and oldscore < newscore:
                if bad == True:
                    continue
                else:
                    newscore = -newscore

            heappush(next_step_locations, (newscore, newloc, newdir))
            if (y, x) not in previous_locations:
                previous_locations[(y, x)] = set()
                previous_locations[(y, x)].add((location[0], location[1]))
            else:
                if (y, x) not in previous_locations:
                    print(f"previous_locations ({y}, {x}) was previously populated!")
                    print(previous_locations[(y, x)])
                    print(f"Adding {location[0]}, {location[1]}")

                previous_locations[(y, x)].add((location[0], location[1]))
            # if newloc == (8, 3):
            #     visited = follow_and_count_previous_locations(
            #         previous_locations, newloc
            #     )
            #     print_map(map, visited)
            #     print(newscore)
    return previous_locations


def follow_and_count_previous_locations(
    previous_locations, location=None, visited=None
):
    """
    DFS that
    """
    if visited is None:
        visited = set()
    if location is None:
        # start at the end
        location = (1, width - 2)

    visited.add(location)

    if location == (height - 2, 1):
        return visited

    # if len(previous_locations[location]) > 1:
    #     print(f"previous_locations for {location} is {previous_locations[location]}")

    for previous_location in previous_locations[location]:
        if previous_location not in visited:
            follow_and_count_previous_locations(
                previous_locations, previous_location, visited
            )
    return visited


def part2():
    map = construct_map(2)

    previous_locations = find_min_score_between_two_points(map)
    print(f"Score at the end: {map[1][width - 2]}")
    visited = follow_and_count_previous_locations(previous_locations)
    print_map(map, visited)
    print(len(visited))


if __name__ == "__main__":
    part2()
