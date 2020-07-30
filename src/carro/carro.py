import msvcrt
import time

'''
SIMULADOR DE CARRO

O carro irá acelerar ao máximo, travar ao máximo ou desacelerar por si mesmo, sem situações intermédias
O carro acelera de forma constante ao longo de uma dada mudança
O carro trava ou abranda a ritmos constantes, independentemente da mudança
'''

REDLINE = 6500  # RPM - Rotações por minuto
MAX_ROTACOES = 8000  # Máximo de rotações que a simulação permitirá - Pode ser superior à redline
SUGESTAO_MUDAR_MUDANCA = 1000  # Quão abaixo da redline, em RPM, se sugere que se mude de mudança
VELOCIDADE_MAXIMA = 200  # km/h - quilómetros por hora
DESACELERACAO = 10  # km/h abrandados num segundo, no caso de não se estar a acelerar nem a travar
TRAVAGEM_POR_SEGUNDO = 40  # km/h travados por segundo
SEGUNDOS_POR_HORA = 3600

#  Simulação inicial onde se mede o número de inputs lidos por segundo - Tecla ENTER mantida premida
TEMPO_SIMULACAO = 3.0  # Segundos
INPUTS_SEGUNDO_OMISSAO = 20

#  Tempo de espera por um comando antes de se considerar que nada foi introduzido, em segundos
ESPERA_POR_COMANDO = 0.2

#  Mudanças para a frente - Existe sempre marcha-atrás
NUMERO_MUDANCAS = 5  # Máximo: 8

#  Tempo para ir de 0 RPM à redline em cada mudança na aceleração máxima, em segundos
ACELERACAO_1_MUDANCA = 2
ACELERACAO_2_MUDANCA = 6
ACELERACAO_3_MUDANCA = 12
ACELERACAO_4_MUDANCA = 25
ACELERACAO_5_MUDANCA = 40
ACELERACAO_6_MUDANCA = 50
ACELERACAO_7_MUDANCA = 70
ACELERACAO_8_MUDANCA = 90
ACELERACAO_MARCHA_ATRAS = 2

#  Velocidades em km/h na redline em cada mudança
VELOCIDADE_REDLINE_1_MUDANCA = VELOCIDADE_MAXIMA / 5
VELOCIDADE_REDLINE_2_MUDANCA = 2 * (VELOCIDADE_MAXIMA / 5)
VELOCIDADE_REDLINE_3_MUDANCA = 3 * (VELOCIDADE_MAXIMA / 5)
VELOCIDADE_REDLINE_4_MUDANCA = 4 * (VELOCIDADE_MAXIMA / 5)
VELOCIDADE_REDLINE_5_MUDANCA = VELOCIDADE_MAXIMA
VELOCIDADE_REDLINE_6_MUDANCA = 6 * (VELOCIDADE_MAXIMA / 5)
VELOCIDADE_REDLINE_7_MUDANCA = 7 * (VELOCIDADE_MAXIMA / 5)
VELOCIDADE_REDLINE_8_MUDANCA = 8 * (VELOCIDADE_MAXIMA / 5)
VELOCIDADE_REDLINE_MARCHA_ATRAS = VELOCIDADE_MAXIMA / 5

#  Comandos
ACELERAR = b'w'
ACELERAR_2 = b'H'  # Seta para cima
TRAVAR = b's'
TRAVAR_2 = b'P'  # Seta para baixo
MUDANCA_ACIMA = b'd'
MUDANCA_ACIMA_2 = b'M'  # Seta para a direita
MUDANCA_ABAIXO = b'a'
MUDANCA_ABAIXO_2 = b'K'  # Seta para a esquerda
SAIR = b'q'
ACELERAR_STRING = "Tecla W ou Seta para cima"
TRAVAR_STRING = "Tecla S ou Seta para baixo"
MUDANCA_ACIMA_STRING = "Tecla D ou Seta para a direita"
MUDANCA_ABAIXO_STRING = "Tecla A ou Seta para a esquerda"
SAIR_STRING = "Tecla Q"

#  Tipos de desaceleracao
DESACELERACAO_TRAVAGEM = 1
DESACELERACAO_ABRANDAMENTO = 2


