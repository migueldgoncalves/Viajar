class Coordenada:

    def __init__(self, latitude: float, longitude: float):
        self.latitude: float = latitude
        self.longitude: float = longitude

    def get_coordenadas(self) -> tuple:
        return self.get_latitude(), self.get_longitude()

    def get_latitude(self) -> float:
        return self.latitude

    def get_longitude(self) -> float:
        return self.longitude

    def set_latitude(self, latitude: float):
        self.latitude = latitude

    def set_longitude(self, longitude: float):
        self.longitude = longitude

    def __str__(self):
        return str((self.latitude, self.longitude))

    def __eq__(self, other):
        return self.get_latitude() == other.get_latitude() and self.get_longitude() == other.get_longitude()

    def __hash__(self):
        return hash(self.get_coordenadas())
