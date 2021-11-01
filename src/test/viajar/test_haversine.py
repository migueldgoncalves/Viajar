import unittest

from viajar import haversine

NORTE = haversine.NORTE
NORDESTE = haversine.NORDESTE
ESTE = haversine.ESTE
SUDESTE = haversine.SUDESTE
SUL = haversine.SUL
SUDOESTE = haversine.SUDOESTE
OESTE = haversine.OESTE
NOROESTE = haversine.NOROESTE

obter_ponto_cardeal = haversine.obter_ponto_cardeal


class TestHaversine(unittest.TestCase):

    def test_obter_ponto_cardeal_mesmo_ponto(self):
        self.assertEqual("", obter_ponto_cardeal((39.0, 0), (39.0, 0)))

    def test_obter_ponto_cardeal_mesma_longitude(self):
        self.assertEqual(NORTE, obter_ponto_cardeal((39.0, 0), (39.5, 0)))
        self.assertEqual(SUL, obter_ponto_cardeal((39.0, 0), (38.5, 0)))

    def test_obter_ponto_cardeal_mesma_latitude(self):
        self.assertEqual(ESTE, obter_ponto_cardeal((39.0, 0), (39.0, 1)))
        self.assertEqual(OESTE, obter_ponto_cardeal((39.0, 0), (39.0, -1)))

    def test_obter_ponto_cardeal_diagonais(self):
        self.assertEqual(NORTE, obter_ponto_cardeal((39.0, 0), (40.0, 0)))
        self.assertEqual(NORTE, obter_ponto_cardeal((39.0, 0), (40.0, 0.1)))
        self.assertEqual(NORTE, obter_ponto_cardeal((39.0, 0), (40.0, 0.2)))
        self.assertEqual(NORTE, obter_ponto_cardeal((39.0, 0), (40.0, 0.3)))
        self.assertEqual(NORTE, obter_ponto_cardeal((39.0, 0), (40.0, 0.4)))
        self.assertEqual(NORDESTE, obter_ponto_cardeal((39.0, 0), (40.0, 0.5)))
        self.assertEqual(NORDESTE, obter_ponto_cardeal((39.0, 0), (40.0, 0.6)))
        self.assertEqual(NORDESTE, obter_ponto_cardeal((39.0, 0), (40.0, 0.7)))
        self.assertEqual(NORDESTE, obter_ponto_cardeal((39.0, 0), (40.0, 0.8)))
        self.assertEqual(NORDESTE, obter_ponto_cardeal((39.0, 0), (40.0, 0.9)))
        self.assertEqual(NORDESTE, obter_ponto_cardeal((39.0, 0), (40.0, 1)))
        self.assertEqual(NORDESTE, obter_ponto_cardeal((39.0, 0), (39.9, 1)))
        self.assertEqual(NORDESTE, obter_ponto_cardeal((39.0, 0), (39.8, 1)))
        self.assertEqual(NORDESTE, obter_ponto_cardeal((39.0, 0), (39.7, 1)))
        self.assertEqual(NORDESTE, obter_ponto_cardeal((39.0, 0), (39.6, 1)))
        self.assertEqual(NORDESTE, obter_ponto_cardeal((39.0, 0), (39.5, 1)))
        self.assertEqual(ESTE, obter_ponto_cardeal((39.0, 0), (39.4, 1)))
        self.assertEqual(ESTE, obter_ponto_cardeal((39.0, 0), (39.3, 1)))
        self.assertEqual(ESTE, obter_ponto_cardeal((39.0, 0), (39.2, 1)))
        self.assertEqual(ESTE, obter_ponto_cardeal((39.0, 0), (39.1, 1)))
        self.assertEqual(ESTE, obter_ponto_cardeal((39.0, 0), (39, 1)))
        self.assertEqual(ESTE, obter_ponto_cardeal((39.0, 0), (38.9, 1)))
        self.assertEqual(ESTE, obter_ponto_cardeal((39.0, 0), (38.8, 1)))
        self.assertEqual(ESTE, obter_ponto_cardeal((39.0, 0), (38.7, 1)))
        self.assertEqual(ESTE, obter_ponto_cardeal((39.0, 0), (38.6, 1)))
        self.assertEqual(SUDESTE, obter_ponto_cardeal((39.0, 0), (38.5, 1)))
        self.assertEqual(SUDESTE, obter_ponto_cardeal((39.0, 0), (38.4, 1)))
        self.assertEqual(SUDESTE, obter_ponto_cardeal((39.0, 0), (38.3, 1)))
        self.assertEqual(SUDESTE, obter_ponto_cardeal((39.0, 0), (38.2, 1)))
        self.assertEqual(SUDESTE, obter_ponto_cardeal((39.0, 0), (38.1, 1)))
        self.assertEqual(SUDESTE, obter_ponto_cardeal((39.0, 0), (38, 1)))
        self.assertEqual(SUDESTE, obter_ponto_cardeal((39.0, 0), (38, 0.9)))
        self.assertEqual(SUDESTE, obter_ponto_cardeal((39.0, 0), (38, 0.8)))
        self.assertEqual(SUDESTE, obter_ponto_cardeal((39.0, 0), (38, 0.7)))
        self.assertEqual(SUDESTE, obter_ponto_cardeal((39.0, 0), (38, 0.6)))
        self.assertEqual(SUDESTE, obter_ponto_cardeal((39.0, 0), (38, 0.5)))
        self.assertEqual(SUL, obter_ponto_cardeal((39.0, 0), (38, 0.4)))
        self.assertEqual(SUL, obter_ponto_cardeal((39.0, 0), (38, 0.3)))
        self.assertEqual(SUL, obter_ponto_cardeal((39.0, 0), (38, 0.2)))
        self.assertEqual(SUL, obter_ponto_cardeal((39.0, 0), (38, 0.1)))
        self.assertEqual(SUL, obter_ponto_cardeal((39.0, 0), (38, 0)))
        self.assertEqual(SUL, obter_ponto_cardeal((39.0, 0), (38, -0.1)))
        self.assertEqual(SUL, obter_ponto_cardeal((39.0, 0), (38, -0.2)))
        self.assertEqual(SUL, obter_ponto_cardeal((39.0, 0), (38, -0.3)))
        self.assertEqual(SUL, obter_ponto_cardeal((39.0, 0), (38, -0.4)))
        self.assertEqual(SUDOESTE, obter_ponto_cardeal((39.0, 0), (38, -0.5)))
        self.assertEqual(SUDOESTE, obter_ponto_cardeal((39.0, 0), (38, -0.6)))
        self.assertEqual(SUDOESTE, obter_ponto_cardeal((39.0, 0), (38, -0.7)))
        self.assertEqual(SUDOESTE, obter_ponto_cardeal((39.0, 0), (38, -0.8)))
        self.assertEqual(SUDOESTE, obter_ponto_cardeal((39.0, 0), (38, -0.9)))
        self.assertEqual(SUDOESTE, obter_ponto_cardeal((39.0, 0), (38, -1)))
        self.assertEqual(SUDOESTE, obter_ponto_cardeal((39.0, 0), (38.1, -1)))
        self.assertEqual(SUDOESTE, obter_ponto_cardeal((39.0, 0), (38.2, -1)))
        self.assertEqual(SUDOESTE, obter_ponto_cardeal((39.0, 0), (38.3, -1)))
        self.assertEqual(SUDOESTE, obter_ponto_cardeal((39.0, 0), (38.4, -1)))
        self.assertEqual(SUDOESTE, obter_ponto_cardeal((39.0, 0), (38.5, -1)))
        self.assertEqual(OESTE, obter_ponto_cardeal((39.0, 0), (38.6, -1)))
        self.assertEqual(OESTE, obter_ponto_cardeal((39.0, 0), (38.7, -1)))
        self.assertEqual(OESTE, obter_ponto_cardeal((39.0, 0), (38.8, -1)))
        self.assertEqual(OESTE, obter_ponto_cardeal((39.0, 0), (38.9, -1)))
        self.assertEqual(OESTE, obter_ponto_cardeal((39.0, 0), (39, -1)))
        self.assertEqual(OESTE, obter_ponto_cardeal((39.0, 0), (39.1, -1)))
        self.assertEqual(OESTE, obter_ponto_cardeal((39.0, 0), (39.2, -1)))
        self.assertEqual(OESTE, obter_ponto_cardeal((39.0, 0), (39.3, -1)))
        self.assertEqual(OESTE, obter_ponto_cardeal((39.0, 0), (39.4, -1)))
        self.assertEqual(NOROESTE, obter_ponto_cardeal((39.0, 0), (39.5, -1)))
        self.assertEqual(NOROESTE, obter_ponto_cardeal((39.0, 0), (39.6, -1)))
        self.assertEqual(NOROESTE, obter_ponto_cardeal((39.0, 0), (39.7, -1)))
        self.assertEqual(NOROESTE, obter_ponto_cardeal((39.0, 0), (39.8, -1)))
        self.assertEqual(NOROESTE, obter_ponto_cardeal((39.0, 0), (39.9, -1)))
        self.assertEqual(NOROESTE, obter_ponto_cardeal((39.0, 0), (40, -1)))
        self.assertEqual(NOROESTE, obter_ponto_cardeal((39.0, 0), (40, -0.9)))
        self.assertEqual(NOROESTE, obter_ponto_cardeal((39.0, 0), (40, -0.8)))
        self.assertEqual(NOROESTE, obter_ponto_cardeal((39.0, 0), (40, -0.7)))
        self.assertEqual(NOROESTE, obter_ponto_cardeal((39.0, 0), (40, -0.6)))
        self.assertEqual(NOROESTE, obter_ponto_cardeal((39.0, 0), (40, -0.5)))
        self.assertEqual(NORTE, obter_ponto_cardeal((39.0, 0), (40, -0.4)))
        self.assertEqual(NORTE, obter_ponto_cardeal((39.0, 0), (40, -0.3)))
        self.assertEqual(NORTE, obter_ponto_cardeal((39.0, 0), (40, -0.2)))
        self.assertEqual(NORTE, obter_ponto_cardeal((39.0, 0), (40, -0.1)))