from viajar import local, locais


class LocalEspanha(local.Local):

    municipio = ''
    comarca = ''
    provincia = ''
    comunidade_autonoma = ''

    def __init__(self, nome, locais_circundantes, latitude, longitude, altitude, municipio, comarca, provincia):
        super().__init__(nome, locais_circundantes)
        self.set_coordenadas(latitude, longitude)
        self.set_altitude(altitude)
        self.set_municipio(municipio)
        self.set_comarca(comarca)
        self.set_provincia(provincia)
        self.set_pais(locais.ESPANHA)
        self.calcular_entidades_geograficas()

    def set_municipio(self, municipio):
        self.municipio = municipio

    def set_comarca(self, comarca):
        self.comarca = comarca

    def set_provincia(self, provincia):
        self.provincia = provincia

    def set_comunidade_autonoma(self, comunidade_autonoma):
        self.comunidade_autonoma = comunidade_autonoma

    def get_municipio(self):
        return self.municipio

    def get_comarca(self):
        return self.comarca

    def get_provincia(self):
        return self.provincia

    def get_comunidade_autonoma(self):
        return self.comunidade_autonoma

    #  A província permite obter a comunidade autónoma
    def calcular_entidades_geograficas(self):
        if self.provincia in locais.provincias_andalucia:
            self.set_comunidade_autonoma(locais.ANDALUCIA)

    #  Ex: Ayamonte, Província de Huelva, Andalucía
    def imprimir_info_breve(self):
        print("Está em", self.nome + ",", "Província de", self.provincia + ",", self.comunidade_autonoma)

    def imprimir_info_completa(self):
        if self.altitude == 1:
            print("Altitude:", self.altitude, "metro")
        else:
            print("Altitude:", self.altitude, "metros")
        print("Coordenadas:", str(self.coordenadas[0]) + ",", self.coordenadas[1])
        print("Município:", self.municipio)
        print("Comarca:", self.comarca)
        print("Província:", self.provincia)
        print("Comunidade Autónoma:", self.comunidade_autonoma)
        print("País:", self.pais)
