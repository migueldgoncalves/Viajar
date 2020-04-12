from viajar import local, nomes


class LocalEspanha(local.Local):

    distrito = ''
    municipio = ''
    comarca = ''
    provincia = ''
    comunidade_autonoma = ''

    def __init__(self, nome, locais_circundantes, latitude, longitude, altitude, municipio, comarca, provincia):
        super().__init__(nome, locais_circundantes, latitude, longitude, altitude)
        self.distrito = ''
        self.set_municipio(municipio)
        self.set_comarca(comarca)
        self.set_provincia(provincia)
        self.set_pais(nomes.ESPANHA)
        self.calcular_entidades_geograficas()

    def set_distrito(self, distrito):
        self.distrito = distrito

    def set_municipio(self, municipio):
        self.municipio = municipio

    def set_comarca(self, comarca):
        self.comarca = comarca

    def set_provincia(self, provincia):
        self.provincia = provincia

    def set_comunidade_autonoma(self, comunidade_autonoma):
        self.comunidade_autonoma = comunidade_autonoma

    def get_distrito(self):
        return self.distrito

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
        if self.provincia in nomes.provincias_andalucia:
            self.set_comunidade_autonoma(nomes.ANDALUCIA)

    #  Ex: Ayamonte, Província de Huelva, Andalucía
    def imprimir_info_breve(self):
        nome = self.nome.split(",")[0]  # Ex: "Álamo, Alcoutim" e "Álamo, Mértola" -> Álamo
        print("Está em", nome + ",", self.municipio + ",", "Província de", self.provincia + ",",
              self.comunidade_autonoma)

    def imprimir_info_completa(self):
        if self.altitude == 1:
            print("Altitude:", self.altitude, "metro")
        else:
            print("Altitude:", self.altitude, "metros")
        print("Coordenadas:", str(self.coordenadas[0]) + ",", self.coordenadas[1])
        if self.info_extra != '':
            print(self.info_extra)
        if self.distrito != '':
            print("Distrito:", self.distrito)
        print("Município:", self.municipio)
        print("Comarca:", self.comarca)
        print("Província:", self.provincia)
        print("Comunidade Autónoma:", self.comunidade_autonoma)
        print("País:", self.pais)
