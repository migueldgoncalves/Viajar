"""
Road and railway names to be processed by the automatic information generator
"""


class Way:
    """
    Data access object representing a way, either a road or a railway. Does not represent an OSM way
    """
    def __init__(self, display_name: str, osm_name: str, country: str, way_type: str):
        """
        Initializer
        :param display_name: Custom and translatable name. Will be inserted in the names of the files storing the way info
        :param osm_name: Name of the way in OSM. Must be in the local language (Portuguese, Spanish, Catalan, etc)
        :param country: Country of the way. It is assumed a way always belongs to a single country
        :param way_type: Road or railway
        """
        assert display_name
        assert osm_name
        assert country in ALL_SUPPORTED_COUNTRIES
        assert way_type in [ROAD, RAILWAY]

        self.display_name = display_name
        self.osm_name = osm_name
        self.country = country
        self.way_type = way_type


# Way types

ROAD = 'Road'
RAILWAY = 'Railway'

# Countries

ANDORRA = "AD"
CANARY_ISLANDS = "ES-CN"  # Part of Spain, in different server
GIBRALTAR = "GI"
PORTUGAL = "PT"
SPAIN = "ES"
ALL_SUPPORTED_COUNTRIES = [ANDORRA, CANARY_ISLANDS, GIBRALTAR, PORTUGAL, SPAIN]

# Freeways and highways

ES_A1 = Way("A-1", "Autovía del Norte", SPAIN, ROAD)
ES_A2 = Way("A-2", "Autovía del Nordeste", SPAIN, ROAD)
ES_A3 = Way("A-3", "Autovía del Este", SPAIN, ROAD)
ES_A4 = Way("A-4", "Autovía del Sur", SPAIN, ROAD)
ES_A5 = Way("A-5", "Autovía del Suroeste", SPAIN, ROAD)
ES_A6 = Way("A-6", "Autovía del Noroeste", SPAIN, ROAD)
ES_A7 = Way("A-7", "Autovía del Mediterráneo", SPAIN, ROAD)
ES_A8 = Way("A-8", "Autovía del Cantábrico", SPAIN, ROAD)
ES_A10 = Way("A-10", "Autovía de la Barranca", SPAIN, ROAD)
ES_A42 = Way("A-42", "Autovía de Toledo", SPAIN, ROAD)
ES_A44 = Way("A-44", "Autovía de Sierra Nevada-Costa Tropical", SPAIN, ROAD)
ES_A45 = Way("A-45", "Autovía de Málaga", SPAIN, ROAD)
ES_A49 = Way("A-49", "Autopista del Quinto Centenario", SPAIN, ROAD)
ES_A50 = Way("A-50", "Autovía Ávila-Salamanca", SPAIN, ROAD)
ES_A52 = Way("A-52", "Autovía de las Rías Baixas", SPAIN, ROAD)
ES_A55 = Way("A-55", "Autovía do Atlántico", SPAIN, ROAD)
ES_A58 = Way("A-58", "Autovía Trujillo-Cáceres", SPAIN, ROAD)
ES_A62 = Way("A-62", "Autovía de Castilla", SPAIN, ROAD)
ES_A66 = Way("A-66", "Autovía Ruta de la Plata", SPAIN, ROAD)
ES_A92 = Way("A-92", "Autovía de Andalucía", SPAIN, ROAD)
ES_A92M = Way("A-92M", "Autovía A-92 Málaga", SPAIN, ROAD)
ES_A92N = Way("A-92N", "Autovía A-92 Norte", SPAIN, ROAD)
ES_A483 = Way("A-483", "Bollullos-Matalascañas", SPAIN, ROAD)
ES_A497 = Way("A-497", "Autovía de Huelva a Punta Umbría", SPAIN, ROAD)
ES_AP1 = Way("AP-1", "Autopista del Norte", SPAIN, ROAD)
ES_AP2 = Way("AP-2", "Autopista Zaragoza-Mediterráneo", SPAIN, ROAD)
ES_AP4 = Way("AP-4", "Autopista del Sur", SPAIN, ROAD)
ES_AP6 = Way("AP-6", "Autopista del Noroeste", SPAIN, ROAD)
ES_AP7 = Way("AP-7", "Autopista del Mediterráneo", SPAIN, ROAD)
ES_AP8 = Way("AP-8", "Autopista del Cantábrico", SPAIN, ROAD)
ES_AP9 = Way("AP-9", "Autoestrada do Atlántico", SPAIN, ROAD)
ES_AP51 = Way("AP-51", "Conexión Ávila", SPAIN, ROAD)
ES_AV20 = Way("AV-20", "Circunvalación de Ávila", SPAIN, ROAD)
ES_EXA1 = Way("EX-A1", "Autovía del Norte de Extremadura", SPAIN, ROAD)
ES_EXA2 = Way("EX-A2", "Autovía de las Vegas Altas", SPAIN, ROAD)
ES_GR30 = Way("GR-30", "Circunvalación de Granada", SPAIN, ROAD)
ES_H30 = Way("H-30", "Ronda Exterior Norte", SPAIN, ROAD)
ES_M30 = Way("M-30", "Autovía de Circunvalación M-30", SPAIN, ROAD)
ES_M40 = Way("M-40", "Autopista de Circunvalación M-40", SPAIN, ROAD)
ES_M45 = Way("M-45", "Autopista de Circunvalación M-45", SPAIN, ROAD)
ES_M50 = Way("M-50", "Autopista de Circunvalación M-50", SPAIN, ROAD)
ES_R2 = Way("R-2", "Radial R-2", SPAIN, ROAD)
ES_R3 = Way("R-3", "Radial R-3", SPAIN, ROAD)
ES_R4 = Way("R-4", "Radial R-4", SPAIN, ROAD)
ES_R5 = Way("R-5", "Radial R-5", SPAIN, ROAD)

