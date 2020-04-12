SEPARADOR_DESTINOS = "/"


class Local:

    nome = ''
    locais_circundantes = {}
    sentidos = {}  # Destinos principais seguindo numa direcção. Ex: Sentido Beja/Mértola e Castro Marim/VRSA no IC27
    sentidos_info_extra = {}  # Informação extra associada aos sentidos. Ex: Linha 1 do metro, ou comboio Regional
    coordenadas = (0, 0)  # Ex: (37.215788, -7.405922)
    altitude = 0  # Metros
    pais = ''
    info_extra = ''  # Informação extra associada ao local. Ex: Reserva natural

    def __init__(self, nome, locais_circundantes, latitude, longitude, altitude):
        self.nome = nome
        self.locais_circundantes = locais_circundantes
        self.sentidos = {}  # Necessário para tornar uma variável de classe numa variável de instância
        self.sentidos_info_extra = {}
        self.coordenadas = (latitude, longitude)
        self.altitude = altitude
        self.pais = ''
        self.info_extra = ''

    def set_nome(self, nome):
        self.nome = nome

    def set_locais_circundantes(self, locais_circundantes):
        self.locais_circundantes = locais_circundantes

    def set_sentidos(self, sentidos):
        self.sentidos = sentidos

    def set_sentidos_info_extra(self, sentidos_info_extra):
        self.sentidos_info_extra = sentidos_info_extra

    def set_coordenadas(self, latitude, longitude):
        self.coordenadas = (latitude, longitude)

    def set_altitude(self, altitude):
        self.altitude = altitude

    def set_pais(self, pais):
        self.pais = pais

    def set_info_extra(self, info_extra):
        self.info_extra = info_extra

    def add_local_circundante(self, local, ponto_cardeal, distancia):
        self.locais_circundantes[local] = [ponto_cardeal, distancia]

    def add_sentido_info_extra(self, destino, info_extra):
        self.sentidos_info_extra[destino] = info_extra

    def add_sentido(self, destino, sentido, info_extra):
        self.sentidos[destino] = sentido
        self.add_sentido_info_extra(destino, info_extra)

    def remove_local_circundante(self, local):
        del self.locais_circundantes[local]

    def remove_sentido(self, destino):
        del self.sentidos[destino]

    def remove_sentido_info_extra(self, destino):
        del self.sentidos_info_extra[destino]

    def get_nome(self):
        return self.nome

    def get_locais_circundantes(self):
        return self.locais_circundantes

    def get_sentidos(self):
        return self.sentidos

    def get_sentidos_info_extra(self):
        return self.sentidos_info_extra

    #  Informação extra associada à direcção de uma dada via, como a linha de metro ou o serviço ferroviário
    def get_sentido_info_extra(self, direccao):
        if direccao in self.sentidos_info_extra:
            info_extra = self.sentidos_info_extra[direccao]
            if len(info_extra) == 0:
                return None
            if len(info_extra) == 1:
                return info_extra[0]
            info_extra_string = ''
            for unidade_info_extra in info_extra:
                info_extra_string = info_extra_string + ' ' + SEPARADOR_DESTINOS + ' ' + unidade_info_extra
            return info_extra_string[3:]  # Os primeiros caracteres estão a mais
        return None

    #  Destinos principais seguindo por uma certa direcção de, por exemplo, uma via rápida ou uma via férrea
    def get_sentido(self, direccao):
        if direccao in self.sentidos:
            destinos = self.sentidos[direccao]
            if len(destinos) == 1:
                return destinos[0]
            destinos_string = ''
            for destino in destinos:
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

    def get_info_extra(self):
        return self.info_extra

    def imprimir_info_breve(self):
        print("Está em", self.nome)

    def imprimir_info_completa(self):
        print("Informação não disponível")
