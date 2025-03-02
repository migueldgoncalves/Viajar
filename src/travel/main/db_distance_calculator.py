"""
This script calculates shortest distances according to the Viajar DB.
    It has 2 modes of operation: between 2 locations, and from a starting point.
"""
from typing import Union
import copy

from travel.main import travel, db_interface

DISTANCE_TYPE_KILOMETERS = "distance_type_kilometers"
DISTANCE_TYPE_HOPS = "distance_type_hops"

DISTANCE_CALCULATION_TYPE_A_TO_B = "distance_calculation_a_to_b"
DISTANCE_CALCULATION_TYPE_FROM_A = "distance_calculation_from_a"

INFINITE_DISTANCE = 999999
ROUNDING_NUMBER_OF_DIGITS = 1

# Configuration
START_LOCATION = 'Andorra-Spain Border - Andorran Customs'
END_LOCATION = 'AP-9 - Exit 93'
DISTANCE_TYPE = DISTANCE_TYPE_HOPS
DISTANCE_CALCULATION_TYPE = DISTANCE_CALCULATION_TYPE_FROM_A
MEANS_OF_TRANSPORT = travel.CAR
DESTINATIONS_TO_PRINT = 10

# # # # # # # # # # # #
# Auxiliary routines #
# # # # # # # # # # # #

def _check_parameter_validity(start_location: str, end_location: str, distance_type: str, means_of_transport: Union[str, list[str]]) -> None:
    if not start_location:
        raise Exception("Start location was not provided or is empty")

    # The end location is optional, depending on the desired distance calculation type

    if distance_type not in [DISTANCE_TYPE_KILOMETERS, DISTANCE_TYPE_HOPS]:
        raise Exception(f"Invalid distance type provided: {distance_type}")

    if not means_of_transport:
        raise Exception("No means of transport were provided")
    if type(means_of_transport) == str:
        means_of_transport = [means_of_transport]
    valid_means_of_transport: list[str] = []
    for transport in means_of_transport:
        if transport in travel.ALL_MEANS_TRANSPORT:
            valid_means_of_transport.append(transport)
    if not valid_means_of_transport:
        raise Exception(f"All provided means of transport were invalid. Provided: {means_of_transport}")

def _get_processed_map(means_of_transport: list[str]) -> dict[str, dict[str, float]]:
    db: db_interface.DBInterface = db_interface.DBInterface()
    db.create_and_populate_travel_db()

    connections_info = db.get_all_connections_for_distance_calculation(means_of_transport)

    db.exit()

    return_value: dict[str, dict[str, float]] = {}
    for connection in connections_info:
        location_a: str = connection[0]
        location_b: str = connection[1]
        distance: float = connection[2]

        if location_a not in return_value:
            return_value[location_a] = {}
        if location_b not in return_value:
            return_value[location_b] = {}

        return_value[location_a][location_b] = distance
        return_value[location_b][location_a] = distance

    return return_value

# # # # # # # # #
# Main routines #
# # # # # # # # #

