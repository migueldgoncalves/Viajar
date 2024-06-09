from travel.main import location

COUNTRY = 'Andorra'


class LocationAndorra(location.Location):

    def __init__(self, name: str, connections: dict[tuple[str, str], tuple[str, float, str]], latitude: float,
                 longitude: float, altitude: int, parish: str):
        super().__init__(name, connections, latitude, longitude, altitude)
        self.country = COUNTRY
        self.parish: str = parish

    def get_parish(self) -> str:
        return self.parish

    def set_parish(self, parish: str) -> None:
        self.parish = parish

    def print_info_brief(self) -> None:
        print(self.get_info_brief_to_print())

    def get_info_brief_to_print(self) -> str:
        """
        Ex: Andorra-Spain Border - Andorran Border Post, Sant Julià de Lòria, Andorra
        """
        name = self.name.split(",")[0]  # Ex: "Álamo, Alcoutim" and "Álamo, Mértola" -> Álamo
        return f'You are in {name}, {self.parish}, {self.country}'

    def print_info_complete(self) -> None:
        super().print_info_complete()
        print(f'Country: {self.get_country()}')
        print(f'Parish: {self.get_parish()}')
