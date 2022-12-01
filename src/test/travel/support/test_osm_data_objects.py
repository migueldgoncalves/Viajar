import unittest

from travel.support.osm_interface import OsmNode, OsmWay


class TestOsmDataObjects(unittest.TestCase):

    def setUp(self):
        self.node_1: OsmNode = OsmNode(1, 1, -1)
        self.node_2: OsmNode = OsmNode(2, 2, -2)
        self.node_3: OsmNode = OsmNode(3, 3, -3)

    #  #  #  #  #  #  #
    #  OSM node tests  #
    #  #  #  #  #  #  #

    def test_node_initializer_invalid_parameters(self):
        # All parameters are invalid
        with self.assertRaises(AssertionError):
            OsmNode(0, -91, -181)

        # Node ID is invalid
        with self.assertRaises(AssertionError):
            OsmNode(-1, -90, -180)

        # Latitude is invalid
        with self.assertRaises(AssertionError):
            OsmNode(1, -91, -180)
        with self.assertRaises(AssertionError):
            OsmNode(1, 91, 180)

        # Longitude is invalid
        with self.assertRaises(AssertionError):
            OsmNode(1, -90, -181)
        with self.assertRaises(AssertionError):
            OsmNode(1, 90, 181)

    def test_node_initializer_successful(self):
        # Minimum latitude and longitude
        node = OsmNode(1, -90, -180)
        self.assertEqual(1, node.node_id)
        self.assertEqual(-90, node.latitude)
        self.assertEqual(-180, node.longitude)
        self.assertEqual(set(), node.surrounding_node_ids)

        # Maximum latitude and longitude
        node = OsmNode(1, 90, 180)
        self.assertEqual(1, node.node_id)
        self.assertEqual(90, node.latitude)
        self.assertEqual(180, node.longitude)
        self.assertEqual(set(), node.surrounding_node_ids)

        # Add surrounding node IDs
        node.surrounding_node_ids.add(2)
        self.assertEqual({2}, node.surrounding_node_ids)
        node.surrounding_node_ids.add(3)
        self.assertEqual({2, 3}, node.surrounding_node_ids)
        node.surrounding_node_ids.add(3)
        self.assertEqual({2, 3}, node.surrounding_node_ids)

    #  #  #  #  #  #  #
    #  OSM way tests  #
    #  #  #  #  #  #  #

    def test_way_initializer_invalid_parameters(self):
        # All invalid parameters
        with self.assertRaises(AssertionError):
            OsmWay(0, [])

        # Invalid way ID
        with self.assertRaises(AssertionError):
            OsmWay(-1, [self.node_1, self.node_2, self.node_3])
        with self.assertRaises(AssertionError):
            OsmWay(0, [self.node_1, self.node_2, self.node_3])

        # Invalid OSM node list
        with self.assertRaises(AssertionError):
            OsmWay(1, [])

    def test_way_initializer_successful(self):
        way = OsmWay(1, [self.node_1, self.node_2, self.node_3])

        self.assertEqual(1, way.way_id)
        self.assertEqual([self.node_1, self.node_2, self.node_3], way.node_list)

    def tearDown(self):
        self.node_1 = None
        self.node_2 = None
        self.node_3 = None
