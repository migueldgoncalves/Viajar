import unittest

from combate import combatente

FORCA_INICIAL = 100
VELOCIDADE_INICIAL = 100


class CombatenteTest(unittest.TestCase):

    personagem = None

    def setUp(self):
        self.personagem = combatente.Combatente(FORCA_INICIAL, FORCA_INICIAL, 3, False, True)

    def test_get_forca(self):
        self.assertEqual(FORCA_INICIAL, self.personagem.get_forca())
        self.personagem.saude_braco_dominante = combatente.SAUDE_INICIAL - combatente.SAUDE_POR_FORCA + 1
        self.assertEqual(FORCA_INICIAL, self.personagem.get_forca())
        self.personagem.saude_braco_dominante = combatente.SAUDE_INICIAL - combatente.SAUDE_POR_FORCA
        self.assertEqual(FORCA_INICIAL - 1, self.personagem.get_forca())
        self.personagem.saude_braco_dominante = combatente.SAUDE_INICIAL - (2 * combatente.SAUDE_POR_FORCA) + 1
        self.assertEqual(FORCA_INICIAL - 1, self.personagem.get_forca())
        self.personagem.saude_braco_dominante = combatente.SAUDE_INICIAL - (2 * combatente.SAUDE_POR_FORCA)
        self.assertEqual(FORCA_INICIAL - 2, self.personagem.get_forca())

        nova_personagem = combatente.Combatente(0, 0, 3, False, True)
        self.assertTrue(nova_personagem.get_forca() > 0)

    def test_get_velocidade(self):
        self.assertEqual(VELOCIDADE_INICIAL, self.personagem.get_velocidade())
        self.personagem.saude_perna_esquerda = combatente.SAUDE_INICIAL - combatente.SAUDE_POR_VELOCIDADE + 1
        self.personagem.saude_perna_direita = combatente.SAUDE_INICIAL - combatente.SAUDE_POR_VELOCIDADE + 1
        self.assertEqual(VELOCIDADE_INICIAL, self.personagem.get_velocidade())
        self.personagem.saude_perna_esquerda = combatente.SAUDE_INICIAL - combatente.SAUDE_POR_VELOCIDADE
        self.personagem.saude_perna_direita = combatente.SAUDE_INICIAL - combatente.SAUDE_POR_VELOCIDADE
        self.assertEqual(VELOCIDADE_INICIAL - 1, self.personagem.get_velocidade())
        self.personagem.saude_perna_esquerda = combatente.SAUDE_INICIAL - (2 * combatente.SAUDE_POR_VELOCIDADE) + 1
        self.personagem.saude_perna_direita = combatente.SAUDE_INICIAL - (2 * combatente.SAUDE_POR_VELOCIDADE) + 1
        self.assertEqual(VELOCIDADE_INICIAL - 1, self.personagem.get_velocidade())
        self.personagem.saude_perna_esquerda = combatente.SAUDE_INICIAL - (2 * combatente.SAUDE_POR_VELOCIDADE)
        self.personagem.saude_perna_direita = combatente.SAUDE_INICIAL - (2 * combatente.SAUDE_POR_VELOCIDADE)
        self.assertEqual(VELOCIDADE_INICIAL - 2, self.personagem.get_velocidade())

        nova_personagem = combatente.Combatente(0, 0, 3, False, True)
        self.assertTrue(nova_personagem.get_velocidade() > 0)

    def test_aumentar_dor(self):
        self.personagem.aumentar_dor(0)
        self.assertEqual(0, self.personagem.get_dor())
        self.personagem.aumentar_dor(combatente.SAUDE_POR_DOR - 1)
        self.assertEqual(0, self.personagem.get_dor())
        self.personagem.aumentar_dor(combatente.SAUDE_POR_DOR)
        self.assertEqual(1, self.personagem.get_dor())
        self.personagem.aumentar_dor(2 * combatente.SAUDE_POR_DOR - 1)
        self.assertEqual(2, self.personagem.get_dor())
        self.personagem.aumentar_dor(2 * combatente.SAUDE_POR_DOR)
        self.assertEqual(4, self.personagem.get_dor())

    def test_aumentar_hemorragia(self):
        for i in range(1000):
            self.personagem.aumentar_hemorragia(1)
        self.assertEqual(0, self.personagem.get_hemorragia())
        for i in range(1000):
            self.personagem.aumentar_hemorragia(0.5 / combatente.EXTENSAO_HEMORRAGIA)
        self.assertEqual(0, self.personagem.get_hemorragia())
        while not self.personagem.get_hemorragia() > 0:
            self.personagem.aumentar_hemorragia(0.6 / combatente.EXTENSAO_HEMORRAGIA)
        self.assertEqual(1, self.personagem.get_hemorragia())
        while not self.personagem.get_hemorragia() > 1:
            self.personagem.aumentar_hemorragia(1 / combatente.EXTENSAO_HEMORRAGIA)
        self.assertEqual(2, self.personagem.get_hemorragia())
        while not self.personagem.get_hemorragia() > 2:
            self.personagem.aumentar_hemorragia(1.4 / combatente.EXTENSAO_HEMORRAGIA)
        self.assertEqual(3, self.personagem.get_hemorragia())
        while not self.personagem.get_hemorragia() > 3:
            self.personagem.aumentar_hemorragia(1.5 / combatente.EXTENSAO_HEMORRAGIA)
        self.assertEqual(5, self.personagem.get_hemorragia())
        while not self.personagem.get_hemorragia() > 5:
            self.personagem.aumentar_hemorragia(2 / combatente.EXTENSAO_HEMORRAGIA)
        self.assertEqual(7, self.personagem.get_hemorragia())

    def test_diminuir_saude_geral(self):
        self.personagem.diminuir_saude_geral(0)
        self.assertEqual(combatente.SAUDE_INICIAL, self.personagem.get_saude_geral())
        self.personagem.diminuir_saude_geral(1)
        self.assertEqual(combatente.SAUDE_INICIAL - 1, self.personagem.get_saude_geral())
        self.personagem.diminuir_saude_geral(combatente.SAUDE_INICIAL)
        self.assertEqual(-1, self.personagem.get_saude_geral())

    def test_diminuir_saude_cabeca(self):
        self.personagem.diminuir_saude_cabeca(0)
        self.assertEqual(combatente.SAUDE_INICIAL, self.personagem.get_saude_geral())
        self.assertEqual(combatente.SAUDE_INICIAL, self.personagem.get_saude_cabeca())
        self.personagem.diminuir_saude_cabeca(1)
        self.assertEqual(combatente.SAUDE_INICIAL - round(1 * combatente.IMPACTO_CABECA_SAUDE),
                         self.personagem.get_saude_geral())
        self.assertEqual(combatente.SAUDE_INICIAL - 1, self.personagem.get_saude_cabeca())
        self.personagem.set_saude_cabeca(combatente.SAUDE_INICIAL)
        self.personagem.set_saude_geral(combatente.SAUDE_INICIAL)
        self.personagem.diminuir_saude_cabeca(combatente.SAUDE_INICIAL)
        self.assertEqual(combatente.SAUDE_INICIAL - round(combatente.SAUDE_INICIAL * combatente.IMPACTO_CABECA_SAUDE),
                         self.personagem.get_saude_geral())
        self.assertEqual(0, self.personagem.get_saude_cabeca())

    def test_diminuir_saude_peito(self):
        self.personagem.diminuir_saude_peito(0)
        self.assertEqual(combatente.SAUDE_INICIAL, self.personagem.get_saude_geral())
        self.assertEqual(combatente.SAUDE_INICIAL, self.personagem.get_saude_peito())
        self.personagem.diminuir_saude_peito(1)
        self.assertEqual(combatente.SAUDE_INICIAL - round(1 * combatente.IMPACTO_PEITO_SAUDE),
                         self.personagem.get_saude_geral())
        self.assertEqual(combatente.SAUDE_INICIAL - 1, self.personagem.get_saude_peito())
        self.personagem.set_saude_peito(combatente.SAUDE_INICIAL)
        self.personagem.set_saude_geral(combatente.SAUDE_INICIAL)
        self.personagem.diminuir_saude_peito(combatente.SAUDE_INICIAL)
        self.assertEqual(combatente.SAUDE_INICIAL - round(combatente.SAUDE_INICIAL * combatente.IMPACTO_PEITO_SAUDE),
                         self.personagem.get_saude_geral())
        self.assertEqual(0, self.personagem.get_saude_peito())

    def test_diminuir_saude_barriga(self):
        self.personagem.diminuir_saude_barriga(0)
        self.assertEqual(combatente.SAUDE_INICIAL, self.personagem.get_saude_geral())
        self.assertEqual(combatente.SAUDE_INICIAL, self.personagem.get_saude_barriga())
        self.personagem.diminuir_saude_barriga(1)
        self.assertEqual(combatente.SAUDE_INICIAL - round(1 * combatente.IMPACTO_BARRIGA_SAUDE),
                         self.personagem.get_saude_geral())
        self.assertEqual(combatente.SAUDE_INICIAL - 1, self.personagem.get_saude_barriga())
        self.personagem.set_saude_barriga(combatente.SAUDE_INICIAL)
        self.personagem.set_saude_geral(combatente.SAUDE_INICIAL)
        self.personagem.diminuir_saude_barriga(combatente.SAUDE_INICIAL)
        self.assertEqual(combatente.SAUDE_INICIAL - round(combatente.SAUDE_INICIAL * combatente.IMPACTO_BARRIGA_SAUDE),
                         self.personagem.get_saude_geral())
        self.assertEqual(0, self.personagem.get_saude_barriga())

    def test_diminuir_saude_braco_dominante(self):
        self.personagem.diminuir_saude_braco_dominante(0)
        self.assertEqual(combatente.SAUDE_INICIAL, self.personagem.get_saude_geral())
        self.assertEqual(combatente.SAUDE_INICIAL, self.personagem.get_saude_braco_dominante())
        self.personagem.diminuir_saude_braco_dominante(1)
        self.assertEqual(combatente.SAUDE_INICIAL - round(1 * combatente.IMPACTO_BRACO_SAUDE),
                         self.personagem.get_saude_geral())
        self.assertEqual(combatente.SAUDE_INICIAL - 1, self.personagem.get_saude_braco_dominante())
        self.personagem.set_saude_braco_dominante(combatente.SAUDE_INICIAL)
        self.personagem.set_saude_geral(combatente.SAUDE_INICIAL)
        self.personagem.diminuir_saude_braco_dominante(combatente.SAUDE_INICIAL)
        self.assertEqual(combatente.SAUDE_INICIAL - round(combatente.SAUDE_INICIAL * combatente.IMPACTO_BRACO_SAUDE),
                         self.personagem.get_saude_geral())
        self.assertEqual(0, self.personagem.get_saude_braco_dominante())

    def test_diminuir_saude_braco_nao_dominante(self):
        self.personagem.diminuir_saude_braco_nao_dominante(0)
        self.assertEqual(combatente.SAUDE_INICIAL, self.personagem.get_saude_geral())
        self.assertEqual(combatente.SAUDE_INICIAL, self.personagem.get_saude_braco_nao_dominante())
        self.personagem.diminuir_saude_braco_nao_dominante(1)
        self.assertEqual(combatente.SAUDE_INICIAL - round(1 * combatente.IMPACTO_BRACO_SAUDE),
                         self.personagem.get_saude_geral())
        self.assertEqual(combatente.SAUDE_INICIAL - 1, self.personagem.get_saude_braco_nao_dominante())
        self.personagem.set_saude_braco_nao_dominante(combatente.SAUDE_INICIAL)
        self.personagem.set_saude_geral(combatente.SAUDE_INICIAL)
        self.personagem.diminuir_saude_braco_nao_dominante(combatente.SAUDE_INICIAL)
        self.assertEqual(combatente.SAUDE_INICIAL - round(combatente.SAUDE_INICIAL * combatente.IMPACTO_BRACO_SAUDE),
                         self.personagem.get_saude_geral())
        self.assertEqual(0, self.personagem.get_saude_braco_nao_dominante())

    def test_diminuir_saude_perna_esquerda(self):
        self.personagem.diminuir_saude_perna_esquerda(0)
        self.assertEqual(combatente.SAUDE_INICIAL, self.personagem.get_saude_geral())
        self.assertEqual(combatente.SAUDE_INICIAL, self.personagem.get_saude_perna_esquerda())
        self.personagem.diminuir_saude_perna_esquerda(1)
        self.assertEqual(combatente.SAUDE_INICIAL - round(1 * combatente.IMPACTO_PERNA_SAUDE),
                         self.personagem.get_saude_geral())
        self.assertEqual(combatente.SAUDE_INICIAL - 1, self.personagem.get_saude_perna_esquerda())
        self.personagem.set_saude_perna_esquerda(combatente.SAUDE_INICIAL)
        self.personagem.set_saude_geral(combatente.SAUDE_INICIAL)
        self.personagem.diminuir_saude_perna_esquerda(combatente.SAUDE_INICIAL)
        self.assertEqual(combatente.SAUDE_INICIAL - round(combatente.SAUDE_INICIAL * combatente.IMPACTO_PERNA_SAUDE),
                         self.personagem.get_saude_geral())
        self.assertEqual(0, self.personagem.get_saude_perna_esquerda())

    def test_diminuir_saude_perna_direita(self):
        self.personagem.diminuir_saude_perna_direita(0)
        self.assertEqual(combatente.SAUDE_INICIAL, self.personagem.get_saude_geral())
        self.assertEqual(combatente.SAUDE_INICIAL, self.personagem.get_saude_perna_direita())
        self.personagem.diminuir_saude_perna_direita(1)
        self.assertEqual(combatente.SAUDE_INICIAL - round(1 * combatente.IMPACTO_PERNA_SAUDE),
                         self.personagem.get_saude_geral())
        self.assertEqual(combatente.SAUDE_INICIAL - 1, self.personagem.get_saude_perna_direita())
        self.personagem.set_saude_perna_direita(combatente.SAUDE_INICIAL)
        self.personagem.set_saude_geral(combatente.SAUDE_INICIAL)
        self.personagem.diminuir_saude_perna_direita(combatente.SAUDE_INICIAL)
        self.assertEqual(combatente.SAUDE_INICIAL - round(combatente.SAUDE_INICIAL * combatente.IMPACTO_PERNA_SAUDE),
                         self.personagem.get_saude_geral())
        self.assertEqual(0, self.personagem.get_saude_perna_direita())

    def test_gerador_parametros(self):
        for i in range(1000):
            if combatente.Combatente.gerador_parametros() < (combatente.SAUDE_INICIAL - 24):
                self.fail("Valor demasiado baixo")
            if combatente.Combatente.gerador_parametros() > (combatente.SAUDE_INICIAL + 24):
                self.fail("Valor demasiado alto")

    def tearDown(self):
        self.personagem = None
