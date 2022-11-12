from combat import fighter, random

IMPACTO_DOR = 20  # Pontos de ataque e de defesa perdidos com cada ponto de dor

BONUS_DEFESA_BRACO_DOMINANTE = 1500  # Pontos a somar à defesa do combatente quando o seu braço dominante for atacado
BONUS_DEFESA_BRACO_NAO_DOMINANTE = 0
BONUS_DEFESA_PERNAS = 0
BONUS_DEFESA_BARRIGA = 500
BONUS_DEFESA_PEITO = 1000
BONUS_DEFESA_CABECA = 1000

DIFERENCA_PONTOS_POR_SAUDE = 100  # Diferença entre pontos de ataque e de defesa necessária para tirar 1 ponto de saúde

DEFESA_ESCUDO = 2000  # Pontos de defesa adicionais caso se tenha escudo


class Ronda:

    jogador = None
    inimigo = None
    ronda = 0

    #  #  #  #  #  #  #  #  #  #  #
    #  Opções adicionais do menu  #
    #  #  #  #  #  #  #  #  #  #  #

    @staticmethod
    def sair():
        print("")
        print("Escolheu sair do combate")
        print("Até à próxima")
        exit()

    #  #  #  #  #  #  #  #  #
    #  Métodos auxiliares   #
    #  #  #  #  #  #  #  #  #

    @staticmethod
    def imprimir_estatisticas(personagem):
        if not personagem.get_cpu():
            print("As suas estatísticas:")
        else:
            print("As estatísticas do seu inimigo:")
        print("Saúde geral:", str(personagem.get_saude_geral()) + "; Cabeça:", str(personagem.get_saude_cabeca()) +
              "; Peito:", str(personagem.get_saude_peito()) + "; Barriga:", str(personagem.get_saude_barriga()) +
              "; Braço dominante:", str(personagem.get_saude_braco_dominante()) + "; Braço não dominante:",
              str(personagem.get_saude_braco_nao_dominante()) + "; Perna esquerda:",
              str(personagem.get_saude_perna_esquerda()) + "; Perna direita:", str(personagem.get_saude_perna_direita())
              + "; Força:", str(personagem.get_forca()) + "; Velocidade:", str(personagem.get_velocidade()) + "; Dor:",
              str(personagem.get_dor()) + "; Hemorragia:", str(personagem.get_hemorragia()))
        print("")

    #  Retorna True se a opção for aceitável, False em caso contrário
    @staticmethod
    def avalia_opcao(opcao, numero_opcoes):
        try:
            opcao = int(opcao)
            if 0 <= opcao <= numero_opcoes:  # A opção 0 permite sempre sair do jogo
                return True
            else:
                return False
        except ValueError:  # Input não é um número
            return False

    @staticmethod
    def ataque(atacante, defensor, parte_corpo):
        pontos_ataque_base = atacante.get_forca() * atacante.get_arma() * random.Random.throw_dice(2)
        ataque_perdido_dor = atacante.get_dor() * IMPACTO_DOR
        pontos_ataque_total = pontos_ataque_base - ataque_perdido_dor

        if not atacante.get_cpu():
            print("O seu ataque:")
        else:
            print("O ataque do seu inimigo:")
        print("Pontos de ataque base:", pontos_ataque_base)
        print("Pontos de ataque perdidos com a dor:", ataque_perdido_dor)
        print("TOTAL:", pontos_ataque_total)
        print("")

        pontos_defesa_base = defensor.get_velocidade() * defensor.get_arma() * random.Random.throw_dice(2)
        if defensor.get_escudo():
            pontos_defesa_escudo = DEFESA_ESCUDO
        else:
            pontos_defesa_escudo = 0
        if parte_corpo == 1:
            defesa_bonus_parte_corpo = BONUS_DEFESA_CABECA
        elif parte_corpo == 2:
            defesa_bonus_parte_corpo = BONUS_DEFESA_PEITO
        elif parte_corpo == 3:
            defesa_bonus_parte_corpo = BONUS_DEFESA_BARRIGA
        elif parte_corpo == 4:
            defesa_bonus_parte_corpo = BONUS_DEFESA_BRACO_DOMINANTE
        elif parte_corpo == 5:
            defesa_bonus_parte_corpo = BONUS_DEFESA_BRACO_NAO_DOMINANTE
        elif (parte_corpo == 6) | (parte_corpo == 7):
            defesa_bonus_parte_corpo = BONUS_DEFESA_PERNAS
        else:
            defesa_bonus_parte_corpo = 0
        defesa_perdida_dor = defensor.get_dor() * IMPACTO_DOR
        pontos_defesa_total = pontos_defesa_base + pontos_defesa_escudo + defesa_bonus_parte_corpo - defesa_perdida_dor

        if not defensor.get_cpu():
            print("A sua defesa:")
        else:
            print("A defesa do seu inimigo:")
        print("Pontos de defesa base:", pontos_defesa_base)
        if defensor.get_escudo():
            print("Pontos de defesa do escudo:", pontos_defesa_escudo)
        print("Pontos de defesa da parte do corpo:", defesa_bonus_parte_corpo)
        print("Pontos de defesa perdidos com a dor:", defesa_perdida_dor)
        print("TOTAL:", pontos_defesa_total)
        print("")

        if pontos_ataque_total > pontos_defesa_total:
            saude_perdida = (pontos_ataque_total - pontos_defesa_total) // DIFERENCA_PONTOS_POR_SAUDE
            if not atacante.get_cpu():
                print("Atacou o seu inimigo")
            else:
                print("O seu inimigo atacou-o")
            print("")
            if parte_corpo == 1:
                defensor.diminuir_saude_cabeca(saude_perdida)
            elif parte_corpo == 2:
                defensor.diminuir_saude_peito(saude_perdida)
            elif parte_corpo == 3:
                defensor.diminuir_saude_barriga(saude_perdida)
            elif parte_corpo == 4:
                defensor.diminuir_saude_braco_dominante(saude_perdida)
            elif parte_corpo == 5:
                defensor.diminuir_saude_braco_nao_dominante(saude_perdida)
            elif parte_corpo == 6:
                defensor.diminuir_saude_perna_esquerda(saude_perdida)
            elif parte_corpo == 7:
                defensor.diminuir_saude_perna_direita(saude_perdida)
            print("")
        else:
            if not defensor.get_cpu():
                print("Defendeu o ataque do seu inimigo")
            else:
                print("O seu inimigo defendeu o seu ataque")
            print("")

    #  #  #  #  #  #  #  #
    #  Método principal  #
    #  #  #  #  #  #  #  #

    def ronda_loop(self):
        print("Bem-vindo/a ao combate")
        self.jogador = fighter.Combatente("Jogador1", 0, 0, 3, True, False)
        self.inimigo = fighter.Combatente("Inimigo", 0, 0, 3, False, True)
        print("A sua personagem tem", self.jogador.get_forca(), "pontos de força e", self.jogador.get_velocidade(),
              "pontos de velocidade")
        print("O seu inimigo tem", self.inimigo.get_forca(), "pontos de força e", self.inimigo.get_velocidade(),
              "pontos de velocidade")
        print("")

        while True:
            self.ronda += 1
            print("RONDA", self.ronda)
            print("")
            self.imprimir_estatisticas(self.jogador)
            self.imprimir_estatisticas(self.inimigo)
            print("Escolha a parte do corpo a atacar")
            print("0 - Sair do jogo; 1 - Cabeça; 2 - Peito; 3 - Barriga; 4 - Braço dominante; 5 - Braço não dominante; "
                  "6 - Perna esquerda; 7 - Perna direita")

            #  Validar opção
            opcao = 0
            opcao_e_valida = False
            while not opcao_e_valida:
                opcao = input("Escreva a opção aqui: ")
                print("")
                opcao_e_valida = self.avalia_opcao(opcao, 7)

            #  Opção correcta - Agir em função da mesma
            if int(opcao) == 0:
                self.sair()

            self.ataque(self.jogador, self.inimigo, int(opcao))
            if self.inimigo.get_saude_geral() <= 0:
                print("Matou o seu inimigo")
                exit()
            self.ataque(self.inimigo, self.jogador, random.Random.get_random_int(7))
            if self.jogador.get_saude_geral() <= 0:
                print("Morreu")
                exit()

            self.jogador.diminuir_saude_geral_hemorragia()
            if self.jogador.get_saude_geral() <= 0:
                print("Morreu de hemorragia")
                exit()
            self.inimigo.diminuir_saude_geral_hemorragia()
            if self.inimigo.get_saude_geral() <= 0:
                print("O seu inimigo morreu de hemorragia")
                exit()
