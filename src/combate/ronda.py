from combate import combatente


class Ronda:

    aliados = []
    inimigos = []

    def criar_combatentes(self, aliados, inimigos):
        self.aliados.append(combatente.Combatente(0, 0, 3, True, False))  # Personagem controlada pelo jogador
        for i in range(aliados):
            self.aliados.append(combatente.Combatente(0, 0, 3, False, True))
        for i in range(inimigos):
            self.inimigos.append(combatente.Combatente(0, 0, 3, False, True))
