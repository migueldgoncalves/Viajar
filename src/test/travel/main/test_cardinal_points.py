import unittest

from travel.main.cardinal_points import NORTE, NORDESTE, ESTE, SUDESTE, SUL, SUDOESTE, OESTE, NOROESTE, obter_ponto_cardeal_oposto


class CardinalPointsTest(unittest.TestCase):

    def test_obter_ponto_cardeal_oposto(self):
        self.assertEqual(SUL, obter_ponto_cardeal_oposto(NORTE))
        self.assertEqual(SUDOESTE, obter_ponto_cardeal_oposto(NORDESTE))
        self.assertEqual(OESTE, obter_ponto_cardeal_oposto(ESTE))
        self.assertEqual(NOROESTE, obter_ponto_cardeal_oposto(SUDESTE))
        self.assertEqual(NORTE, obter_ponto_cardeal_oposto(SUL))
        self.assertEqual(NORDESTE, obter_ponto_cardeal_oposto(SUDOESTE))
        self.assertEqual(ESTE, obter_ponto_cardeal_oposto(OESTE))
        self.assertEqual(SUDESTE, obter_ponto_cardeal_oposto(NOROESTE))
        self.assertEqual('', obter_ponto_cardeal_oposto('Invalid'))
        self.assertEqual('', obter_ponto_cardeal_oposto(''))
