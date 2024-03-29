from typing import Optional, Union
import requests
from xml.dom import minidom

from travel.support import ways
from travel.support.coordinates import Coordinates

"""
Interface to OpenStreetMap API
Machines running instances of OSM can be Dockers running locally
"""

# Servers
DOCKER_IP = '127.0.0.1'  # Localhost
PORT_GIBRALTAR_SPAIN = 12345  # Same Docker instance contains maps of Spain and Gibraltar - Does not include Canary Islands
PORT_PORTUGAL = 12346
PORT_ANDORRA = 12347
PORT_CANARY_ISLANDS = 12348

##############################
# OpenStreetMap administrative levels

# General
COUNTRY = 2  # Applies to countries. Gibraltar and its waters are covered by a level-2 relation as well

# Andorra
ANDORRAN_PARISH = 7  # In Catalan, "parròquia"

# Gibraltar
GIBRALTAR_ADMIN_LEVEL = 4  # Covers the territory of Gibraltar. The sum of Gibraltar territory and waters is covered by a level-2 relation

# Portugal
AUTONOMOUS_REGION = 4  # Azores and Madeira
PORTUGUESE_DISTRICT = 6  # In Portuguese, "distrito", same as in Spanish
PORTUGUESE_MUNICIPALITY = 7  # In Portuguese, "concelho"
PORTUGUESE_PARISH = 8  # In Portuguese, "freguesia"
PORTUGUESE_HISTORIC_PARISH = 'historic_parish'  # Former Portuguese parishes (pre-2013), in the past were associated with level 9

# Spain
AUTONOMOUS_COMMUNITY = 4
PROVINCE = 6
COMARCA = 7
SPANISH_MUNICIPALITY = 8  # In Spanish, "municipio"
SPANISH_DISTRICT = 9  # In Spanish, "distrito"
##############################

# Detail levels allow to balance between the accuracy of the results and the time spent calculating them
DETAIL_LEVEL_INTERCITY = 1
DETAIL_LEVEL_URBAN = 2
ALL_DETAIL_LEVELS = [DETAIL_LEVEL_INTERCITY, DETAIL_LEVEL_URBAN]

DISTANCE_RECTANGLE_MARGIN = 0.1  # Degrees. 1 degree = Very approximately 100 km in the Iberian Peninsula

# Some or all of the most relevant road and path types are expected to be present below
# Reference: https://wiki.openstreetmap.org/wiki/Key:highway
TAGS_DETAIL_LEVEL_INTERCITY = [
    'motorway', 'trunk', 'primary', 'secondary', 'motorway_link', 'trunk_link', 'primary_link', 'secondary_link',
    'motorway_junction',
]
TAGS_DETAIL_LEVEL_URBAN = TAGS_DETAIL_LEVEL_INTERCITY + [
    'tertiary', 'unclassified', 'residential', 'tertiary_link', 'living_street', 'service',
]
TAGS_DESIRED_ROADS = {
    DETAIL_LEVEL_INTERCITY: TAGS_DETAIL_LEVEL_INTERCITY,
    DETAIL_LEVEL_URBAN: TAGS_DETAIL_LEVEL_URBAN,
}


class ExtremePoints:
    """
    Data access object to store the extreme points of a region
    """
    def __init__(self, name: str, admin_level: int, country: str,
                 north: Coordinates, south: Coordinates, east: Coordinates, west: Coordinates):
        assert name
        assert admin_level >= COUNTRY
        assert country in ways.ALL_SUPPORTED_COUNTRIES
        assert north
        assert south
        assert east
        assert west
        assert len({north, south, east, west}) == 4  # No coordinates should be repeated

        self.name: str = name
        self.admin_level: int = admin_level
        self.country: str = country
        self.north: Coordinates = north
        self.south: Coordinates = south
        self.east: Coordinates = east
        self.west: Coordinates = west

    def __str__(self):
        return f'Name: {self.name}\n' \
               f'Administrative level: {self.admin_level}\n' \
               f'Country: {self.country}\n' \
               f'North: {self.north}\n' \
               f'South: {self.south}\n' \
               f'East: {self.east}\n' \
               f'West: {self.west}'


