import unittest
import io

from travel.support.distance_calculator import DistanceCalculator
from travel.support.coordinates import Coordinates
from travel.support import ways, osm_interface
from test.travel.support import test_fail_if_servers_down
from test.utils import redirect_output


class TestDistanceCalculator(unittest.TestCase):

    def setUp(self) -> None:
        self.dist_calc = DistanceCalculator()

    def test_setup(self):
        self.assertEqual({}, self.dist_calc.processed_map)

    def test_generate_processed_map_invalid_parameters(self):
        # All invalid parameters
        with self.assertRaises(AssertionError):
            self.dist_calc.generate_processed_map([], None, None, None, None)

        # Empty coordinate list
        with self.assertRaises(AssertionError):
            self.dist_calc.generate_processed_map([], ways.ROAD, ways.PORTUGAL, osm_interface.DETAIL_LEVEL_URBAN, None)

        # Too short coordinate list
        with self.assertRaises(AssertionError):
            self.dist_calc.generate_processed_map([Coordinates(39.0, -8.0)], ways.ROAD, ways.PORTUGAL, osm_interface.DETAIL_LEVEL_URBAN, None)

        # No way type
        with self.assertRaises(AssertionError):
            self.dist_calc.generate_processed_map([Coordinates(39.0, -8.0), Coordinates(40.0, -7.0)], None, ways.PORTUGAL, osm_interface.DETAIL_LEVEL_URBAN, None)

        # Invalid way type
        with self.assertRaises(AssertionError):
            self.dist_calc.generate_processed_map([Coordinates(39.0, -8.0), Coordinates(40.0, -7.0)], 'Invalid way type', ways.PORTUGAL, osm_interface.DETAIL_LEVEL_URBAN, None)

        # No country
        with self.assertRaises(AssertionError):
            self.dist_calc.generate_processed_map([Coordinates(39.0, -8.0), Coordinates(40.0, -7.0)], ways.ROAD, None, osm_interface.DETAIL_LEVEL_URBAN, None)

        # Invalid country
        with self.assertRaises(AssertionError):
            self.dist_calc.generate_processed_map([Coordinates(39.0, -8.0), Coordinates(40.0, -7.0)], ways.ROAD, 'Invalid country', osm_interface.DETAIL_LEVEL_URBAN, None)

        # No area detail and no way name
        with self.assertRaises(AssertionError):
            self.dist_calc.generate_processed_map([Coordinates(39.0, -8.0), Coordinates(40.0, -7.0)], ways.ROAD, ways.PORTUGAL, None, None)

        # Invalid area detail, no way name
        with self.assertRaises(AssertionError):
            self.dist_calc.generate_processed_map([Coordinates(39.0, -8.0), Coordinates(40.0, -7.0)], ways.ROAD, ways.PORTUGAL, -1, None)

        # No area detail, invalid way name
        self.dist_calc.generate_processed_map([Coordinates(39.0, -8.0), Coordinates(40.0, -7.0)], ways.ROAD, ways.PORTUGAL, None, 'Invalid way name')
        self.assertEqual({}, self.dist_calc.processed_map)

    def test_generate_processed_map_check_large_area_warning(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down
        stdout_redirect: io.StringIO = redirect_output()

        expected_output = "Warning: The area to cover is very large - This operation can take a very long time"

        coordinates_10_10_acceptable = [Coordinates(39.0, -8.0), Coordinates(39.05, -8.05)]  # 5.6 x 4.3 km
        coordinates_10_10_large = [Coordinates(39.0, -8.0), Coordinates(39.1, -8.15)]  # 11.1 x 13.0 km
        coordinates_100_100_acceptable = [Coordinates(39.0, -8.0), Coordinates(39.5, -8.5)]  # 55.6 x 43.2 km
        coordinates_100_100_large = [Coordinates(39.0, -8.0), Coordinates(40.0, -9.2)]  # 111.2 x 103.7 km
        coordinates_iberian_peninsula = [Coordinates(36.0, -9.0), Coordinates(43.0, 2.0)]

        freeway_in_small_area: str = ways.PT_A5.osm_name
        freeway_in_large_area: str = ways.ES_A4.osm_name

        railway_in_small_area: str = ways.PT_LISBON_METRO_RED_LINE.osm_name
        railway_in_large_area: str = ways.PT_BEIRA_BAIXA_LINE.osm_name

        # Areas with acceptable size
        self.dist_calc.generate_processed_map(
            coordinates_10_10_acceptable, ways.ROAD, ways.PORTUGAL, area_detail=osm_interface.DETAIL_LEVEL_URBAN, way_name=None)
        self.dist_calc.generate_processed_map(
            coordinates_10_10_acceptable, ways.RAILWAY, ways.PORTUGAL, area_detail=osm_interface.DETAIL_LEVEL_URBAN, way_name=None)
        self.dist_calc.generate_processed_map(
            coordinates_100_100_acceptable, ways.ROAD, ways.PORTUGAL, area_detail=osm_interface.DETAIL_LEVEL_INTERCITY, way_name=None)
        self.dist_calc.generate_processed_map(
            coordinates_100_100_acceptable, ways.RAILWAY, ways.PORTUGAL, area_detail=osm_interface.DETAIL_LEVEL_INTERCITY, way_name=None)
        # Warning should not appear even when covering large ways
        self.dist_calc.generate_processed_map(
            coordinates_iberian_peninsula, ways.ROAD, ways.PORTUGAL, area_detail=None, way_name=freeway_in_small_area)
        self.dist_calc.generate_processed_map(
            coordinates_iberian_peninsula, ways.ROAD, ways.PORTUGAL, area_detail=None, way_name=railway_in_small_area)
        self.dist_calc.generate_processed_map(
            coordinates_iberian_peninsula, ways.ROAD, ways.SPAIN, area_detail=None, way_name=freeway_in_large_area)
        self.dist_calc.generate_processed_map(
            coordinates_iberian_peninsula, ways.ROAD, ways.PORTUGAL, area_detail=None, way_name=railway_in_large_area)

        # Ensures warning did not appear
        self.assertEqual(0, stdout_redirect.getvalue().count(expected_output))

        # Large areas
        self.dist_calc.generate_processed_map(
            coordinates_10_10_large, ways.ROAD, ways.PORTUGAL, area_detail=osm_interface.DETAIL_LEVEL_URBAN, way_name=None)
        self.dist_calc.generate_processed_map(
            coordinates_10_10_large, ways.RAILWAY, ways.PORTUGAL, area_detail=osm_interface.DETAIL_LEVEL_URBAN, way_name=None)
        self.dist_calc.generate_processed_map(
            coordinates_100_100_large, ways.ROAD, ways.PORTUGAL, area_detail=osm_interface.DETAIL_LEVEL_INTERCITY, way_name=None)
        self.dist_calc.generate_processed_map(
            coordinates_100_100_large, ways.RAILWAY, ways.PORTUGAL, area_detail=osm_interface.DETAIL_LEVEL_INTERCITY, way_name=None)

        # Ensures warning appeared for every callback
        self.assertEqual(4, stdout_redirect.getvalue().count(expected_output))  # One appearance per routine call with large area

    def test_generate_processed_map_successful(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        # This routine can be tested through calls to higher-level routines, with fewer lines of code
        # As such, this test will contain two tests cases

        coordinates = [Coordinates(39.0, -8.0), Coordinates(40.0, -9.0)]
        way_type = ways.ROAD
        country = ways.PORTUGAL
        area_detail = osm_interface.DETAIL_LEVEL_INTERCITY
        way_name = ways.PT_A1.osm_name

        # Entire area

        self.dist_calc.generate_processed_map(coordinates, way_type, country, area_detail, None)

        self.assertEqual(129918, len(self.dist_calc.processed_map))  # Number of processed nodes in the map

        for node_id in self.dist_calc.processed_map:
            assert node_id
            assert self.dist_calc.processed_map[node_id]

        node_id = 320080135
        self.assertEqual(39.121356, self.dist_calc.processed_map[node_id].latitude)
        self.assertEqual(-8.9103214, self.dist_calc.processed_map[node_id].longitude)
        self.assertEqual(node_id, self.dist_calc.processed_map[node_id].node_id)
        self.assertEqual({25398012, 25398015, 320080136}, self.dist_calc.processed_map[node_id].surrounding_node_ids)

        # Single way

        self.dist_calc.generate_processed_map(coordinates, way_type, country, None, way_name)

        self.assertEqual(5504, len(self.dist_calc.processed_map))  # Number of processed nodes in the map

        for node_id in self.dist_calc.processed_map:
            assert node_id
            assert self.dist_calc.processed_map[node_id]

        node_id = 25398450
        self.assertEqual(39.2031381, self.dist_calc.processed_map[node_id].latitude)
        self.assertEqual(-8.7930774, self.dist_calc.processed_map[node_id].longitude)
        self.assertEqual(node_id, self.dist_calc.processed_map[node_id].node_id)
        self.assertEqual({194100060, 4080875384}, self.dist_calc.processed_map[node_id].surrounding_node_ids)

    def tearDown(self) -> None:
        self.dist_calc = None
