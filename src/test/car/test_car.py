import unittest

from car.car import Car
from car import vehicle


class CarTest(unittest.TestCase):

    def setUp(self):
        self.car: Car = Car()

    def test_get_idle_to_redline_time_for_gear(self):
        self.assertEqual(0, self.car.get_idle_to_redline_time_for_gear(vehicle.REVERSE_GEAR - 1))
        self.assertEqual(2, self.car.get_idle_to_redline_time_for_gear(vehicle.REVERSE_GEAR))
        self.assertEqual(0, self.car.get_idle_to_redline_time_for_gear(vehicle.NEUTRAL_GEAR))
        self.assertEqual(2, self.car.get_idle_to_redline_time_for_gear(1))
        self.assertEqual(90, self.car.get_idle_to_redline_time_for_gear(8))
        self.assertEqual(0, self.car.get_idle_to_redline_time_for_gear(9))

    def test_get_redline_speed_for_gear(self):
        self.assertEqual(0, self.car.get_redline_speed_for_gear(vehicle.REVERSE_GEAR - 1))
        self.assertEqual(40, self.car.get_redline_speed_for_gear(vehicle.REVERSE_GEAR))
        self.assertEqual(0, self.car.get_redline_speed_for_gear(vehicle.NEUTRAL_GEAR))
        self.assertEqual(40, self.car.get_redline_speed_for_gear(1))
        self.assertEqual(320, self.car.get_redline_speed_for_gear(8))
        self.assertEqual(0, self.car.get_redline_speed_for_gear(9))
