import unittest

from combate import aleatorio


class AleatorioTest(unittest.TestCase):

    def test_um_dado(self):
        valores = [1, 2, 3, 4, 5, 6]
        for i in range(1000):
            dado = aleatorio.Aleatorio.um_dado()
            if (dado < 1) | (dado > 6):
                self.fail("Valor incorrecto")
            if dado in valores:
                valores.remove(dado)
        if len(valores) > 0:
            self.fail("Valores em falta")

    def test_dois_dados(self):
        valores = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        for i in range(1000):
            dado = aleatorio.Aleatorio.dois_dados()
            if (dado < 1) | (dado > 12):
                self.fail("Valor incorrecto")
            if dado in valores:
                valores.remove(dado)
        if len(valores) > 0:
            self.fail("Valores em falta")

    def test_percentagem_aleatoria(self):
        valores = []
        for i in range(0, 100):
            valores.append(i)
        for i in range(10000):
            percentagem = aleatorio.Aleatorio.percentagem_aleatoria()
            if (percentagem < 0) | (percentagem > 100):
                self.fail("Valor incorrecto")
            if percentagem in valores:
                valores.remove(percentagem)
        if len(valores) > 0:
            self.fail("Valores em falta")