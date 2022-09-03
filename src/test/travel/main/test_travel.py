import unittest
import unittest.mock
import datetime
import io
import sys

from travel.main import travel


def _redirect_output() -> io.StringIO:
    """
    Redirects stdout to be monitorable inside tests

    :return: Object to where stdout is now being redirected
    """
    stdout_redirect: io.StringIO = io.StringIO()
    sys.stdout = stdout_redirect
    return stdout_redirect


class TravelTest(unittest.TestCase):

    def setUp(self):
        self.initial_location: str = 'Guerreiros do Rio'
        with unittest.mock.patch('builtins.input', side_effect=["n"]):  # Provides option to car usage menu
            self.travel: travel.Travel = travel.Travel(self.initial_location)

    def test_constructor(self):
        self.assertEqual(self.initial_location, self.travel.initial_location)
        self.assertTrue(self.travel.db_initialized)
        self.assertEqual(0.0, self.travel.car.velocidade)
        self.assertEqual(self.initial_location, self.travel.current_journey.get_current_location())
        self.assertEqual(travel.DEFAULT_MEANS_TRANSPORT, self.travel.current_journey.get_current_means_transport())
        self.assertEqual(0.0, self.travel.current_journey.get_traveled_distance())
        self.assertFalse(self.travel.is_car_requested)

    def test_print_location_info(self):
        stdout_redirect: io.StringIO = _redirect_output()

        self.travel.print_location_info()
        self.assertTrue("Coordinates: 37.396353, -7.446837" in stdout_redirect.getvalue())

    def test_print_journey_statistics_zero_elapsed_days(self):
        stdout_redirect: io.StringIO = _redirect_output()

        self.travel.print_journey_statistics()
        self.assertTrue("\nYou have traveled 0.0 km" in stdout_redirect.getvalue())
        self.assertTrue("\nYou have been travelling for 00:00:00" in stdout_redirect.getvalue())
        self.assertTrue("\nYou have consumed 0.0 liters of fuel" in stdout_redirect.getvalue())
        self.assertTrue("\nYou have spent 0.0 euros in fuel" in stdout_redirect.getvalue())

    def test_print_journey_statistics_one_elapsed_day(self):
        stdout_redirect: io.StringIO = _redirect_output()

        self.travel.current_journey.set_elapsed_days(1)

        self.travel.print_journey_statistics()
        self.assertTrue("\nYou have traveled 0.0 km" in stdout_redirect.getvalue())
        self.assertTrue("\nYou have been travelling for 1 day and 00:00:00" in stdout_redirect.getvalue())
        self.assertTrue("\nYou have consumed 0.0 liters of fuel" in stdout_redirect.getvalue())
        self.assertTrue("\nYou have spent 0.0 euros in fuel" in stdout_redirect.getvalue())

    def test_print_journey_statistics_multiple_elapsed_days(self):
        stdout_redirect: io.StringIO = _redirect_output()

        self.travel.current_journey.set_elapsed_days(2)

        self.travel.print_journey_statistics()
        self.assertTrue("\nYou have traveled 0.0 km" in stdout_redirect.getvalue())
        self.assertTrue("\nYou have been travelling for 2 days and 00:00:00" in stdout_redirect.getvalue())
        self.assertTrue("\nYou have consumed 0.0 liters of fuel" in stdout_redirect.getvalue())
        self.assertTrue("\nYou have spent 0.0 euros in fuel" in stdout_redirect.getvalue())

    def test_change_means_transport(self):
        means_transport_to_string: dict[str, str] = {
            travel.CAR: travel.SWITCHED_TO_CAR_STRING,
            travel.BOAT: travel.SWITCHED_TO_BOAT_STRING,
            travel.TRAIN: travel.SWITCHED_TO_TRAIN_STRING,
            travel.PLANE: travel.SWITCHED_TO_PLANE_STRING,
            travel.HIGH_SPEED_TRAIN: travel.SWITCHED_TO_HIGH_SPEED_TRAIN_STRING,
            travel.TRANSFER: travel.SWITCHED_TO_TRANSFER_STRING
        }
        for means_of_transport in means_transport_to_string:
            stdout_redirect: io.StringIO = _redirect_output()  # Clears redirect object from previous prints

            self.travel.change_means_transport(means_of_transport)
            switched_string: str = means_transport_to_string[means_of_transport]
            self.assertTrue(switched_string in stdout_redirect.getvalue())

        stdout_redirect: io.StringIO = _redirect_output()  # Clears redirect object from previous prints

        self.travel.current_journey.set_current_location('Gare do Oriente')  # Location with "standard" train and high-speed train
        self.travel.change_means_transport(travel.TRAIN)
        self.assertTrue(travel.SWITCHED_TO_STANDARD_TRAIN_STRING in stdout_redirect.getvalue())

    def test_get_current_location_object(self):
        self.assertEqual(self.initial_location, self.travel.get_current_location_object().get_name())
        from travel.main.location_portugal import LocationPortugal
        self.assertEqual(type(LocationPortugal('', {}, 0.0, 0.0, 0, '', '', '', '', '')),
                         type(self.travel.get_current_location_object()))

    def test_seconds_to_datetime(self):
        with self.assertRaises(ValueError):
            travel.Travel.seconds_to_datetime(-1)
        self.assertEqual(datetime.time(0, 0, 0), travel.Travel.seconds_to_datetime(0))
        self.assertEqual(datetime.time(0, 0, 1), travel.Travel.seconds_to_datetime(1))
        self.assertEqual(datetime.time(0, 0, 59), travel.Travel.seconds_to_datetime(59))
        self.assertEqual(datetime.time(0, 1, 0), travel.Travel.seconds_to_datetime(60))
        self.assertEqual(datetime.time(0, 1, 1), travel.Travel.seconds_to_datetime(61))
        self.assertEqual(datetime.time(0, 1, 59), travel.Travel.seconds_to_datetime(119))
        self.assertEqual(datetime.time(0, 2, 0), travel.Travel.seconds_to_datetime(120))
        self.assertEqual(datetime.time(0, 2, 1), travel.Travel.seconds_to_datetime(121))
        self.assertEqual(datetime.time(0, 59, 59), travel.Travel.seconds_to_datetime(3600 - 1))
        self.assertEqual(datetime.time(1, 0, 0), travel.Travel.seconds_to_datetime(3600))
        self.assertEqual(datetime.time(1, 0, 1), travel.Travel.seconds_to_datetime(3600 + 1))
        self.assertEqual(datetime.time(1, 0, 59), travel.Travel.seconds_to_datetime(3600 + 59))
        self.assertEqual(datetime.time(1, 1, 0), travel.Travel.seconds_to_datetime(3600 + 60))
        self.assertEqual(datetime.time(1, 1, 1), travel.Travel.seconds_to_datetime(3600 + 61))
        self.assertEqual(datetime.time(23, 59, 59), travel.Travel.seconds_to_datetime(3600 * 24 - 1))
        with self.assertRaises(ValueError):
            travel.Travel.seconds_to_datetime(3600 * 24)

    def test_increment_traveled_time(self):
        with self.assertRaises(ValueError):
            self.travel.increment_traveled_time(-1)

        self.travel.increment_traveled_time(0)
        self.assertEqual(datetime.time(0, 0, 0), self.travel.current_journey.elapsed_time)
        self.assertEqual(0, self.travel.current_journey.elapsed_days)

        self.travel.increment_traveled_time(1)
        self.assertEqual(datetime.time(0, 0, 1), self.travel.current_journey.elapsed_time)
        self.assertEqual(0, self.travel.current_journey.elapsed_days)

        self.travel.increment_traveled_time(59)
        self.assertEqual(datetime.time(0, 1, 0), self.travel.current_journey.elapsed_time)
        self.assertEqual(0, self.travel.current_journey.elapsed_days)

        self.travel.increment_traveled_time(60)
        self.assertEqual(datetime.time(0, 2, 0), self.travel.current_journey.elapsed_time)
        self.assertEqual(0, self.travel.current_journey.elapsed_days)

        self.travel.increment_traveled_time(61)
        self.assertEqual(datetime.time(0, 3, 1), self.travel.current_journey.elapsed_time)
        self.assertEqual(0, self.travel.current_journey.elapsed_days)

        self.travel.increment_traveled_time(3600 - 1)
        self.assertEqual(datetime.time(1, 3, 0), self.travel.current_journey.elapsed_time)
        self.assertEqual(0, self.travel.current_journey.elapsed_days)

        self.travel.increment_traveled_time(3600)
        self.assertEqual(datetime.time(2, 3, 0), self.travel.current_journey.elapsed_time)
        self.assertEqual(0, self.travel.current_journey.elapsed_days)

        self.travel.increment_traveled_time(3600 + 1)
        self.assertEqual(datetime.time(3, 3, 1), self.travel.current_journey.elapsed_time)
        self.assertEqual(0, self.travel.current_journey.elapsed_days)

        self.travel.increment_traveled_time(3600 - 59)
        self.assertEqual(datetime.time(4, 2, 2), self.travel.current_journey.elapsed_time)
        self.assertEqual(0, self.travel.current_journey.elapsed_days)

        self.travel.increment_traveled_time(3600 + 60)
        self.assertEqual(datetime.time(5, 3, 2), self.travel.current_journey.elapsed_time)
        self.assertEqual(0, self.travel.current_journey.elapsed_days)

        self.travel.increment_traveled_time(3600 + 61)
        self.assertEqual(datetime.time(6, 4, 3), self.travel.current_journey.elapsed_time)
        self.assertEqual(0, self.travel.current_journey.elapsed_days)

        self.travel.increment_traveled_time(3600 * 24 - 1)
        self.assertEqual(datetime.time(6, 4, 2), self.travel.current_journey.elapsed_time)
        self.assertEqual(1, self.travel.current_journey.elapsed_days)

        self.travel.increment_traveled_time(3600 * 24 - 1)
        self.assertEqual(datetime.time(6, 4, 1), self.travel.current_journey.elapsed_time)
        self.assertEqual(2, self.travel.current_journey.elapsed_days)

        with self.assertRaises(ValueError):
            self.travel.increment_traveled_time(3600 * 24)

    def test_update_journey(self):
        self.travel.update_journey('Laranjeiras')

        total_distance: float = 1.2
        slowest_travel_time: int = int(total_distance / travel.MAX_SPEED * 3600)
        fastest_travel_time: int = int(total_distance / travel.MIN_SPEED * 3600)
        self.assertTrue(travel.Travel.seconds_to_datetime(slowest_travel_time) <= self.travel.current_journey.elapsed_time
                        <= travel.Travel.seconds_to_datetime(fastest_travel_time))
        self.assertEqual(total_distance, self.travel.current_journey.get_traveled_distance())
        self.assertEqual('Laranjeiras', self.travel.current_journey.get_current_location())
        self.assertEqual(travel.CAR, self.travel.current_journey.get_current_means_transport())

        self.travel.update_journey('Montinho das Laranjeiras')

        total_distance: float = total_distance + 0.5
        slowest_travel_time: int = int(total_distance / travel.MAX_SPEED * 3600)
        fastest_travel_time: int = int(total_distance / travel.MIN_SPEED * 3600)
        self.assertTrue(travel.Travel.seconds_to_datetime(slowest_travel_time) <= self.travel.current_journey.elapsed_time
                        <= travel.Travel.seconds_to_datetime(fastest_travel_time))
        self.assertEqual(total_distance, self.travel.current_journey.get_traveled_distance())
        self.assertEqual('Montinho das Laranjeiras', self.travel.current_journey.get_current_location())
        self.assertEqual(travel.CAR, self.travel.current_journey.get_current_means_transport())

        self.travel.update_journey('Alcoutim')

        total_distance: float = total_distance + 8.8
        slowest_travel_time: int = int(total_distance / travel.MAX_SPEED * 3600)
        fastest_travel_time: int = int(total_distance / travel.MIN_SPEED * 3600)
        self.assertTrue(travel.Travel.seconds_to_datetime(slowest_travel_time) <= self.travel.current_journey.elapsed_time
                        <= travel.Travel.seconds_to_datetime(fastest_travel_time))
        self.assertEqual(total_distance, self.travel.current_journey.get_traveled_distance())
        self.assertEqual('Alcoutim', self.travel.current_journey.get_current_location())
        self.assertEqual(travel.CAR, self.travel.current_journey.get_current_means_transport())

    def test_request_car_simulation_usage(self):
        with unittest.mock.patch('builtins.input', side_effect=["n"]):  # Provides option to car usage menu
            is_car_requested: bool = self.travel.request_car_simulation_usage()
        self.assertFalse(is_car_requested)
        with unittest.mock.patch('builtins.input', side_effect=["N"]):  # Provides option to car usage menu
            is_car_requested: bool = self.travel.request_car_simulation_usage()
        self.assertFalse(is_car_requested)

        with unittest.mock.patch('builtins.input', side_effect=["y"]):  # Provides option to car usage menu
            is_car_requested: bool = self.travel.request_car_simulation_usage()
        self.assertTrue(is_car_requested)
        with unittest.mock.patch('builtins.input', side_effect=["Y"]):  # Provides option to car usage menu
            is_car_requested: bool = self.travel.request_car_simulation_usage()
        self.assertTrue(is_car_requested)

    # make_journey() routine is tested in integration tests of test_integration.py
