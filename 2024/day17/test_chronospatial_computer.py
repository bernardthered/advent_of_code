import unittest

from chronospatial_computer import set_registers, run_program, get_register


class TestChronospatialComputer(unittest.TestCase):
    """
    Tests are named for the examples in the instructions (https://adventofcode.com/2024/day/17):
        If register C contains 9, the program 2,6 would set register B to 1.
        If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
        If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
        If register B contains 29, the program 1,7 would set register B to 26.
        If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.

    """

    def test_bullet_1(self):
        set_registers(c=9)
        run_program("2,6")
        self.assertEqual(get_register("b"), 1)

    def test_bullet_2(self):
        set_registers(a=10)
        outputs = run_program("5,0,5,1,5,4")
        self.assertEqual(outputs, "0,1,2")

    def test_bullet_3(self):
        set_registers(a=2024)
        outputs = run_program("0,1,5,4,3,0")
        self.assertEqual(outputs, "4,2,5,6,7,7,7,7,3,1,0")
        self.assertEqual(get_register("a"), 0)

    def test_bullet_4(self):
        set_registers(b=29)
        run_program("1,7")
        self.assertEqual(get_register("b"), 26)

    def test_bullet_5(self):
        set_registers(b=2024)
        set_registers(c=43690)
        run_program("4,0")
        self.assertEqual(get_register("b"), 44354)
