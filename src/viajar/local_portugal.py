from viajar import local, nomes


class LocalPortugal(local.Local):

    freguesia = ''
    concelho = ''
    distrito = ''
    entidade_intermunicipal = ''
    regiao = ''

    def __init__(self, nome, locais_circundantes, latitude, longitude, altitude, freguesia, concelho):
        super().__init__(nome, locais_circundantes, latitude, longitude, altitude)
        self.set_freguesia(freguesia)
        self.set_concelho(concelho)
        self.set_pais(nomes.PORTUGAL)
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
        if self.concelho in nomes.concelhos_beja:
            self.set_distrito(nomes.DISTRITO_BEJA)
        elif self.concelho in nomes.concelhos_faro:
            self.set_distrito(nomes.DISTRITO_FARO)

        #  Obter a entidade intermunicipal
        if self.concelho in nomes.baixo_alentejo_entidade:
            self.set_entidade_intermunicipal(nomes.BAIXO_ALENTEJO)
        elif self.concelho in nomes.algarve:
            self.set_entidade_intermunicipal(nomes.ALGARVE)

        #  Obter a região
        if self.concelho in nomes.baixo_alentejo_regiao:
            self.set_regiao(nomes.BAIXO_ALENTEJO)
        elif self.concelho in nomes.algarve:
            self.set_regiao(nomes.ALGARVE)

    #  Ex: Odeleite, Castro Marim, Distrito de Faro
    def imprimir_info_breve(self):
        nome = self.nome.split(",")[0]  # Ex: "Álamo, Alcoutim" e "Álamo, Mértola" -> Álamo
        print("Está em", nome + ",", self.concelho + ", Distrito de", self.distrito)

    def imprimir_info_completa(self):
        if self.altitude == 1:
            print("Altitude:", self.altitude, "metro")
        else:
            print("Altitude:", self.altitude, "metros")
        print("Coordenadas:", str(self.coordenadas[0]) + ",", self.coordenadas[1])
        if self.info_extra != '':
            print(self.info_extra)
        print("Freguesia:", self.freguesia)
        print("Concelho:", self.concelho)
        print("Distrito:", self.distrito)
        print("Entidade Intermunicipal:", self.entidade_intermunicipal)
        print("Região:", self.regiao)
        print("País:", self.pais)
