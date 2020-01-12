SEPARADOR_DESTINOS = "/"


class Local:

    nome = ''
    locais_circundantes = {}
    sentidos = {}  # Destinos principais seguindo numa direcção. Ex: Sentido Beja/Mértola e Castro Marim/VRSA no IC27
    coordenadas = (0, 0)  # Ex: (37.215788, -7.405922)
    altitude = 0  # Metros
    pais = ''

    def __init__(self, nome, locais_circundantes):
        self.nome = nome
        self.locais_circundantes = locais_circundantes
        self.sentidos = {}  # Necessário para tornar uma variável de classe numa variável de instância

    def set_nome(self, nome):
        self.nome = nome

    def set_locais_circundantes(self, locais_circundantes):
        self.locais_circundantes = locais_circundantes

    def set_sentidos(self, sentidos):
        self.sentidos = sentidos

    def set_coordenadas(self, latitude, longitude):
        self.coordenadas = (latitude, longitude)

    def set_altitude(self, altitude):
        self.altitude = altitude

    def set_pais(self, pais):
        self.pais = pais

    def add_local_circundante(self, local, ponto_cardeal, distancia):
        self.locais_circundantes[local] = [ponto_cardeal, distancia]

    def add_sentido(self, destino, sentido):
        self.sentidos[destino] = sentido

    def remove_local_circundante(self, local):
        del self.locais_circundantes[local]

    def remove_sentido(self, local):
        del self.sentidos[local]

    def get_nome(self):
        return self.nome

    def get_locais_circundantes(self):
        return self.locais_circundantes

    def get_sentidos(self):
        return self.sentidos

    #  Destinos principais seguindo por uma certa direcção de, por exemplo, uma via rápida ou uma via férrea
    def get_sentido(self, destino):
        if destino in self.sentidos:
            destinos = self.sentidos[destino]
            if len(destinos) == 1:
                return destinos[0]
            destinos_string = ''
            for x in destinos:
                destino = x.split(",")[0]
                destinos_string = destinos_string + ' ' + SEPARADOR_DESTINOS + ' ' + destino
            return destinos_string[3:]  # Os primeiros caracteres estão a mais
        return None

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
