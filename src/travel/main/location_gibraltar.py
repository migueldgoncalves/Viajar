from __future__ import annotations

from travel.main import location

COUNTRY = 'United Kingdom - British Overseas Territory of Gibraltar'


class LocationGibraltar(location.Location):

    def __init__(self, name: str, connections: dict[tuple[str, str], tuple[str, float, str]], latitude: float,
                 longitude: float, altitude: int):
        super().__init__(name, connections, latitude, longitude, altitude)
        self.country = COUNTRY

    def print_info_brief(self) -> None:
        print(self.get_info_brief_to_print())

    def get_info_brief_to_print(self) -> str:
        """
        Ex: Gibraltar-Spain border - Gibraltar side, Gibraltar
        """
        name = self.name.split(",")[0]  # Ex: "Álamo, Alcoutim" and "Álamo, Mértola" -> Álamo
        return f'You are in {name}, Gibraltar'

    def print_info_complete(self) -> None:
        super().print_info_complete()
        print(f'Country: {self.get_country()}')
