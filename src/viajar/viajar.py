import random
import datetime

from viajar import viagem, bd_interface
from carro import carro

#  Opções
SAIR = 0  # Não alterar
SAIR_STRING = "Sair da viagem"
CARRO_STRING = "Voltar à estrada"
BARCO_STRING = "Subir a bordo de um barco"
AVIAO_STRING = "Embarcar num avião"
COMBOIO_STRING = "Entrar a bordo de um comboio"
METRO_STRING = "Entrar numa composição de metro"
INFORMACOES_LOCAL = "Mostrar informações do local"
ESTATISTICAS_VIAGEM = "Mostrar estatísticas da viagem"
OPCAO_CARRO = "s"
OPCAO_CARRO_STRING = "Tecla S"
OPCAO_NAO_CARRO = "n"
OPCAO_NAO_CARRO_STRING = "Tecla N"

#  Separadores do menu
SEPARADOR_MODO = "->"
SEPARADOR_SENTIDO = "»"

#  Velocidades (km/h)
VELOCIDADE_MINIMA = 50
VELOCIDADE_MAXIMA = 120

#  Pontos cardeais
NORTE = "N"
NORDESTE = "NE"
ESTE = "E"
SUDESTE = "SE"
SUL = "S"
SUDOESTE = "SO"
OESTE = "O"
NOROESTE = "NO"

#  Modos de viagem
CARRO = 'Carro'
BARCO = 'Barco'
AVIAO = 'Avião'
COMBOIO = 'Comboio'
METRO = 'Metro'

#  Outros
LOCAL_INICIAL = 'Guerreiros do Rio'
CASAS_DECIMAIS = 2


