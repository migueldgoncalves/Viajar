from viajar import local

DISTRITO_BEJA = "Beja"
DISTRITO_FARO = "Faro"

#  Distrito de Beja
CONCELHO_BEJA = "Beja"
CONCELHO_MERTOLA = "Mértola"
CONCELHO_SERPA = "Serpa"

#  Distrito de Faro
CONCELHO_ALCOUTIM = "Alcoutim"
CONCELHO_CASTRO_MARIM = "Castro Marim"
CONCELHO_FARO = "Faro"
CONCELHO_OLHAO = "Olhão"
CONCELHO_TAVIRA = "Tavira"
CONCELHO_VRSA = "Vila Real de Santo António"

#  Entidades intermunicipais e regiões
BAIXO_ALENTEJO = "Baixo Alentejo"
ALGARVE = "Algarve"


class LocalPortugal(local.Local):

    concelhos_beja = [CONCELHO_BEJA, CONCELHO_MERTOLA, CONCELHO_SERPA]
    concelhos_faro = [CONCELHO_ALCOUTIM, CONCELHO_CASTRO_MARIM, CONCELHO_FARO, CONCELHO_OLHAO, CONCELHO_TAVIRA,
                      CONCELHO_VRSA]

    baixo_alentejo_entidade = [CONCELHO_BEJA, CONCELHO_MERTOLA, CONCELHO_SERPA]
    baixo_alentejo_regiao = [CONCELHO_BEJA, CONCELHO_MERTOLA, CONCELHO_SERPA]
    algarve = [CONCELHO_ALCOUTIM, CONCELHO_CASTRO_MARIM, CONCELHO_FARO, CONCELHO_OLHAO, CONCELHO_TAVIRA,
               CONCELHO_VRSA]

    freguesia = ''
    concelho = ''
    distrito = ''
    entidade_intermunicipal = ''
    regiao = ''

    def __init__(self, nome, locais_circundantes, freguesia, concelho):
        super().__init__(nome, locais_circundantes)
        self.set_freguesia(freguesia)
        self.set_concelho(concelho)
        self.calcular_entidades_geograficas()

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

    #  O concelho permite obter o distrito, a entidade intermunicipal e a região
    def calcular_entidades_geograficas(self):
        #  Obter o distrito
        if self.concelho in self.concelhos_beja:
            self.set_distrito(DISTRITO_BEJA)
        elif self.concelho in self.concelhos_faro:
            self.set_distrito(DISTRITO_FARO)

        #  Obter a entidade intermunicipal
        if self.concelho in self.baixo_alentejo_entidade:
            self.set_entidade_intermunicipal(BAIXO_ALENTEJO)
        elif self.concelho in self.algarve:
            self.set_entidade_intermunicipal(ALGARVE)

        #  Obter a região
        if self.concelho in self.baixo_alentejo_regiao:
            self.set_regiao(BAIXO_ALENTEJO)
        elif self.concelho in self.algarve:
            self.set_regiao(ALGARVE)

    #  Ex: Odeleite, Castro Marim, Distrito de Faro
    def imprimir_info_breve(self):
        print("Está em", self.nome, ",", self.concelho, ", Distrito de", self.distrito)

    def imprimir_info_completa(self):
        print("Altitude:", self.altitude, "metros")
        print("Coordenadas:", self.coordenadas[0], ",", self.coordenadas[1])
        print("Freguesia:", self.freguesia)
        print("Concelho:", self.concelho)
        print("Distrito:", self.distrito)
        print("Entidade intermunicipal:", self.entidade_intermunicipal)
        print("Região:", self.regiao)
        print("País:", self.pais)