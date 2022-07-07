from __future__ import annotations

from viajar import location


def is_single_province_autonomous_community(autonomous_community: str, province: str) -> bool:
    return autonomous_community == province


class LocationSpain(location.Location):
    """
    Class representing a location in Spain
    """

    def __init__(self, name: str, connections: dict[tuple[str, str], tuple[str, float, str]], latitude: float,
                 longitude: float, altitude: int, municipality: str, comarcas: list[str], province: str,
                 autonomous_community: str):
        super().__init__(name, connections, latitude, longitude, altitude)
        self.district: str = ''  # ES: Distrito (OSM admin level 9). In some regions will correspond to other admin divisions, such as parroquia in Galicia
        self.municipality: str = municipality  # ES: Municipio (OSM admin level 8). In some regions will have a different name, such as concello in Galicia
        self.comarcas: list[str] = comarcas  # OSM admin level 7. According to https://en.wikipedia.org/wiki/Comarcas_of_Spain, translation can be district, county, area, or zone
        self.province: str = province  # ES: Provincia (OSM admin level 6)
        self.autonomous_community: str = autonomous_community  # ES: Comunidad Autónoma (OSM admin level 4)
        self.country = 'Spain'

    def set_district(self, district: str) -> None:
        """
        ES: Distrito (OSM admin level 9). In some regions will correspond to other admin divisions, such as parroquia in Galicia
        """
        self.district = district

    def set_municipality(self, municipality: str) -> None:
        """
        ES: Municipio (OSM admin level 8). In some regions will have a different name, such as concello in Galicia
        """
        self.municipality = municipality

    def set_comarcas(self, comarcas: list[str]) -> None:
        """
        OSM admin level 7. According to https://en.wikipedia.org/wiki/Comarcas_of_Spain, translation can be district, county, area, or zone
        """
        self.comarcas = comarcas

    def set_province(self, province: str) -> None:
        """
        ES: Provincia (OSM admin level 6)
        """
        self.province = province

    def set_autonomous_community(self, autonomous_community: str) -> None:
        """
        ES: Comunidad Autónoma (OSM admin level 4)
        """
        self.autonomous_community = autonomous_community

    def get_district(self) -> str:
        """
        ES: Distrito (OSM admin level 9). In some regions will correspond to other admin divisions, such as parroquia in Galicia
        """
        return self.district

    def get_municipality(self) -> str:
        """
        ES: Municipio (OSM admin level 8). In some regions will have a different name, such as concello in Galicia
        """
        return self.municipality

    def get_comarcas(self) -> list[str]:
        """
        OSM admin level 7. According to https://en.wikipedia.org/wiki/Comarcas_of_Spain, translation can be district, county, area, or zone
        """
        return self.comarcas

    def get_province(self) -> str:
        """
        ES: Provincia (OSM admin level 6)
        """
        return self.province

    def get_autonomous_community(self) -> str:
        """
        ES: Comunidad Autónoma (OSM admin level 4)
        """
        return self.autonomous_community

    def print_info_brief(self) -> None:
        """
        Example for multi-province autonomous community: You are in Ayamonte, Huelva Province, Andalucía
        Example for single province autonomous community: You are in A-5 - Exit 3, Madrid, Madrid Community
        """
        name: str = self.get_name().split(",")[0]  # Ex: "Álamo, Alcoutim" and "Álamo, Mértola" -> Álamo
        if is_single_province_autonomous_community(self.get_autonomous_community(), self.get_province()):
            print(f'You are in {name}, {self.get_municipality()}, {self.get_autonomous_community()}')
        else:
            print(f'You are in {name}, {self.get_municipality()}, {self.get_province()} Province, {self.get_autonomous_community()}')

    def print_info_complete(self) -> None:
        super().print_info_complete()

        # District - OSM admin level 9
        if self.district != '':
            if self.autonomous_community == 'Galiza':
                print(f'Parish/parroquia: {self.get_district()}')
            elif self.autonomous_community == 'Região de Murcia':
                print(f'District/pedanía: {self.get_district()}')
            else:
                print(f'District: {self.get_district()}')

        # Municipality - OSM admin level 8
        if self.autonomous_community == 'Galiza':
            print(f'Municipality/concello: {self.get_municipality()}')
        else:
            print(f'Municipality: {self.get_municipality()}')

        # Comarca - OSM admin level 7
        if len(self.get_comarcas()) == 0:
            if self.autonomous_community == "Extremadura":
                print("Mancomunidad integral: None")
            else:
                print("Comarca: None")
        elif len(self.get_comarcas()) == 1:
            if self.autonomous_community == "Extremadura":
                print(f'Mancomunidad integral: {self.get_comarcas()[0]}')
            else:
                print(f'Comarca: {self.get_comarcas()[0]}')
        else:
            comarca_string: str = ''  # Ex: "Comarcas: Aljarafe, Comarca Metropolitana de Sevilla"
            for comarca in self.get_comarcas():
                comarca_string = f'{comarca_string}, {comarca}'
            print(f'Comarcas: {comarca_string[2:]}')  # First 2 chars should be removed

        # Province - OSM admin level 6
        if not is_single_province_autonomous_community(self.get_autonomous_community(), self.get_province()):
            print(f'Province: {self.get_province()}')

        # Autonomous community - OSM admin level 4
        print(f'Autonomous community: {self.get_autonomous_community()}')

        print(f'Country: {self.get_country()}')
