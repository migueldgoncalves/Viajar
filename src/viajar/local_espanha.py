from viajar import local


class LocalEspanha(local.Local):

    def __init__(self, nome, locais_circundantes, latitude, longitude, altitude, municipio, comarcas, provincia,
                 comunidade_autonoma):
        super().__init__(nome, locais_circundantes, latitude, longitude, altitude)
        self.distrito = ''  # Na Galiza pode guardar o nome da paróquia (nível equivalente no OpenStreetMap)
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

    #  Ex: Ayamonte, Província de Huelva, Andaluzia
    def imprimir_info_breve(self):
        nome = self.nome.split(",")[0]  # Ex: "Álamo, Alcoutim" e "Álamo, Mértola" -> Álamo
        if LocalEspanha.is_comunidade_uniprovincial(self.comunidade_autonoma):
            print("Está em", nome + ",", self.municipio + ",", self.comunidade_autonoma)
        else:
            print("Está em", nome + ",", self.municipio + ",", "Província de", self.provincia + ",",
                  self.comunidade_autonoma)

    def imprimir_info_completa(self):
        super().imprimir_info_completa()
        if self.distrito != '':
            if self.comunidade_autonoma == 'Galiza':  # Na Galiza os municípios (localmente, concellos) subdividem-se em paróquias (parroquias)
                print("Paróquia:", self.distrito)  # Mesmo nível administrativo no OpenStreetMap
            elif self.comunidade_autonoma == 'Região de Murcia':
                print("Pedanía:", self.distrito)
            else:
                print("Distrito:", self.distrito)
        if self.comunidade_autonoma == 'Galiza':
            print("Concelho:", self.municipio)  # Na Galiza, concellos
        else:
            print("Município:", self.municipio)
        if len(self.comarcas) == 0:
            if self.comunidade_autonoma == "Extremadura":
                #  A Extremadura tem uma segunda entidade semelhante à comarca, a mancomunidade integral
                print("Mancomunidade integral: Nenhuma")
            else:
                print("Comarca: Nenhuma")  # Termo genérico
        elif len(self.comarcas) == 1:
            if self.comunidade_autonoma == "Extremadura":
                print("Mancomunidade integral:", self.comarcas[0])
            else:
                print("Comarca:", self.comarcas[0])
        else:
            comarca_string = ''
            for comarca in self.comarcas:
                comarca_string = comarca_string + ', ' + comarca
            print("Comarcas:", comarca_string[2:])  # Os primeiros caracteres estão a mais
        if not LocalEspanha.is_comunidade_uniprovincial(self.comunidade_autonoma):
            print("Província:", self.provincia)  # Comunidades autónomas uniprovinciais não têm governos provinciais
        print("Comunidade Autónoma:", self.comunidade_autonoma)
        print("País:", self.pais)

    @staticmethod
    def is_comunidade_uniprovincial(comunidade_autonoma):
        return comunidade_autonoma in ["Comunidade de Madrid", "Região de Murcia"]
