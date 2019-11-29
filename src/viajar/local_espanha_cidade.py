from viajar import local_espanha, locais


class LocalEspanhaCidade(local_espanha.LocalEspanha):

    distrito = ''

    def __init__(self, nome, locais_circundantes, latitude, longitude, altitude, municipio, comarca, provincia,
                 distrito):
        super().__init__(nome, locais_circundantes, latitude, longitude, altitude, municipio, comarca, provincia)
        self.set_distrito(distrito)

    def set_distrito(self, distrito):
        self.distrito = distrito

    def get_distrito(self):
        return self.distrito

    def imprimir_info_completa(self):
        if self.altitude == 1:
            print("Altitude:", self.altitude, "metro")
        else:
            print("Altitude:", self.altitude, "metros")
        print("Coordenadas:", str(self.coordenadas[0]) + ",", self.coordenadas[1])
        print("Distrito:", self.distrito)
        print("Município:", self.municipio)
        print("Comarca:", self.comarca)
        print("Província:", self.provincia)
        print("Comunidade Autónoma:", self.comunidade_autonoma)
        print("País:", self.pais)