class Carro:

    velocidade = 0  # km/h
    rotacoes_por_minuto = 0
    mudanca = 0
    distancia_percorrida = 0  # Quilómetros
    primeira_vez = True  # Se é / será a 1ª vez que a simulação de viagem utiliza o carro
    inputs_por_segundo = 0

    #  #  #  #  #  #  #  #  #  #
    #  Instruções da simulação  #
    #  #  #  #  #  #  #  #  #  #

    @staticmethod
    def instrucoes():
        print("\nBem-vindo/a ao carro")
        print("")
        print("** INSTRUÇÕES GERAIS **")
        print("Tem os seguintes comandos à sua disposição:")
        print("")
        print(SAIR_STRING, "-", "Sair da simulação")
        print(ACELERAR_STRING, "-", "Acelerar")
        print(TRAVAR_STRING, "-", "Travar")
        print(MUDANCA_ACIMA_STRING, "-", "Meter a mudança acima")
        print(MUDANCA_ABAIXO_STRING, "-", "Meter a mudança abaixo")
        print("")
        print("Pressione a tecla correspondente para introduzir o comando")
        print("Pode dar um toque rápido na tecla ou mantê-la premida o tempo que desejar")
        print("As mudanças são sequenciais")
        print("A mais baixa é a marcha-atrás. Segue-se o ponto morto. Por fim as", NUMERO_MUDANCAS,
              "mudanças para a frente")
        print("")
        print("** SÓ PARA A VIAGEM NO BAIXO GUADIANA **")
        print("Ao chegar a um local, tem de pressionar uma tecla para o carro entrar no mesmo")
        print("Só assim irá completar esse troço da viagem")
        print("")
        print("Boa viagem!")
        print("")

    #  #  #  #  #  #  #  #
    #  Simulação inicial  #
    #  #  #  #  #  #  #  #

    #  Calcula o número de inputs aceites por segundo - Tecla ENTER mantida premida
    @staticmethod
    def calcular_inputs_por_segundo():
        print("Vai começar-se por se simular uma aceleração")
        input("Mantenha premida a tecla ENTER durante " + str(TEMPO_SIMULACAO) + " segundos: ")
        contador = 0
        time.perf_counter()  # Iniciar contagem do tempo
        while time.perf_counter() < TEMPO_SIMULACAO:
            print("A velocidade do carro é", contador, "km/h")
            input("Mantenha premida a tecla ENTER:")
            contador += 1
        print("Simulação terminada")
        print("Obrigado por esperar")
        print("Pode largar a tecla ENTER")
        return float(contador) / TEMPO_SIMULACAO

    #  #  #  #  #  #  #  #
    #  Acções do carro  #
    #  #  #  #  #  #  #  #

    def mudar_mudanca(self, mudanca):
        self.mudanca = mudanca
        self.actualizar_rpm()

    def acelerar(self, inputs_segundo):
        if inputs_segundo <= 0:
            inputs_segundo = INPUTS_SEGUNDO_OMISSAO
        if (self.mudanca == -1) & (self.rotacoes_por_minuto < MAX_ROTACOES):
            self.velocidade -= (VELOCIDADE_REDLINE_MARCHA_ATRAS / ACELERACAO_MARCHA_ATRAS / inputs_segundo)
        if (self.mudanca == 1) & (self.rotacoes_por_minuto < MAX_ROTACOES):
            self.velocidade += (VELOCIDADE_REDLINE_1_MUDANCA / ACELERACAO_1_MUDANCA / inputs_segundo)
        if (self.mudanca == 2) & (self.rotacoes_por_minuto < MAX_ROTACOES):
            self.velocidade += (VELOCIDADE_REDLINE_2_MUDANCA / ACELERACAO_2_MUDANCA / inputs_segundo)
        if (self.mudanca == 3) & (self.rotacoes_por_minuto < MAX_ROTACOES):
            self.velocidade += (VELOCIDADE_REDLINE_3_MUDANCA / ACELERACAO_3_MUDANCA / inputs_segundo)
        if (self.mudanca == 4) & (self.rotacoes_por_minuto < MAX_ROTACOES):
            self.velocidade += (VELOCIDADE_REDLINE_4_MUDANCA / ACELERACAO_4_MUDANCA / inputs_segundo)
        if (self.mudanca == 5) & (self.rotacoes_por_minuto < MAX_ROTACOES):
            self.velocidade += (VELOCIDADE_REDLINE_5_MUDANCA / ACELERACAO_5_MUDANCA / inputs_segundo)
        if (self.mudanca == 6) & (self.rotacoes_por_minuto < MAX_ROTACOES):
            self.velocidade += (VELOCIDADE_REDLINE_6_MUDANCA / ACELERACAO_6_MUDANCA / inputs_segundo)
        if (self.mudanca == 7) & (self.rotacoes_por_minuto < MAX_ROTACOES):
            self.velocidade += (VELOCIDADE_REDLINE_7_MUDANCA / ACELERACAO_7_MUDANCA / inputs_segundo)
        if (self.mudanca == 8) & (self.rotacoes_por_minuto < MAX_ROTACOES):
            self.velocidade += (VELOCIDADE_REDLINE_8_MUDANCA / ACELERACAO_8_MUDANCA / inputs_segundo)
        self.actualizar_rpm()

    def desacelerar(self, inputs_por_segundo, desaceleracao):
        perda_velocidade = 0
        if inputs_por_segundo <= 0:
            inputs_por_segundo = INPUTS_SEGUNDO_OMISSAO
        if desaceleracao == DESACELERACAO_TRAVAGEM:  # Carro a travar por acção do utilizador
            perda_velocidade = TRAVAGEM_POR_SEGUNDO / inputs_por_segundo
        elif desaceleracao == DESACELERACAO_ABRANDAMENTO:  # Carro a abrandar sozinho
            perda_velocidade = DESACELERACAO * ESPERA_POR_COMANDO

        if self.velocidade > 0:
            if self.velocidade >= perda_velocidade:
                self.velocidade -= perda_velocidade
            else:
                self.velocidade = 0
        elif self.velocidade < 0:
            if abs(self.velocidade) >= perda_velocidade:
                self.velocidade += perda_velocidade
            else:
                self.velocidade = 0
        self.actualizar_rpm()

    #  #  #  #  #  #  #  #  #
    #  Métodos auxiliares  #
    #  #  #  #  #  #  #  #  #

    def imprimir_mudanca(self):
        if self.mudanca > 0:
            print("Está na", str(self.mudanca) + "ª", "mudança")
        if self.mudanca == 0:
            print("Está em ponto morto")
        if self.mudanca == -1:
            print("Está na marcha-atrás")

    def imprimir_estado_carro(self, distancia_a_percorrer, destino):
        print("")
        print("Velocidade actual:", int(self.velocidade), "km/h")
        self.imprimir_mudanca()
        if (0 < self.mudanca < NUMERO_MUDANCAS) & (self.rotacoes_por_minuto < (REDLINE - SUGESTAO_MUDAR_MUDANCA)):
            print(int(self.rotacoes_por_minuto), "RPM")
        #  Mudança mais alta OU ponto morto OU marcha-atrás
        elif (not(0 < self.mudanca < NUMERO_MUDANCAS)) & (abs(self.rotacoes_por_minuto) < REDLINE):
            print(int(self.rotacoes_por_minuto), "RPM")
        elif (0 < self.mudanca < NUMERO_MUDANCAS) & (
                (REDLINE - SUGESTAO_MUDAR_MUDANCA) <= self.rotacoes_por_minuto < REDLINE):
            print(int(self.rotacoes_por_minuto), "RPM - Mude de mudança")
        else:
            print(int(self.rotacoes_por_minuto), "RPM - Redline!")
        print("Percorreu", round(self.distancia_percorrida, 3), "km")
        if distancia_a_percorrer > 0:
            print("Faltam", round((distancia_a_percorrer - self.distancia_percorrida), 3), "km para chegar a", destino)

    def actualizar_rpm(self):
        if self.mudanca == -1:  # Marcha-atrás
            self.rotacoes_por_minuto = abs(self.velocidade * REDLINE / VELOCIDADE_REDLINE_MARCHA_ATRAS)
        if self.mudanca == 0:  # Ponto morto
            self.rotacoes_por_minuto = 0
        if self.mudanca == 1:
            self.rotacoes_por_minuto = self.velocidade * REDLINE / VELOCIDADE_REDLINE_1_MUDANCA
        if self.mudanca == 2:
            self.rotacoes_por_minuto = self.velocidade * REDLINE / VELOCIDADE_REDLINE_2_MUDANCA
        if self.mudanca == 3:
            self.rotacoes_por_minuto = self.velocidade * REDLINE / VELOCIDADE_REDLINE_3_MUDANCA
        if self.mudanca == 4:
            self.rotacoes_por_minuto = self.velocidade * REDLINE / VELOCIDADE_REDLINE_4_MUDANCA
        if self.mudanca == 5:
            self.rotacoes_por_minuto = self.velocidade * REDLINE / VELOCIDADE_REDLINE_5_MUDANCA
        if self.mudanca == 6:
            self.rotacoes_por_minuto = self.velocidade * REDLINE / VELOCIDADE_REDLINE_6_MUDANCA
        if self.mudanca == 7:
            self.rotacoes_por_minuto = self.velocidade * REDLINE / VELOCIDADE_REDLINE_7_MUDANCA
        if self.mudanca == 8:
            self.rotacoes_por_minuto = self.velocidade * REDLINE / VELOCIDADE_REDLINE_8_MUDANCA

    def incrementar_distancia(self, tempo_decorrido):
        self.distancia_percorrida += tempo_decorrido * self.velocidade / SEGUNDOS_POR_HORA

    def reiniciar_carro(self):
        self.velocidade = 0
        self.rotacoes_por_minuto = 0
        self.mudanca = 0
        self.distancia_percorrida = 0

    #  #  #  #  #  #  #  #
    #  Método principal  #
    #  #  #  #  #  #  #  #

    def viajar(self, distancia_a_percorrer, destino):
        tempo_decorrido = 0
        if self.primeira_vez:  # Se é a 1ª vez que a simulação de carro está a correr
            self.instrucoes()
            self.inputs_por_segundo = self.calcular_inputs_por_segundo()  # Basta calcularem-se 1 vez
        #  Distancia ser 0 == Viagem infinita
        while (distancia_a_percorrer == 0) | (self.distancia_percorrida < distancia_a_percorrer):
            temporizador = time.perf_counter()  # Início e reinício da contagem do tempo
            while (distancia_a_percorrer == 0) | (self.distancia_percorrida < distancia_a_percorrer):
                if msvcrt.kbhit():  # Tecla a ser premida
                    break
                if time.perf_counter() >= (temporizador + ESPERA_POR_COMANDO):  # Nenhuma tecla foi premida
                    self.desacelerar(self.inputs_por_segundo, DESACELERACAO_ABRANDAMENTO)  # Não se acelerou nem travou
                    self.imprimir_estado_carro(distancia_a_percorrer, destino)
                    self.incrementar_distancia(time.perf_counter() - temporizador)
                    temporizador = time.perf_counter()  # Reiniciar temporizador
            caracter = msvcrt.getch()  # Lê a tecla que foi pressionada
            if caracter == SAIR:
                print("")
                print("Escolheu sair do carro")
                print("Até à próxima!")
                exit()
            if (caracter == ACELERAR) | (caracter == ACELERAR_2):
                self.acelerar(self.inputs_por_segundo)
                self.imprimir_estado_carro(distancia_a_percorrer, destino)
            if (caracter == TRAVAR) | (caracter == TRAVAR_2):
                self.desacelerar(self.inputs_por_segundo, DESACELERACAO_TRAVAGEM)
                self.imprimir_estado_carro(distancia_a_percorrer, destino)
            if (caracter == MUDANCA_ACIMA) | (caracter == MUDANCA_ACIMA_2):
                if self.mudanca < NUMERO_MUDANCAS:  # Se a mudança não é já a mais alta
                    self.mudar_mudanca(self.mudanca + 1)
                    self.imprimir_estado_carro(distancia_a_percorrer, destino)
            if (caracter == MUDANCA_ABAIXO) | (caracter == MUDANCA_ABAIXO_2):
                if self.mudanca >= 0:  # Se a mudança não é a marcha-atrás
                    self.mudar_mudanca(self.mudanca - 1)
                    self.imprimir_estado_carro(distancia_a_percorrer, destino)
            self.incrementar_distancia(time.perf_counter() - temporizador)
            tempo_decorrido += time.perf_counter() - temporizador
        print("")
        print("Chegou ao seu destino")
        self.reiniciar_carro()
        if self.primeira_vez:
            self.primeira_vez = False
        return tempo_decorrido  # Tempo passado ao volante na simulação
