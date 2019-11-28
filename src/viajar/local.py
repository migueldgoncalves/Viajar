class Local:

    nome = ''
    locais_circundantes = {}
    coordenadas = (0, 0)  # Ex: (39.00, -9.00)
    altitude = 0  # Metros
    pais = ''

    def __init__(self, nome, locais_circundantes):
        self.nome = nome
        self.locais_circundantes = locais_circundantes

    def set_nome(self, nome):
        self.nome = nome

    def set_locais_circundantes(self, locais_circundantes):
        self.locais_circundantes = locais_circundantes

    def set_coordenadas(self, latitude, longitude):
        self.coordenadas = (latitude, longitude)

    def set_altitude(self, altitude):
        self.altitude = altitude

    def set_pais(self, pais):
        self.pais = pais

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

    def get_coordenadas(self):
        return self.coordenadas

    def get_altitude(self):
        return self.altitude

    def get_pais(self):
        return self.pais

    def imprimir_info_breve(self):
        print("Está em", self.nome)

    def imprimir_info_completa(self):
        print("Informação não disponível")
