from __future__ import annotations
from typing import Optional

DESTINATIONS_SEPARATOR = "/"


class Location:
    """
    Class representing a generic location, with data common to every location
    """

    def __init__(self, name: str, connections: dict[tuple[str, str], tuple[str, float, str]], latitude: float,
                 longitude: float, altitude: int):
        self.name: str = name
        self.connections: dict[tuple[str, str], tuple[str, float, str]] = connections
        # Main destinations available from this location. Ex: Beja/Mértola and Castro Marim/Vila Real de Santo António in IC27
        self.destinations: dict[tuple[str, str], list[str]] = {}
        # Available ways from this location. Ex: Lisbon Metro - Red Line, North Line - Regional, A1, AP-6
        self.ways: dict[tuple[str, str], str] = {}
        self.coordinates: tuple[float, float] = (latitude, longitude)  # Ex: (37.215788, -7.405922)
        self.altitude: int = altitude  # Meters
        self.country: str = ''
        self.protected_area: str = ''
        self.island: str = ''
        self.batch: int = 0  # 100 = Location is part of the first 100 locations that were introduced

    def set_name(self, name: str) -> None:
        self.name = name

    def set_connections(self, connections: dict[tuple[str, str], tuple[str, float, str]]) -> None:
        self.connections = connections

    def set_destinations(self, destinations: dict[tuple[str, str], list[str]]) -> None:
        self.destinations = destinations

    def set_ways(self, ways: dict[tuple[str, str], str]) -> None:
        self.ways = ways

    def set_coordinates(self, latitude: float, longitude: float) -> None:
        self.coordinates = (latitude, longitude)

    def set_altitude(self, altitude: int) -> None:
        self.altitude = altitude

    def set_country(self, country: str) -> None:
        self.country = country

    def set_protected_area(self, protected_area: str) -> None:
        self.protected_area = protected_area

    def set_island(self, island: str) -> None:
        self.island = island

    def set_batch(self, batch: int) -> None:
        self.batch = batch

    def add_connection(self, surrounding_location: str, means_transport: str, cardinal_point: str, distance: float) -> None:
        self.connections[(surrounding_location, means_transport)] = (cardinal_point, distance, means_transport)

    def add_way(self, surrounding_location: str, means_transport: str, way: str) -> None:
        self.ways[(surrounding_location, means_transport)] = way

    def add_destination(self, destination: str, surrounding_location: str, means_transport: str, way: str) -> None:
        if not (surrounding_location, means_transport) in self.destinations:
            self.destinations[(surrounding_location, means_transport)] = []
        elif destination in self.destinations[(surrounding_location, means_transport)]:
            return
        self.destinations[(surrounding_location, means_transport)].append(destination)
        self.add_way(surrounding_location, means_transport, way)

    def remove_connection(self, surrounding_location: str, means_transport: str) -> None:
        if (surrounding_location, means_transport) in self.connections:
            del self.connections[(surrounding_location, means_transport)]

    def remove_destinations_from_connection(self, surrounding_location: str, means_transport: str) -> None:
        if (surrounding_location, means_transport) in self.destinations:
            del self.destinations[(surrounding_location, means_transport)]

    def remove_way(self, surrounding_location: str, means_transport: str) -> None:
        if (surrounding_location, means_transport) in self.ways:
            del self.ways[(surrounding_location, means_transport)]

    def get_name(self) -> str:
        return self.name

    def get_connections(self) -> dict[tuple[str, str], tuple[str, float, str]]:
        return self.connections

    def get_destinations(self) -> dict[tuple[str, str], list[str]]:
        return self.destinations

    def get_ways(self) -> dict[tuple[str, str], str]:
        return self.ways

    def get_way(self, surrounding_location: str, means_transport: str) -> Optional[str]:
        return self.ways.get((surrounding_location, means_transport), None)

    def get_destinations_as_string(self, surrounding_location: str, means_transport: str) -> Optional[str]:
        """
        If there are no destinations, return is None
        If there is 1 destination, return is that destination
        If there are 3 destinations "Santarém", "Coimbra" and "Porto", return is "Santarém / Coimbra / Porto"
        """
        if (surrounding_location, means_transport) in self.destinations:
            destinations: list[str] = self.destinations[(surrounding_location, means_transport)]
            if len(destinations) == 1:
                return destinations[0]
            destinations_string: str = ''
            for destination in destinations:
                destinations_string = f'{destinations_string} {DESTINATIONS_SEPARATOR} {destination}'
            return destinations_string[3:]  # Removes first chars
        return None

    def get_cardinal_point(self, surrounding_location: str, means_transport: str) -> Optional[str]:
        connection: Optional[tuple[str, float, str]] = self.connections.get((surrounding_location, means_transport), None)
        if connection:
            return connection[0]
        else:
            return None

    def get_distance(self, surrounding_location: str, means_transport: str) -> Optional[float]:
        connection: Optional[tuple[str, float, str]] = self.connections.get((surrounding_location, means_transport), None)
        if connection:
            return connection[1]
        else:
            return None

    def get_coordinates(self) -> tuple[float, float]:
        return self.coordinates

    def get_latitude(self) -> float:
        return self.get_coordinates()[0]

    def get_longitude(self) -> float:
        return self.get_coordinates()[1]

    def get_altitude(self) -> int:
        return self.altitude

    def get_country(self) -> str:
        return self.country

    def get_protected_area(self) -> str:
        return self.protected_area

    def get_island(self) -> str:
        return self.island

    def get_batch(self) -> int:
        return self.batch

    def print_info_brief(self) -> None:
        print(self.get_info_brief_to_print())

    def get_info_brief_to_print(self) -> str:
        return f'You are in {self.get_name()}'

    def print_info_complete(self) -> None:
        if self.altitude == 1:
            print(f'Altitude: {self.get_altitude()} meter')
        else:
            print(f'Altitude: {self.get_altitude()} meters')
        print(f'Coordinates: {self.get_latitude()}, {self.get_longitude()}')
        if self.protected_area != '':
            print(f'Protected area: {self.protected_area}')
        if self.island != '':
            print(f'Island: {self.island}')
