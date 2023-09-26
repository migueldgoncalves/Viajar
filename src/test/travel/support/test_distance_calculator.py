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

        self.assertEqual(133359, len(self.dist_calc.processed_map))  # Number of processed nodes in the map

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

        self.assertEqual(5595, len(self.dist_calc.processed_map))  # Number of processed nodes in the map

        for node_id in self.dist_calc.processed_map:
            assert node_id
            assert self.dist_calc.processed_map[node_id]

        node_id = 25398450
        self.assertEqual(39.2031381, self.dist_calc.processed_map[node_id].latitude)
        self.assertEqual(-8.7930774, self.dist_calc.processed_map[node_id].longitude)
        self.assertEqual(node_id, self.dist_calc.processed_map[node_id].node_id)
        self.assertEqual({194100060, 4080875384}, self.dist_calc.processed_map[node_id].surrounding_node_ids)

    def test_calculate_distance_with_adjusts_invalid_parameters(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        # No processed map
        with self.assertRaises(AssertionError):
            self.dist_calc.calculate_distance_with_adjusts(Coordinates(39.0, -7.0), Coordinates(40.0, -8.0))

        self.dist_calc.generate_processed_map([Coordinates(39.0, -7.0), Coordinates(39.1, -7.1)], ways.ROAD, ways.PORTUGAL, osm_interface.DETAIL_LEVEL_URBAN, None)

        # No source coordinates
        with self.assertRaises(AssertionError):
            self.dist_calc.calculate_distance_with_adjusts(None, Coordinates(40.0, -8.0))

        # No destination coordinates
        with self.assertRaises(AssertionError):
            self.dist_calc.calculate_distance_with_adjusts(Coordinates(39.0, -7.0), None)

        # All coordinates missing
        with self.assertRaises(AssertionError):
            self.dist_calc.calculate_distance_with_adjusts(None, None)

        # Source and destination are the same
        with self.assertRaises(AssertionError):
            self.dist_calc.calculate_distance_with_adjusts(Coordinates(39.0, -7.0), Coordinates(39.0, -7.0))

    def test_calculate_distance_with_adjusts_successful_continental_portugal(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        # Urban route - Lisbon city center
        bottom_left_map_corner = Coordinates(38.713735, -9.156029)
        upper_right_map_corner = Coordinates(38.728909, -9.140453)
        source = Coordinates(38.718072, -9.151916)
        destination = Coordinates(38.722280, -9.148404)
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.ROAD, ways.PORTUGAL, osm_interface.DETAIL_LEVEL_URBAN, None)
        self.assertEqual(0.6, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In Google Maps, 0.7 km
        self.assertEqual(0.5, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=False))

        # Intercity route - Alentejo
        bottom_left_map_corner = Coordinates(37.507273, -8.454736)
        upper_right_map_corner = Coordinates(38.100089, -7.508203)
        source = Coordinates(37.596948, -8.175737)
        destination = Coordinates(37.901726, -7.843903)
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.ROAD, ways.PORTUGAL, osm_interface.DETAIL_LEVEL_INTERCITY, None)
        self.assertEqual(49.7, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In Google Maps, 50.1 km
        # Testing with less_checks=False takes too long - Skipping

        # Route inside a single road - A1 freeway/motorway
        bottom_left_map_corner = Coordinates(36.848715, -9.573958)
        upper_right_map_corner = Coordinates(42.306369, -5.670825)
        source = Coordinates(38.790766, -9.114402)
        destination = Coordinates(41.076935, -8.578457)
        road_name = ways.PT_A1.osm_name
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.ROAD, ways.PORTUGAL, None, road_name)
        self.assertEqual(291.2, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In Google Maps, 291 km. Rounded for values >= 100 km
        # Testing with less_checks=False takes too long - Skipping

        # Route inside a single railway - North Line
        bottom_left_map_corner = Coordinates(36.848715, -9.573958)
        upper_right_map_corner = Coordinates(42.306369, -5.670825)
        source = Coordinates(38.725984, -9.112900)
        destination = Coordinates(41.146064, -8.585946)
        railway_name = ways.PT_NORTH_LINE.osm_name
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.RAILWAY, ways.PORTUGAL, None, railway_name)
        self.assertEqual(334.2, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In reality, 336 km. A bit less, since start and end points were placed near and not inside the terminal stations
        # Testing with less_checks=False takes too long - Skipping

    def test_calculate_distance_with_adjusts_successful_continental_spain(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        # Urban route - Barcelona city center
        bottom_left_map_corner = Coordinates(41.375156, 2.149157)
        upper_right_map_corner = Coordinates(41.394981, 2.175449)
        source = Coordinates(41.379022, 2.156946)
        destination = Coordinates(41.390751, 2.165275)
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.ROAD, ways.SPAIN, osm_interface.DETAIL_LEVEL_URBAN, None)
        self.assertEqual(1.6, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In Google Maps, 1.8 km
        self.assertEqual(1.5, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=False))

        # Intercity route - Castilla-La Mancha
        bottom_left_map_corner = Coordinates(39.118756, -4.355722)
        upper_right_map_corner = Coordinates(39.563157, -3.195433)
        source = Coordinates(39.232904, -4.167522)
        destination = Coordinates(39.407921, -3.797675)
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.ROAD, ways.SPAIN, osm_interface.DETAIL_LEVEL_INTERCITY, None)
        self.assertEqual(67.0, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In Google Maps, 43.9 km. 64.5 km if using route with less secondary roads
        # Testing with less_checks=False takes too long - Skipping

        # Route inside a single road - A-4 freeway/motorway
        bottom_left_map_corner = Coordinates(35.843717, -9.937978)
        upper_right_map_corner = Coordinates(42.953178, 3.702633)
        source = Coordinates(37.408592, -5.946347)
        destination = Coordinates(40.375060, -3.682381)
        road_name = ways.ES_A4.osm_name
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.ROAD, ways.SPAIN, None, road_name)
        self.assertEqual(516.8, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In Google Maps, 517 km. Rounded for values >= 100 km
        # Testing with less_checks=False takes too long - Skipping

        # Route inside a single railway - Alcázar de San Juan-Badajoz Line
        bottom_left_map_corner = Coordinates(35.843717, -9.937978)
        upper_right_map_corner = Coordinates(42.953178, 3.702633)
        source = Coordinates(38.90639,-6.33439)
        destination = Coordinates(38.98522,-3.91282)
        railway_name = ways.ES_ALCAZAR_DE_SAN_JUAN_BADAJOZ.osm_name
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.RAILWAY, ways.SPAIN, None, railway_name)
        self.assertEqual(276.1, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In reality, 278 km. A bit less, since starting point was placed near and not inside the station
        # Testing with less_checks=False takes too long - Skipping

    def test_calculate_distance_with_adjusts_successful_gibraltar(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        # Urban route
        bottom_left_map_corner = Coordinates(36.101591, -5.388635)
        upper_right_map_corner = Coordinates(36.160580, -5.325853)
        source = Coordinates(36.154972, -5.348429)
        destination = Coordinates(36.109353, -5.345692)
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.ROAD, ways.GIBRALTAR, osm_interface.DETAIL_LEVEL_URBAN, None)
        self.assertEqual(6.0, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In Google Maps, 6.0 km if avoiding the Gibraltar Airport Runway
        # Testing with less_checks=False takes too long - Skipping

        # Gibraltar is small enough to be covered with an urban level of detail - No need to perform tests with an intercity level of detail

        # Route inside a single road - Europa Road
        bottom_left_map_corner = Coordinates(36.101591, -5.388635)
        upper_right_map_corner = Coordinates(36.160580, -5.325853)
        source = Coordinates(36.13497, -5.35181)
        destination = Coordinates(36.11017, -5.34535)
        road_name = ways.GI_EUROPA_ROAD.osm_name
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.ROAD, ways.GIBRALTAR, None, road_name)
        self.assertEqual(3.1, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In Google Maps, 3.2 km
        self.assertEqual(3.0, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=False))

        # Gibraltar has no railways

    def test_calculate_distance_with_adjusts_successful_andorra(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        # Urban route - Andorra-la-Vella city center
        bottom_left_map_corner = Coordinates(42.4905, 1.4880)
        upper_right_map_corner = Coordinates(42.5263, 1.5741)
        source = Coordinates(42.504305, 1.514556)
        destination = Coordinates(42.509593, 1.541506)
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.ROAD, ways.ANDORRA, osm_interface.DETAIL_LEVEL_URBAN, None)
        self.assertEqual(2.4, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In Google Maps, 2.5 km
        # Testing with less_checks=False takes too long - Skipping

        # Intercity route - Entire country
        bottom_left_map_corner = Coordinates(42.4144, 1.3431)
        upper_right_map_corner = Coordinates(42.6663, 1.8745)
        source = Coordinates(42.435280, 1.472793)
        destination = Coordinates(42.549009, 1.737475)
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.ROAD, ways.ANDORRA, osm_interface.DETAIL_LEVEL_INTERCITY, None)
        self.assertEqual(36.2, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In Google Maps, 36.5 km
        # Testing with less_checks=False takes too long - Skipping

        # Route inside a single road - Dos Valires Tunnel
        bottom_left_map_corner = Coordinates(42.4144, 1.3431)
        upper_right_map_corner = Coordinates(42.6663, 1.8745)
        source = Coordinates(42.518571, 1.554789)
        destination = Coordinates(42.529434, 1.522012)
        road_name = ways.AD_DOS_VALIRES_TUNNEL.osm_name
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.ROAD, ways.ANDORRA, None, road_name)
        self.assertEqual(2.9, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In Google Maps, 3.0 km
        # Testing with less_checks=False takes too long - Skipping

        # There are no railways in Andorra

    def test_calculate_distance_with_adjusts_successful_balearic_islands(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        # Urban route - Palma de Mallorca city center
        bottom_left_map_corner = Coordinates(39.5638, 2.6366)
        upper_right_map_corner = Coordinates(39.5944, 2.6782)
        source = Coordinates(39.569661, 2.641618)
        destination = Coordinates(39.573224, 2.651509)
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.ROAD, ways.SPAIN, osm_interface.DETAIL_LEVEL_URBAN, None)
        self.assertEqual(1.1, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In Google Maps, 1.2 km
        # Testing with less_checks=False takes too long - Skipping

        # Intercity route - Menorca Island
        bottom_left_map_corner = Coordinates(39.7739, 3.6749)
        upper_right_map_corner = Coordinates(40.1432, 4.4083)
        source = Coordinates(39.815148, 4.269328)
        destination = Coordinates(40.002915, 3.801283)
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.ROAD, ways.SPAIN, osm_interface.DETAIL_LEVEL_INTERCITY, None)
        self.assertEqual(52.7, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In Google Maps, 56.1 km
        # Testing with less_checks=False takes too long - Skipping

        # Route inside a single road - Ma-13
        bottom_left_map_corner = Coordinates(39.1222, 2.2275)
        upper_right_map_corner = Coordinates(40.0801, 3.5568)
        source = Coordinates(39.588792, 2.670573)
        destination = Coordinates(39.790996, 3.016499)
        road_name = ways.ES_MA13.osm_name
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.ROAD, ways.SPAIN, None, road_name)
        self.assertEqual(38.6, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In Google Maps, 38.7 km
        # Testing with less_checks=False takes too long - Skipping

        # Route inside a single railway - SFM T3 line
        bottom_left_map_corner = Coordinates(39.1222, 2.2275)
        upper_right_map_corner = Coordinates(40.0801, 3.5568)
        source = Coordinates(39.57667, 2.65464)
        destination = Coordinates(39.57055, 3.20285)
        railway_name = ways.ES_SFM_T3.osm_name
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.RAILWAY, ways.SPAIN, None, railway_name)
        self.assertEqual(64.0, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In reality, 64 km
        # Testing with less_checks=False takes too long - Skipping

    def test_calculate_distance_with_adjusts_successful_canary_islands(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        # Urban route - Las Palmas de Gran Canaria city center
        bottom_left_map_corner = Coordinates(28.1245, -15.4560)
        upper_right_map_corner = Coordinates(28.1456,-15.4270)
        source = Coordinates(28.128788, -15.446335)
        destination = Coordinates(28.137339, -15.429743)
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.ROAD, ways.CANARY_ISLANDS, osm_interface.DETAIL_LEVEL_URBAN, None)
        self.assertEqual(2.0, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In Google Maps, 2.1 km
        self.assertEqual(2.0, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=False))

        # Intercity route - Fuerteventura Island
        bottom_left_map_corner = Coordinates(27.9934, -14.6173)
        upper_right_map_corner = Coordinates(28.7869,-13.7206)
        source = Coordinates(28.057337, -14.354274)
        destination = Coordinates(28.729187, -13.871352)
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.ROAD, ways.CANARY_ISLANDS, osm_interface.DETAIL_LEVEL_INTERCITY, None)
        self.assertEqual(112.2, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In Google Maps, 109 km. Rounded for distances >= 100 km
        # Testing with less_checks=False takes too long - Skipping

        # Route inside a single road - GC-1
        bottom_left_map_corner = Coordinates(27.7032, -15.8958)
        upper_right_map_corner = Coordinates(28.2173, -15.3053)
        source = Coordinates(27.83220, -15.75288)
        destination = Coordinates(28.05608, -15.41808)
        road_name = ways.ES_GC1.osm_name
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.ROAD, ways.CANARY_ISLANDS, None, road_name)
        self.assertEqual(65.9, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In Google Maps, 66.0 km
        # Testing with less_checks=False takes too long - Skipping

        # Route inside a single railway - Line 1 of Tenerife Tramway
        bottom_left_map_corner = Coordinates(27.9473, -16.9093)
        upper_right_map_corner = Coordinates(28.6364, -16.0538)
        source = Coordinates(28.48621, -16.31630)
        destination = Coordinates(28.45902, -16.25102)
        railway_name = ways.ES_TENERIFE_TRAMWAY_T1.osm_name
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.RAILWAY, ways.CANARY_ISLANDS, None, railway_name)
        self.assertEqual(12.4, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In reality, 12.5 km
        # Testing with less_checks=False takes too long - Skipping

    def test_calculate_distance_with_adjusts_successful_madeira_islands(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        # Urban route - Funchal city center
        bottom_left_map_corner = Coordinates(32.6408, -16.9222)
        upper_right_map_corner = Coordinates(32.6610, -16.8928)
        source = Coordinates(32.6474, -16.9133)
        destination = Coordinates(32.6560, -16.8924)
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.ROAD, ways.PORTUGAL, osm_interface.DETAIL_LEVEL_URBAN, None)
        self.assertEqual(2.5, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In Google Maps, 2.6 km
        self.assertEqual(2.4, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=False))

        # Intercity route - Porto Santo Island
        bottom_left_map_corner = Coordinates(32.6474, -16.9133)
        upper_right_map_corner = Coordinates(33.1303, -16.2457)
        source = Coordinates(33.02483, -16.37955)
        destination = Coordinates(33.09665, -16.31359)
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.ROAD, ways.PORTUGAL, osm_interface.DETAIL_LEVEL_INTERCITY, None)
        self.assertEqual(13.7, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In Google Maps, 12.8 km
        # Testing with less_checks=False takes too long - Skipping

        # Route inside a single road - VR 1
        bottom_left_map_corner = Coordinates(32.6002, -17.3515)
        upper_right_map_corner = Coordinates(32.8687, -16.6175)
        source = Coordinates(32.68354, -17.05193)
        destination = Coordinates(32.74267, -16.73667)
        road_name = ways.PT_VR1.osm_name
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.ROAD, ways.PORTUGAL, None, road_name)
        self.assertEqual(43.4, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In Google Maps, 43.5 km
        # Testing with less_checks=False takes too long - Skipping

        # There are no railways in the Madeira Islands

    def test_calculate_distance_with_adjusts_successful_azores_islands(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        # Urban route - Ponta Delgada city center
        bottom_left_map_corner = Coordinates(37.7336, -25.6813)
        upper_right_map_corner = Coordinates(37.7523, -25.6530)
        source = Coordinates(37.7381, -25.6738)
        destination = Coordinates(37.7458, -25.6563)
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.ROAD, ways.PORTUGAL, osm_interface.DETAIL_LEVEL_URBAN, None)
        self.assertEqual(1.8, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In Google Maps, 2.2 km
        self.assertEqual(1.8, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=False))

        # Intercity route - Pico Island
        bottom_left_map_corner = Coordinates(38.3590, -28.6153)
        upper_right_map_corner = Coordinates(38.5669, -28.0193)
        source = Coordinates(38.53468, -28.52817)
        destination = Coordinates(38.42466, -28.05887)
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.ROAD, ways.PORTUGAL, osm_interface.DETAIL_LEVEL_INTERCITY, None)
        self.assertEqual(46.8, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In Google Maps, 46.9 km
        # Testing with less_checks=False takes too long - Skipping

        # Route inside a single road - EN 1-1A
        bottom_left_map_corner = Coordinates(37.6904, -25.9236)
        upper_right_map_corner = Coordinates(37.8987, -25.0948)
        source = Coordinates(37.745718, -25.699344)
        destination = Coordinates(37.75245, -25.65329)
        road_name = ways.PT_EN11A.osm_name
        self.dist_calc.generate_processed_map([bottom_left_map_corner, upper_right_map_corner], ways.ROAD, ways.PORTUGAL, None, road_name)
        self.assertEqual(4.5, self.dist_calc.calculate_distance_with_adjusts(source, destination, less_checks=True))  # In Google Maps, 4.6 km
        # Testing with less_checks=False takes too long - Skipping

        # There are no railways in the Azores Islands

    def test_calculate_distance_invalid_parameters(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        # No processed map
        with self.assertRaises(AssertionError):
            self.dist_calc.calculate_distance(Coordinates(39.0, -7.0), Coordinates(40.0, -8.0))

        self.dist_calc.generate_processed_map([Coordinates(39.0, -7.0), Coordinates(39.1, -7.1)], ways.ROAD, ways.PORTUGAL, osm_interface.DETAIL_LEVEL_URBAN, None)

        # No source coordinates
        with self.assertRaises(AssertionError):
            self.dist_calc.calculate_distance(None, Coordinates(40.0, -8.0))

        # No destination coordinates
        with self.assertRaises(AssertionError):
            self.dist_calc.calculate_distance(Coordinates(39.0, -7.0), None)

        # All coordinates missing
        with self.assertRaises(AssertionError):
            self.dist_calc.calculate_distance(None, None)

        # Source and destination are the same
        with self.assertRaises(AssertionError):
            self.dist_calc.calculate_distance(Coordinates(39.0, -7.0), Coordinates(39.0, -7.0))

    # Routine calculate_distance() is invoked repeatedly on every call to calculate_distance_with_adjusts()
    # No need for dedicated unit tests

    def test_coordinates_to_nearest_node_invalid_parameters(self):
        with self.assertRaises(AssertionError):
            self.dist_calc._coordinates_to_nearest_node(None)

    def test_coordinates_to_nearest_node_successful(self):
        # Routine _coordinates_to_nearest_node() is invoked repeatedly on every call to calculate_distance_with_adjusts()
        # Therefore, this routine will contain a single test case
        self.dist_calc.generate_processed_map([Coordinates(39.0, -9.0), Coordinates(38.0, -8.0)], way_type=ways.ROAD, country=ways.PORTUGAL, area_detail=osm_interface.DETAIL_LEVEL_INTERCITY, way_name=None)
        self.assertEqual(4460356197, self.dist_calc._coordinates_to_nearest_node(Coordinates(39.1, -9.1)).node_id)

    def tearDown(self) -> None:
        self.dist_calc = None
