import unittest

from advent_day_11_part_1_2024 import compute_cost_of_garden


sample_data_part1 = [
    (
        """AAAA
BBCD
BBCC
EEEC""",
        140,
    ),
    (
        """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO""",
        772,
    ),
    (
        """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE""",
        1930,
    ),
]

sample_data_part2 = [
    (
        """AAAA
BBCD
BBCC
EEEC""",
        80,
    ),
    (
        """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE""",
        236,
    ),
    (
        """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA""",
        368,
    ),
    (
        """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE""",
        1206,
    ),
]


class TestComputeCostOfGargen(unittest.TestCase):
    def test_part1_with_sample_data(self):
        for garden, expected_cost in sample_data_part1:
            self.assertEqual(compute_cost_of_garden(garden), expected_cost)

    def test_part2_with_sample_data(self):
        for garden, expected_cost in sample_data_part2:
            self.assertEqual(compute_cost_of_garden(garden, style=2), expected_cost)
