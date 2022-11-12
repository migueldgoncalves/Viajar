import unittest

from combat.random import Random


class RandomTest(unittest.TestCase):

    def test_throw_dice_successful(self):
        number_tries: int = 10000
        for dice_number in range(1, 100 + 1, 10):
            minimum: int = 1
            maximum: int = dice_number * 6
            values: list[int] = [i for i in range(minimum, maximum + 1)]
            for i in range(number_tries):
                die: int = Random.throw_dice(dice_number)
                if (die < minimum) or (die > maximum):
                    self.fail("Incorrect value")
                if die in values:
                    values.remove(die)
            if len(values) > 0:
                self.fail("Missing values")

    def test_throw_dice_invalid_argument(self):
        self.assertEqual(0, Random.throw_dice(-1))
        self.assertEqual(0, Random.throw_dice(0))

    def test_get_random_percentage(self):
        number_tries: int = 100000
        minimum: int = 0
        maximum: int = 1
        values: list[float] = [i * 0.01 for i in range(minimum * 100, maximum * 100 + 1)]
        for i in range(number_tries):
            value: float = Random.get_random_percentage()
            if (value < minimum) or (value > maximum):
                self.fail("Incorrect value")
            if value in values:
                values.remove(value)
        if len(values) > 0:
            self.fail("Missing values")

    def test_get_random_int_successful(self):
        number_tries: int = 10000
        for i in range(1, 100 + 1, 10):
            minimum: int = 1
            maximum: int = i
            values: list[float] = [i for i in range(minimum, maximum + 1)]
            for _ in range(number_tries):
                value: float = Random.get_random_int(maximum)
                if (value < minimum) or (value > maximum):
                    self.fail("Incorrect value")
                if value in values:
                    values.remove(value)
            if len(values) > 0:
                self.fail("Missing values")

    def test_get_random_int_invalid_argument(self):
        self.assertEqual(0, Random.get_random_int(-1))
        self.assertEqual(0, Random.get_random_int(0))
