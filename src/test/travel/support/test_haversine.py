import unittest

from travel.support.haversine import get_cardinal_point, get_haversine_distance, MAX_ERROR_RATE
from travel.main.cardinal_points import NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH, SOUTHWEST, WEST, NORTHWEST
from travel.support.coordinates import Coordinates


class TestHaversine(unittest.TestCase):

    def test_get_cardinal_point_invalid_parameters(self):
        with self.assertRaises(AssertionError):
            get_cardinal_point(None, None)
        with self.assertRaises(AssertionError):
            get_cardinal_point(Coordinates(0.0, 0.0), None)
        with self.assertRaises(AssertionError):
            get_cardinal_point(None, Coordinates(0.0, 0.0))

    def test_get_cardinal_point_same_point(self):
        with self.assertRaises(AssertionError):
            get_cardinal_point(Coordinates(39.0, 0), Coordinates(39.0, 0))

    def test_get_cardinal_point_same_longitude(self):
        self.assertEqual(NORTH, get_cardinal_point(Coordinates(39.0, 0), Coordinates(39.5, 0)))
        self.assertEqual(SOUTH, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38.5, 0)))

    def test_get_cardinal_point_same_latitude(self):
        self.assertEqual(EAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(39.0, 1)))
        self.assertEqual(WEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(39.0, -1)))

    def test_get_cardinal_point_diagonals(self):
        self.assertEqual(NORTH, get_cardinal_point(Coordinates(39.0, 0), Coordinates(40.0, 0)))
        self.assertEqual(NORTH, get_cardinal_point(Coordinates(39.0, 0), Coordinates(40.0, 0.1)))
        self.assertEqual(NORTH, get_cardinal_point(Coordinates(39.0, 0), Coordinates(40.0, 0.2)))
        self.assertEqual(NORTH, get_cardinal_point(Coordinates(39.0, 0), Coordinates(40.0, 0.3)))
        self.assertEqual(NORTH, get_cardinal_point(Coordinates(39.0, 0), Coordinates(40.0, 0.4)))
        self.assertEqual(NORTHEAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(40.0, 0.5)))
        self.assertEqual(NORTHEAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(40.0, 0.6)))
        self.assertEqual(NORTHEAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(40.0, 0.7)))
        self.assertEqual(NORTHEAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(40.0, 0.8)))
        self.assertEqual(NORTHEAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(40.0, 0.9)))
        self.assertEqual(NORTHEAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(40.0, 1)))
        self.assertEqual(NORTHEAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(39.9, 1)))
        self.assertEqual(NORTHEAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(39.8, 1)))
        self.assertEqual(NORTHEAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(39.7, 1)))
        self.assertEqual(NORTHEAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(39.6, 1)))
        self.assertEqual(NORTHEAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(39.5, 1)))
        self.assertEqual(EAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(39.4, 1)))
        self.assertEqual(EAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(39.3, 1)))
        self.assertEqual(EAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(39.2, 1)))
        self.assertEqual(EAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(39.1, 1)))
        self.assertEqual(EAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(39, 1)))
        self.assertEqual(EAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38.9, 1)))
        self.assertEqual(EAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38.8, 1)))
        self.assertEqual(EAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38.7, 1)))
        self.assertEqual(EAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38.6, 1)))
        self.assertEqual(SOUTHEAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38.5, 1)))
        self.assertEqual(SOUTHEAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38.4, 1)))
        self.assertEqual(SOUTHEAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38.3, 1)))
        self.assertEqual(SOUTHEAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38.2, 1)))
        self.assertEqual(SOUTHEAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38.1, 1)))
        self.assertEqual(SOUTHEAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38, 1)))
        self.assertEqual(SOUTHEAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38, 0.9)))
        self.assertEqual(SOUTHEAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38, 0.8)))
        self.assertEqual(SOUTHEAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38, 0.7)))
        self.assertEqual(SOUTHEAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38, 0.6)))
        self.assertEqual(SOUTHEAST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38, 0.5)))
        self.assertEqual(SOUTH, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38, 0.4)))
        self.assertEqual(SOUTH, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38, 0.3)))
        self.assertEqual(SOUTH, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38, 0.2)))
        self.assertEqual(SOUTH, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38, 0.1)))
        self.assertEqual(SOUTH, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38, 0)))
        self.assertEqual(SOUTH, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38, -0.1)))
        self.assertEqual(SOUTH, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38, -0.2)))
        self.assertEqual(SOUTH, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38, -0.3)))
        self.assertEqual(SOUTH, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38, -0.4)))
        self.assertEqual(SOUTHWEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38, -0.5)))
        self.assertEqual(SOUTHWEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38, -0.6)))
        self.assertEqual(SOUTHWEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38, -0.7)))
        self.assertEqual(SOUTHWEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38, -0.8)))
        self.assertEqual(SOUTHWEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38, -0.9)))
        self.assertEqual(SOUTHWEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38, -1)))
        self.assertEqual(SOUTHWEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38.1, -1)))
        self.assertEqual(SOUTHWEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38.2, -1)))
        self.assertEqual(SOUTHWEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38.3, -1)))
        self.assertEqual(SOUTHWEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38.4, -1)))
        self.assertEqual(SOUTHWEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38.5, -1)))
        self.assertEqual(WEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38.6, -1)))
        self.assertEqual(WEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38.7, -1)))
        self.assertEqual(WEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38.8, -1)))
        self.assertEqual(WEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(38.9, -1)))
        self.assertEqual(WEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(39, -1)))
        self.assertEqual(WEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(39.1, -1)))
        self.assertEqual(WEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(39.2, -1)))
        self.assertEqual(WEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(39.3, -1)))
        self.assertEqual(WEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(39.4, -1)))
        self.assertEqual(NORTHWEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(39.5, -1)))
        self.assertEqual(NORTHWEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(39.6, -1)))
        self.assertEqual(NORTHWEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(39.7, -1)))
        self.assertEqual(NORTHWEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(39.8, -1)))
        self.assertEqual(NORTHWEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(39.9, -1)))
        self.assertEqual(NORTHWEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(40, -1)))
        self.assertEqual(NORTHWEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(40, -0.9)))
        self.assertEqual(NORTHWEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(40, -0.8)))
        self.assertEqual(NORTHWEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(40, -0.7)))
        self.assertEqual(NORTHWEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(40, -0.6)))
        self.assertEqual(NORTHWEST, get_cardinal_point(Coordinates(39.0, 0), Coordinates(40, -0.5)))
        self.assertEqual(NORTH, get_cardinal_point(Coordinates(39.0, 0), Coordinates(40, -0.4)))
        self.assertEqual(NORTH, get_cardinal_point(Coordinates(39.0, 0), Coordinates(40, -0.3)))
        self.assertEqual(NORTH, get_cardinal_point(Coordinates(39.0, 0), Coordinates(40, -0.2)))
        self.assertEqual(NORTH, get_cardinal_point(Coordinates(39.0, 0), Coordinates(40, -0.1)))

    def test_get_haversine_distance_invalid_parameters(self):
        with self.assertRaises(AssertionError):
            get_haversine_distance(None, None)
        with self.assertRaises(AssertionError):
            get_haversine_distance(Coordinates(0.0, 0.0), None)
        with self.assertRaises(AssertionError):
            get_haversine_distance(None, Coordinates(0.0, 0.0))

    def test_get_haversine_distance_same_point(self):
        self.assertEqual(0.0, get_haversine_distance(Coordinates(39.0, 0.0), Coordinates(39.0, 0.0)))

    def test_get_haversine_distance_successful(self):
        parameters_list = [
            [Coordinates(39.0, 0), Coordinates(40.0, 0), 111.2],
            [Coordinates(39.0, 0), Coordinates(40.0, 0.1), 111.5],
            [Coordinates(39.0, 0), Coordinates(40.0, 0.2), 112.5],
            [Coordinates(39.0, 0), Coordinates(40.0, 0.3), 114.1],
            [Coordinates(39.0, 0), Coordinates(40.0, 0.4), 116.4],
            [Coordinates(39.0, 0), Coordinates(40.0, 0.5), 119.2],
            [Coordinates(39.0, 0), Coordinates(40.0, 0.6), 122.5],
            [Coordinates(39.0, 0), Coordinates(40.0, 0.7), 126.4],
            [Coordinates(39.0, 0), Coordinates(40.0, 0.8), 130.7],
            [Coordinates(39.0, 0), Coordinates(40.0, 0.9), 135.4],
            [Coordinates(39.0, 0), Coordinates(40.0, 1), 140.5],
            [Coordinates(39.0, 0), Coordinates(39.9, 1), 131.9],
            [Coordinates(39.0, 0), Coordinates(39.8, 1), 123.7],
            [Coordinates(39.0, 0), Coordinates(39.7, 1), 116.0],
            [Coordinates(39.0, 0), Coordinates(39.6, 1), 108.9],
            [Coordinates(39.0, 0), Coordinates(39.5, 1), 102.5],
            [Coordinates(39.0, 0), Coordinates(39.4, 1), 97.0],
            [Coordinates(39.0, 0), Coordinates(39.3, 1), 92.5],
            [Coordinates(39.0, 0), Coordinates(39.2, 1), 89.1],
            [Coordinates(39.0, 0), Coordinates(39.1, 1), 87.0],
            [Coordinates(39.0, 0), Coordinates(39, 1), 86.4],
            [Coordinates(39.0, 0), Coordinates(38.9, 1), 87.2],
            [Coordinates(39.0, 0), Coordinates(38.8, 1), 89.3],
            [Coordinates(39.0, 0), Coordinates(38.7, 1), 92.8],
            [Coordinates(39.0, 0), Coordinates(38.6, 1), 97.4],
            [Coordinates(39.0, 0), Coordinates(38.5, 1), 103.0],
            [Coordinates(39.0, 0), Coordinates(38.4, 1), 109.4],
            [Coordinates(39.0, 0), Coordinates(38.3, 1), 116.6],
            [Coordinates(39.0, 0), Coordinates(38.2, 1), 124.4],
            [Coordinates(39.0, 0), Coordinates(38.1, 1), 132.6],
            [Coordinates(39.0, 0), Coordinates(38, 1), 141.2],
            [Coordinates(39.0, 0), Coordinates(38, 0.9), 136.0],
            [Coordinates(39.0, 0), Coordinates(38, 0.8), 131.2],
            [Coordinates(39.0, 0), Coordinates(38, 0.7), 126.8],
            [Coordinates(39.0, 0), Coordinates(38, 0.6), 122.9],
            [Coordinates(39.0, 0), Coordinates(38, 0.5), 119.4],
            [Coordinates(39.0, 0), Coordinates(38, 0.4), 116.5],
            [Coordinates(39.0, 0), Coordinates(38, 0.3), 114.2],
            [Coordinates(39.0, 0), Coordinates(38, 0.2), 112.5],
            [Coordinates(39.0, 0), Coordinates(38, 0.1), 111.5],
            [Coordinates(39.0, 0), Coordinates(38, 0), 111.2],
            [Coordinates(39.0, 0), Coordinates(38, -0.1), 111.5],
            [Coordinates(39.0, 0), Coordinates(38, -0.2), 112.5],
            [Coordinates(39.0, 0), Coordinates(38, -0.3), 114.2],
            [Coordinates(39.0, 0), Coordinates(38, -0.4), 116.5],
            [Coordinates(39.0, 0), Coordinates(38, -0.5), 119.4],
            [Coordinates(39.0, 0), Coordinates(38, -0.6), 122.8],
            [Coordinates(39.0, 0), Coordinates(38, -0.7), 126.8],
            [Coordinates(39.0, 0), Coordinates(38, -0.8), 131.2],
            [Coordinates(39.0, 0), Coordinates(38, -0.9), 136.0],
            [Coordinates(39.0, 0), Coordinates(38, -1), 141.2],
            [Coordinates(39.0, 0), Coordinates(38.1, -1), 132.6],
            [Coordinates(39.0, 0), Coordinates(38.2, -1), 124.4],
            [Coordinates(39.0, 0), Coordinates(38.3, -1), 116.6],
            [Coordinates(39.0, 0), Coordinates(38.4, -1), 109.5],
            [Coordinates(39.0, 0), Coordinates(38.5, -1), 103.0],
            [Coordinates(39.0, 0), Coordinates(38.6, -1), 97.4],
            [Coordinates(39.0, 0), Coordinates(38.7, -1), 92.8],
            [Coordinates(39.0, 0), Coordinates(38.8, -1), 89.3],
            [Coordinates(39.0, 0), Coordinates(38.9, -1), 87.2],
            [Coordinates(39.0, 0), Coordinates(39, -1), 86.4],
            [Coordinates(39.0, 0), Coordinates(39.1, -1), 87.1],
            [Coordinates(39.0, 0), Coordinates(39.2, -1), 89.1],
            [Coordinates(39.0, 0), Coordinates(39.3, -1), 92.5],
            [Coordinates(39.0, 0), Coordinates(39.4, -1), 97.0],
            [Coordinates(39.0, 0), Coordinates(39.5, -1), 102.5],
            [Coordinates(39.0, 0), Coordinates(39.6, -1), 108.9],
            [Coordinates(39.0, 0), Coordinates(39.7, -1), 116.0],
            [Coordinates(39.0, 0), Coordinates(39.8, -1), 123.7],
            [Coordinates(39.0, 0), Coordinates(39.9, -1), 131.9],
            [Coordinates(39.0, 0), Coordinates(40, -1), 140.4],
            [Coordinates(39.0, 0), Coordinates(40, -0.9), 135.4],
            [Coordinates(39.0, 0), Coordinates(40, -0.8), 130.7],
            [Coordinates(39.0, 0), Coordinates(40, -0.7), 126.4],
            [Coordinates(39.0, 0), Coordinates(40, -0.6), 122.5],
            [Coordinates(39.0, 0), Coordinates(40, -0.5), 119.2],
            [Coordinates(39.0, 0), Coordinates(40, -0.4), 116.4],
            [Coordinates(39.0, 0), Coordinates(40, -0.3), 114.1],
            [Coordinates(39.0, 0), Coordinates(40, -0.2), 112.5],
            [Coordinates(39.0, 0), Coordinates(40, -0.1), 111.5],
        ]

        for parameters in parameters_list:
            source = parameters[0]
            destination = parameters[1]
            distance = parameters[2]

            self.assertTrue(distance - distance * MAX_ERROR_RATE <= get_haversine_distance(source, destination) <= distance + distance * MAX_ERROR_RATE)
