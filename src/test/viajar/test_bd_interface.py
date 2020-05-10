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
