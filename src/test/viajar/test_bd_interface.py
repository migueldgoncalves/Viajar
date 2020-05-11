import unittest

from viajar import bd_interface


class TestBDInterface(unittest.TestCase):

    def setUp(self):
        self.bd_interface = bd_interface.BDInterface()

    def test_local_base_portugal(self):
        local = self.bd_interface.obter_local('Palmeira')

        self.assertEqual('Palmeira', local.nome)
        self.assertEqual(1, len(list(local.locais_circundantes)))
        self.assertEqual(['NE', 0.7, 'Carro'], local.locais_circundantes['IC27 - Saída 6'])
        self.assertEqual(0, len(list(local.sentidos)))
        self.assertEqual(0, len(list(local.sentidos_info_extra)))
        self.assertEqual((37.398627, -7.52961), local.coordenadas)
        self.assertEqual(85, local.altitude)
        self.assertEqual('Portugal', local.pais)
        self.assertEqual('', local.info_extra)
        self.assertEqual('Alcoutim', local.freguesia)
        self.assertEqual('Alcoutim', local.concelho)
        self.assertEqual('Faro', local.distrito)
        self.assertEqual('Algarve', local.entidade_intermunicipal)
        self.assertEqual('Algarve', local.regiao)

        local = self.bd_interface.obter_local('Marismas de Isla Cristina')

        self.assertEqual('Marismas de Isla Cristina', local.nome)
        self.assertEqual(1, len(list(local.locais_circundantes)))
        self.assertEqual(['SE', 2.5, 'Carro'], local.locais_circundantes['Punta del Moral'])
        self.assertEqual(0, len(list(local.sentidos)))
        self.assertEqual(0, len(list(local.sentidos_info_extra)))
        self.assertEqual((37.201359, -7.351221), local.coordenadas)
        self.assertEqual(2, local.altitude)
        self.assertEqual('Espanha', local.pais)
        self.assertEqual('', local.info_extra)
        self.assertEqual('', local.distrito)
        self.assertEqual('Ayamonte', local.municipio)
        self.assertEqual('Costa Occidental de Huelva', local.comarca)
        self.assertEqual('Huelva', local.provincia)
        self.assertEqual('Andaluzia', local.comunidade_autonoma)

    def test_obter_ponto_cardeal_oposto(self):
        self.assertEqual('S', bd_interface.BDInterface.obter_ponto_cardeal_oposto('N'))
        self.assertEqual('SO', bd_interface.BDInterface.obter_ponto_cardeal_oposto('NE'))
        self.assertEqual('O', bd_interface.BDInterface.obter_ponto_cardeal_oposto('E'))
        self.assertEqual('NO', bd_interface.BDInterface.obter_ponto_cardeal_oposto('SE'))
        self.assertEqual('N', bd_interface.BDInterface.obter_ponto_cardeal_oposto('S'))
        self.assertEqual('NE', bd_interface.BDInterface.obter_ponto_cardeal_oposto('SO'))
        self.assertEqual('E', bd_interface.BDInterface.obter_ponto_cardeal_oposto('O'))
        self.assertEqual('SE', bd_interface.BDInterface.obter_ponto_cardeal_oposto('NO'))
        self.assertEqual('', bd_interface.BDInterface.obter_ponto_cardeal_oposto('Inválido'))

    def test_ordenar_dicionario(self):
        dicionario = {'tres': 'c', 'um': 'a', 'dois': 'b'}
        ordem = [3, 1, 2]
        ordem_2 = [3, 2, 1]
        ordem_3 = [2, 1, 3]
        ordem_4 = [2, 3, 1]
        ordem_5 = [1, 2, 3]
        ordem_6 = [1, 3, 2]
        self.assertEqual(dicionario, bd_interface.BDInterface.ordenar_dicionario(dicionario, ordem))
        self.assertEqual(dicionario, bd_interface.BDInterface.ordenar_dicionario(dicionario, ordem_2))
        self.assertEqual(dicionario, bd_interface.BDInterface.ordenar_dicionario(dicionario, ordem_3))
        self.assertEqual(dicionario, bd_interface.BDInterface.ordenar_dicionario(dicionario, ordem_4))
        self.assertEqual(dicionario, bd_interface.BDInterface.ordenar_dicionario(dicionario, ordem_5))
        self.assertEqual(dicionario, bd_interface.BDInterface.ordenar_dicionario(dicionario, ordem_6))
        self.assertEqual(['um', 'dois', 'tres'], list(bd_interface.BDInterface.ordenar_dicionario(dicionario, ordem)))
        self.assertEqual(['dois', 'um', 'tres'], list(bd_interface.BDInterface.ordenar_dicionario(dicionario, ordem_2)))
        self.assertEqual(['um', 'tres', 'dois'], list(bd_interface.BDInterface.ordenar_dicionario(dicionario, ordem_3)))
        self.assertEqual(['dois', 'tres', 'um'], list(bd_interface.BDInterface.ordenar_dicionario(dicionario, ordem_4)))
        self.assertEqual(['tres', 'um', 'dois'], list(bd_interface.BDInterface.ordenar_dicionario(dicionario, ordem_5)))
        self.assertEqual(['tres', 'dois', 'um'], list(bd_interface.BDInterface.ordenar_dicionario(dicionario, ordem_6)))
