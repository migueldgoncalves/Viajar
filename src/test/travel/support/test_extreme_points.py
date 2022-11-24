import unittest

from travel.support import ways
from travel.support import osm_interface
from travel.support.osm_interface import ExtremePoints
from travel.support.coordinate import Coordinate


class TestExtremePoints(unittest.TestCase):
    
    def setUp(self):
        self.north = Coordinate(1, 0)
        self.south = Coordinate(-1, 0)
        self.east = Coordinate(0, 1)
        self.west = Coordinate(0, -1)

        self.extreme_points = ExtremePoints('Portugal', osm_interface.COUNTRY, ways.PORTUGAL, self.north, self.south, self.east, self.west)

    def test_initializer_null_parameters(self):
        with self.assertRaises(AssertionError):
            ExtremePoints('', 0, '', None, None, None, None)
        with self.assertRaises(AssertionError):
            ExtremePoints('', osm_interface.COUNTRY, ways.PORTUGAL, self.north, self.south, self.east, self.west)
        with self.assertRaises(AssertionError):
            ExtremePoints('Portugal', 0, ways.PORTUGAL, self.north, self.south, self.east, self.west)
        with self.assertRaises(AssertionError):
            ExtremePoints('Portugal', osm_interface.COUNTRY, '', self.north, self.south, self.east, self.west)
        with self.assertRaises(AssertionError):
            ExtremePoints('Portugal', osm_interface.COUNTRY, ways.PORTUGAL, None, self.south, self.east, self.west)
        with self.assertRaises(AssertionError):
            ExtremePoints('Portugal', osm_interface.COUNTRY, ways.PORTUGAL, self.north, None, self.east, self.west)
        with self.assertRaises(AssertionError):
            ExtremePoints('Portugal', osm_interface.COUNTRY, ways.PORTUGAL, self.north, self.south, None, self.west)
        with self.assertRaises(AssertionError):
            ExtremePoints('Portugal', osm_interface.COUNTRY, ways.PORTUGAL, self.north, self.south, self.east, None)

    def test_initializer_invalid_parameters(self):
        with self.assertRaises(AssertionError):
            invalid_admin_level = 1  # Unused in this project, supra-national level
            ExtremePoints("Portugal", invalid_admin_level, osm_interface.COUNTRY, self.north, self.south, self.east, self.west)
        
        # Inequality tests - All coordinates must be different

        with self.assertRaises(AssertionError):
            ExtremePoints("Portugal", osm_interface.COUNTRY, ways.PORTUGAL, self.north, self.north, self.north, self.north)
        with self.assertRaises(AssertionError):
            ExtremePoints("Portugal", osm_interface.COUNTRY, ways.PORTUGAL, self.north, self.north, self.east, self.west)
        with self.assertRaises(AssertionError):
            ExtremePoints("Portugal", osm_interface.COUNTRY, ways.PORTUGAL, self.north, self.south, self.north, self.west)
        with self.assertRaises(AssertionError):
            ExtremePoints("Portugal", osm_interface.COUNTRY, ways.PORTUGAL, self.north, self.south, self.east, self.north)
        with self.assertRaises(AssertionError):
            ExtremePoints("Portugal", osm_interface.COUNTRY, ways.PORTUGAL, self.north, self.south, self.south, self.west)
        with self.assertRaises(AssertionError):
            ExtremePoints("Portugal", osm_interface.COUNTRY, ways.PORTUGAL, self.north, self.south, self.east, self.south)
        with self.assertRaises(AssertionError):
            ExtremePoints("Portugal", osm_interface.COUNTRY, ways.PORTUGAL, self.north, self.south, self.east, self.east)

    def test_initializer_successful(self):
        self.assertEqual('Portugal', self.extreme_points.name)
        self.assertEqual(osm_interface.COUNTRY, self.extreme_points.admin_level)
        self.assertEqual(ways.PORTUGAL, self.extreme_points.country)
        self.assertEqual(self.north, self.extreme_points.north)
        self.assertEqual(self.south, self.extreme_points.south)
        self.assertEqual(self.east, self.extreme_points.east)
        self.assertEqual(self.west, self.extreme_points.west)

    def test_str(self):
        self.assertEqual(
            f'Name: Portugal\n'
            f'Administrative level: 2\n'
            f'Country: PT\n'
            f'North: (1, 0)\n'
            f'South: (-1, 0)\n'
            f'East: (0, 1)\n'
            f'West: (0, -1)',
            str(self.extreme_points))

    def tearDown(self):
        self.north = None
        self.south = None
        self.east = None
        self.west = None
