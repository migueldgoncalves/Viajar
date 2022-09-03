from __future__ import annotations

from travel.main import location

COUNTRY = 'Portugal'


class LocationPortugal(location.Location):
    """
    Class representing a location in Portugal
    """

    def __init__(self, name: str, connections: dict[tuple[str, str], tuple[str, float, str]], latitude: float,
                 longitude: float, altitude: int, parish: str, municipality: str, district: str, intermunicipal_entity: str,
                 region: str):
        super().__init__(name, connections, latitude, longitude, altitude)
        self.parish: str = parish  # PT: Freguesia (OSM admin level 8) - Note: Receives historic parish (pre-2013) if applicable
        self.municipality: str = municipality  # PT: Concelho (OSM admin level 7)
        self.district: str = district  # PT: Distrito (OSM admin level 6)
        self.intermunicipal_entity: str = intermunicipal_entity  # PT: Entidade intermunicipal
        self.region: str = region  # PT: Região
        self.country: str = COUNTRY

    def set_parish(self, parish: str) -> None:
        """
        PT: Freguesia (OSM admin level 8) - Note: Receives historic parish (pre-2013) if applicable
        """
        self.parish = parish

    def set_municipality(self, municipality: str) -> None:
        """
        PT: Concelho (OSM admin level 7)
        """
        self.municipality = municipality

    def set_district(self, district: str) -> None:
        """
        PT: Distrito (OSM admin level 6)
        """
        self.district = district

    def set_intermunicipal_entity(self, intermunicipal_entity: str) -> None:
        """
        PT: Entidade intermunicipal
        """
        self.intermunicipal_entity = intermunicipal_entity

    def set_region(self, region: str) -> None:
        """
        PT: Região
        """
        self.region = region

    def get_parish(self) -> str:
        """
        PT: Freguesia (OSM admin level 8) - Note: Receives historic parish (pre-2013) if applicable
        """
        return self.parish

    def get_municipality(self) -> str:
        """
        PT: Concelho (OSM admin level 7)
        """
        return self.municipality

    def get_district(self) -> str:
        """
        PT: Distrito (OSM admin level 6)
        """
        return self.district

    def get_intermunicipal_entity(self) -> str:
        """
        PT: Entidade intermunicipal
        """
        return self.intermunicipal_entity

    def get_region(self) -> str:
        """
        PT: Região
        """
        return self.region

    def print_info_brief(self) -> None:
        print(self.get_info_brief_to_print())

    def get_info_brief_to_print(self) -> str:
        """
        Example: You are in Odeleite, Castro Marim, Faro District
        """
        name = self.get_name().split(",")[0]  # Ex: "Álamo, Alcoutim" and "Álamo, Mértola" -> Álamo
        return f'You are in {name}, {self.get_municipality()}, {self.get_district()} District'

    def print_info_complete(self) -> None:
        super().print_info_complete()
        print(f'Parish: {self.get_parish()}')
        print(f'Municipality: {self.get_municipality()}')
        print(f'District: {self.get_district()}')
        print(f'Intermunicipal entity: {self.get_intermunicipal_entity()}')
        print(f'Region: {self.get_region()}')
        print(f'Country: {self.get_country()}')
