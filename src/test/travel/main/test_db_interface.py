import unittest

from travel.main.db_interface import DBInterface
from travel.main.cardinal_points import NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH, SOUTHWEST, WEST, NORTHWEST
from travel.main.travel import CAR, BOAT, TRAIN, PLANE, HIGH_SPEED_TRAIN, SUBWAY, TRANSFER
from travel.main import location_portugal, location_spain, location_gibraltar, location_andorra, location_beyond_iberian_peninsula

test_db_name: str = 'viajartestdatabase'


class TestDBInterface(unittest.TestCase):

    def setUp(self):
        self.db_interface = DBInterface()
        self.db_interface.create_and_populate_travel_db()

        try:
            DBInterface.delete_database(test_db_name)
        except:  # DB does not exist?
            pass
    
    def test_database_creation_deletion(self):
        self.assertFalse(DBInterface.is_db_created(test_db_name))
        self.assertTrue(DBInterface.create_database(test_db_name))
        self.assertTrue(DBInterface.is_db_created(test_db_name))
        self.assertTrue(DBInterface.delete_database(test_db_name))
        self.assertFalse(DBInterface.is_db_created(test_db_name))

    def test_determine_location_country(self):
        self.assertEqual('', '')
        self.assertEqual('', self.db_interface.get_location_country('Invalid location'))
        self.assertEqual(location_portugal.COUNTRY, self.db_interface.get_location_country('Guerreiros do Rio'))
        self.assertEqual(location_spain.COUNTRY, self.db_interface.get_location_country('Ayamonte'))
        self.assertEqual(location_gibraltar.COUNTRY, self.db_interface.get_location_country('Western Beach'))
        self.assertEqual(location_andorra.COUNTRY, self.db_interface.get_location_country('Andorra-Spain Border - Andorran Border Post'))
        self.assertEqual('France', self.db_interface.get_location_country('A9 - France-Spain Border'))

    def test_get_location_object_portugal(self):
        # No destinations, 1 connection, 1 means of transport, no protected area
        location: location_portugal.LocationPortugal = self.db_interface.get_location_object('Palmeira')
        self.assertEqual('Palmeira', location.get_name())
        self.assertEqual(1, len(list(location.get_connections())))
        self.assertEqual((NORTHEAST, 0.7, CAR), location.get_connections()[('IC27 - Saída 6', CAR)])
        self.assertEqual(0, len(list(location.get_destinations())))
        self.assertEqual(0, len(list(location.get_ways())))
        self.assertEqual((37.398627, -7.52961), location.get_coordinates())
        self.assertEqual(85, location.get_altitude())
        self.assertEqual(location_portugal.COUNTRY, location.get_country())
        self.assertEqual('', location.get_protected_area())
        self.assertEqual('', location.get_island())
        self.assertEqual('Alcoutim e Pereiro', location.get_parish())
        self.assertEqual('Alcoutim', location.get_municipality())
        self.assertEqual('Faro', location.get_district())
        self.assertEqual('Algarve', location.get_intermunicipal_entity())
        self.assertEqual('Algarve', location.get_region())

        # Multiple destinations, connections and means of transport, no protected area
        location = self.db_interface.get_location_object('Gare do Oriente')
        self.assertEqual('Gare do Oriente', location.get_name())
        self.assertEqual(12, len(list(location.get_connections())))
        self.assertEqual((SOUTHWEST, 0.7, SUBWAY), location.get_connections()[('Estação Cabo Ruivo', SUBWAY)])
        self.assertEqual((NORTH, 11.0, TRAIN), location.get_connections()[('Estação da Póvoa', TRAIN)])
        self.assertEqual(12, len(list(location.get_destinations())))
        self.assertEqual((['Alameda', 'São Sebastião']), location.get_destinations()[('Estação Cabo Ruivo', SUBWAY)])
        self.assertEqual(['Azambuja', 'Porto - Campanhã', 'Vila Franca de Xira'], location.get_destinations()[('Estação da Póvoa', TRAIN)])
        self.assertEqual(12, len(list(location.get_ways())))
        self.assertEqual('Linha Vermelha - Metro de Lisboa', location.get_way('Estação Cabo Ruivo', SUBWAY))
        self.assertEqual('Linha da Azambuja/Linha do Norte - Regional', location.get_ways()[('Estação da Póvoa', TRAIN)])
        self.assertEqual((38.767983, -9.099004), location.get_coordinates())
        self.assertEqual(6, location.get_altitude())
        self.assertEqual(location_portugal.COUNTRY, location.get_country())
        self.assertEqual('', location.get_protected_area())
        self.assertEqual('', location.get_island())
        self.assertEqual('Parque das Nações', location.get_parish())
        self.assertEqual('Lisboa', location.get_municipality())
        self.assertEqual('Lisboa', location.get_district())
        self.assertEqual('Área Metropolitana de Lisboa', location.get_intermunicipal_entity())
        self.assertEqual('Estremadura', location.get_region())

        # Multiple destinations, connections and means of transport, with protected area
        location = self.db_interface.get_location_object('Mértola')
        self.assertEqual('Mértola', location.get_name())
        self.assertEqual(4, len(list(location.get_connections())))
        self.assertEqual((SOUTHEAST, 6.0, CAR), location.get_connections()[('Monte Alto', CAR)])
        self.assertEqual((SOUTHEAST, 10.2, BOAT), location.get_connections()[('Penha da Águia', BOAT)])
        self.assertEqual(3, len(list(location.get_destinations())))
        self.assertEqual((['Pomarão', 'Vila Real de Santo António']), location.get_destinations()[('Penha da Águia', BOAT)])
        self.assertEqual(3, len(list(location.get_ways())))
        self.assertEqual('Rio Guadiana', location.get_way('Penha da Águia', BOAT))
        self.assertEqual((37.641575, -7.660828), location.get_coordinates())
        self.assertEqual(60, location.get_altitude())
        self.assertEqual(location_portugal.COUNTRY, location.get_country())
        self.assertEqual('Parque Natural do Vale do Guadiana', location.get_protected_area())
        self.assertEqual('', location.get_island())
        self.assertEqual('Mértola', location.get_parish())
        self.assertEqual('Mértola', location.get_municipality())
        self.assertEqual('Beja', location.get_district())
        self.assertEqual('Baixo Alentejo', location.get_intermunicipal_entity())
        self.assertEqual('Baixo Alentejo', location.get_region())

        # Multiple destinations, one connection and means of transport, without protected area, with island
        location = self.db_interface.get_location_object('Cabo de Santa Maria')
        self.assertEqual('Cabo de Santa Maria', location.get_name())
        self.assertEqual(1, len(list(location.get_connections())))
        self.assertEqual((NORTHEAST, 2.2, BOAT), location.get_connections()[('Praia da Barreta', BOAT)])
        self.assertEqual(1, len(list(location.get_destinations())))
        self.assertEqual((['Faro', 'Vila Nova de Cacela']), location.get_destinations()[('Praia da Barreta', BOAT)])
        self.assertEqual(1, len(list(location.get_ways())))
        self.assertEqual('Ria Formosa', location.get_way('Praia da Barreta', BOAT))
        self.assertEqual((36.959245, -7.891501), location.get_coordinates())
        self.assertEqual(0, location.get_altitude())
        self.assertEqual(location_portugal.COUNTRY, location.get_country())
        self.assertEqual('Ria Formosa', location.get_protected_area())
        self.assertEqual('Barreta', location.get_island())
        self.assertEqual('Faro (Sé e São Pedro)', location.get_parish())
        self.assertEqual('Faro', location.get_municipality())
        self.assertEqual('Faro', location.get_district())
        self.assertEqual('Algarve', location.get_intermunicipal_entity())
        self.assertEqual('Algarve', location.get_region())

    def test_get_location_object_spain(self):
        # No destinations, one connection, one means of transport, no protected area, with island, with comarca, no district
        location: location_spain.LocationSpain = self.db_interface.get_location_object('Marismas de Isla Cristina')
        self.assertEqual('Marismas de Isla Cristina', location.get_name())
        self.assertEqual(1, len(list(location.get_connections())))
        self.assertEqual((SOUTHEAST, 2.5, CAR), location.get_connections()[('Punta del Moral', CAR)])
        self.assertEqual(0, len(list(location.get_destinations())))
        self.assertEqual(0, len(list(location.get_ways())))
        self.assertEqual((37.201359, -7.351221), location.get_coordinates())
        self.assertEqual(2, location.get_altitude())
        self.assertEqual(location_spain.COUNTRY, location.get_country())
        self.assertEqual('', location.get_protected_area())
        self.assertEqual('Canela', location.get_island())
        self.assertEqual('', location.get_district())
        self.assertEqual('Ayamonte', location.get_municipality())
        self.assertEqual('Costa Occidental de Huelva', location.get_comarca())
        self.assertEqual('Huelva', location.get_province())
        self.assertEqual('Andaluzia', location.get_autonomous_community())

        # Multiple destinations, multiple connections, multiple means of transport, no protected area, with comarca, with district
        location = self.db_interface.get_location_object('Estação de Sevilha-Santa Justa')
        self.assertEqual('Estação de Sevilha-Santa Justa', location.get_name())
        self.assertEqual(3, len(list(location.get_connections())))
        self.assertEqual((EAST, 2.2, CAR), location.get_connections()[('Avenida de Andalucía, Sevilha', CAR)])
        self.assertEqual((NORTHEAST, 125.6, HIGH_SPEED_TRAIN), location.get_connections()[('Estação de Córdoba', HIGH_SPEED_TRAIN)])
        self.assertEqual(1, len(list(location.get_destinations())))
        self.assertEqual(['Antequera-Santa Ana', 'Granada', 'Madrid-Puerta de Atocha', 'Málaga-María Zambrano'], location.get_destinations()[('Estação de Córdoba', HIGH_SPEED_TRAIN)])
        self.assertEqual(1, len(list(location.get_ways())))
        self.assertEqual('LAV Madrid-Sevilha', location.get_way('Estação de Córdoba', HIGH_SPEED_TRAIN))
        self.assertEqual((37.393095, -5.97369), location.get_coordinates())
        self.assertEqual(10, location.get_altitude())
        self.assertEqual(location_spain.COUNTRY, location.get_country())
        self.assertEqual('', location.get_protected_area())
        self.assertEqual('', location.get_island())
        self.assertEqual('San Pablo-Santa Justa', location.get_district())
        self.assertEqual('Sevilha', location.get_municipality())
        self.assertEqual('Comarca Metropolitana de Sevilha', location.get_comarca())
        self.assertEqual('Sevilha', location.get_province())
        self.assertEqual('Andaluzia', location.get_autonomous_community())

        # No destinations, multiple connections, multiple means of transport, no protected area, no comarca, no district
        location = self.db_interface.get_location_object('Aeroporto de Badajoz')
        self.assertEqual('Aeroporto de Badajoz', location.get_name())
        self.assertEqual(13, len(list(location.get_connections())))
        self.assertEqual((SOUTHWEST, 132.4, PLANE), location.get_connections()[('Aeroporto de Beja', PLANE)])
        self.assertEqual((SOUTHWEST, 5.9, CAR), location.get_connections()[('Villafranco del Guadiana', CAR)])
        self.assertEqual(0, len(list(location.get_destinations())))
        self.assertEqual(0, len(list(location.get_ways())))
        self.assertEqual((38.894054, -6.818687), location.get_coordinates())
        self.assertEqual(180, location.get_altitude())
        self.assertEqual(location_spain.COUNTRY, location.get_country())
        self.assertEqual('', location.get_protected_area())
        self.assertEqual('', location.get_island())
        self.assertEqual('', location.get_district())
        self.assertEqual('Badajoz', location.get_municipality())
        self.assertEqual('None', location.get_comarca())
        self.assertEqual('Badajoz', location.get_province())
        self.assertEqual('Extremadura', location.get_autonomous_community())

        # Multiple destinations, multiple connections, one means of transport, with protected area, with comarca, no district
        location = self.db_interface.get_location_object('A-4 - Saída 250-252')
        self.assertEqual('A-4 - Saída 250-252', location.get_name())
        self.assertEqual(2, len(list(location.get_connections())))
        self.assertEqual((NORTHEAST, 5.4, CAR), location.get_connections()[('A-4 - Saída 243', CAR)])
        self.assertEqual((SOUTHWEST, 3.9, CAR), location.get_connections()[('A-4 - Saída 257', CAR)])
        self.assertEqual(2, len(list(location.get_destinations())))
        self.assertEqual(2, len(list(location.get_ways())))
        self.assertEqual((38.371207, -3.517313), location.get_coordinates())
        self.assertEqual(582, location.get_altitude())
        self.assertEqual(location_spain.COUNTRY, location.get_country())
        self.assertEqual('Parque Natural de Despeñaperros', location.get_protected_area())
        self.assertEqual('', location.get_island())
        self.assertEqual('', location.get_district())
        self.assertEqual('Santa Elena', location.get_municipality())
        self.assertEqual('Sierra Morena', location.get_comarca())
        self.assertEqual('Jaén', location.get_province())
        self.assertEqual('Andaluzia', location.get_autonomous_community())

    def test_get_location_object_gibraltar(self):
        # No destinations, one connection, one means of transport, no protected area
        location: location_gibraltar.LocationGibraltar = self.db_interface.get_location_object('Western Beach')
        self.assertEqual('Western Beach', location.get_name())
        self.assertEqual(1, len(list(location.get_connections())))
        self.assertEqual((NORTHEAST, 0.5, CAR), location.get_connections()[('Fronteira Espanha-Gibraltar - Lado de Gibraltar', CAR)])
        self.assertEqual(0, len(list(location.get_destinations())))
        self.assertEqual(0, len(list(location.get_ways())))
        self.assertEqual((36.153103, -5.351108), location.get_coordinates())
        self.assertEqual(2, location.get_altitude())
        self.assertEqual(location_gibraltar.COUNTRY, location.get_country())
        self.assertEqual('', location.get_protected_area())
        self.assertEqual('', location.get_island())

    def test_get_location_object_andorra(self):
        location: location_andorra.LocationAndorra = self.db_interface.get_location_object('Andorra-Spain Border - Andorran Border Post')
        self.assertEqual('Andorra-Spain Border - Andorran Border Post', location.get_name())
        self.assertEqual(2, len(list(location.get_connections())))
        self.assertEqual((NORTHEAST, 0.1, CAR), location.get_connections()[('Andorra-Spain Border - Andorran Customs', CAR)])
        self.assertEqual((SOUTHWEST, 0.1, CAR), location.get_connections()[('Andorra-Spain Border - Spanish Border Post', CAR)])
        self.assertEqual(2, len(list(location.get_destinations())))
        self.assertEqual(2, len(list(location.get_ways())))
        self.assertEqual((42.43534, 1.47288), location.get_coordinates())
        self.assertEqual(847, location.get_altitude())
        self.assertEqual(location_andorra.COUNTRY, location.get_country())
        self.assertEqual('', location.get_protected_area())
        self.assertEqual('', location.get_island())
        self.assertEqual('Sant Julià de Lòria', location.get_parish())

    def test_get_location_object_beyond_iberian_peninsula(self):
        location: location_beyond_iberian_peninsula.LocationBeyondIberianPeninsula = self.db_interface.get_location_object('A9 - France-Spain Border')
        self.assertEqual('A9 - France-Spain Border', location.get_name())
        self.assertEqual(2, len(list(location.get_connections())))
        self.assertEqual((NORTHWEST, 8.6, CAR), location.get_connections()[('A9 - Exit 43', CAR)])
        self.assertEqual((SOUTH, 0.1, CAR), location.get_connections()[('AP-7 - Fronteira Espanha-França', CAR)])
        self.assertEqual(2, len(list(location.get_destinations())))
        self.assertEqual(2, len(list(location.get_ways())))
        self.assertEqual((42.4645, 2.86551), location.get_coordinates())
        self.assertEqual(297, location.get_altitude())
        self.assertEqual('France', location.get_country())
        self.assertEqual('', location.get_protected_area())
        self.assertEqual('', location.get_island())
        self.assertEqual('France métropolitaine', location.get_osm_admin_level(3))
        self.assertEqual('Occitanie', location.get_osm_admin_level(4))
        self.assertEqual('', location.get_osm_admin_level(5))
        self.assertEqual('Pyrénées-Orientales', location.get_osm_admin_level(6))
        self.assertEqual('Céret', location.get_osm_admin_level(7))
        self.assertEqual('Le Perthus', location.get_osm_admin_level(8))
        self.assertEqual('', location.get_osm_admin_level(9))
        self.assertEqual({3: 'France métropolitaine', 4: 'Occitanie', 6: 'Pyrénées-Orientales', 7: 'Céret', 8: 'Le Perthus'}, location.get_all_osm_admin_levels())

    def test_get_total_location_number(self):
        self.assertTrue(self.db_interface.get_total_location_number() > 0)

    def test_order_dictionary(self):
        dictionary = {'three': 'c', 'one': 'a', 'two': 'b'}
        order = [3, 1, 2]
        order_2 = [3, 2, 1]
        order_3 = [2, 1, 3]
        order_4 = [2, 3, 1]
        order_5 = [1, 2, 3]
        order_6 = [1, 3, 2]
        self.assertEqual(dictionary, DBInterface.order_dictionary(dictionary, order))
        self.assertEqual(dictionary, DBInterface.order_dictionary(dictionary, order_2))
        self.assertEqual(dictionary, DBInterface.order_dictionary(dictionary, order_3))
        self.assertEqual(dictionary, DBInterface.order_dictionary(dictionary, order_4))
        self.assertEqual(dictionary, DBInterface.order_dictionary(dictionary, order_5))
        self.assertEqual(dictionary, DBInterface.order_dictionary(dictionary, order_6))
        self.assertEqual(['one', 'two', 'three'], list(DBInterface.order_dictionary(dictionary, order)))
        self.assertEqual(['two', 'one', 'three'], list(DBInterface.order_dictionary(dictionary, order_2)))
        self.assertEqual(['one', 'three', 'two'], list(DBInterface.order_dictionary(dictionary, order_3)))
        self.assertEqual(['two', 'three', 'one'], list(DBInterface.order_dictionary(dictionary, order_4)))
        self.assertEqual(['three', 'one', 'two'], list(DBInterface.order_dictionary(dictionary, order_5)))
        self.assertEqual(['three', 'two', 'one'], list(DBInterface.order_dictionary(dictionary, order_6)))
