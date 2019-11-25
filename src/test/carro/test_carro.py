import unittest

from carro import carro


class CarroTest(unittest.TestCase):

    def test_abrandar_carro(self):
        carro_teste = carro.Carro()
        carro_teste.velocidade = 100
        carro_teste.desacelerar(0, carro.DESACELERACAO * carro.ESPERA_POR_COMANDO)
        self.assertEqual(98, carro_teste.velocidade)
        carro_teste.velocidade = 1
        carro_teste.desacelerar(0, carro.DESACELERACAO * carro.ESPERA_POR_COMANDO)
        self.assertEqual(0, carro_teste.velocidade)
        carro_teste.velocidade = 0
        self.assertEqual(0, carro_teste.velocidade)
        carro_teste.velocidade = -1
        carro_teste.desacelerar(0, carro.DESACELERACAO * carro.ESPERA_POR_COMANDO)
        self.assertEqual(0, carro_teste.velocidade)
        carro_teste.velocidade = -200
        carro_teste.desacelerar(0, carro.DESACELERACAO * carro.ESPERA_POR_COMANDO)
        self.assertEqual(-198, carro_teste.velocidade)


if __name__ == '__main__':
    unittest.main()
