# Solution to
# https://adventofcode.com/2024/day/16

from collections import deque
from heapq import heappop, heappush
import os

DIRECTIONS = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
height = 0
width = 0


class MapRow(list):
    def __str__(self):
        return "".join([str(char).rjust(5) for char in self])


class Map(list):
    def __str__(self):
        return "\n\n".join([str(row) for row in self])


def construct_map(input_filenumber: int) -> Map[list[str]]:
    global height
    global width

    script_path = os.path.dirname(os.path.realpath(__file__))
    input = open(os.path.join(script_path, f"input_{input_filenumber}.txt"))
    map = Map(MapRow(line.strip()) for line in input.readlines() if line)

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
    Modified Dijkstra's algorithm.

    Keeps the set of next locations to process as a heapq sorted list so we can cheaply get
    the item with the least score by popping it off the left hand side.

    Return the minimum number of steps to get from start to end.
    """
    next_step_locations = []
    visited = set()
    scores = {}

    # Starting score always 0
    # The start is always in the lower left corner (with # walls inbetween it and the sides of the map)
    # Starting direction always east (1)
    heappush(next_step_locations, (0, (height - 2, 1), (None, None), 1))
    previous_locations = {}

    while next_step_locations:
        score, location, dir = heappop(next_step_locations)
        y, x = location
        if location == (2, width - 1):
            # This is the ending square. No reason to move through it and check adjacent squares
            continue

        for newscore, newloc, newdir in get_adjacent_squares_costs_and_new_directions(
            score, location, dir
        ):

            newy, newx = newloc
            if map[newy][newx] == "#" or (newy, newx, dir) in visited:
                continue

            old_score = (
                scores[(newy, newx, newdir)] if (newy, newx, newdir) in scores else None
            )
            if old_score:
                if old_score == newscore:
                    previous_locations[(newy, newx, newdir)].add((y, x, dir))
                elif old_score > newscore:
                    scores[(newy, newx, newdir)] = newscore
                    previous_locations[(newy, newx, newdir)] = set([(y, x, dir)])
            else:
                scores[(newy, newx, newdir)] = newscore
                previous_locations[(newy, newx, newdir)] = set([(y, x, dir)])

            heappush(next_step_locations, (newscore, newloc, newdir))
        visited.add((y, x, dir))

    return previous_locations, scores


def follow_and_count_previous_locations(previous_locations, scores):
    q = deque()
    on_the_path = set([(1, width - 2)])

    score_moving_north = scores.get((1, width - 2, 0), None)
    score_moving_east = scores.get((1, width - 2, 1), None)

    if score_moving_north <= score_moving_east:
        q.append(previous_locations[(1, width - 2, 0)])
    if score_moving_east <= score_moving_north:
        q.append(previous_locations[(1, width - 2, 1)])

    while q:
        previous_loc_set = q.popleft()
        for prev_loc in previous_loc_set:
            on_the_path.add((prev_loc[0], prev_loc[1]))
            q.append(previous_locations.get(prev_loc, set()))
    on_the_path.add((height - 2, 1))
    return on_the_path


def part2():
    map = construct_map(3)
    previous_locations, scores = find_min_score_between_two_points(map)
    visited = follow_and_count_previous_locations(previous_locations, scores)
    print()
    print_map(map, visited)
    print(len(visited))
    print()


if __name__ == "__main__":
    part2()
