#  Países
ESPANHA = "Espanha"
PORTUGAL = "Portugal"


#  #  #  #  #
#  Espanha  #
#  #  #  #  #

#  Comunidades autónomas
ANDALUCIA = "Andalucía"

#  Províncias
PROVINCIA_HUELVA = "Huelva"
PROVINCIA_SEVILHA = "Sevilha"
provincias_andalucia = [PROVINCIA_HUELVA, PROVINCIA_SEVILHA]

#  Comarcas da Andalucía
COMARCA_ALJARAFE = "Aljarafe"
COMARCA_METROPOLITANA_HUELVA = "Comarca Metropolitana de Huelva"
COMARCA_METROPOLITANA_SEVILHA = "Comarca Metropolitana de Sevilha"
COMARCA_COSTA_OCCIDENTAL_HUELVA = "Costa Occidental de Huelva"
COMARCA_EL_ANDEVALO = "El Andévalo"
COMARCA_EL_CONDADO = "El Condado"

#  Municípios da Andalucía
MUNICIPIO_AYAMONTE = "Ayamonte"
MUNICIPIO_BOLLULLOS_PAR_CONDADO = "Bollullos Par del Condado"
MUNICIPIO_BORMUJOS = "Bormujos"
MUNICIPIO_CAMAS = "Camas"
MUNICIPIO_CARTAYA = "Cartaya"
MUNICIPIO_CASTILLEJA_DE_LA_CUESTA = "Castilleja de la Cuesta"
MUNICIPIO_ESPARTINAS = "Espartinas"
MUNICIPIO_GIBRALEON = "Gibraleón"
MUNICIPIO_HUELVA = "Huelva"
MUNICIPIO_ISLA_CRISTINA = "Isla Cristina"
MUNICIPIO_LEPE = "Lepe"
MUNICIPIO_SAN_JUAN_AZNALFARACHE = "San Juan de Aznalfarache"
MUNICIPIO_SEVILHA = "Sevilha"

#  Distritos de Sevilha
DISTRITO_ESTE_ALCOSA_TORREBLANCA = "Este-Alcosa-Torreblanca"
DISTRITO_BELLAVISTA_LA_PALMERA = "Bellavista-La Palmera"
DISTRITO_LOS_REMEDIOS = "Los Remedios"
DISTRITO_TRIANA = "Triana"

#  Estradas
A_4 = "A-4"
A_49 = "A-49"
A_483 = "A-483"
A_66 = "A-66"
H_31 = "H-31"
SE_30 = "SE-30"
SE_40 = "SE-40"


#  #  #  #  #  #
#   Portugal   #
#  #  #  #  #  #

#  Distritos
DISTRITO_BEJA = "Beja"
DISTRITO_FARO = "Faro"

#  Entidades intermunicipais e regiões
BAIXO_ALENTEJO = "Baixo Alentejo"
ALGARVE = "Algarve"

#  Concelhos do Distrito de Beja
CONCELHO_BEJA = "Beja"
CONCELHO_MERTOLA = "Mértola"
CONCELHO_SERPA = "Serpa"
concelhos_beja = [CONCELHO_BEJA, CONCELHO_MERTOLA, CONCELHO_SERPA]

#  Concelhos do Distrito de Faro
CONCELHO_ALCOUTIM = "Alcoutim"
CONCELHO_CASTRO_MARIM = "Castro Marim"
CONCELHO_FARO = "Faro"
CONCELHO_LOULE = "Loulé"
CONCELHO_OLHAO = "Olhão"
CONCELHO_SAO_BRAS_ALPORTEL = "São Brás de Alportel"
CONCELHO_TAVIRA = "Tavira"
CONCELHO_VRSA = "Vila Real de Santo António"
concelhos_faro = [CONCELHO_ALCOUTIM, CONCELHO_CASTRO_MARIM, CONCELHO_FARO, CONCELHO_LOULE, CONCELHO_OLHAO,
                  CONCELHO_SAO_BRAS_ALPORTEL, CONCELHO_TAVIRA, CONCELHO_VRSA]

#  Concelhos das entidades intermunicipais e regiões
algarve = [CONCELHO_ALCOUTIM, CONCELHO_CASTRO_MARIM, CONCELHO_FARO, CONCELHO_LOULE, CONCELHO_OLHAO,
           CONCELHO_SAO_BRAS_ALPORTEL, CONCELHO_TAVIRA, CONCELHO_VRSA]
baixo_alentejo_entidade = [CONCELHO_BEJA, CONCELHO_MERTOLA, CONCELHO_SERPA]
baixo_alentejo_regiao = [CONCELHO_BEJA, CONCELHO_MERTOLA, CONCELHO_SERPA]

#  Freguesias do Algarve
FREGUESIA_ALCOUTIM = "Alcoutim"
FREGUESIA_ALTURA = "Altura"
FREGUESIA_CACHOPO = "Cachopo"
FREGUESIA_CASTRO_MARIM = "Castro Marim"
FREGUESIA_ESTOI = "Estoi"
FREGUESIA_GIOES = "Giões"
FREGUESIA_MARTINLONGO = "Martinlongo"
FREGUESIA_MONCARAPACHO = "Moncarapacho"
FREGUESIA_MONTE_GORDO = "Monte Gordo"
FREGUESIA_MONTENEGRO = "Montenegro"
FREGUESIA_PEREIRO = "Pereiro"
FREGUESIA_SALIR = "Salir"
FREGUESIA_SANTIAGO_TAVIRA = "Santiago"
FREGUESIA_SAO_BRAS_ALPORTEL = "São Brás de Alportel"
FREGUESIA_VAQUEIROS = "Vaqueiros"
FREGUESIA_VILA_NOVA_CACELA = "Vila Nova de Cacela"
FREGUESIA_VRSA = "Vila Real de Santo António"

#  Freguesias do Baixo Alentejo
FREGUESIA_SAO_BRISSOS = "São Brissos"
FREGUESIA_SERPA = "Serpa"
FREGUESIA_VILA_NOVA_SAO_BENTO = "Vila Nova de São Bento"

#  Estradas
A22 = "A22"
IC27 = "IC27"
IP2 = "IP2"
N122 = "N122"
N123 = "N123"
N125 = "N125"
N125_6 = "N125-6"
N265 = "N265"
N392 = "N392"
M507 = "M507"


#  #  #  #  #  #  #  #  #  #  #  #  #  #  #
#   Funções relativas a nomes de locais   #
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #

def nome_saida_via_rapida(via_rapida, saida):
    #  Ex: IC27 - Fim
    if saida in ["Início", "Fim"]:
        return via_rapida + "-" + saida
    #  Ex: A-49-Saída 1
    else:
        return via_rapida + "-Saída " + str(saida)


def nome_cruzamento_estradas(estrada1, estrada2):
    artigo1 = verificador_artigo_definido(estrada1)
    artigo2 = verificador_artigo_definido(estrada2)
    #  Ex: Cruzamento da N122 com a N123
    return "Cruzamento d" + artigo1 + " " + estrada1 + " com " + artigo2 + " " + estrada2


#  Verifica o artigo definido ("a", "o") a empregar para se referir a uma estrada
def verificador_artigo_definido(nome):
    if nome[0:1] in ["IP", "IC"]:
        return "o"
    else:
        return "a"
