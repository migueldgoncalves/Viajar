from combate import aleatorio

SAUDE_INICIAL = 100

IMPACTO_BRACO_SAUDE = 0.2  # Perder 1 ponto de saúde no braço tira 0.2 pontos de saúde geral
IMPACTO_PERNA_SAUDE = 0.2
IMPACTO_BARRIGA_SAUDE = 0.8
IMPACTO_PEITO_SAUDE = 1
IMPACTO_CABECA_SAUDE = 1

BONUS_DEFESA_BRACO_DOMINANTE = 1500  # Pontos a somar à defesa do combatente quando o seu braço dominante for atacado
BONUS_DEFESA_BRACO_NAO_DOMINANTE = 0
BONUS_DEFESA_PERNAS = 0
BONUS_DEFESA_BARRIGA = 500
BONUS_DEFESA_PEITO = 1000
BONUS_DEFESA_CABECA = 1000

IMPACTO_DOR = 20  # Pontos de ataque e de defesa perdidos com cada ponto de dor
SAUDE_POR_DOR = 5  # Pontos de saúde que é preciso perder para se ganhar um ponto de dor
SAUDE_POR_FORCA = 4  # Pontos de saúde no braço dominante que é necessário perder para se perder 1 ponto de força
SAUDE_POR_VELOCIDADE = 4  # Pontos de saúde nas pernas que é necessário perder para se perder 1 ponto de velocidade

PROBABILIDADE_HEMORRAGIA = 2  # Num ataque, a probabilidade de hemorragia em % é este parâmetro vezes a saúde perdida
EXTENSAO_HEMORRAGIA = 0.05  # Em caso de ataque, os pontos de hemorragia ganhos são este parâmetro vezes a saúde perdida

DEFESA_ESCUDO = 2000  # Pontos de defesa caso se tenha escudo

DIFERENCA_PONTOS_POR_SAUDE = 100  # Diferença mínima entre pontos de ataque e de defesa para se desferir danos

CABECA = "Cabeça"
PEITO = "Peito"
BARRIGA = "Barriga"
BRACO_DOMINANTE = "Braço Dominante"
BRACO_NAO_DOMINANTE = "Braço Não Dominante"
PERNA_ESQUERDA = "Perna Esquerda"
PERNA_DIREITA = "Perna Direita"


