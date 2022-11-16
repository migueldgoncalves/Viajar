from combat import fighter, random


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
    def imprimir_estatisticas(personagem: fighter.Fighter):
        if not personagem.get_cpu():
            print("As suas estatísticas:")
        else:
            print("As estatísticas do seu inimigo:")
        print("Saúde geral:", str(personagem.get_general_health()) + "; Cabeça:", str(personagem.get_body_part_health(fighter.HEAD)) +
              "; Peito:", str(personagem.get_body_part_health(fighter.CHEST)) + "; Barriga:", str(personagem.get_body_part_health(fighter.BELLY)) +
              "; Braço dominante:", str(personagem.get_body_part_health(fighter.DOMINANT_ARM)) + "; Braço não dominante:",
              str(personagem.get_body_part_health(fighter.NON_DOMINANT_ARM)) + "; Perna esquerda:",
              str(personagem.get_body_part_health(fighter.LEFT_LEG)) + "; Perna direita:", str(personagem.get_body_part_health(fighter.RIGHT_LEG))
              + "; Força:", str(personagem.get_current_strength()) + "; Velocidade:", str(personagem.get_current_speed()) + "; Dor:",
              str(personagem.get_pain()) + "; Hemorragia:", str(personagem.get_bleeding()))
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
    def ataque(atacante: fighter.Fighter, defensor: fighter.Fighter, parte_corpo):
        if not atacante.get_cpu():
            print("O seu ataque:")
        else:
            print("O ataque do seu inimigo:")
        pontos_ataque_total = atacante.get_attack_points()

        if not defensor.get_cpu():
            print("A sua defesa:")
        else:
            print("A defesa do seu inimigo:")
        pontos_defesa_total = defensor.get_defense_points()

        if pontos_ataque_total > pontos_defesa_total:
            defensor.decrease_body_part_health_from_attack(pontos_ataque_total, pontos_defesa_total, parte_corpo)
            print("")
            if not atacante.get_cpu():
                print("Atacou o seu inimigo")
            else:
                print("O seu inimigo atacou-o")
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
        self.jogador = fighter.Fighter("Jogador1", 0, 0, 3, False, False)
        self.inimigo = fighter.Fighter("Inimigo", 0, 0, 3, False, True)
        print("A sua personagem tem", self.jogador.get_current_strength(), "pontos de força e", self.jogador.get_current_speed(),
              "pontos de velocidade")
        print("O seu inimigo tem", self.inimigo.get_current_strength(), "pontos de força e", self.inimigo.get_current_speed(),
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
            if self.inimigo.get_general_health() <= 0:
                print("Matou o seu inimigo")
                exit()
            self.ataque(self.inimigo, self.jogador, random.Random.get_random_int(7))
            if self.jogador.get_general_health() <= 0:
                print("Morreu")
                exit()

            self.jogador.decrease_general_health_from_bleeding()
            if self.jogador.get_general_health() <= 0:
                print("Morreu de hemorragia")
                exit()
            self.inimigo.decrease_general_health_from_bleeding()
            if self.inimigo.get_general_health() <= 0:
                print("O seu inimigo morreu de hemorragia")
                exit()
