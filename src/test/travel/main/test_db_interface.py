import unittest

from travel.main.db_interface import DBInterface
from travel.main.cardinal_points import NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH, SOUTHWEST, WEST, NORTHWEST
from travel.main.travel import CARRO, BARCO, COMBOIO, AVIAO, COMBOIO_ALTA_VELOCIDADE, METRO, TRANSBORDO

test_db_name: str = 'viajartestdatabase'


class TestBDInterface(unittest.TestCase):

    def setUp(self):
        self.bd_interface = DBInterface()
        self.bd_interface.create_and_populate_travel_db()

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

    def test_local_base_portugal(self):
        local = self.bd_interface.obter_local('Palmeira')

        self.assertEqual('Palmeira', local.name)
        self.assertEqual(1, len(list(local.connections)))
        self.assertEqual([NORTHEAST, 0.7, CARRO], local.connections[('IC27 - Saída 6', CARRO)])
        self.assertEqual(0, len(list(local.destinations)))
        self.assertEqual(0, len(list(local.ways)))
        self.assertEqual((37.398627, -7.52961), local.coordinates)
        self.assertEqual(85, local.altitude)
        self.assertEqual('Portugal', local.country)
        self.assertEqual('', local.protected_area)
        self.assertEqual('Alcoutim', local.parish)
        self.assertEqual('Alcoutim', local.municipality)
        self.assertEqual('Faro', local.district)
        self.assertEqual('Algarve', local.intermunicipal_entity)
        self.assertEqual('Algarve', local.region)
        local.add_destination('Alcoutim', 'IC27 - Saída 6', 'Carro', 'Estrada')
        self.assertEqual(1, len(list(local.destinations)))
        self.assertEqual(['Alcoutim'], local.destinations[('IC27 - Saída 6', 'Carro')])
        self.assertEqual(1, len(list(local.ways)))
        self.assertEqual('Estrada', local.ways[('IC27 - Saída 6', 'Carro')])
        local.add_connection('IC27 - Saída 6', 'Comboio', 'NE', 0.8)
        self.assertEqual(2, len(list(local.connections)))
        self.assertEqual(('NE', 0.8, 'Comboio'), local.connections[('IC27 - Saída 6', 'Comboio')])
        local.add_destination('Alcoutim', 'IC27 - Saída 6', 'Comboio', 'Caminho-de-ferro')
        self.assertEqual(2, len(list(local.destinations)))
        self.assertEqual(['Alcoutim'], local.destinations[('IC27 - Saída 6', 'Comboio')])
        self.assertEqual(2, len(list(local.ways)))
        self.assertEqual('Caminho-de-ferro', local.ways[('IC27 - Saída 6', 'Comboio')])
        local.add_connection('IC27 - Saída 6', 'Barco', 'NE', 0.9)
        self.assertEqual(3, len(list(local.connections)))
        self.assertEqual(('NE', 0.9, 'Barco'), local.connections[('IC27 - Saída 6', 'Barco')])
        local.add_destination('Alcoutim', 'IC27 - Saída 6', 'Barco', 'Água')
        self.assertEqual(3, len(list(local.destinations)))
        self.assertEqual(['Alcoutim'], local.destinations[('IC27 - Saída 6', 'Barco')])
        self.assertEqual(3, len(list(local.ways)))
        self.assertEqual('Água', local.ways[('IC27 - Saída 6', 'Barco')])

        local = self.bd_interface.obter_local('Marismas de Isla Cristina')

        self.assertEqual('Marismas de Isla Cristina', local.name)
        self.assertEqual(1, len(list(local.connections)))
        self.assertEqual([SOUTHEAST, 2.5, CARRO], local.connections[('Punta del Moral', CARRO)])
        self.assertEqual(0, len(list(local.destinations)))
        self.assertEqual(0, len(list(local.ways)))
        self.assertEqual((37.201359, -7.351221), local.coordinates)
        self.assertEqual(2, local.altitude)
        self.assertEqual('Spain', local.country)
        self.assertEqual('', local.protected_area)
        self.assertEqual('', local.district)
        self.assertEqual('Ayamonte', local.municipality)
        self.assertEqual(1, len(local.comarcas))
        self.assertEqual('Costa Occidental de Huelva', local.comarcas[0])
        self.assertEqual('Huelva', local.province)
        self.assertEqual('Andaluzia', local.autonomous_community)

    def test_ordenar_dicionario(self):
        dicionario = {'tres': 'c', 'um': 'a', 'dois': 'b'}
        ordem = [3, 1, 2]
        ordem_2 = [3, 2, 1]
        ordem_3 = [2, 1, 3]
        ordem_4 = [2, 3, 1]
        ordem_5 = [1, 2, 3]
        ordem_6 = [1, 3, 2]
        self.assertEqual(dicionario, DBInterface.ordenar_dicionario(dicionario, ordem))
        self.assertEqual(dicionario, DBInterface.ordenar_dicionario(dicionario, ordem_2))
        self.assertEqual(dicionario, DBInterface.ordenar_dicionario(dicionario, ordem_3))
        self.assertEqual(dicionario, DBInterface.ordenar_dicionario(dicionario, ordem_4))
        self.assertEqual(dicionario, DBInterface.ordenar_dicionario(dicionario, ordem_5))
        self.assertEqual(dicionario, DBInterface.ordenar_dicionario(dicionario, ordem_6))
        self.assertEqual(['um', 'dois', 'tres'], list(DBInterface.ordenar_dicionario(dicionario, ordem)))
        self.assertEqual(['dois', 'um', 'tres'], list(DBInterface.ordenar_dicionario(dicionario, ordem_2)))
        self.assertEqual(['um', 'tres', 'dois'], list(DBInterface.ordenar_dicionario(dicionario, ordem_3)))
        self.assertEqual(['dois', 'tres', 'um'], list(DBInterface.ordenar_dicionario(dicionario, ordem_4)))
        self.assertEqual(['tres', 'um', 'dois'], list(DBInterface.ordenar_dicionario(dicionario, ordem_5)))
        self.assertEqual(['tres', 'dois', 'um'], list(DBInterface.ordenar_dicionario(dicionario, ordem_6)))
