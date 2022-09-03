import unittest
import copy

from travel.main import location_portugal, location_spain, location, location_gibraltar


class LocationTest(unittest.TestCase):

    def setUp(self):
        self.name: str = 'Lisbon'
        self.connections: dict[tuple[str, str], tuple[str, float, str]] = {
            ('Setúbal', 'Car'): ('SE', 50.0, 'Car'),
            ('Cascais', 'Train'): ('W', 25.0, 'Train'),
            ('Odivelas', 'Subway'): ('N', 5.0, 'Subway'),
            ('Porto', 'Plane'): ('N', 300.0, 'Plane')
        }
        self.destinations: dict[tuple[str, str], list[str]] = {
            ('Setúbal', 'Car'): ['Alentejo', 'Faro'],
            ('Cascais', 'Train'): ['Cabo da Roca', 'Guincho'],
            ('Odivelas', 'Subway'): ['Odivelas'],
            ('Porto', 'Plane'): ['Santarém', 'Coimbra', 'Aveiro']
        }
        self.ways: dict[tuple[str, str], str] = {
            ('Setúbal', 'Car'): 'A2',
            ('Cascais', 'Train'): 'A5',
            ('Odivelas', 'Subway'): 'Lisbon Metro - Yellow Line',
        }
        self.latitude: float = 38.732746
        self.longitude: float = -9.134384
        self.altitude: int = 50
        self.protected_area: str = 'Serra da Arrábida'
        self.batch: int = 100

        self.parish: str = 'Parque das Nações'
        self.municipality_pt: str = 'Oeiras'
        self.district_pt: str = 'Lisbon'
        self.intermunicipal_entity: str = 'Lisbon Metropolitan Area'
        self.region: str = 'Estremadura'

        self.district_es: str = 'Barajas'
        self.municipality_es: str = 'Alcalá de Henares'
        self.comarcas: list[str] = ['Madrid Metropolitan Area', 'Aljarafe']
        self.province = 'Guadalajara'
        self.autonomous_community: str = 'Madrid Community'

        self.major_residential_areas: list[str] = ['North District', 'East Side']

        self.location: location.Location = location.Location(
            self.name, copy.deepcopy(self.connections), self.latitude, self.longitude, self.altitude)
        self.location_portugal: location_portugal.LocationPortugal = location_portugal.LocationPortugal(
            self.name, copy.deepcopy(self.connections), self.latitude, self.longitude, self.altitude, self.parish,
            self.municipality_pt, self.district_pt, self.intermunicipal_entity, self.region)
        self.location_spain: location_spain.LocationSpain = location_spain.LocationSpain(
            self.name, copy.deepcopy(self.connections), self.latitude, self.longitude, self.altitude, self.municipality_es,
            self.comarcas, self.province, self.autonomous_community)
        self.location_gibraltar: location_gibraltar.LocationGibraltar = location_gibraltar.LocationGibraltar(
            self.name, copy.deepcopy(self.connections), self.latitude, self.longitude, self.altitude, self.major_residential_areas)

    def test_getters_location(self):
        self.assertEqual(self.name, self.location.get_name())

        self.assertEqual(tuple(self.connections.keys()), tuple(self.location.get_connections().keys()))
        self.assertEqual(tuple(self.connections.values()), tuple(self.location.get_connections().values()))

        self.assertEqual({}, self.location.get_destinations())
        self.assertEqual(None, self.location.get_destinations_as_string('Cascais', 'Train'))

        self.assertEqual({}, self.location.get_ways())
        self.assertEqual(None, self.location.get_way('Aveiro', 'Tram'))

        self.assertEqual('W', self.location.get_cardinal_point('Cascais', 'Train'))
        self.assertEqual('N', self.location.get_cardinal_point('Porto', 'Plane'))
        self.assertEqual(None, self.location.get_cardinal_point('Aveiro', 'Tram'))

        self.assertEqual(5.0, self.location.get_distance('Odivelas', 'Subway'))
        self.assertEqual(300.0, self.location.get_distance('Porto', 'Plane'))
        self.assertEqual(None, self.location.get_distance('Aveiro', 'Tram'))

        self.assertEqual((self.latitude, self.longitude), self.location.get_coordinates())
        self.assertEqual(self.latitude, self.location.get_latitude())
        self.assertEqual(self.longitude, self.location.get_longitude())

        self.assertEqual(self.altitude, self.location.get_altitude())

        self.assertEqual('', self.location.get_country())
        self.assertEqual('', self.location.get_protected_area())
        self.assertEqual(0, self.location.get_batch())

        self.assertEqual(None, self.location.print_info_brief())
        self.assertTrue(self.location.get_name() in self.location.get_info_brief_to_print())
        self.assertEqual(None, self.location.print_info_complete())

    def test_setters_location(self):
        self.location.set_name('Porto')
        self.assertEqual('Porto', self.location.get_name())

        new_connections: dict[tuple[str, str], tuple[str, float, str]] = {
            ('Aveiro', 'Car'): ('N', 200.0, 'Car'),
        }
        self.location.set_connections(new_connections)
        self.assertEqual(tuple(new_connections.keys()), tuple(self.location.get_connections().keys()))
        self.assertEqual(tuple(new_connections.values()), tuple(self.location.get_connections().values()))
        self.location.add_connection('Évora', 'Car', 'E', 100.0)
        self.location.add_connection('Évora', 'Car', 'E', 100.0)
        self.connections[('Évora', 'Car')] = ('E', 100.0, 'Car')
        self.assertEqual(tuple(new_connections.keys()), tuple(self.location.get_connections().keys()))
        self.assertEqual(tuple(new_connections.values()), tuple(self.location.get_connections().values()))
        self.location.remove_connection('Évora', 'Car')
        self.location.remove_connection('Évora', 'Car')
        del self.connections[('Évora', 'Car')]
        self.assertEqual(tuple(new_connections.keys()), tuple(self.location.get_connections().keys()))
        self.assertEqual(tuple(new_connections.values()), tuple(self.location.get_connections().values()))
        self.assertEqual(None, self.location.remove_connection('Évora', 'Car'))
        self.assertEqual(None, self.location.remove_connection('Guarda', 'Boat'))

        self.location.set_destinations(copy.deepcopy(self.destinations))
        self.assertEqual(tuple(self.destinations.keys()), tuple(self.location.get_destinations().keys()))
        self.assertEqual(tuple(self.destinations.values()), tuple(self.location.get_destinations().values()))
        self.assertEqual(None, self.location.get_destinations_as_string('Aveiro', 'Tram'))
        self.assertEqual('Odivelas', self.location.get_destinations_as_string('Odivelas', 'Subway'))
        self.assertEqual('Alentejo / Faro', self.location.get_destinations_as_string('Setúbal', 'Car'))
        self.assertEqual('Santarém / Coimbra / Aveiro', self.location.get_destinations_as_string('Porto', 'Plane'))
        self.location.add_destination('Braga', 'Porto', 'Plane', 'North Line')
        self.location.add_destination('Braga', 'Porto', 'Plane', 'North Line')
        self.destinations[('Porto', 'Plane')].append('Braga')
        self.assertEqual(tuple(self.destinations.keys()), tuple(self.location.get_destinations().keys()))
        self.assertEqual(tuple(self.destinations.values()), tuple(self.location.get_destinations().values()))
        self.assertEqual('Santarém / Coimbra / Aveiro / Braga', self.location.get_destinations_as_string('Porto', 'Plane'))
        self.location.add_destination('Gafanha da Nazaré', 'Aveiro', 'Tram', 'West Line')
        self.location.add_destination('Gafanha da Nazaré', 'Aveiro', 'Tram', 'West Line')
        self.destinations[('Aveiro', 'Tram')] = ['Gafanha da Nazaré']
        self.assertEqual(tuple(self.destinations.keys()), tuple(self.location.get_destinations().keys()))
        self.assertEqual(tuple(self.destinations.values()), tuple(self.location.get_destinations().values()))
        self.assertEqual('Gafanha da Nazaré', self.location.get_destinations_as_string('Aveiro', 'Tram'))
        self.assertEqual(None, self.location.get_destinations_as_string('Aveiro', 'Car'))
        self.location.remove_destinations_from_connection('Aveiro', 'Tram')
        self.location.remove_destinations_from_connection('Aveiro', 'Tram')
        self.location.remove_destinations_from_connection('Bragança', 'Helicopter')
        del self.destinations[('Aveiro', 'Tram')]
        self.assertEqual(tuple(self.destinations.keys()), tuple(self.location.get_destinations().keys()))
        self.assertEqual(tuple(self.destinations.values()), tuple(self.location.get_destinations().values()))
        self.assertEqual(None, self.location.get_destinations_as_string('Aveiro', 'Tram'))

        self.location.set_ways(copy.deepcopy(self.ways))
        self.assertEqual(tuple(self.ways.keys()), tuple(self.location.get_ways().keys()))
        self.assertEqual(tuple(self.ways.values()), tuple(self.location.get_ways().values()))
        self.assertEqual(self.ways[('Setúbal', 'Car')], self.location.get_way('Setúbal', 'Car'))
        self.assertEqual(self.ways[('Cascais', 'Train')], self.location.get_way('Cascais', 'Train'))
        self.assertEqual(None, self.location.get_way('Aveiro', 'Tram'))
        self.location.add_way('Portalegre', 'Car', 'IP2')
        self.location.add_way('Portalegre', 'Car', 'IP2')
        self.ways[('Portalegre', 'Car')] = 'IP2'
        self.assertEqual(tuple(self.ways.keys()), tuple(self.location.get_ways().keys()))
        self.assertEqual(tuple(self.ways.values()), tuple(self.location.get_ways().values()))
        self.assertEqual(self.ways[('Portalegre', 'Car')], self.location.get_way('Portalegre', 'Car'))
        self.location.remove_way('Portalegre', 'Car')
        self.location.remove_way('Portalegre', 'Car')
        self.location.remove_way('Elvas', 'Car')
        del self.ways[('Portalegre', 'Car')]
        self.assertEqual(tuple(self.ways.keys()), tuple(self.location.get_ways().keys()))
        self.assertEqual(tuple(self.ways.values()), tuple(self.location.get_ways().values()))
        self.assertEqual(None, self.location.get_way('Portalegre', 'Car'))

        self.location.set_coordinates(39.0, -9.0)
        self.assertEqual((39.0, -9.0), self.location.get_coordinates())
        self.assertEqual(39.0, self.location.get_latitude())
        self.assertEqual(-9.0, self.location.get_longitude())

        self.location.set_altitude(300)
        self.assertEqual(300, self.location.get_altitude())

        self.location.set_country('France')
        self.assertEqual('France', self.location.get_country())

        self.location.set_protected_area(self.protected_area)
        self.assertEqual(self.protected_area, self.location.get_protected_area())

        self.location.set_batch(self.batch)
        self.assertEqual(self.batch, self.location.get_batch())

    def test_location_portugal(self):
        self.assertEqual(self.name, self.location_portugal.get_name())
        self.location_portugal.set_name('Porto')
        self.assertEqual('Porto', self.location_portugal.get_name())

        self.assertEqual(self.parish, self.location_portugal.get_parish())
        self.location_portugal.set_parish('Alcoutim e Pereiro')
        self.assertEqual('Alcoutim e Pereiro', self.location_portugal.get_parish())

        self.assertEqual(self.municipality_pt, self.location_portugal.get_municipality())
        self.location_portugal.set_municipality('Alcoutim')
        self.assertEqual('Alcoutim', self.location_portugal.get_municipality())

        self.assertEqual(self.district_pt, self.location_portugal.get_district())
        self.location_portugal.set_district('Faro')
        self.assertEqual('Faro', self.location_portugal.get_district())

        self.assertEqual(self.intermunicipal_entity, self.location_portugal.get_intermunicipal_entity())
        self.location_portugal.set_intermunicipal_entity('Algarve')
        self.assertEqual('Algarve', self.location_portugal.get_intermunicipal_entity())

        self.assertEqual(self.region, self.location_portugal.get_region())
        self.location_portugal.set_region('Lower Alentejo')
        self.assertEqual('Lower Alentejo', self.location_portugal.get_region())

        self.assertEqual(location_portugal.COUNTRY, self.location_portugal.get_country())

        self.assertEqual(None, self.location_portugal.print_info_brief())
        self.assertTrue(self.location_portugal.get_name() in self.location_portugal.get_info_brief_to_print())
        self.assertEqual(None, self.location_portugal.print_info_complete())

    def test_location_spain(self):
        self.assertEqual(self.name, self.location_spain.get_name())
        self.location_spain.set_name('Madrid')
        self.assertEqual('Madrid', self.location_spain.get_name())

        self.assertEqual('', self.location_spain.get_district())
        self.location_spain.set_district(self.district_es)
        self.assertEqual(self.district_es, self.location_spain.get_district())

        self.assertEqual(self.municipality_es, self.location_spain.get_municipality())
        self.location_spain.set_municipality('Barcelona')
        self.assertEqual('Barcelona', self.location_spain.get_municipality())

        self.assertEqual(self.comarcas, self.location_spain.get_comarcas())
        self.location_spain.set_comarcas(['Sierra Norte, Comarca Metropolitana de Sevilla'])
        self.assertEqual(['Sierra Norte, Comarca Metropolitana de Sevilla'], self.location_spain.get_comarcas())
        self.location_spain.set_comarcas(['Comarca de Vigo'])
        self.assertEqual(['Comarca de Vigo'], self.location_spain.get_comarcas())

        self.assertEqual(self.province, self.location_spain.get_province())
        self.location_spain.set_province('Girona')
        self.assertEqual('Girona', self.location_spain.get_province())

        self.assertTrue(location_spain.is_single_province_autonomous_community('', ''))
        self.assertTrue(location_spain.is_single_province_autonomous_community('Madrid Community', 'Madrid Community'))
        self.assertFalse(location_spain.is_single_province_autonomous_community('Andaluzia', 'Seville'))

        self.assertEqual(self.autonomous_community, self.location_spain.get_autonomous_community())
        self.location_spain.set_autonomous_community('Basque Country')
        self.assertEqual('Basque Country', self.location_spain.get_autonomous_community())

        self.assertEqual(location_spain.COUNTRY, self.location_spain.get_country())

        self.assertEqual(None, self.location_spain.print_info_brief())
        self.assertTrue(self.location_spain.get_name() in self.location_spain.get_info_brief_to_print())
        self.assertEqual(None, self.location_spain.print_info_complete())

    def test_location_gibraltar(self):
        self.assertEqual(self.name, self.location_gibraltar.get_name())
        self.location_gibraltar.set_name('Gibraltar')
        self.assertEqual('Gibraltar', self.location_gibraltar.get_name())

        self.assertEqual(self.major_residential_areas, self.location_gibraltar.get_major_residential_areas())
        self.location_gibraltar.set_major_residential_areas(['Reclamation Areas', 'Sandpits Area'])
        self.assertEqual(['Reclamation Areas', 'Sandpits Area'], self.location_gibraltar.get_major_residential_areas())
        self.location_gibraltar.set_major_residential_areas(['Town Area'])
        self.assertEqual(['Town Area'], self.location_gibraltar.get_major_residential_areas())

        self.assertEqual(location_gibraltar.COUNTRY, self.location_gibraltar.get_country())

        self.assertEqual(None, self.location_gibraltar.print_info_brief())
        self.assertTrue(self.location_gibraltar.get_name() in self.location_gibraltar.get_info_brief_to_print())
        self.assertEqual(None, self.location_gibraltar.print_info_complete())