PT_A1 = Way("A1", "Autoestrada do Norte", PORTUGAL, ROAD)
PT_A2 = Way("A2", "Autoestrada do Sul", PORTUGAL, ROAD)
PT_A3 = Way("A3", "Autoestrada de Entre-Douro-e-Minho", PORTUGAL, ROAD)
PT_A4 = Way("A4", "Autoestrada Transmontana", PORTUGAL, ROAD)
PT_A5 = Way("A5", "Autoestrada da Costa do Estoril", PORTUGAL, ROAD)
PT_A6 = Way("A6", "Autoestrada do Alentejo Central", PORTUGAL, ROAD)
PT_A7 = Way("A7", "Autoestrada do Douro", PORTUGAL, ROAD)
PT_A8 = Way("A8", "Autoestrada do Oeste", PORTUGAL, ROAD)
PT_A8_1 = Way("A8-1", "Circular Oriental de Leiria", PORTUGAL, ROAD)
PT_A9 = Way("A9 CREL", "Circular Regional Exterior de Lisboa (CREL)", PORTUGAL, ROAD)
PT_A10 = Way("A10", "Autoestrada do Ribatejo", PORTUGAL, ROAD)
PT_A11 = Way("A11", "Autoestrada do Baixo Minho", PORTUGAL, ROAD)
PT_A12 = Way("A12", "Autoestrada do Sul do Tejo", PORTUGAL, ROAD)
PT_A13 = Way("A13", "Autoestrada do Pinhal Interior", PORTUGAL, ROAD)
PT_A13_1 = Way("A13-1", "Radial de Coimbra", PORTUGAL, ROAD)
PT_A14 = Way("A14", "Autoestrada do Baixo Mondego", PORTUGAL, ROAD)
PT_A15 = Way("A15", "Autoestrada do Atlântico", PORTUGAL, ROAD)
PT_A16 = Way("A16", "Circular Exterior da Área Metropolitana de Lisboa", PORTUGAL, ROAD)
PT_A17 = Way("A17", "Autoestrada do Litoral Centro", PORTUGAL, ROAD)
# A18 is in project
PT_A19 = Way("A19", "Variante da Batalha", PORTUGAL, ROAD)
PT_A20 = Way("A20", "Circular Regional Interior do Porto", PORTUGAL, ROAD)
PT_A21 = Way("A21", "Autoestrada de Mafra", PORTUGAL, ROAD)
PT_A22 = Way("A22", "Via do Infante", PORTUGAL, ROAD)
PT_A23 = Way("A23", "Autoestrada da Beira Interior", PORTUGAL, ROAD)
PT_A24 = Way("A24", "Autoestrada do Interior Norte", PORTUGAL, ROAD)
PT_A25 = Way("A25", "Autoestrada das Beiras Litoral e Alta", PORTUGAL, ROAD)
PT_A26 = Way("A26", "Autoestrada do Baixo Alentejo", PORTUGAL, ROAD)
PT_A26_1 = Way("A26-1", "Variante de Sines", PORTUGAL, ROAD)
PT_A27 = Way("A27", "Autoestrada do Vale do Lima", PORTUGAL, ROAD)
PT_A28 = Way("A28", "Autoestrada do Litoral Norte", PORTUGAL, ROAD)
PT_A29 = Way("A29", "Autoestrada da Costa de Prata", PORTUGAL, ROAD)
# A30 corresponds to a stretch of the IC2 highway in Lisbon
# A31 corresponds to a stretch of the IC2 highway in Coimbra
PT_A32 = Way("A32", "Autoestrada de Entre Douro-e-Vouga", PORTUGAL, ROAD)
PT_A33 = Way("A33", "Circular Regional Interior da Península de Setúbal (CRIPS)", PORTUGAL, ROAD)
# A34 corresponds to a stretch of the IC8 highway in Pombal
# A35 corresponds to the IC12 highway
# A36 corresponds to the IC17 highway
# A37 corresponds to the IC19 highway
# A38 corresponds to the IC20 highway
# A39 corresponds to the IC21 highway
# A40 corresponds to the IC22 highway
PT_A41 = Way("A41 CREP", "Circular Regional Exterior do Porto", PORTUGAL, ROAD)
PT_A42 = Way("A42", "Autoestrada do Douro Litoral", PORTUGAL, ROAD)
PT_A43 = Way("A43", "Radial de Gondomar", PORTUGAL, ROAD)
PT_A44 = Way("A44", "Autoestrada de Vila Nova de Gaia", PORTUGAL, ROAD)
PT_CSB = Way("Braga South Circular", "Circular Sul de Braga", PORTUGAL, ROAD)
PT_IC17 = Way("IC17 CRIL", "Circular Regional Interior de Lisboa (CRIL)", PORTUGAL, ROAD)
PT_IC22 = Way("IC22", "Radial de Odivelas", PORTUGAL, ROAD)
PT_IC27 = Way("IC27", "IC 27", PORTUGAL, ROAD)
PT_VRI = Way("VRI", "Via Regional Interior", PORTUGAL, ROAD)