class Combatente:

    forca = 0
    velocidade = 0
    arma = 0
    saude_geral = 0
    saude_cabeca = 0
    saude_peito = 0
    saude_barriga = 0
    saude_braco_dominante = 0
    saude_braco_nao_dominante = 0
    saude_perna_esquerda = 0
    saude_perna_direita = 0
    escudo = False
    dor = 0
    hemorragia = 0
    cpu = False  # True - Controlado pelo computador

    def __init__(self, forca, velocidade, arma, escudo, cpu):
        if forca == 0:
            self.forca = self.gerador_parametros()
        else:
            self.forca = forca

        if velocidade == 0:
            self.velocidade = self.gerador_parametros()
        else:
            self.velocidade = velocidade

        self.saude_geral = SAUDE_INICIAL
        self.saude_cabeca = SAUDE_INICIAL
        self.saude_peito = SAUDE_INICIAL
        self.saude_barriga = SAUDE_INICIAL
        self.saude_braco_dominante = SAUDE_INICIAL
        self.saude_braco_nao_dominante = SAUDE_INICIAL
        self.saude_perna_esquerda = SAUDE_INICIAL
        self.saude_perna_direita = SAUDE_INICIAL

        self.arma = arma
        self.escudo = escudo
        self.dor = 0
        self.hemorragia = 0

        self.cpu = cpu

    def get_forca(self):
        return self.forca - ((SAUDE_INICIAL - self.saude_braco_dominante) // SAUDE_POR_FORCA)

    def get_velocidade(self):
        return self.velocidade - ((SAUDE_INICIAL - ((self.saude_perna_esquerda + self.saude_perna_direita) / 2))
                                  // SAUDE_POR_VELOCIDADE)

    def get_arma(self):
        return self.arma

    def get_saude_geral(self):
        return self.saude_geral

    def get_saude_cabeca(self):
        return self.saude_cabeca

    def get_saude_peito(self):
        return self.saude_peito

    def get_saude_barriga(self):
        return self.saude_barriga

    def get_saude_braco_dominante(self):
        return self.saude_braco_dominante

    def get_saude_braco_nao_dominante(self):
        return self.saude_braco_nao_dominante

    def get_saude_perna_esquerda(self):
        return self.saude_perna_esquerda

    def get_saude_perna_direita(self):
        return self.saude_perna_direita

    def get_escudo(self):
        return self.escudo

    def get_dor(self):
        return self.dor

    def get_hemorragia(self):
        return self.hemorragia

    def get_cpu(self):
        return self.cpu

    def set_forca(self, forca):
        self.forca = forca

    def set_velocidade(self, velocidade):
        self.velocidade = velocidade

    def set_arma(self, arma):
        self.arma = arma

    def set_saude_geral(self, saude_geral):
        self.saude_geral = saude_geral

    def set_saude_cabeca(self, saude_cabeca):
        self.saude_cabeca = saude_cabeca

    def set_saude_peito(self, saude_peito):
        self.saude_peito = saude_peito

    def set_saude_barriga(self, saude_barriga):
        self.saude_barriga = saude_barriga

    def set_saude_braco_dominante(self, saude_braco_dominante):
        self.saude_braco_dominante = saude_braco_dominante

    def set_saude_braco_nao_dominante(self, saude_braco_nao_dominante):
        self.saude_braco_nao_dominante = saude_braco_nao_dominante

    def set_saude_perna_esquerda(self, saude_perna_esquerda):
        self.saude_perna_esquerda = saude_perna_esquerda

    def set_saude_perna_direita(self, saude_perna_direita):
        self.saude_perna_direita = saude_perna_direita

    def set_escudo(self, escudo):
        self.escudo = escudo

    def set_dor(self, dor):
        self.dor = dor

    def set_hemorragia(self, hemorragia):
        self.hemorragia = hemorragia

    def set_cpu(self, cpu):
        self.cpu = cpu

    def aumentar_dor(self, saude_perdida):
        self.dor += saude_perdida // SAUDE_POR_DOR

    def aumentar_hemorragia(self, saude_perdida):
        probabilidade_hemorragia = PROBABILIDADE_HEMORRAGIA * saude_perdida
        if probabilidade_hemorragia <= aleatorio.Aleatorio.percentagem_aleatoria():
            self.hemorragia += round(saude_perdida * EXTENSAO_HEMORRAGIA)

    def diminuir_saude_geral(self, saude_perdida):
        self.saude_geral -= round(saude_perdida)

    def diminuir_saude_cabeca(self, saude_perdida):
        self.saude_cabeca -= saude_perdida
        self.diminuir_saude_geral(IMPACTO_CABECA_SAUDE * saude_perdida)

    def diminuir_saude_peito(self, saude_perdida):
        self.saude_peito -= saude_perdida
        self.diminuir_saude_geral(IMPACTO_PEITO_SAUDE * saude_perdida)

    def diminuir_saude_barriga(self, saude_perdida):
        self.saude_barriga -= saude_perdida
        self.diminuir_saude_geral(IMPACTO_BARRIGA_SAUDE * saude_perdida)

    def diminuir_saude_braco_dominante(self, saude_perdida):
        self.saude_braco_dominante -= saude_perdida
        self.diminuir_saude_geral(IMPACTO_BRACO_SAUDE * saude_perdida)

    def diminuir_saude_braco_nao_dominante(self, saude_perdida):
        self.saude_braco_nao_dominante -= saude_perdida
        self.diminuir_saude_geral(IMPACTO_BRACO_SAUDE * saude_perdida)

    def diminuir_saude_perna_esquerda(self, saude_perdida):
        self.saude_perna_esquerda -= saude_perdida
        self.diminuir_saude_geral(IMPACTO_PERNA_SAUDE * saude_perdida)

    def diminuir_saude_perna_direita(self, saude_perdida):
        self.saude_perna_direita -= saude_perdida
        self.diminuir_saude_geral(IMPACTO_PERNA_SAUDE * saude_perdida)

    @staticmethod
    def gerador_parametros():
        dados = aleatorio.Aleatorio.dois_dados() + aleatorio.Aleatorio.dois_dados()
        if (dados % 2) == 0:
            return SAUDE_INICIAL + dados
        else:
            return SAUDE_INICIAL - dados
