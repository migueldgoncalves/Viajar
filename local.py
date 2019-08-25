class Local:

    nome = ''
    locais_circundantes = {}

    def __init__(self, nome, locais_circundantes):
        self.nome = nome
        self.locais_circundantes = locais_circundantes

    def set_nome(self, nome):
        self.nome = nome

    def set_locais_circundantes(self, locais_circundantes):
        self.locais_circundantes = locais_circundantes

    def add_local_circundante(self, local, ponto_cardeal, distancia):
        self.locais_circundantes[local] = [ponto_cardeal, distancia]

    def remove_local_circundante(self, local):
        del self.locais_circundantes[local]

    def get_nome(self):
        return self.nome

    def get_locais_circundantes(self):
        return self.locais_circundantes

    def get_ponto_cardeal(self, local):
        return self.locais_circundantes[local][0]

    def get_distancia(self, local):
        return self.locais_circundantes[local][1]
