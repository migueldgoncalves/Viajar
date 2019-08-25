import viagem
import locais
import random
import datetime

#  Opções
SEPARADOR = "-"
SAIR = 0  # Não alterar
SAIR_STRING = "Sair da viagem"
ESTATISTICAS_VIAGEM = "Mostrar estatísticas da viagem"

#  Velocidades (km/h)
VELOCIDADE_MINIMA = 50
VELOCIDADE_MAXIMA = 120

#  Outros
LOCAL_INICIAL = locais.GUERREIROS_DO_RIO
CASAS_DECIMAIS = 2


class Viajar:
    lista_locais = []  # Receberá todos os locais disponíveis
    viagem_actual = viagem.Viagem()

    #  #  #  #  #  #  #  #  #  #  #
    #  Opções adicionais do menu  #
    #  #  #  #  #  #  #  #  #  #  #

    @staticmethod
    def sair():
        print("\nEscolheu sair da viagem")
        print("Até à próxima")
        exit()

    def estatisticas_viagem(self):
        print("\nPercorreu", round(self.viagem_actual.get_distancia(), CASAS_DECIMAIS), "km")
        print("Está ao volante há", self.viagem_actual.get_tempo())
        print("Consumiu", round(self.viagem_actual.get_consumo_combustivel(), CASAS_DECIMAIS), "litros de combustível")
        print("Gastou", round(self.viagem_actual.get_dinheiro_gasto(), CASAS_DECIMAIS), "euros em combustível")

    #  #  #  #  #  #  #  #  #
    #  Métodos auxiliares   #
    #  #  #  #  #  #  #  #  #

    #  Retorna 1 se a opção for aceitável, 0 em caso contrário
    @staticmethod
    def avalia_opcao(opcao, numero_opcoes):
        try:
            opcao = int(opcao)
            if SAIR <= opcao <= (numero_opcoes + 1):  # Destinos disponíveis + saída + mostrar estatísticas da viagem
                return 1
            else:
                return 0
        except ValueError:  # Input não é um número
            return 0

    def get_local_actual(self):
        for x in self.lista_locais:
            if x.get_nome() == self.viagem_actual.get_local():
                return x

    @staticmethod
    def conversor_tempo(segundos):
        horas = segundos // 3600
        segundos = segundos - (horas * 3600)
        minutos = segundos // 60
        segundos = segundos - (minutos * 60)
        return datetime.time(int(horas), int(minutos), int(segundos))

    def actualizar_viagem(self, destino):
        print("Escolheu ir para", destino)
        locais_circundantes = self.get_local_actual().get_locais_circundantes()
        distancia = locais_circundantes[destino][1]
        tempo = self.conversor_tempo(distancia / int(random.uniform(VELOCIDADE_MINIMA, VELOCIDADE_MAXIMA)) * 3600)
        self.viagem_actual.add_distancia(distancia)
        self.viagem_actual.add_tempo(tempo)
        self.viagem_actual.set_local(destino)

    #  #  #  #  #  #  #  #
    #  Método principal  #
    #  #  #  #  #  #  #  #

    def realizar_viagem(self):
        #  Obter os locais
        self.lista_locais = locais.Locais.preencher_lista_locais(locais.Locais())

        #  Inicializar viagem
        self.viagem_actual.set_local(LOCAL_INICIAL)
        self.viagem_actual.set_modo(locais.CARRO)
        print("Bem-vindo/a à viagem")
        print("O seu local de origem será", LOCAL_INICIAL)

        #  Realizar viagem
        while True:
            locais_circundantes = self.get_local_actual().get_locais_circundantes()
            nomes_locais = list(locais_circundantes.keys())

            #  Imprimir início do menu
            print("\nEstá em", self.viagem_actual.get_local())
            print("Escolha uma das seguintes opções")
            print("Escreva o número correspondente e pressione ENTER")
            print(SAIR, SEPARADOR, SAIR_STRING)  # Opção de sair

            #  Opções de locais
            iterador = 1
            for x in nomes_locais:
                print(iterador, SEPARADOR, x, "(" + locais_circundantes[x][0] + ",",
                      locais_circundantes[x][1], "km)")  # Exemplo: 1 - Laranjeiras (N, 1 km)
                iterador += 1

            #  Opção das estatísticas da viagem - Fim do menu
            print(iterador, SEPARADOR, ESTATISTICAS_VIAGEM)

            #  Validar opção
            opcao = 0
            opcao_e_valida = 0
            while opcao_e_valida == 0:
                opcao = input("Escreva a opção aqui: ")
                if self.avalia_opcao(opcao, len(nomes_locais)) == 1:
                    opcao_e_valida = 1

            #  Opção correcta - Agir em função da mesma
            if int(opcao) == 0:
                self.sair()
            elif int(opcao) == iterador:
                self.estatisticas_viagem()
            else:
                opcao = int(opcao) - 1  # Opção 1 corresponde ao elemento 0, e por aí em diante
                self.actualizar_viagem(nomes_locais[opcao])
