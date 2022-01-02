SEPARADOR_DESTINOS = "/"


class Local:

    def __init__(self, nome, locais_circundantes, latitude, longitude, altitude):
        self.nome = nome
        self.locais_circundantes = locais_circundantes
        self.sentidos = {}  # Destinos principais seguindo numa direcção. Ex: Beja/Mértola e Castro Marim/VRSA no IC27
        self.sentidos_info_extra = {}  # Informação extra dos sentidos. Ex: Linha 1 do metro, ou comboio Regional
        self.coordenadas = (latitude, longitude)  # Ex: (37.215788, -7.405922)
        self.altitude = altitude  # Metros
        self.pais = ''
        self.info_extra = ''  # Informação extra associada ao local. Ex: Reserva natural
        self.lote = 0  # 100 = Local faz parte dos primeiros 100 locais introduzidos

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

    def set_lote(self, lote):
        self.lote = lote

    def add_local_circundante(self, local, meio_transporte, ponto_cardeal, distancia):
        self.locais_circundantes[(local, meio_transporte)] = [ponto_cardeal, distancia, meio_transporte]

    def add_sentido_info_extra(self, sentido, meio_transporte, info_extra):
        self.sentidos_info_extra[(sentido, meio_transporte)] = info_extra

    def add_sentido(self, destino, sentido, meio_transporte, info_extra):
        self.sentidos[(sentido, meio_transporte)] = destino
        self.add_sentido_info_extra(sentido, meio_transporte, info_extra)

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
    def get_sentido_info_extra(self, direccao, meio_transporte):
        if (direccao, meio_transporte) in self.sentidos_info_extra:
            info_extra = self.sentidos_info_extra[(direccao, meio_transporte)]
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
    def get_sentido(self, direccao, meio_transporte):
        if (direccao, meio_transporte) in self.sentidos:
            destinos = self.sentidos[(direccao, meio_transporte)]
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

    def get_lote(self):
        return self.lote

    def imprimir_info_breve(self):
        print("Está em", self.nome)

    def imprimir_info_completa(self):
        if self.altitude == 1:
            print("Altitude:", self.altitude, "metro")
        else:
            print("Altitude:", self.altitude, "metros")
        print("Coordenadas:", str(self.coordenadas[0]) + ",", self.coordenadas[1])
        if self.info_extra != '':
            print(self.info_extra)
