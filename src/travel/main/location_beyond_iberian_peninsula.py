from travel.main import location


class LocationBeyondIberianPeninsula(location.Location):

    def __init__(self, name: str, connections: dict[tuple[str, str], tuple[str, float, str]], latitude: float,
                 longitude: float, altitude: int, country: str, osm_admin_level_3: str, osm_admin_level_4: str,
                 osm_admin_level_5: str, osm_admin_level_6: str, osm_admin_level_7: str, osm_admin_level_8: str,
                 osm_admin_level_9: str):
        super().__init__(name, connections, latitude, longitude, altitude)
        self.country = country
        self.osm_admin_levels = {
            3: osm_admin_level_3,
            4: osm_admin_level_4,
            5: osm_admin_level_5,
            6: osm_admin_level_6,
            7: osm_admin_level_7,
            8: osm_admin_level_8,
            9: osm_admin_level_9
        }

    def get_country(self) -> str:
        return self.country

    def set_country(self, country: str) -> None:
        self.country = country

    def get_osm_admin_level(self, osm_admin_level: int) -> str:
        if self.osm_admin_levels.get(osm_admin_level, None):
            return self.osm_admin_levels[osm_admin_level]
        else:
            return ''

    def set_osm_admin_level(self, osm_admin_level: int, value: str) -> None:
        self.osm_admin_levels[osm_admin_level] = value

    def get_all_osm_admin_levels(self) -> dict[int, str]:
        return_value: dict[int, str] = {}
        for key, value in self.osm_admin_levels.items():
            if value:
                return_value[key] = value
        return return_value

    def print_info_brief(self) -> None:
        print(self.get_info_brief_to_print())

    def get_info_brief_to_print(self) -> str:
        """
        Ex: A9 - Exit 43, France
        """
        name = self.name.split(",")[0]  # Ex: "Álamo, Alcoutim" and "Álamo, Mértola" -> Álamo
        return f'You are in {name}, {", ".join(self.get_all_osm_admin_levels().values().__reversed__())}, {self.get_country()}'

    def print_info_complete(self) -> None:
        super().print_info_complete()
        print(f'Country: {self.get_country()}')
        for osm_admin_level in self.get_all_osm_admin_levels().keys():
            print(f'{osm_admin_level}: {self.get_osm_admin_level(osm_admin_level)}')