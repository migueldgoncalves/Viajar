import unittest

from travel.support import ways
from travel.support.ways import Way


class TestWay(unittest.TestCase):

    def setUp(self):
        self.way = Way("A1", "Autoestrada do Norte", ways.PORTUGAL, ways.ROAD)

    def test_initializer_invalid_arguments(self):
        with self.assertRaises(AssertionError):
            Way('', '', '', '')
        with self.assertRaises(AssertionError):
            Way('', "Autoestrada do Norte", ways.PORTUGAL, ways.ROAD)
        with self.assertRaises(AssertionError):
            Way('A1', '', ways.PORTUGAL, ways.ROAD)
        with self.assertRaises(AssertionError):
            Way('A1', "Autoestrada do Norte", '', ways.ROAD)
        with self.assertRaises(AssertionError):
            Way('A1', "Autoestrada do Norte", 'Invalid country', ways.ROAD)
        with self.assertRaises(AssertionError):
            Way('A1', "Autoestrada do Norte", ways.PORTUGAL, '')
        with self.assertRaises(AssertionError):
            Way('A1', "Autoestrada do Norte", ways.PORTUGAL, 'Invalid way type')

    def test_initializer_successful(self):
        self.assertEqual("A1", self.way.display_name)
        self.assertEqual("Autoestrada do Norte", self.way.osm_name)
        self.assertEqual(ways.PORTUGAL, self.way.country)
        self.assertEqual(ways.ROAD, self.way.way_type)

    def tearDown(self):
        self.way = None
