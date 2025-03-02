import unittest

from travel.main import db_distance_calculator, travel


class TestDBDistanceCalculator(unittest.TestCase):

    def setUp(self):
        pass

    def test_distance_between_locations_invalid_parameters(self):
        with self.assertRaises(Exception):
            db_distance_calculator.get_shortest_distance_between_locations('', 'Laranjeiras', db_distance_calculator.DISTANCE_TYPE_HOPS, [travel.CAR])
        with self.assertRaises(Exception):
            db_distance_calculator.get_shortest_distance_between_locations('Invalid Location', 'Laranjeiras', db_distance_calculator.DISTANCE_TYPE_HOPS, [travel.CAR])
        with self.assertRaises(Exception):
            db_distance_calculator.get_shortest_distance_between_locations('Guerreiros do Rio', '', db_distance_calculator.DISTANCE_TYPE_HOPS, [travel.CAR])
        with self.assertRaises(Exception):
            db_distance_calculator.get_shortest_distance_between_locations('Guerreiros do Rio', 'Invalid Location', db_distance_calculator.DISTANCE_TYPE_HOPS, [travel.CAR])
        with self.assertRaises(Exception):
            db_distance_calculator.get_shortest_distance_between_locations('Guerreiros do Rio', 'Laranjeiras', '', [travel.CAR])
        with self.assertRaises(Exception):
            db_distance_calculator.get_shortest_distance_between_locations('Guerreiros do Rio', 'Laranjeiras', 'Invalid Distance Type', [travel.CAR])
        with self.assertRaises(Exception):
            db_distance_calculator.get_shortest_distance_between_locations('Guerreiros do Rio', 'Laranjeiras', db_distance_calculator.DISTANCE_TYPE_HOPS, [])
        with self.assertRaises(Exception):
            db_distance_calculator.get_shortest_distance_between_locations('Guerreiros do Rio', 'Laranjeiras', db_distance_calculator.DISTANCE_TYPE_HOPS, ["Invalid Means of Transport"])

    def test_distance_between_2_connected_locations(self):
        # These locations are directly connected
        start_location = "Guerreiros do Rio"
        end_location = "Laranjeiras"
        means_of_transport = travel.CAR
        distance_type = db_distance_calculator.DISTANCE_TYPE_KILOMETERS

        expected_distance_kilometers = 1.2
        expected_distance_hops = 1
        expected_result = (expected_distance_kilometers, expected_distance_hops)

        result: tuple[float, int] = db_distance_calculator.get_shortest_distance_between_locations(
            start_location=start_location,
            end_location=end_location,
            distance_type=distance_type,
            means_of_transport=means_of_transport
        )
        self.assertEqual(expected_result, result)

    def test_distance_between_2_close_locations(self):
        # These locations are close if going by boat, but far away if going by car
        start_location = "Guerreiros do Rio"
        end_location = "Sanlúcar de Guadiana"
        distance_type = db_distance_calculator.DISTANCE_TYPE_HOPS

        # Test - Travel by car

        means_of_transport = travel.CAR
        expected_distance_kilometers = 67.5
        expected_distance_hops = 20
        expected_result = (expected_distance_kilometers, expected_distance_hops)

        result: tuple[float, int] = db_distance_calculator.get_shortest_distance_between_locations(
            start_location=start_location,
            end_location=end_location,
            distance_type=distance_type,
            means_of_transport=means_of_transport
        )
        self.assertEqual(expected_result, result)

        # Test - Travel by all means of transport

        means_of_transport = travel.ALL_MEANS_TRANSPORT
        expected_distance_kilometers = 11.0
        expected_distance_hops = 3
        expected_result = (expected_distance_kilometers, expected_distance_hops)

        result: tuple[float, int] = db_distance_calculator.get_shortest_distance_between_locations(
            start_location=start_location,
            end_location=end_location,
            distance_type=distance_type,
            means_of_transport=means_of_transport
        )
        self.assertEqual(expected_result, result)

    def test_distance_between_2_distant_locations(self):
        start_location = "Guerreiros do Rio"
        end_location = "Andorra-Spain Border - Andorran Customs"
        distance_type = db_distance_calculator.DISTANCE_TYPE_KILOMETERS

        # Test - Travel by car

        means_of_transport = travel.CAR
        expected_distance_kilometers = 1487.9
        expected_distance_hops = 398
        expected_result = (expected_distance_kilometers, expected_distance_hops)

        result: tuple[float, int] = db_distance_calculator.get_shortest_distance_between_locations(
            start_location=start_location,
            end_location=end_location,
            distance_type=distance_type,
            means_of_transport=means_of_transport
        )
        self.assertEqual(expected_result, result)

        # Test - Travel by all means of transport

        means_of_transport = travel.ALL_MEANS_TRANSPORT
        expected_distance_kilometers = 1429.3
        expected_distance_hops = 273
        expected_result = (expected_distance_kilometers, expected_distance_hops)

        result: tuple[float, int] = db_distance_calculator.get_shortest_distance_between_locations(
            start_location=start_location,
            end_location=end_location,
            distance_type=distance_type,
            means_of_transport=means_of_transport
        )
        self.assertEqual(expected_result, result)

    def test_distance_from_island_location(self):
        start_location = "Port of Ponta Delgada - Portas do Mar Passenger Terminal"
        distance_type = db_distance_calculator.DISTANCE_TYPE_HOPS
        means_of_transport = travel.CAR

        expected_min_locations = 10
        expected_max_locations = 500

        result: dict[tuple[float, int], str] = db_distance_calculator.get_shortest_distances_from_location(
            start_location=start_location,
            distance_type=distance_type,
            means_of_transport=means_of_transport
        )

        self.assertTrue(len(result) > expected_min_locations)
        self.assertTrue(len(result) < expected_max_locations)
        for distances in result:
            distance_kilometers: float = distances[0]
            distance_hops: int = distances[1]
            location_name: str = result[distances]

            self.assertTrue(distance_kilometers > 0)
            self.assertTrue(distance_hops > 0)
            self.assertTrue(location_name != '')
            self.assertTrue(location_name is not None)

    def test_distance_from_iberian_peninsula_location(self):
        start_location = "Guerreiros do Rio"
        distance_type = db_distance_calculator.DISTANCE_TYPE_KILOMETERS
        means_of_transport = travel.ALL_MEANS_TRANSPORT

        expected_min_locations = 3500
        expected_max_locations = 1000000

        result: dict[tuple[float, int], str] = db_distance_calculator.get_shortest_distances_from_location(
            start_location=start_location,
            distance_type=distance_type,
            means_of_transport=means_of_transport
        )

        self.assertTrue(len(result) > expected_min_locations)
        self.assertTrue(len(result) < expected_max_locations)
        for distances in result:
            distance_kilometers: float = distances[0]
            distance_hops: int = distances[1]
            location_name: str = result[distances]

            self.assertTrue(distance_kilometers > 0)
            self.assertTrue(distance_hops > 0)
            self.assertTrue(location_name != '')
            self.assertTrue(location_name is not None)

    def tearDown(self):
        pass