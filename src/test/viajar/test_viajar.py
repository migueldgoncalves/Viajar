import unittest
import datetime

from viajar import viajar


class ViajarTest(unittest.TestCase):

    def test_avalia_opcao(self):
        self.assertEqual(False, viajar.Viajar.avalia_opcao(-1, 3))
        self.assertEqual(True, viajar.Viajar.avalia_opcao(0, 3))
        self.assertEqual(True, viajar.Viajar.avalia_opcao(1, 3))
        self.assertEqual(True, viajar.Viajar.avalia_opcao(2, 3))
        self.assertEqual(True, viajar.Viajar.avalia_opcao(3, 3))
        self.assertEqual(False, viajar.Viajar.avalia_opcao(4, 3))
        self.assertEqual(False, viajar.Viajar.avalia_opcao("", 3))
        self.assertEqual(False, viajar.Viajar.avalia_opcao("a", 3))
        self.assertEqual(False, viajar.Viajar.avalia_opcao("Opção inválida", 3))

    def test_conversor_tempo(self):
        self.assertEqual(datetime.time(0, 0, 45), viajar.Viajar.conversor_tempo(45))


if __name__ == '__main__':
    unittest.main()
