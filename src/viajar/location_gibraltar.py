from __future__ import annotations

from viajar import location

COUNTRY = 'United Kingdom - British Overseas Territory of Gibraltar'


class LocationGibraltar(location.Location):

    def __init__(self, name: str, connections: dict[tuple[str, str], tuple[str, float, str]], latitude: float,
                 longitude: float, altitude: int, major_residential_areas: list[str]):
        super().__init__(name, connections, latitude, longitude, altitude)
        self.major_residential_areas: list[str] = major_residential_areas
        self.country = COUNTRY

    def set_major_residential_areas(self, major_residential_areas: list[str]) -> None:
        self.major_residential_areas = major_residential_areas

    def get_major_residential_areas(self) -> list[str]:
        return self.major_residential_areas

    def print_info_brief(self) -> None:
        """
        Ex: Gibraltar-Spain border - Gibraltar side, Gibraltar
        """
        name = self.name.split(",")[0]  # Ex: "Álamo, Alcoutim" and "Álamo, Mértola" -> Álamo
        print(f'You are in {name}, Gibraltar')

    def print_info_complete(self) -> None:
        super().print_info_complete()
        if len(self.get_major_residential_areas()) == 1:
            print(f'Major Residential Area: {self.get_major_residential_areas()[0]}')
        elif len(self.get_major_residential_areas()) > 1:
            major_residential_area_string: str = ''
            for major_residential_area in self.get_major_residential_areas():
                major_residential_area_string = f'{major_residential_area_string}, {major_residential_area}'
            print(f'Major Residential Areas: {major_residential_area_string[2:]}')  # First 2 chars should be removed
        print(f'Country: {self.get_country()}')