# Railways

ES_CIUDAD_REAL_BADAJOZ = Way("Ciudad Real-Badajoz Line", "Ciudad Real-Badajoz", SPAIN, RAILWAY)
ES_MADRID_CERCANIAS_C3 = Way("Madrid Suburban Trains - C-3 Line", "Tren C-3: Chamartín -> Sol -> Atocha -> Aranjuez", SPAIN, RAILWAY)
ES_MADRID_METRO_LINE_8 = Way("Madrid Metro - Line 8", "Línea 8: Nuevos Ministerios-Aeropuerto T4", SPAIN, RAILWAY)

PT_ALFARELOS_BRANCH_LINE = Way("Alfarelos Branch Line", "Ramal de Alfarelos", PORTUGAL, RAILWAY)
PT_BEIRA_ALTA_LINE = Way("Beira Alta Line", "Linha da Beira Alta", PORTUGAL, RAILWAY)
PT_BEIRA_BAIXA_LINE = Way("Beira Baixa Line", "Linha da Beira Baixa", PORTUGAL, RAILWAY)
PT_BRAGA_BRANCH_LINE = Way("Braga Branch Line", "Ramal de Braga", PORTUGAL, RAILWAY)
PT_BRAGA_LINE = Way("Braga Line", "Linha de Braga", PORTUGAL, RAILWAY)
PT_CASCAIS_LINE = Way("Cascais Line", "Linha de Cascais", PORTUGAL, RAILWAY)
PT_CINTURA_LINE = Way("Cintura Line", "Linha de Cintura", PORTUGAL, RAILWAY)
PT_DOURO_LINE = Way("Douro Line", "Linha do Douro", PORTUGAL, RAILWAY)
PT_EAST_LINE = Way("East Line", "Linha do Leste", PORTUGAL, RAILWAY)
PT_GUIMARAES_LINE = Way("Guimarães Line", "Linha de Guimarães", PORTUGAL, RAILWAY)
PT_LISBON_METRO_RED_LINE = Way("Lisbon Metro - Red Line", "Linha Vermelha: São Sebastião → Aeroporto", PORTUGAL, RAILWAY)
PT_MINHO_LINE = Way("Minho Line", "Linha do Minho", PORTUGAL, RAILWAY)
PT_NORTH_LINE = Way("North Line", "Linha do Norte", PORTUGAL, RAILWAY)
PT_SINTRA_LINE = Way("Sintra Line", "Linha de Sintra", PORTUGAL, RAILWAY)
PT_SOUTH_LINE = Way("South Line", "Linha do Sul", PORTUGAL, RAILWAY)
PT_TOMAR_BRANCH_LINE = Way("Tomar Branch Line", "Ramal de Tomar", PORTUGAL, RAILWAY)
PT_VOUGA_LINE = Way("Vouga Line", "Linha do Vouga", PORTUGAL, RAILWAY)
PT_WEST_LINE = Way("West Line", "Linha do Oeste", PORTUGAL, RAILWAY)