def _get_shortest_distances(start_location: str, end_location: str, distance_type: str, means_of_transport: Union[str, list[str]]) -> tuple[dict[tuple[float, int], str], list[str]]:
    _check_parameter_validity(start_location, end_location, distance_type, means_of_transport)
    if type(means_of_transport) == str:
        means_of_transport = [means_of_transport]

    processed_map: dict[str, dict[str, float]] = _get_processed_map(means_of_transport)

    # Dijkstra's algorithm

    unvisited_locations: set[str] = set(processed_map.keys())

    distances: dict[str, Union[int, float]] = {location_name: INFINITE_DISTANCE for location_name in processed_map}
    distances[start_location] = 0
    distances_other_distance_type: dict[str, Union[int, float]] = {location_name: INFINITE_DISTANCE for location_name in processed_map}  # Ex: If the user has requested distances by kilometers, this dictionary keeps distances by hops
    distances_other_distance_type[start_location] = 0

    shortest_routes: dict[str, list[str]] = {start_location: [start_location]}

    while True:
        current_location: str = ''

        if not unvisited_locations or (end_location and end_location == current_location):
            break  # Reached the end of the algorithm

        # Get from the unvisited locations the location that is closer to the starting point
        minimum_distance_to_start: Union[float, int] = INFINITE_DISTANCE
        for location in unvisited_locations:
            distance: float = distances[location]
            if distance < minimum_distance_to_start:
                minimum_distance_to_start = distance
                current_location = location

        if not current_location:  # No more locations are reachable - End of algorithm
            break

        # Visit the unvisited neighbors of the current location
        for neighbor in processed_map[current_location]:
            if neighbor in unvisited_locations:
                if distance_type == DISTANCE_TYPE_KILOMETERS:
                    distance_from_current_to_neighbor: Union[int, float] = processed_map[current_location][neighbor]
                    other_distance_from_current_to_neighbor: Union[int, float] = 1
                else:  # Distance by hops. As the two locations are adjacent, this is a single hop
                    distance_from_current_to_neighbor: Union[int, float] = 1
                    other_distance_from_current_to_neighbor: Union[int, float] = processed_map[current_location][neighbor]
                distance_to_current_location: Union[int, float] = distances[current_location]
                other_distance_to_current_location: Union[int, float] = distances_other_distance_type[current_location]

                distance_through_current_location: Union[int, float] = round(distance_to_current_location + distance_from_current_to_neighbor, ROUNDING_NUMBER_OF_DIGITS)
                other_distance_through_current_location: Union[int, float] = round(other_distance_to_current_location + other_distance_from_current_to_neighbor, ROUNDING_NUMBER_OF_DIGITS)  # Prevents numbers such as 1487.900000000001. See https://www.reddit.com/r/learnpython/comments/nsa4iy/sum_of_two_float_results_in_00000000001_extra/
                known_shortest_distance: Union[int, float] = distances[neighbor]

                if distance_through_current_location < known_shortest_distance:
                    distances[neighbor] = distance_through_current_location
                    distances_other_distance_type[neighbor] = other_distance_through_current_location

                    if neighbor not in shortest_routes:
                        shortest_routes[neighbor] = []
                    shortest_routes[neighbor] = copy.deepcopy(shortest_routes[current_location])
                    shortest_routes[neighbor].append(neighbor)

        unvisited_locations.remove(current_location)

    # Generates the first element of the return value. First comes the distance by kilometers, then the distance by hops
    # TODO - Fix use case where two locations have the same number of kilometers and hops - One of them will be overwritten
    if distance_type == DISTANCE_TYPE_KILOMETERS:
        distances_to_return: dict[tuple[float, int], str] = {
            (distances[location], distances_other_distance_type[location]): location for location in distances if location != start_location
        }  # Locations indexed by their distances
    else:
        distances_to_return: dict[tuple[float, int], str] = {
            (distances_other_distance_type[location], distances[location]): location for location in distances if location != start_location
        }  # Locations indexed by their distances

    if end_location:
        return distances_to_return, shortest_routes[end_location]
    else:
        return distances_to_return, []

def get_shortest_distance_between_locations(start_location: str, end_location: str, distance_type: str, means_of_transport: Union[str, list[str]]) -> tuple[float, int]:
    def print_route_description(route: list[str]) -> None:
        print(f'The shortest route is:')
        print('Start')
        for i in range(len(route)):
            print(f'{i}. {route[i]}')
        print('End')

    if not end_location:
        raise Exception("No end location was provided")

    distances, route_description = _get_shortest_distances(start_location, end_location, distance_type, means_of_transport)

    for distance_tuple in distances:  # Example: {(1.2, 1): "Laranjeiras", (2.0, 2): "Montinho das Laranjeiras", (8.0, 3): "Alcoutim", ...}
        if distances[distance_tuple] == end_location:
            print_route_description(route_description)
            return distance_tuple
    else:  # for-else - Destination was not reached
        return INFINITE_DISTANCE, INFINITE_DISTANCE

