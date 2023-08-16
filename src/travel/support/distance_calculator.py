import travel.support.haversine as haversine
import travel.support.osm_interface as osm_interface
from travel.support.coordinates import Coordinates
from travel.support import ways

"""
This module calculates distances by road and rail between two points
It support 3 operation modes:
    -Distances inside the same road or railway
    -Distances inside a certain area, taking into account the most important roads
    -Distances inside a certain urban area, taking into account more types of streets and roads
"""

WARNING_AREA_SIZE_INTERCITY = 100 ** 2  # Will print warning if area to cover is larger than 100 x 100 km
WARNING_AREA_SIZE_URBAN = 10 ** 2

INFINITE_DISTANCE = 999999  # km

# Adjust to coordinates, to help find the shortest distance
COORDINATE_ADJUST = 0.0005  # 0.001 decimal degrees = very approximately 100 meters in the Iberian Peninsula


class DistanceCalculator:
    """
    Main class for distance calculation
    How to use:
        First, generate the processed map OR processed road/railway with the desired name
        Then, execute the Dijkstra's algorithm for as many pairs (source, destination) as desired
    """
    def __init__(self) -> None:
        self.processed_map: dict[int, osm_interface.OsmNode] = {}

    def generate_processed_map(self, coordinate_list: list[Coordinates], way_type: str, country: str,
                               area_detail: int = None, way_name: str = None) -> None:
        """
        Creates a map containing all provided coordinates, suitable for execution of Dijkstra's algorithm
        The resulting map is added to the class instance variables, instead of being returned
        :param coordinate_list: Coordinates to include in the map
        :param way_type: What type of way should be considered: road or railway? Only one type of way will be considered
        :param country: Country of the area or way to process. Only one country at a time is supported
        :param area_detail: Optional - Level of detail of the area to cover. Only considered if way type is roads
            The more detail, the more road types are considered:
                A high level of detail allows to cover streets inside the same city. It should only be used for areas
                    with a size up to a few square kilometers, or processing will be very slow
                With a lower level of detail, only the main roads are covered
            Area detail is not considered for railways (they are always far fewer than roads), or if the way name is provided
            Should be provided if way_name is not provided
        :param way_name: Optional - OSM way name (Ex: "Autoestrada do Norte" - North freeway/motorway).
            If provided, only that way will be considered
            Provide the desired way name, if the goal is to cover a single road or railway
            Should be provided if area_detail is not provided
        :return:
        """
        assert coordinate_list and len(coordinate_list) > 1
        assert way_type in ways.ALL_WAY_TYPES
        assert country in ways.ALL_SUPPORTED_COUNTRIES
        assert way_name or (area_detail in osm_interface.ALL_DETAIL_LEVELS)  # One of the two must be provided

        print("Getting area representation...")

        if area_detail:  # The objective is to cover an area
            node_list, ways_to_consider, area_extreme_points = osm_interface.OsmInterface.process_area_for_distance_calculation(
                coordinate_list, way_type, area_detail, country)

            min_latitude: float = area_extreme_points[0]
            max_latitude: float = area_extreme_points[1]
            min_longitude: float = area_extreme_points[2]
            max_longitude: float = area_extreme_points[3]

            digits = 1
            north_south_distance = round(
                haversine.get_haversine_distance(Coordinates(min_latitude, min_longitude), Coordinates(max_latitude, min_longitude)), digits)
            east_west_distance = round(
                haversine.get_haversine_distance(Coordinates(min_latitude, min_longitude), Coordinates(min_latitude, max_longitude)), digits)
            print(f"The area of interest has {north_south_distance} km from north to south and {east_west_distance} km from east to west")

            if area_detail == osm_interface.DETAIL_LEVEL_INTERCITY and north_south_distance * east_west_distance > WARNING_AREA_SIZE_INTERCITY or \
                    area_detail == osm_interface.DETAIL_LEVEL_URBAN and north_south_distance * east_west_distance > WARNING_AREA_SIZE_URBAN:
                print("Warning: The area to cover is very large - This operation can take a very long time")

            # As soon as the surrounding nodes info is received, there will be all the required info to run the Dijkstra's algorith
            self.processed_map: dict[int, osm_interface.OsmNode] = node_list  # Does not have surrounding nodes info yet

        else:  # The objective is to cover an individual road or railway

            # As soon as the surrounding nodes info is received, there will be all the required info to run the Dijkstra's algorith
            return_value: tuple[dict[int, osm_interface.OsmNode], dict[int, osm_interface.OsmWay]] = \
                osm_interface.OsmInterface.process_way_for_distance_calculation(way_name, country)

            self.processed_map: dict[int, osm_interface.OsmNode] = return_value[0]  # Does not have surrounding nodes info yet
            ways_to_consider: dict[int, osm_interface.OsmWay] = return_value[1]

            # In this case, extreme points are not going to be considered
            min_latitude: float = -90.0
            max_latitude: float = 90.0
            min_longitude: float = -180.0
            max_longitude: float = 180.0

        # Add surrounding nodes
        print("Adding surrounding nodes info...")
        for way_id in ways_to_consider:
            way: osm_interface.OsmWay = ways_to_consider[way_id]

            if len(way.node_list) <= 1:  # Way with no nodes - Ignore
                continue

            for index, node in enumerate(way.node_list):  # All nodes of the way, whether of not inside the desired rectangular area
                if index == 0:  # First node of the way
                    next_node: osm_interface.OsmNode = way.node_list[1]
                    if (min_latitude <= next_node.latitude <= max_latitude) and \
                            (min_longitude <= next_node.longitude <= max_longitude):  # Surrounding node is inside the desired rectangle
                        if self.processed_map.get(node.node_id, None):
                            self.processed_map[node.node_id].surrounding_node_ids.add(next_node.node_id)

                elif index == len(way.node_list) - 1:  # Last node of the way
                    previous_node: osm_interface.OsmNode = way.node_list[index - 1]
                    if (min_latitude <= previous_node.latitude <= max_latitude) and \
                            (min_longitude <= previous_node.longitude <= max_longitude):  # Surrounding node is inside the desired rectangle
                        if self.processed_map.get(node.node_id, None):
                            self.processed_map[node.node_id].surrounding_node_ids.add(previous_node.node_id)

                else:  # Node is somewhere in the way, not at the start, not at the end
                    next_node: osm_interface.OsmNode = way.node_list[index + 1]
                    if (min_latitude <= next_node.latitude <= max_latitude) and \
                            (min_longitude <= next_node.longitude <= max_longitude):  # Surrounding node is inside the desired rectangle
                        if self.processed_map.get(node.node_id, None):
                            self.processed_map[node.node_id].surrounding_node_ids.add(next_node.node_id)
                    previous_node: osm_interface.OsmNode = way.node_list[index - 1]
                    if (min_latitude <= previous_node.latitude <= max_latitude) and \
                            (min_longitude <= previous_node.longitude <= max_longitude):  # Surrounding node is inside the desired rectangle
                        if self.processed_map.get(node.node_id, None):
                            self.processed_map[node.node_id].surrounding_node_ids.add(previous_node.node_id)

        self.processed_map = {node_id: self.processed_map[node_id] for node_id in self.processed_map if
                              len(self.processed_map[node_id].surrounding_node_ids) > 0}  # Keep only nodes with surrounding nodes

        print("Representation of the area obtained")
        return

    def calculate_distance_with_adjusts(self, source: Coordinates, destination: Coordinates, less_checks=True) -> float:
        """
        Returns the shortest distance obtained after performing a series of distance calculations using similar coordinates.
        Repeats the distance calculation by slightly adjusting the source and destination calculations each time.
            Allows to overcome having two parallel OSM ways in the same freeway/motorway, for example, where the distance
                obtained with the exact provided coordinates can be Infinite or a very large value
        Routine is expected to be mainly used for distance calculation inside the same road or railway
        Requires having processed a map or way beforehand
        :param less_checks: If True, 9 calculations are performed. If False, 81 calculations are performed
        """
        def _calculate_distance_with_adjusts(source_coordinates: Coordinates, destination_coordinates: Coordinates,
                                             adjust_1: float, adjust_2: float, adjust_3: float, adjust_4: float,
                                             verbose=False) -> float:
            """
            Calculates distance between 2 points, with provided coordinate adjusts
            :param adjust_1: Value to add to source latitude, in decimal degrees. Can be negative
            :param adjust_2: Value to add to source longitude, in decimal degrees. Can be negative
            :param adjust_3: Value to add to destination latitude, in decimal degrees. Can be negative
            :param adjust_4: Value to add to destination longitude, in decimal degrees. Can be negative
            """
            # Recalculates coordinates
            source_latitude = source_coordinates.latitude + adjust_1
            source_longitude = source_coordinates.longitude + adjust_2
            destination_latitude = destination_coordinates.latitude + adjust_3
            destination_longitude = destination_coordinates.longitude + adjust_4

            source_coordinates = Coordinates(source_latitude, source_longitude)
            destination_coordinates = Coordinates(destination_latitude, destination_longitude)

            distance_to_return: float = self.calculate_distance(source_coordinates, destination_coordinates, verbose=verbose)
            return distance_to_return

        shortest_distance: float = INFINITE_DISTANCE

        if less_checks:  # 9 calculations - Latitude and longitude of points receive the same adjustments
            for i in [-COORDINATE_ADJUST, 0, COORDINATE_ADJUST]:
                for j in [-COORDINATE_ADJUST, 0, COORDINATE_ADJUST]:
                    distance: float = _calculate_distance_with_adjusts(source, destination, i, i, j, j, verbose=False)
                    if distance < shortest_distance:
                        shortest_distance = distance

        else:  # 81 calculations - Latitude and longitude of points can receive different adjustments
            for i in [-COORDINATE_ADJUST, 0, COORDINATE_ADJUST]:
                for j in [-COORDINATE_ADJUST, 0, COORDINATE_ADJUST]:
                    for k in [-COORDINATE_ADJUST, 0, COORDINATE_ADJUST]:
                        for l in [-COORDINATE_ADJUST, 0, COORDINATE_ADJUST]:
                            distance: float = _calculate_distance_with_adjusts(source, destination, i, j, k, l, verbose=False)
                            if distance < shortest_distance:
                                shortest_distance = distance

        if distance == INFINITE_DISTANCE:
            print(f"Failed to calculate distance between coordinates {str(source)} and {str(destination)}")

        return distance

    def calculate_distance(self, source: Coordinates, destination: Coordinates, verbose: bool = True) -> float:
        """
        Returns the shortest distance by road or rail between two points, using the Dijkstra's algorithm
        Provided points are converted into the closest points belonging to a road or a railway
        Requires having processed a map or a way beforehand
        """
        if not self.processed_map:
            if verbose:
                print("No map has been processed - Unable to calculate distance")
            return 0.0

        source_node_id: int = self._coordinates_to_nearest_node(source).node_id
        destination_node_id: int = self._coordinates_to_nearest_node(destination).node_id

        # Dijkstra's algorithm

        nodes_yet_to_visit: set[int] = set(self.processed_map.keys())
        distances: dict[int, float] = {node_id: 0 if node_id == source_node_id else INFINITE_DISTANCE for node_id in self.processed_map}  # Distance from node to self is 0
        current_node: int = source_node_id

        while destination_node_id in nodes_yet_to_visit:
            distance_to_node: float = distances[current_node]
            surrounding_nodes: set[int] = self.processed_map[current_node].surrounding_node_ids

            for surrounding_node in surrounding_nodes:
                if surrounding_node not in nodes_yet_to_visit:
                    continue  # Node was already visited - Shortest distance is already known
                current_node_coordinates: Coordinates = Coordinates(
                    self.processed_map[current_node].latitude, self.processed_map[current_node].longitude)
                surrounding_node_coordinates: Coordinates = Coordinates(
                    self.processed_map[surrounding_node].latitude, self.processed_map[surrounding_node].longitude)
                distance_between_nodes: float = haversine.get_haversine_distance(current_node_coordinates, surrounding_node_coordinates)

                if distance_between_nodes + distance_to_node < distances[surrounding_node]:  # Obtained distance is shorter - Update shortest distance to node
                    distances[surrounding_node] = distance_between_nodes + distance_to_node

            nodes_yet_to_visit.remove(current_node)
            if all(distances[node_id] == INFINITE_DISTANCE for node_id in nodes_yet_to_visit) and current_node != source_node_id:
                break  # If at this point all distances to unvisited nodes are still infinite, they are unreachable - End algorithm now

            shortest_known_distance: float = INFINITE_DISTANCE
            for node_id in nodes_yet_to_visit:
                if distances[node_id] < shortest_known_distance:
                    shortest_known_distance = distances[node_id]
                    current_node = node_id

        distance_to_destination: float = round(distances[destination_node_id], 1)  # Note: May not have been found - Will be infinite
        if verbose:
            if distance_to_destination == INFINITE_DISTANCE:
                print("Failed to calculate distance between source and destination")
            else:
                print(f'Distance between source and destination is {distance_to_destination} km')

        return distance_to_destination

    def _coordinates_to_nearest_node(self, coordinates: Coordinates) -> osm_interface.OsmNode:
        """
        Given coordinates, and assuming that map has already been processed, returns the closest map node to the provided coordinates.
        Calculations are approximate - Pythagorean theorem is used instead of Haversine distances for faster execution speeds.
            A degree of longitude in the Iberian Peninsula is approximate, but not the same, as a degree of latitude
        """
        closest_node: osm_interface.OsmNode = osm_interface.OsmNode(0, 0.0, 0.0)  # Safe default - Gulf of Guinea is very far from Iberian Peninsula
        pythagorean_distance: float = INFINITE_DISTANCE
        for node_id in self.processed_map:
            node: osm_interface.OsmNode = self.processed_map[node_id]

            latitude_difference: float = abs(node.latitude - coordinates.latitude)
            longitude_difference: float = abs(node.longitude - coordinates.longitude)
            distance: float = (latitude_difference ** 2 + longitude_difference ** 2) ** 1/2  # c^2 = a^2 + b^2 -> c = sqr(a^2 + b^2)

            if distance < pythagorean_distance:
                closest_node = node
                pythagorean_distance = distance

        return closest_node
