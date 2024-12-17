import unittest

from advent_day_11_part_1_2024 import compute_cost_of_garden


sample_data = [
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


class TestComputeCostOfGargen(unittest.TestCase):
    def test_with_sample_data(self):
        for garden, expected_cost in sample_data:
            print(f"Testing garden '{garden}' w/ expected cost of {expected_cost}!")
            self.assertEqual(compute_cost_of_garden(garden), expected_cost)
