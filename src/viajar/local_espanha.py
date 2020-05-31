from viajar import local


class LocalEspanha(local.Local):

    def __init__(self, nome, locais_circundantes, latitude, longitude, altitude, municipio, comarcas, provincia,
                 comunidade_autonoma):
        super().__init__(nome, locais_circundantes, latitude, longitude, altitude)
        self.distrito = ''
        self.municipio = municipio
        self.comarcas = comarcas
        self.provincia = provincia
        self.comunidade_autonoma = comunidade_autonoma
        self.pais = 'Espanha'

    def set_distrito(self, distrito):
        self.distrito = distrito

    def set_municipio(self, municipio):
        self.municipio = municipio

    def set_comarcas(self, comarcas):
        self.comarcas = comarcas

    def set_provincia(self, provincia):
        self.provincia = provincia

    def set_comunidade_autonoma(self, comunidade_autonoma):
        self.comunidade_autonoma = comunidade_autonoma

    def get_distrito(self):
        return self.distrito

    def get_municipio(self):
        return self.municipio

    def get_comarcas(self):
        return self.comarcas

    def get_provincia(self):
        return self.provincia

    def get_comunidade_autonoma(self):
        return self.comunidade_autonoma

    #  Ex: Ayamonte, Província de Huelva, Andalucía
    def imprimir_info_breve(self):
        nome = self.nome.split(",")[0]  # Ex: "Álamo, Alcoutim" e "Álamo, Mértola" -> Álamo
        print("Está em", nome + ",", self.municipio + ",", "Província de", self.provincia + ",",
              self.comunidade_autonoma)

    def imprimir_info_completa(self):
        super().imprimir_info_completa()
        if self.distrito != '':
            print("Distrito:", self.distrito)
        print("Município:", self.municipio)
        if len(self.comarcas) == 0:
            print("Comarca: Nenhuma")
        elif len(self.comarcas) == 1:
            print("Comarca:", self.comarcas[0])
        else:
            comarca_string = ''
            for comarca in self.comarcas:
                comarca_string = comarca_string + ', ' + comarca
            print("Comarcas:", comarca_string[2:])  # Os primeiros caracteres estão a mais
        print("Província:", self.provincia)
        print("Comunidade Autónoma:", self.comunidade_autonoma)
        print("País:", self.pais)
