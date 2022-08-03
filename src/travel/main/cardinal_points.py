"""
Wrapper module for cardinal point constants and utils
"""

NORTH = "N"
NORTHEAST = "NE"
EAST = "E"
SOUTHEAST = "SE"
SOUTH = "S"
SOUTHWEST = "SW"
WEST = "W"
NORTHWEST = "NW"


def get_opposite_cardinal_point(cardinal_point: str) -> str:
    if cardinal_point == NORTH:
        return SOUTH
    elif cardinal_point == NORTHEAST:
        return SOUTHWEST
    elif cardinal_point == EAST:
        return WEST
    elif cardinal_point == SOUTHEAST:
        return NORTHWEST
    elif cardinal_point == SOUTH:
        return NORTH
    elif cardinal_point == SOUTHWEST:
        return NORTHEAST
    elif cardinal_point == WEST:
        return EAST
    elif cardinal_point == NORTHWEST:
        return SOUTHEAST
    else:
        return ''
