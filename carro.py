import msvcrt
import time

'''
O carro irá acelerar ao máximo, travar ao máximo ou desacelerar com a fricção, sem situações intermédias
As 3 situações irão decorrer a um ritmo constante
Assume-se que o carro acelera de forma constante ao longo de uma dada mudança
'''

#  Simulacao inicial onde se mede o número de inputs lidos por segundo - Tecla ENTER mantida premida
TEMPO_SIMULACAO = 5.0  # segundos

#  Mudanças para a frente - Assume-se que existe sempre marcha-atrás
NUMERO_MUDANCAS = 5  # Máximo: 8

#  Tempo para ir de 0 RPM à redline em cada mudança na aceleração máxima, em segundos
ACELERACAO_1_MUDANCA = 3
ACELERACAO_2_MUDANCA = 4
ACELERACAO_3_MUDANCA = 6
ACELERACAO_4_MUDANCA = 10
ACELERACAO_5_MUDANCA = 14
ACELERACAO_6_MUDANCA = 20
ACELERACAO_7_MUDANCA = 25
ACELERACAO_8_MUDANCA = 30
ACELERACAO_MARCHA_ATRAS = 3

REDLINE = 6500  # RPM - Rotações por minuto
MAX_ROTACOES = 8000  # Máximo de rotações que a simulação permitirá - Pode ser superior à redline
VELOCIDADE_MAXIMA = 200  # km/h - quilómetros por hora
DESACELERACAO = 10  # km/h abrandados num segundo - No caso de não se estar a acelerar nem a travar
PONTO_MORTO = 0

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
ACELERAR = "w"
TRAVAR = "s"
MUDANCA_ACIMA = "d"
MUDANCA_ABAIXO = "a"
SAIR = "q"

#  Modos de operação
MODO_ACELERAR = 1
MODO_NEUTRO = 0
MODO_TRAVAR = -1

#  Tempo de espera por um comando - Em segundos - Antes de se considerar que nada foi introduzido
ESPERA_POR_COMANDO = 0.2

class Carro:

    velocidade = 0  # km/h
    rotacoes_por_minuto = 0
    mudanca = 0  # Mudança 0 == Ponto morto
    distancia_percorrida = 0  # Metros
    modo_actual = MODO_NEUTRO

    #  Calcula o número de inputs aceites por segundo (botão ENTER mantido premido)
    def inputs_por_segundo(self):
        print("Agora vai simular-se uma aceleração")
        input("Mantenha premida a tecla ENTER durante " + str(TEMPO_SIMULACAO) + " segundos: ")
        contador = 0
        time.perf_counter()  # Iniciar contagem do tempo
        while time.perf_counter() < TEMPO_SIMULACAO:
            print("A velocidade do carro é", contador)
            input("Mantenha premida a tecla ENTER:")
            contador += 1
        print("Simulação terminada")
        print("Pode largar a tecla ENTER")
        return float(contador) / TEMPO_SIMULACAO

    def imprimir_estado_carro(self):
        print("Velocidade actual:", self.velocidade)

    def mudar_mudanca(self, mudanca):
        self.mudanca = mudanca
        if self.mudanca > 0:
            print("Está na", str(self.mudanca) + "ª", "mudança")
        if self.mudanca == 0:
            print("Está em ponto morto")
        if self.mudanca == -1:
            print("Está na marcha-atrás")

    #  Retorna 1 se a opção for aceitável, 0 em caso contrário
    @staticmethod
    def avalia_opcao(opcao):
        if (opcao == ACELERAR) | (opcao == TRAVAR) | (opcao == MUDANCA_ACIMA) | (opcao == MUDANCA_ABAIXO) | (opcao == SAIR):
            return 1
        else:
            return 0

    def instrucoes(self):
        print("Bem-vindo/a ao carro")
        print("Tem os seguintes comandos à sua disposição:")
        print(ACELERAR, "-", "Acelerar")
        print(TRAVAR, "-", "Travar")
        print(MUDANCA_ACIMA, "-", "Meter a mudança acima")
        print(MUDANCA_ABAIXO, "-", "Meter a mudança abaixo")
        print("Para acelerar ou travar, introduza o comando desejado e mantenha premida a tecla ENTER")
        print("O carro irá acelerar ou travar enquanto mantiver a tecla ENTER premida")
        print("Large a tecla ENTER para deixar o carro 'solto' e para poder introduzir outro comando")
        print("Para mudar a mudança, introduza o comando desejado e pressione ENTER")
        print("O carro irá mudar a mudança e continuar a acelerar ou travar, consoante o que estava a fazer antes")
        print("As mudanças são sequenciais")
        print("A mais baixa é a marcha-atrás. Segue-se o ponto morto. Por fim as", NUMERO_MUDANCAS, "mudanças para a frente")
        print("Boa viagem\n")

    #  #  #  #  #  #  #  #
    #  Método principal  #
    #  #  #  #  #  #  #  #

    def viajar(self):
        self.instrucoes()
        inputs_segundo = self.inputs_por_segundo()
        self.mudar_mudanca(PONTO_MORTO)
        while True:
            temporizador = time.perf_counter()
            while time.perf_counter() < (temporizador + ESPERA_POR_COMANDO):
                opcao = input("Introduza a opção:")


#  Comportamentos
#  Carro a acelerar - Para a frente
#  Carro a acelerar - Para trás
#  Carro a travar - Para a frente
#  Carro a travar - Para trás
#  Carro 'solto'
#  Mudança para a frente
#  Mudança para trás
#  Ponto morto
#  Marcha-atrás