import unittest

from travel.support.osm_interface import OsmInterface


class TestFailIfServersDown(unittest.TestCase):
    """
    This test should be invoked by tests that rely on the OSM servers
    If servers are down, tests will fail with a specific message
    """
    def test_fail_if_servers_down(self):
        connected = OsmInterface().test_connections()
        if not connected:
            self.fail("Servers are not connected")