class Viajar:

    def __init__(self):
        self.base_dados = bd_interface.BDInterface()  # Contêm todos os locais disponíveis

        #  Inicializar viagem
        self.viagem_actual = viagem.Viagem()
        self.carro_viagem = carro.Carro()
        self.viagem_actual.set_local(LOCAL_INICIAL)
        self.viagem_actual.set_modo(CARRO)
        print("Bem-vindo/a à viagem")
        print("Tem", self.base_dados.obter_numero_locais(), "locais disponíveis para visitar")
        print("O seu local de origem será", LOCAL_INICIAL)
        print("")

        #  Utilizador escolhe se deseja simular viagem de carro entre locais
        self.carro_pedido = self.usar_carro()

    #  #  #  #  #  #  #  #  #  #  #
    #  Opções adicionais do menu  #
    #  #  #  #  #  #  #  #  #  #  #

    @staticmethod
    def sair():
        print("")
        print("Escolheu sair da viagem")
        print("Até à próxima")
        exit()

    def informacoes_local(self):
        print("")
        self.get_local_actual().imprimir_info_completa()

    def estatisticas_viagem(self):
        print("\nPercorreu", round(self.viagem_actual.get_distancia(), CASAS_DECIMAIS), "km")
        if self.viagem_actual.get_dias() == 0:  # Ex: Está ao volante há 00:43:25
            print("Está ao volante há", self.viagem_actual.get_tempo())
        elif self.viagem_actual.get_dias() == 1:  # Ex: Está ao volante há 1 dia e 00:43:25
            print("Está ao volante há 1 dia e", self.viagem_actual.get_tempo())
        else:  # Ex: Está ao volante há 3 dias e 00:43:25
            print("Está ao volante há", self.viagem_actual.get_dias(), "dias e", self.viagem_actual.get_tempo())
        print("Consumiu", round(self.viagem_actual.get_consumo_combustivel(), CASAS_DECIMAIS), "litros de combustível")
        print("Gastou", round(self.viagem_actual.get_dinheiro_gasto(), CASAS_DECIMAIS), "euros em combustível")

    def mudar_modo(self, opcao, numero_locais_proximos, modos_disponiveis):
        opcao -= numero_locais_proximos
        self.viagem_actual.set_modo(modos_disponiveis[opcao - 1])
        if self.viagem_actual.get_modo() == CARRO:
            print("\nEstá de volta à estrada")
        elif self.viagem_actual.get_modo() == BARCO:
            print("\nEstá a bordo de um barco")
        elif self.viagem_actual.get_modo() == AVIAO:
            print("\nEstá a bordo de um avião")
        elif self.viagem_actual.get_modo() == COMBOIO:
            print("\nEstá a bordo de um comboio")
        elif self.viagem_actual.get_modo() == METRO:
            print("\nEstá a bordo de uma composição de metro")
        print("Tem novos destinos disponíveis")

    #  #  #  #  #  #  #  #  #
    #  Métodos auxiliares   #
    #  #  #  #  #  #  #  #  #

    #  Retorna True se a opção for aceitável, False em caso contrário
    @staticmethod
    def avalia_opcao(opcao, numero_opcoes):
        try:
            opcao = int(opcao)
            if SAIR <= opcao <= numero_opcoes:  # A opção Sair existe sempre e não conta para o nº de opções
                return True
            else:
                return False
        except ValueError:  # Input não é um número
            return False

    def get_local_actual(self):
        return self.base_dados.obter_local(self.viagem_actual.get_local())

    @staticmethod
    def conversor_tempo(segundos):
        horas = segundos // 3600
        segundos = segundos - (horas * 3600)
        minutos = segundos // 60
        segundos = segundos - (minutos * 60)
        return datetime.time(int(horas), int(minutos), int(segundos))

    def incrementar_tempo(self, tempo):
        tempo = self.conversor_tempo(tempo)
        self.viagem_actual.add_tempo(tempo)

    def actualizar_viagem(self, destino, carro_pedido):
        print("Escolheu ir para", destino)
        locais_circundantes = self.get_local_actual().get_locais_circundantes()
        distancia = locais_circundantes[destino][1]
        if not carro_pedido:  # A simulação de carro não está a ser usada
            self.incrementar_tempo(distancia / int(random.uniform(VELOCIDADE_MINIMA, VELOCIDADE_MAXIMA)) * 3600)
        self.viagem_actual.add_distancia(distancia)
        self.viagem_actual.set_local(destino)
        return distancia

    @staticmethod
    def usar_carro():
        print("Pode simular a viagem de carro entre 2 locais, pressionando a", OPCAO_CARRO_STRING)
        print("Em alternativa, pode saltar directamente para o local seguinte, pressionando a", OPCAO_NAO_CARRO_STRING)
        print("Depois, pressione ENTER")
        while True:
            opcao = input("Introduza a sua opção: ")
            if opcao == OPCAO_CARRO:
                print("")
                print("Escolheu simular a viagem de carro")
                return True
            elif opcao == OPCAO_NAO_CARRO:
                print("")
                print("Escolheu viajar directamente para o destino")
                return False

    #  #  #  #  #  #  #  #
    #  Método principal  #
    #  #  #  #  #  #  #  #

    def realizar_viagem(self):
        while True:
            locais_circundantes = self.get_local_actual().get_locais_circundantes()
            nomes_locais = list(locais_circundantes.keys())

            #  Imprimir início do menu
            print("")
            self.get_local_actual().imprimir_info_breve()
            print("Escolha uma das seguintes opções")
            print("Escreva o número correspondente e pressione ENTER")
            print(SAIR, SEPARADOR_MODO, SAIR_STRING)  # Opção de sair

            #  Opções de locais
            iterador = 1
            locais_circundantes_modo_actual = []
            for x in nomes_locais:
                if locais_circundantes[x][2] == self.viagem_actual.get_modo():
                    locais_circundantes_modo_actual.append(x)
                    texto = str(iterador) + ' ' + SEPARADOR_MODO + ' ' + x + ' ' + "(" + locais_circundantes[x][0] + \
                        ", " + str(locais_circundantes[x][1]) + ' ' + "km)"  # Exemplo: 1 - Laranjeiras (N, 1 km)
                    sentido = self.get_local_actual().get_sentido(x)  # Destinos possíveis por essa direcção
                    sentido_info_extra = self.get_local_actual().get_sentido_info_extra(x)  # Info extra da direcção
                    if sentido is not None:
                        if sentido_info_extra is None:
                            texto = texto + ' ' + SEPARADOR_SENTIDO + ' ' + "Sentido " + sentido
                        else:
                            texto = texto + ' ' + SEPARADOR_SENTIDO + ' ' + sentido_info_extra + ": Sentido " + sentido
                    print(texto)
                    iterador += 1

            #  Opções de mudança de modo
            modos_disponiveis = []
            for x in nomes_locais:
                if (locais_circundantes[x][2] != self.viagem_actual.get_modo()) & \
                        (modos_disponiveis.__contains__(locais_circundantes[x][2]) is False):
                    modos_disponiveis.append(locais_circundantes[x][2])
            if len(modos_disponiveis) > 0:
                for x in modos_disponiveis:
                    if x == CARRO:
                        print(iterador, SEPARADOR_MODO, CARRO_STRING)
                    elif x == BARCO:
                        print(iterador, SEPARADOR_MODO, BARCO_STRING)
                    elif x == AVIAO:
                        print(iterador, SEPARADOR_MODO, AVIAO_STRING)
                    elif x == COMBOIO:
                        print(iterador, SEPARADOR_MODO, COMBOIO_STRING)
                    elif x == METRO:
                        print(iterador, SEPARADOR_MODO, METRO_STRING)
                    iterador += 1

            #  Opção das informações do local
            print(iterador, SEPARADOR_MODO, INFORMACOES_LOCAL)
            iterador += 1

            #  Opção das estatísticas da viagem - Fim do menu
            print(iterador, SEPARADOR_MODO, ESTATISTICAS_VIAGEM)

            #  Validar opção
            opcao = 0
            opcao_e_valida = False
            while not opcao_e_valida:
                opcao = input("Escreva a opção aqui: ")
                opcao_e_valida = self.avalia_opcao(opcao, iterador)

            #  Opção correcta - Agir em função da mesma
            if int(opcao) == SAIR:  # 0
                self.sair()
            elif (len(locais_circundantes_modo_actual) < int(opcao) <= (len(locais_circundantes_modo_actual) +
                                                                        len(modos_disponiveis))):
                #  Opções de mudança de modo (ex: Carro para Barco), se estiverem disponíveis
                self.mudar_modo(int(opcao), len(locais_circundantes_modo_actual), modos_disponiveis)
            elif int(opcao) == iterador - 1:  # Penúltima opção
                self.informacoes_local()
            elif int(opcao) == iterador:  # Iterador tem o valor da última opção disponível
                self.estatisticas_viagem()
            else:  # Opções dos destinos
                opcao = int(opcao) - 1  # Opção 1 corresponde ao elemento 0, e por aí em diante
                destino = locais_circundantes_modo_actual[opcao]
                distancia_a_percorrer = self.actualizar_viagem(destino, self.carro_pedido)

                #  Activar simulação se se pediu, e se a viagem é por estrada
                if self.carro_pedido & (self.viagem_actual.get_modo() == CARRO):
                    tempo_decorrido = self.carro_viagem.viajar(distancia_a_percorrer, destino)
                    self.incrementar_tempo(tempo_decorrido)
