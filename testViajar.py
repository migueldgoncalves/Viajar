import unittest
import viajar
import carro
import datetime


class TestViajar(unittest.TestCase):

    def test_avalia_opcao(self):
        self.assertEqual(viajar.Viajar.avalia_opcao(-1, 3), 0)
        self.assertEqual(viajar.Viajar.avalia_opcao(0, 3), 1)
        self.assertEqual(viajar.Viajar.avalia_opcao(1, 3), 1)
        self.assertEqual(viajar.Viajar.avalia_opcao(2, 3), 1)
        self.assertEqual(viajar.Viajar.avalia_opcao(3, 3), 1)
        self.assertEqual(viajar.Viajar.avalia_opcao(4, 3), 1)
        self.assertEqual(viajar.Viajar.avalia_opcao(5, 3), 0)
        self.assertEqual(viajar.Viajar.avalia_opcao("", 3), 0)
        self.assertEqual(viajar.Viajar.avalia_opcao("a", 3), 0)
        self.assertEqual(viajar.Viajar.avalia_opcao("Opção inválida", 3), 0)

    def test_conversor_tempo(self):
        self.assertEqual(viajar.Viajar.conversor_tempo(45), datetime.time(0, 0, 45))

    def test_abradar_carro(self):
        carro_teste = carro.Carro()
        carro_teste.velocidade = 100
        carro_teste.abrandar_carro()
        self.assertEqual(98, carro_teste.velocidade)
        carro_teste.velocidade = 1
        carro_teste.abrandar_carro()
        self.assertEqual(0, carro_teste.velocidade)
        carro_teste.velocidade = 0
        self.assertEqual(0, carro_teste.velocidade)
        carro_teste.velocidade = -1
        carro_teste.abrandar_carro()
        self.assertEqual(0, carro_teste.velocidade)
        carro_teste.velocidade = -200
        carro_teste.abrandar_carro()
        self.assertEqual(-198, carro_teste.velocidade)


if __name__ == '__main__':
    unittest.main()