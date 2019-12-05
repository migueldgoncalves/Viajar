from viajar import local_portugal


class LocalPortugalRiaFormosa(local_portugal.LocalPortugal):

    ilha = ''

    def __init__(self, nome, locais_circundantes, latitude, longitude, altitude, freguesia, concelho, ilha):
        super().__init__(nome, locais_circundantes, latitude, longitude, altitude, freguesia, concelho)
        self.set_ilha(ilha)

    def set_ilha(self, ilha):
        self.ilha = ilha

    def get_ilha(self):
        return self.ilha

    def imprimir_info_completa(self):
        if self.altitude == 1:
            print("Altitude:", self.altitude, "metro")
        else:
            print("Altitude:", self.altitude, "metros")
        print("Coordenadas:", str(self.coordenadas[0]) + ",", self.coordenadas[1])
        print("Ilha da Ria Formosa:", self.ilha)
        print("Freguesia:", self.freguesia)
        print("Concelho:", self.concelho)
        print("Distrito:", self.distrito)
        print("Entidade Intermunicipal:", self.entidade_intermunicipal)
        print("Região:", self.regiao)
        print("País:", self.pais)
