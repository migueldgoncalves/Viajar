class Coordinate:
    """
    Data access object representing a set of coordinates
    """

    def __init__(self, latitude: float, longitude: float):
        assert -90 <= latitude <= 90
        assert -180 <= longitude <= 180

        self.latitude: float = latitude
        self.longitude: float = longitude

    def get_coordinates(self) -> tuple[float, float]:
        return self.get_latitude(), self.get_longitude()

    def get_latitude(self) -> float:
        return self.latitude

    def get_longitude(self) -> float:
        return self.longitude

    def set_latitude(self, latitude: float) -> None:
        assert -90 <= latitude <= 90
        self.latitude = latitude

    def set_longitude(self, longitude: float) -> None:
        assert -180 <= longitude <= 180
        self.longitude = longitude

    def __str__(self) -> str:
        return str((self.latitude, self.longitude))

    def __eq__(self, other) -> bool:
        return self.get_latitude() == other.get_latitude() and self.get_longitude() == other.get_longitude()

    def __hash__(self) -> int:
        return hash(self.get_coordinates())
