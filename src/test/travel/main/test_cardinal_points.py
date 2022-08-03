import unittest

from travel.main.cardinal_points import NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH, SOUTHWEST, WEST, NORTHWEST, get_opposite_cardinal_point


class CardinalPointsTest(unittest.TestCase):

    def test_obter_ponto_cardeal_oposto(self):
        self.assertEqual(SOUTH, get_opposite_cardinal_point(NORTH))
        self.assertEqual(SOUTHWEST, get_opposite_cardinal_point(NORTHEAST))
        self.assertEqual(WEST, get_opposite_cardinal_point(EAST))
        self.assertEqual(NORTHWEST, get_opposite_cardinal_point(SOUTHEAST))
        self.assertEqual(NORTH, get_opposite_cardinal_point(SOUTH))
        self.assertEqual(NORTHEAST, get_opposite_cardinal_point(SOUTHWEST))
        self.assertEqual(EAST, get_opposite_cardinal_point(WEST))
        self.assertEqual(SOUTHEAST, get_opposite_cardinal_point(NORTHWEST))
        self.assertEqual('', get_opposite_cardinal_point('Invalid'))
        self.assertEqual('', get_opposite_cardinal_point(''))