def get_shortest_distances_from_location(start_location: str, distance_type: str, means_of_transport: Union[str, list[str]]) -> dict[tuple[float, int], str]:
    return _get_shortest_distances(start_location, "", distance_type, means_of_transport)[0]

def main():
    def on_distance_calculation_type_a_to_b():
        distance_in_kilometers, distance_in_hops = get_shortest_distance_between_locations(
            start_location=START_LOCATION,
            end_location=END_LOCATION,
            distance_type=DISTANCE_TYPE,
            means_of_transport=MEANS_OF_TRANSPORT
        )

        if distance_in_kilometers == INFINITE_DISTANCE:  # Error - Failed to find distance
            print(f'Could not find distance from {START_LOCATION} to {END_LOCATION}, using the following means of transport: {MEANS_OF_TRANSPORT}')
        else:  # Success
            print(f"Distance from {START_LOCATION} to {END_LOCATION}: {distance_in_kilometers} kilometers and {distance_in_hops} hops. Means of transport taken into account: {MEANS_OF_TRANSPORT}")

    def on_distance_calculation_type_from_a():
        distances: dict[tuple[float, int], str] = get_shortest_distances_from_location(
            start_location=START_LOCATION,
            distance_type=DISTANCE_TYPE,
            means_of_transport=MEANS_OF_TRANSPORT
        )  # Example: {(1.2, 1): "Laranjeiras", (2.0, 2): "Montinho das Laranjeiras", (8.0, 3): "Alcoutim", ...}

        if DISTANCE_TYPE == DISTANCE_TYPE_KILOMETERS:  # Distance in kilometers is the first element in the tuple
            distance_tuples: list[tuple[float, int]] = sorted(distances)  # Returns a list with the sorted keys
        elif DISTANCE_TYPE == DISTANCE_TYPE_HOPS:  # Distance in hops is the second element in the tuple
            distance_tuples: list[tuple[float, int]] = sorted(distances, key=lambda tup: tup[1])
        else:
            print("Error - Invalid distance type. Aborting.")
            exit(1)

        if not distance_tuples:  # Error
            print(f'No distances found from location {START_LOCATION} using means of transport: {MEANS_OF_TRANSPORT}')
            exit(0)

        # Prints the closest locations
        for i in range(int(DESTINATIONS_TO_PRINT / 2)):
            if i >= len(distances):
                print("No more destinations found")
                break

            distance_tuple: tuple[float, int] = distance_tuples[i]
            distance_in_kilometers = distance_tuple[0]
            distance_in_hops = distance_tuple[1]
            location_name: str = distances[distance_tuple]
            print(f"Distance from {START_LOCATION} to {location_name}: {distance_in_kilometers} kilometers and {distance_in_hops} hops")

        print("...")

        # Prints the furthest locations
        for i in range(int(DESTINATIONS_TO_PRINT / 2)):
            j = i + len(distances) - 1 - int(DESTINATIONS_TO_PRINT / 2)
            if j >= len(distances):
                print("No more destinations found")
                break

            distance_tuple: tuple[float, int] = distance_tuples[j]
            distance_in_kilometers = distance_tuple[0]
            distance_in_hops = distance_tuple[1]
            location_name: str = distances[distance_tuple]
            print(f"Distance from {START_LOCATION} to {location_name}: {distance_in_kilometers} kilometers and {distance_in_hops} hops")

    if DISTANCE_CALCULATION_TYPE == DISTANCE_CALCULATION_TYPE_A_TO_B:
        on_distance_calculation_type_a_to_b()
    elif DISTANCE_CALCULATION_TYPE == DISTANCE_CALCULATION_TYPE_FROM_A:
        on_distance_calculation_type_from_a()
    else:
        print("Error - Invalid distance calculation type. Aborting.")
        exit(1)
