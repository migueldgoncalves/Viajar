from viajar import local


class LocalGibraltar(local.Local):

    def __init__(self, nome, locais_circundantes, latitude, longitude, altitude, major_residential_areas):
        super().__init__(nome, locais_circundantes, latitude, longitude, altitude)
        self.major_residential_areas = major_residential_areas
        self.pais = 'Reino Unido - Gibraltar'

    def set_major_residential_areas(self, major_residential_areas):
        self.major_residential_areas = major_residential_areas

    def get_major_residential_areas(self):
        return self.major_residential_areas

    #  Ex: Fronteira Espanha-Gibraltar - Lado de Gibraltar, Gibraltar
    def imprimir_info_breve(self):
        nome = self.nome.split(",")[0]  # Ex: "Álamo, Alcoutim" e "Álamo, Mértola" -> Álamo
        print("Está em", nome + ", Gibraltar")

    def imprimir_info_completa(self):
        super().imprimir_info_completa()
        if len(self.major_residential_areas) == 1:
            print("Major Residential Area:", self.major_residential_areas[0])
        elif len(self.major_residential_areas) > 1:
            major_residential_area_string = ''
            for major_residential_area in self.major_residential_areas:
                major_residential_area_string = major_residential_area_string + ', ' + major_residential_area
            print("Major Residential Areas:", major_residential_area_string[2:])  # Os primeiros caracteres estão a mais
        print("País:", self.pais)
