import unittest

from travel.support.coordinates import Coordinates


class TestCoordinates(unittest.TestCase):

    def setUp(self):
        self.coordinates_a = Coordinates(-90, -180)
        self.coordinates_b = Coordinates(90, 180)
        self.coordinates_c = Coordinates(0, 0)

    def test_initializer_invalid_arguments(self):
        with self.assertRaises(AssertionError):
            Coordinates(-91, 181)
        with self.assertRaises(AssertionError):
            Coordinates(-91, 0)
        with self.assertRaises(AssertionError):
            Coordinates(91, 0)
        with self.assertRaises(AssertionError):
            Coordinates(0, -181)
        with self.assertRaises(AssertionError):
            Coordinates(0, 181)

    def test_initializer_successful(self):
        self.assertEqual(-90, self.coordinates_a.latitude)
        self.assertEqual(-180, self.coordinates_a.longitude)

        self.assertEqual(90, self.coordinates_b.latitude)
        self.assertEqual(180, self.coordinates_b.longitude)

        self.assertEqual(0, self.coordinates_c.latitude)
        self.assertEqual(0, self.coordinates_c.longitude)

    def test_get_coordinates(self):
        self.assertEqual((-90, -180), self.coordinates_a.get_coordinates())
        self.assertEqual((90, 180), self.coordinates_b.get_coordinates())
        self.assertEqual((0, 0), self.coordinates_c.get_coordinates())

    def test_get_latitude(self):
        self.assertEqual(-90, self.coordinates_a.get_latitude())
        self.assertEqual(90, self.coordinates_b.get_latitude())
        self.assertEqual(0, self.coordinates_c.get_latitude())

    def test_get_longitude(self):
        self.assertEqual(-180, self.coordinates_a.get_longitude())
        self.assertEqual(180, self.coordinates_b.get_longitude())
        self.assertEqual(0, self.coordinates_c.get_longitude())

    def test_set_latitude_invalid_arguments(self):
        with self.assertRaises(AssertionError):
            self.coordinates_a.set_latitude(-91)
        with self.assertRaises(AssertionError):
            self.coordinates_a.set_latitude(91)

    def test_set_latitude_successful(self):
        self.coordinates_a.set_latitude(-90)
        self.assertEqual(-90, self.coordinates_a.latitude)

        self.coordinates_a.set_latitude(0)
        self.assertEqual(0, self.coordinates_a.latitude)

        self.coordinates_a.set_latitude(90)
        self.assertEqual(90, self.coordinates_a.latitude)

    def test_set_longitude_invalid_arguments(self):
        with self.assertRaises(AssertionError):
            self.coordinates_a.set_longitude(-181)
        with self.assertRaises(AssertionError):
            self.coordinates_a.set_longitude(181)

    def test_set_longitude_successful(self):
        self.coordinates_a.set_longitude(-180)
        self.assertEqual(-180, self.coordinates_a.longitude)

        self.coordinates_a.set_longitude(0)
        self.assertEqual(0, self.coordinates_a.longitude)

        self.coordinates_a.set_longitude(180)
        self.assertEqual(180, self.coordinates_a.longitude)

    def test_str(self):
        self.assertEqual('(-90, -180)', str(self.coordinates_a))
        self.assertEqual('(90, 180)', str(self.coordinates_b))
        self.assertEqual('(0, 0)', str(self.coordinates_c))

    def test_eq(self):
        self.assertNotEqual(self.coordinates_a, self.coordinates_b)
        self.assertNotEqual(self.coordinates_b, self.coordinates_c)
        self.assertNotEqual(self.coordinates_a, self.coordinates_c)

        self.assertEqual(self.coordinates_a, self.coordinates_a)
        self.assertEqual(self.coordinates_b, self.coordinates_b)
        self.assertEqual(self.coordinates_c, self.coordinates_c)

        self.assertEqual(self.coordinates_a, Coordinates(-90, -180))
        self.assertEqual(self.coordinates_b, Coordinates(90, 180))
        self.assertEqual(self.coordinates_c, Coordinates(0, 0))

    def test_hash(self):
        self.assertEqual(-7303486224951061299, hash(self.coordinates_a))
        self.assertEqual(-3882216984606157969, hash(self.coordinates_b))
        self.assertEqual(-8458139203682520985, hash(self.coordinates_c))

    def tearDown(self):
        self.coordinates_a = None
        self.coordinates_b = None
        self.coordinates_c = None