class OsmNode:
    """
    Data access object to store the data of an OSM node
    """
    def __init__(self, node_id: int, latitude: float, longitude: float):
        assert node_id >= 0  # Node ID == 0 - Default node ID, used in distance calculation
        assert -90 <= latitude <= 90
        assert -180 <= longitude <= 180

        self.node_id: int = node_id
        self.latitude: float = float(latitude)
        self.longitude: float = float(longitude)
        self.surrounding_node_ids: set[int] = set()  # Contains IDs of nodes that are next to this node in ways and relations


class OsmWay:
    """
    Data access object to store the data of an OSM way
    """
    def __init__(self, way_id: int, node_list: list[OsmNode]):
        assert way_id > 0
        assert node_list

        self.way_id: int = way_id
        self.node_list: list[OsmNode] = node_list


class OsmInterface:

    @staticmethod
    def test_connections() -> bool:
        """
        Returns True if connection could be established with all OSM servers, False otherwise
        """
        try:
            for country in ways.ALL_SUPPORTED_COUNTRIES:
                server_url: str = OsmInterface._get_server_url(country)
                query: str = "out;"  # Simplest query - Just to check if server replies

                raw_response: str = requests.get(f'{server_url}?{query}').content.decode()  # Will raise ConnectionError if server is down
                xml_elem: minidom.Element = OsmInterface._parse_raw_response(raw_response)
                if xml_elem.tagName == 'osm':
                    continue  # Success - Check next server URL
                else:
                    return False  # Server down
        except requests.exceptions.ConnectionError:
            print(f'At least one OSM server is down')
            return False
        except Exception as e:
            print("An exception occurred while checking if OSM servers are running")
            print(e.args)
            return False

        return True

    @staticmethod
    def get_administrative_divisions_by_coordinates(coordinates: Coordinates, country: str = None) -> dict[Union[str, int], str]:
        """
        Given a set of coordinates and optionally the respective country, returns a dictionary mapping administrative divisions numbers or keys
            to the respective values, when available
        While most administrative divisions to be found will be associated to a number between 1 (higher level) to 11 (lower level),
            some may instead be associated to a string key, such as the Portuguese historic parish
        :param coordinates: Coordinates of the desired point
        :param country: Should be provided when called by routine determining country by coordinates. For calls from other routines,
            parameter is determined automatically and does not need to be provided. This occurs because for locations close to borders,
            they can be present as well in the maps of the neighbor country or countries, although with less info.
        """
        assert coordinates

        query: str = f'is_in({coordinates.latitude},{coordinates.longitude}); out geom;'
        if not country:
            country: str = OsmInterface.detect_country_by_coordinates(coordinates)
        if not country:
            return {}

        raw_result: minidom.Element = OsmInterface._query_server(query, country)
        if not raw_result:
            return {}

        response: dict[Union[str, int], str] = {}
        for node in raw_result.childNodes:
            if node.nodeName == 'area':  # Administrative division found
                key: Optional[Union[str, int]] = None
                name: Optional[str] = None
                for sub_node in node.childNodes:
                    if sub_node.nodeName == 'tag':
                        # Gets the key
                        if sub_node.hasAttribute('k') and sub_node.getAttribute('k') == 'admin_level':  # Division level found - Expected to be between 1 and 11
                            key = sub_node.getAttribute('v')
                        elif sub_node.hasAttribute('k') and sub_node.getAttribute('k') in [  # Level was not found, but string key was (ex: Portuguese historic parishes)
                                'political_division', 'border_type', 'boundary'] and not key:
                            key = sub_node.getAttribute('v')
                        # Gets the value
                        elif sub_node.hasAttribute('k') and sub_node.getAttribute('k') == 'name':  # Name of the administrative division
                            name = sub_node.getAttribute('v')
                if key and name:
                    try:
                        key = int(key)
                    except:  # Not an int. Ex: 'historic_parish'
                        pass
                    response[key] = name

        return dict(sorted(response.items(), key=lambda item: str(item[0])))  # Sorts answer by key

    @staticmethod
    def get_road_exits(road_name: str, country: str) -> dict[str, list[Coordinates]]:
        """
        Given the name of a road and the respective country, returns the road exits and respective coordinates
        This routine is expected to be called mainly for freeways (EN-UK: motorways) and highways
        """
        assert road_name
        assert country in ways.ALL_SUPPORTED_COUNTRIES

        # This query returns OSM relations as well as OSM ways matching the name of the road
        desired_node_type = 'motorway_junction'
        query = f'rel[name="{road_name}"];' \
                f'way(r)->.w1;' \
                f'way[name="{road_name}"]->.w2;' \
                f'(node(w.w1);' \
                f'node(w.w2);)->.n1;' \
                f'node.n1[highway={desired_node_type}];' \
                f'out geom;'

        raw_result: minidom.Element = OsmInterface._query_server(query, country)
        if not raw_result:
            return {}

        response: dict[str, list[Coordinates]] = {}
        for node in raw_result.childNodes:
            if node.nodeName == 'node':
                coordinates: Coordinates = Coordinates(float(node.getAttribute('lat')), float(node.getAttribute('lon')))
                exit_id: Optional[str] = None
                for n in node.childNodes:
                    if n.nodeName == 'tag':
                        if n.hasAttribute('k') and n.getAttribute('k') == 'ref':  # Exit has an ID
                            exit_id = n.getAttribute('v')
                if exit_id:
                    if exit_id not in response:
                        response[exit_id] = []
                    response[exit_id].append(coordinates)

        if not response:
            if OsmInterface.test_connections():
                print("The provided road does not have exits with IDs - Is it a freeway/motorway or a highway?")
            return {}

        return dict(sorted(response.items(), key=lambda item: item[0]))  # Sorts response by the exit ID

    @staticmethod
    def get_railway_stations(railway_name: str, country: str) -> dict[str, list[Coordinates]]:
        """
        Given the name of a railway and the respective country, returns the railway stations and the respective coordinates
        """
        assert railway_name
        assert country in ways.ALL_SUPPORTED_COUNTRIES

        # This query gets both the OSM relations and the OSM ways matching the name of the railway
        query = f'rel[name="{railway_name}"];' \
                f'way(r)->.w1;' \
                f'way[name="{railway_name}"]->.w2;' \
                f'(node(w.w1);' \
                f'node(w.w2);)->.n1;' \
                f'node.n1[name];' \
                f'out geom;'

        raw_result: minidom.Element = OsmInterface._query_server(query, country)
        if not raw_result:
            return {}

        response: dict[str, list[Coordinates]] = {}
        for node in raw_result.childNodes:
            if node.nodeName == 'node':
                coordinates: Coordinates = Coordinates(float(node.getAttribute('lat')), float(node.getAttribute('lon')))
                station_name: Optional[str] = None
                for n in node.childNodes:
                    if n.nodeName == 'tag':
                        if n.hasAttribute('k') and n.getAttribute('k') == 'name':  # Node has a name - Likely it is a station
                            station_name = n.getAttribute('v')
                if station_name:
                    if station_name not in response:
                        response[station_name] = []
                    response[station_name].append(coordinates)

        if not response:
            if OsmInterface.test_connections():
                print("No stations were found for the provided line name")
            return {}

        return response

    @staticmethod
    def process_area_for_distance_calculation(coordinate_list: list[Coordinates], way_type: str, detail: int,
                                              country: str, include_margin: bool = True) -> tuple[dict[int, OsmNode], dict[int, OsmWay], list[float]]:
        """
        Returns Node and Way objects to be used in the calculation of distances inside a certain rectangular area
        :param coordinate_list: List of coordinates that delimit the desired area
        :param way_type: What type of way should be considered: road or railways?
        :param detail: Only taken into account if way type is roads. The more detail, the more road types will be processed
        :param country: Country where the area to cover belongs. Determines the server to where requests will be sent
        :param include_margin: If True, a margin is added to the provided coordinates. If False, the coordinates will delimit the area to process
        :return List of Node objects, list of Way objects, and min and max latitude and longitude of the area to cover
        """
        assert coordinate_list
        assert way_type in ways.ALL_WAY_TYPES
        assert detail in ALL_DETAIL_LEVELS
        assert country in ways.ALL_SUPPORTED_COUNTRIES

        tags: list[str] = TAGS_DESIRED_ROADS[detail]

        min_latitude: float = 90.0
        max_latitude: float = -90.0
        min_longitude: float = 180.0
        max_longitude: float = -180.0

        # Calculates the extreme points of the rectangular area
        for coordinates in coordinate_list:
            latitude: float = coordinates.latitude
            longitude: float = coordinates.longitude
            if latitude < min_latitude:
                min_latitude = latitude
            if latitude > max_latitude:
                max_latitude = latitude
            if longitude < min_longitude:
                min_longitude = longitude
            if longitude > max_longitude:
                max_longitude = longitude

        # Adds a margin to the rectangular area, in decimal degrees
        if include_margin:
            min_latitude -= DISTANCE_RECTANGLE_MARGIN
            max_latitude += DISTANCE_RECTANGLE_MARGIN
            min_longitude -= DISTANCE_RECTANGLE_MARGIN
            max_longitude += DISTANCE_RECTANGLE_MARGIN

        area_extreme_coordinates: list[float] = [min_latitude, max_latitude, min_longitude, max_longitude]

        if way_type == ways.ROAD:  # All roads tagged with the desired tags in the intended area
            query = f'[bbox:{min_latitude},{min_longitude},{max_latitude},{max_longitude}];' \
                    '('
            for tag in tags:
                query += f'rel[highway={tag}];'
            query += ')->.r1;' \
                     f'(way(r.r1);'
            for tag in tags:
                query += f'way[highway={tag}];'
            query += ');' \
                     'out geom;'
        elif way_type == ways.RAILWAY:  # All railways in the intended area
            query = 'rel[railway]->.r1;' \
                    '(way(r.r1);' \
                    'way[railway];);' \
                    'out geom;'
        else:
            return {}, {}, []

        raw_result: minidom.Element = OsmInterface._query_server(query, country)
        if not raw_result:
            return {}, {}, []

        node_list: dict[int, OsmNode] = {}
        way_list: dict[int, OsmWay] = {}
        for node in raw_result.childNodes:
            if node.nodeName == 'way' and node.hasAttribute('id'):
                way_id: int = int(node.getAttribute('id'))
                way_nodes_list: list[OsmNode] = []
                for n2 in node.childNodes:
                    if n2.nodeName == 'nd' and n2.hasAttribute('ref') and n2.hasAttribute('lat') and n2.hasAttribute('lon'):
                        node_id: int = int(n2.getAttribute('ref'))
                        lat: float = float(n2.getAttribute('lat'))
                        lon: float = float(n2.getAttribute('lon'))
                        way_nodes_list.append(OsmNode(node_id, lat, lon))
                        node_list[node_id] = OsmNode(node_id, lat, lon)
                if way_nodes_list:
                    way_list[way_id] = OsmWay(way_id, way_nodes_list)

        if not node_list or not way_list:
            if OsmInterface.test_connections():
                print("No OSM relations or OSM ways were found for the provided road or railway")
            return {}, {}, []

        return node_list, way_list, area_extreme_coordinates

    @staticmethod
    def process_way_for_distance_calculation(way_name: str, country: str) -> tuple[dict[int, OsmNode], dict[int, OsmWay]]:
        """
        Given the OSM name of a road or a railway, returns Node and Way objects to be used to calculate distances inside
            that road or railway
        """
        assert way_name
        assert country in ways.ALL_SUPPORTED_COUNTRIES

        query = f'rel[name="{way_name}"]->.r1;' \
                f'(way(r.r1);' \
                f'way[name="{way_name}"];);' \
                'out geom;'

        raw_result: minidom.Element = OsmInterface._query_server(query, country)
        if not raw_result:
            return {}, {}

        node_list: dict[int, OsmNode] = {}
        way_list: dict[int, OsmWay] = {}
        for node in raw_result.childNodes:
            if node.nodeName == 'way' and node.hasAttribute('id'):
                way_id: int = int(node.getAttribute('id'))
                way_node_list: list[OsmNode] = []
                for n2 in node.childNodes:
                    if n2.nodeName == 'nd' and n2.hasAttribute('ref') and n2.hasAttribute('lat') and n2.hasAttribute('lon'):
                        node_id: int = int(n2.getAttribute('ref'))
                        lat: float = float(n2.getAttribute('lat'))
                        lon: float = float(n2.getAttribute('lon'))
                        way_node_list.append(OsmNode(node_id, lat, lon))
                        node_list[node_id] = OsmNode(node_id, lat, lon)
                if way_node_list:
                    way_list[way_id] = OsmWay(way_id, way_node_list)

        if not node_list or not way_list:
            if OsmInterface.test_connections():
                print("No OSM relations or OSM ways were found for the provided road or railway")
            return {}, {}

        return node_list, way_list

    @staticmethod
    def detect_country_by_coordinates(coordinates: Coordinates) -> Optional[str]:
        """
        Automatically detects the country, based on the returns for requests sent to the existing servers
        :return: Country name if it could be determined, None otherwise
        """
        assert coordinates

        for server_country in ways.ALL_SUPPORTED_COUNTRIES:  # Canary Islands appear as a separate country, due to having a dedicated server, although they are part of Spain
            admin_divisions: dict[Union[str, int], str] = OsmInterface.get_administrative_divisions_by_coordinates(coordinates, server_country)

            if admin_divisions.get(COUNTRY):  # Expected to cover Portugal, Andorra, and Gibraltar
                country: str = admin_divisions[COUNTRY]
                if country == 'Portugal':
                    return ways.PORTUGAL
                elif country == 'Andorra':
                    return ways.ANDORRA
                elif country == 'Gibraltar':
                    return ways.GIBRALTAR
                elif country in ['Spain', 'España']:
                    if admin_divisions.get(AUTONOMOUS_COMMUNITY) == 'Canarias':
                        return ways.CANARY_ISLANDS
                    else:
                        return ways.SPAIN
                else:  # Unsupported country
                    return None

            elif admin_divisions.get(AUTONOMOUS_COMMUNITY):  # Expected to cover Spain
                autonomous_community: str = admin_divisions[AUTONOMOUS_COMMUNITY]

                if autonomous_community not in ['Azores', 'Madeira', 'Gibraltar']:  # Admin level is also used in Portugal and Gibraltar
                    if admin_divisions.get(AUTONOMOUS_COMMUNITY) == 'Canarias':
                        return ways.CANARY_ISLANDS
                    else:
                        return ways.SPAIN
        else:
            return None

    @staticmethod
    def get_region_extreme_points(name: str, admin_level: int, country: str) -> Optional[ExtremePoints]:
        assert name
        assert 1 <= admin_level <= 11  # OSM admin levels are between 1 and 11
        assert country in ways.ALL_SUPPORTED_COUNTRIES

        # Historic Portuguese parishes do not have an associated admin level in OSM (used to be level 9 until mid-2021)
        query = f'rel[name="{name}"][admin_level="{admin_level}"];' \
                'out geom;'

        raw_result: minidom.Element = OsmInterface._query_server(query, country)
        if not raw_result:
            print("No results were obtained")
            return None

        max_north: Coordinates = Coordinates(-90.0, 0.0)
        max_south: Coordinates = Coordinates(90.0, 0.0)
        max_west: Coordinates = Coordinates(0.0, 180.0)
        max_east: Coordinates = Coordinates(0.0, -180.0)
        for node in raw_result.childNodes:
            if node.nodeName == 'relation' and node.hasAttribute('id'):  # Desired region
                for n2 in node.childNodes:
                    if n2.nodeName == 'member' and n2.hasAttribute('type') and n2.getAttribute('type') == 'node' and \
                            n2.hasAttribute('lat') and n2.hasAttribute('lon'):  # Node that delimits the region
                        lat = float(n2.getAttribute('lat'))
                        lon = float(n2.getAttribute('lon'))
                        if lat > max_north.latitude:
                            max_north.set_latitude(lat)
                            max_north.set_longitude(lon)
                        if lat < max_south.latitude:
                            max_south.set_latitude(lat)
                            max_south.set_longitude(lon)
                        if lon > max_east.longitude:
                            max_east.set_latitude(lat)
                            max_east.set_longitude(lon)
                        if lon < max_west.longitude:
                            max_west.set_latitude(lat)
                            max_west.set_longitude(lon)
                    elif n2.nodeName == 'member' and n2.hasAttribute('type') and n2.getAttribute('type') == 'way':  # Way that delimits a region
                        for n3 in n2.childNodes:
                            if n3.nodeName == 'nd' and n3.hasAttribute('lat') and n3.hasAttribute('lon'):
                                lat = float(n3.getAttribute('lat'))
                                lon = float(n3.getAttribute('lon'))
                                if lat > max_north.latitude:
                                    max_north.set_latitude(lat)
                                    max_north.set_longitude(lon)
                                if lat < max_south.latitude:
                                    max_south.set_latitude(lat)
                                    max_south.set_longitude(lon)
                                if lon > max_east.longitude:
                                    max_east.set_latitude(lat)
                                    max_east.set_longitude(lon)
                                if lon < max_west.longitude:
                                    max_west.set_latitude(lat)
                                    max_west.set_longitude(lon)

        extreme_points = ExtremePoints(name, admin_level, country, max_north, max_south, max_east, max_west)
        return extreme_points

    @staticmethod
    def _query_server(query: str, country: str) -> Optional[minidom.Element]:
        """
        Base method to send a query to an OSM server and return the parsed response
        :param query: Query string to send to the server
        :param country: Desired country - It is expected that the query applies to a single country
        :return: A Python representation of the response XML on success, None otherwise
        """
        assert query
        assert country in ways.ALL_SUPPORTED_COUNTRIES

        try:
            server_url: str = OsmInterface._get_server_url(country)
            raw_response: str = requests.get(f'{server_url}?data={query}').content.decode()  # An XML encoded as a string
            return OsmInterface._parse_raw_response(raw_response)  # From string to a representation of the response XML

        except requests.exceptions.ConnectionError:
            print(f"Connection with OSM server for country {country} failed to be established - Is server running?")
            return None
        except Exception as e:
            print(f'Error while sending Overpass QL query {query} to OSM server for country {country}')
            print(e)
            return None

    @staticmethod
    def _parse_raw_response(raw_response: str) -> Optional[minidom.Element]:
        """
        Given the raw string response from the OSM servers (always formatted as an XML), returns the essential part of the response
            as a Python XML object
        """
        if raw_response:
            return minidom.parseString(raw_response).childNodes[0]  # Base element - Always delimited by <osm> </osm>
        else:
            return None

    @staticmethod
    def _get_server_url(country: str) -> Optional[str]:
        """
        Given a target country, returns the full OSM server URL, or None if country is unsupported
        """
        if country == ways.ANDORRA:
            port: int = PORT_ANDORRA
        elif country == ways.CANARY_ISLANDS:
            port: int = PORT_CANARY_ISLANDS  # Part of Spain, in different server
        elif country in [ways.GIBRALTAR, ways.SPAIN]:  # Spain and Gibraltar maps are in the same server - Please note that it does not include Canary Islands
            port: int = PORT_GIBRALTAR_SPAIN
        elif country == ways.PORTUGAL:
            port: int = PORT_PORTUGAL
        else:  # Unsupported country
            return None

        server_url = f'http://{DOCKER_IP}:{port}/api/interpreter'  # Please change to https if server is remote
        return server_url
