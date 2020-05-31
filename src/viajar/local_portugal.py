from viajar import local


class LocalPortugal(local.Local):

    def __init__(self, nome, locais_circundantes, latitude, longitude, altitude, freguesia, concelho, distrito,
                 entidade_intermunicipal, regiao):
        super().__init__(nome, locais_circundantes, latitude, longitude, altitude)
        self.freguesia = freguesia
        self.concelho = concelho
        self.distrito = distrito
        self.entidade_intermunicipal = entidade_intermunicipal
        self.regiao = regiao
        self.pais = 'Portugal'

    def set_freguesia(self, freguesia):
        self.freguesia = freguesia

    def set_concelho(self, concelho):
        self.concelho = concelho

    def set_distrito(self, distrito):
        self.distrito = distrito

    def set_entidade_intermunicipal(self, entidade_intermunicipal):
        self.entidade_intermunicipal = entidade_intermunicipal

    def set_regiao(self, regiao):
        self.regiao = regiao

    def get_freguesia(self):
        return self.freguesia

    def get_concelho(self):
        return self.concelho

    def get_distrito(self):
        return self.distrito

    def get_entidade_intermunicipal(self):
        return self.entidade_intermunicipal

    def get_regiao(self):
        return self.regiao

    #  Ex: Odeleite, Castro Marim, Distrito de Faro
    def imprimir_info_breve(self):
        nome = self.nome.split(",")[0]  # Ex: "Álamo, Alcoutim" e "Álamo, Mértola" -> Álamo
        print("Está em", nome + ",", self.concelho + ", Distrito de", self.distrito)

    def imprimir_info_completa(self):
        super().imprimir_info_completa()
        print("Freguesia:", self.freguesia)
        print("Concelho:", self.concelho)
        print("Distrito:", self.distrito)
        print("Entidade Intermunicipal:", self.entidade_intermunicipal)
        print("Região:", self.regiao)
        print("País:", self.pais)
