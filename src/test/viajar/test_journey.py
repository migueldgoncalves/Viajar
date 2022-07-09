import unittest
import datetime

from viajar import journey


class JourneyTest(unittest.TestCase):

    def setUp(self):
        self.journey: journey.Journey = journey.Journey()

    def test_getters_journey(self):
        self.assertEqual(datetime.time(0, 0, 0), self.journey.get_elapsed_time())
        self.assertEqual(0, self.journey.get_elapsed_days())
        self.assertEqual(0, self.journey.get_traveled_distance())
        self.assertEqual('', self.journey.get_current_location())
        self.assertEqual('', self.journey.get_current_means_transport())
        self.assertEqual(0.0, self.journey.get_fuel_consumption())
        self.assertEqual(0.0, self.journey.get_consumed_fuel_price())

    def test_setters_journey(self):
        self.journey.set_elapsed_time(datetime.time(23, 59, 59))
        self.assertEqual(datetime.time(23, 59, 59), self.journey.get_elapsed_time())

        self.journey.set_elapsed_days(100)
        self.assertEqual(100, self.journey.get_elapsed_days())

        self.journey.reset_elapsed_time()
        self.assertEqual(datetime.time(0, 0, 0), self.journey.get_elapsed_time())
        self.assertEqual(0, self.journey.get_elapsed_days())

        self.journey.set_traveled_distance(15.0)
        self.assertEqual(15.0, self.journey.get_traveled_distance())
        self.journey.reset_traveled_distance()
        self.assertEqual(0.0, self.journey.get_traveled_distance())

        self.journey.set_current_location('Lisbon')
        self.assertEqual('Lisbon', self.journey.get_current_location())

        self.journey.set_current_means_transport('Car')
        self.assertEqual('Car', self.journey.get_current_means_transport())

        self.journey.increment_elapsed_time(0, 0, 1)
        self.assertEqual(datetime.time(0, 0, 1), self.journey.get_elapsed_time())
        self.journey.increment_elapsed_time(0, 0, 1)
        self.assertEqual(datetime.time(0, 0, 2), self.journey.get_elapsed_time())
        self.journey.increment_elapsed_time(0, 0, 57)
        self.assertEqual(datetime.time(0, 0, 59), self.journey.get_elapsed_time())
        self.journey.increment_elapsed_time(0, 0, 1)
        self.assertEqual(datetime.time(0, 1, 0), self.journey.get_elapsed_time())
        self.journey.increment_elapsed_time(0, 1, 0)
        self.assertEqual(datetime.time(0, 2, 0), self.journey.get_elapsed_time())
        self.journey.increment_elapsed_time(0, 0, 59)
        self.assertEqual(datetime.time(0, 2, 59), self.journey.get_elapsed_time())
        self.journey.increment_elapsed_time(0, 0, 2)
        self.assertEqual(datetime.time(0, 3, 1), self.journey.get_elapsed_time())
        self.journey.increment_elapsed_time(0, 56, 58)
        self.assertEqual(datetime.time(0, 59, 59), self.journey.get_elapsed_time())
        self.journey.increment_elapsed_time(0, 0, 1)
        self.assertEqual(datetime.time(1, 0, 0), self.journey.get_elapsed_time())
        self.journey.increment_elapsed_time(0, 0, 1)
        self.assertEqual(datetime.time(1, 0, 1), self.journey.get_elapsed_time())
        self.journey.increment_elapsed_time(0, 59, 59)
        self.assertEqual(datetime.time(2, 0, 0), self.journey.get_elapsed_time())
        self.journey.increment_elapsed_time(21, 59, 59)
        self.assertEqual(datetime.time(23, 59, 59), self.journey.get_elapsed_time())
        self.assertEqual(0, self.journey.get_elapsed_days())
        self.journey.increment_elapsed_time(0, 0, 1)
        self.assertEqual(datetime.time(0, 0, 0), self.journey.get_elapsed_time())
        self.assertEqual(1, self.journey.get_elapsed_days())
        self.journey.increment_elapsed_time(0, 1, 0)
        self.assertEqual(datetime.time(0, 1, 0), self.journey.get_elapsed_time())
        self.assertEqual(1, self.journey.get_elapsed_days())
        self.journey.increment_elapsed_time(1, 0, 0)
        self.assertEqual(datetime.time(1, 1, 0), self.journey.get_elapsed_time())
        self.assertEqual(1, self.journey.get_elapsed_days())
        self.journey.increment_elapsed_time(23, 59, 59)
        self.assertEqual(datetime.time(1, 0, 59), self.journey.get_elapsed_time())
        self.assertEqual(2, self.journey.get_elapsed_days())

        self.journey.increment_traveled_distance(10.0)
        self.journey.increment_traveled_distance(15.0)
        self.assertEqual(25.0, self.journey.get_traveled_distance())
