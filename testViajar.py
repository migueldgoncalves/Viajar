import unittest
import viajar
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


if __name__ == '__main__':
    unittest.main()