from math import sin, cos, sqrt, asin, pi

from travel.main.cardinal_points import NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH, SOUTHWEST, WEST, NORTHWEST
from travel.support.coordinates import Coordinates

EARTH_RADIUS = 6371  # km

MAX_ERROR_RATE = 0.5  # Percentage


def get_cardinal_point(source: Coordinates, destination: Coordinates) -> str:
    """
    Given source and destination coordinates, returns the cardinal point of the direction from the source to the destination
    Ex: If source == (39.0, 0.0) and destination == (40.0, 0.0), return value will be "N"
    :param source: Coordinates of the starting point
    :param destination: Coordinates of the destination point
    :return: Cardinal point as a string abbreviation, or an empty string if the source and the destination are the same
    """
    default_reply: str = ''

    assert source
    assert destination
    assert source != destination

    north_south_distance: float = get_haversine_distance(
        Coordinates(source.latitude, 0.0), Coordinates(destination.latitude, 0.0))  # Will always be >= 0
    east_west_distance: float = get_haversine_distance(
        Coordinates(0.0, source.longitude), Coordinates(0.0, destination.longitude))  # Will always be >= 0

    diff_lat: float = float(destination.latitude) - float(source.latitude)
    diff_lon: float = float(destination.longitude) - float(source.longitude)

    if diff_lat == 0:
        if diff_lon > 0:
            return EAST
        elif diff_lon < 0:
            return WEST
    elif diff_lon == 0:
        if diff_lat > 0:
            return NORTH
        elif diff_lat < 0:
            return SOUTH
    elif diff_lat == diff_lon:
        if diff_lat > 0 and diff_lon > 0:
            return NORTHEAST
        elif diff_lat < 0 and diff_lon > 0:
            return SOUTHEAST
        elif diff_lat < 0 and diff_lon < 0:
            return SOUTHWEST
        elif diff_lat > 0 and diff_lon < 0:
            return NORTHWEST
    else:
        if diff_lat > 0 and diff_lon > 0:  # N, NE, E
            if abs(north_south_distance) > 2 * abs(east_west_distance):
                return NORTH
            elif abs(north_south_distance) < 0.5 * abs(east_west_distance):
                return EAST
            else:
                return NORTHEAST
        elif diff_lat < 0 and diff_lon > 0:  # E, SE, S
            if abs(north_south_distance) > 2 * abs(east_west_distance):
                return SOUTH
            elif abs(north_south_distance) < 0.5 * abs(east_west_distance):
                return EAST
            else:
                return SOUTHEAST
        elif diff_lat < 0 and diff_lon < 0:  # S, SW, W
            if abs(north_south_distance) > 2 * abs(east_west_distance):
                return SOUTH
            elif abs(north_south_distance) < 0.5 * abs(east_west_distance):
                return WEST
            else:
                return SOUTHWEST
        elif diff_lat > 0 and diff_lon < 0:  # W, NW, N
            if abs(north_south_distance) > 2 * abs(east_west_distance):
                return NORTH
            elif abs(north_south_distance) < 0.5 * abs(east_west_distance):
                return WEST
            else:
                return NORTHWEST

    return default_reply


def get_haversine_distance(source: Coordinates, destination: Coordinates) -> float:
    """
    Returns the distance of a straight line between source and destination points, in km. Error can be up to 0.5%.
    """
    def _to_radians(decimal: float) -> float:
        """
        Converts degrees to radians
        """
        return decimal * pi / 180

    assert source
    assert destination

    if source == destination:  # Same point
        return 0.0

    diff_lat: float = float(destination.latitude) - float(source.latitude)
    diff_lon: float = float(destination.longitude) - float(source.longitude)

    param_1: float = sin(_to_radians(diff_lat / 2)) ** 2
    param_2: float = cos(_to_radians(float(source.latitude))) * cos(_to_radians(float(destination.latitude))) * (
            sin(_to_radians(diff_lon / 2)) ** 2)
    distance: float = 2 * EARTH_RADIUS * asin(sqrt(param_1 + param_2))

    return distance
