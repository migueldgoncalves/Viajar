import local

#  Pontos cardeais
NORTE = "N"
NORDESTE = "NE"
ESTE = "E"
SUDESTE = "SE"
SUL = "S"
SUDOESTE = "SO"
OESTE = "O"
NOROESTE = "NO"

#  Modos de viagem
CARRO = 1
BARCO = 2
AVIAO = 3
COMBOIO = 4
METRO = 5

#  Nomes dos locais
A_49_SAIDA_125 = "A-49-Saída 125"
A_49_SAIDA_129 = "A-49-Saída 129"
A_49_SAIDA_131 = "A-49-Saída 131"
A22_SAIDA_18 = "A22-Saída 18"
ALAMO = "Álamo"
ALAMO_MERTOLA = "Álamo, Mértola"
ALCARIA = "Alcaria"
ALCOUTIM = "Alcoutim"
ALMADA_DE_OURO = "Almada de Ouro"
ALTA_MORA = "Alta Mora"
AREA_REPOUSO_CASTRO_MARIM = "Área de Repouso de Castro Marim"
AYAMONTE = "Ayamonte"
AZINHAL = "Azinhal"
BALURCO_DE_BAIXO = "Balurco de Baixo"
BALURCO_DE_CIMA = "Balurco de Cima"
BAR_DO_RIO = "Bar do Rio"
BARRAGEM_DE_ODELEITE = "Barragem de Odeleite"
BARRAGEM_DO_BELICHE = "Barragem do Beliche"
BARRANCO_DAS_PEREIRAS = "Barranco das Pereiras"
BOAVISTA = "Boavista"
CAMPO_GOLFE_CASTRO_MARIM = "Campo de Golfe de Castro Marim"
CASA_BRANCA = "Casa Branca"
CASTRO_MARIM = "Castro Marim"
CHOCA_QUEIMADA = "Choça Queimada"
CORTE_DAS_DONAS = "Corte das Donas"
CORTES_PEREIRAS = "Cortes Pereiras"
CORTE_TABELIAO = "Corte Tabelião"
COSTA_ESURI = "Costa Esuri"
EL_GRANADO = "El Granado"
ENTRONCAMENTO_FIM_IC27 = "Entroncamento a seguir ao IC27"
ESPIRITO_SANTO = "Espírito Santo"
FONTE_DO_PENEDO = "Fonte do Penedo"
FOZ_DE_ODELEITE = "Foz de Odeleite"
FURNAZINHAS = "Furnazinhas"
GIOES = "Giões"
GUERREIROS_DO_RIO = "Guerreiros do Rio"
IC27_FIM = "IC27-Fim"
IC27_INICIO = "IC27-Início"
IC27_SAIDA_1 = "IC27-Saída 1"
IC27_SAIDA_2 = "IC27-Saída 2"
IC27_SAIDA_3 = "IC27-Saída 3"
IC27_SAIDA_4 = "IC27-Saída 4"
IC27_SAIDA_5 = "IC27-Saída 5"
IC27_SAIDA_6 = "IC27-Saída 6"
IC27_SAIDA_7 = "IC27-Saída 7"
JUNQUEIRA = "Junqueira"
LARANJEIRAS = "Laranjeiras"
MARTINLONGO = "Martinlongo"
MERTOLA = "Mértola"
MONTE_FERNANDES = "Monte Fernandes"
MONTE_FRANCISCO = "Monte Francisco"
MONTINHO_DAS_LARANJEIRAS = "Montinho das Laranjeiras"
ODELEITE = "Odeleite"
PALMEIRA = "Palmeira"
PARQUE_EMPRESARIAL_ALCOUTIM = "Parque Empresarial de Alcoutim"
PENHA_DA_AGUIA = "Penha da Águia"
PEREIRO = "Pereiro"
PICARRAL = "Piçarral"
PICOITOS = "Picoitos"
POMARAO = "Pomarão"
PONTE_INTERNACIONAL_GUADIANA = "Ponte Internacional do Guadiana"
PONTE_RIO_CHANCA = "Ponte sobre o Rio Chança"
PORTELA_ALTA = "Portela Alta"
PUERTO_DE_LA_LAJA = "Puerto de la Laja"
QUEBRADAS = "Quebradas"
RIBEIRA_DO_VASCAO = "Ribeira do Vascão"
ROTUNDA_DA_ARVORE = "Rotunda da Árvore"
SALGUEIROS = "Salgueiros"
SAN_SILVESTRE_DE_GUZMAN = "San Silvestre de Guzmán"
SANLUCAR_DEL_GUADIANA = "Sanlúcar del Guadiana"
SANTA_MARTA = "Santa Marta"
SAPAL = "Sapal"
SENTINELA = "Sentinela"
TENENCIA = "Tenência"
VAQUEIROS = "Vaqueiros"
VILLABLANCA = "Villablanca"
VILLANUEVA_DE_LOS_CASTILLEJOS = "Villanueva de los Castillejos"
VRSA = "Vila Real de Santo António"

#  Distâncias (km)
A_49_SAIDA_125__VILLABLANCA = 6.1
A_49_SAIDA_125__A_49_SAIDA_129 = 3.9
A_49_SAIDA_129__A_49_SAIDA_131 = 2.3
A_49_SAIDA_129__AYAMONTE = 8.0
A_49_SAIDA_131__AYAMONTE = 3.4
A_49_SAIDA_131__COSTA_ESURI = 2.5
A_49_SAIDA_131__PONTE_INTERNACIONAL_GUADIANA = 1.3
A22_SAIDA_18__AREA_REPOUSO_CASTRO_MARIM = 1.1
A22_SAIDA_18__CASTRO_MARIM = 1.7
A22_SAIDA_18__IC27_INICIO = 0.5
ALAMO__ROTUNDA_DA_ARVORE = 0.5
ALAMO__BARRANCO_DAS_PEREIRAS = 1.2
ALAMO_MERTOLA__BOAVISTA = 7.1
ALAMO_MERTOLA__ESPIRITO_SANTO = 5.8
ALAMO_MERTOLA__MERTOLA = 8.0
ALCARIA__FOZ_DE_ODELEITE = 3.5
ALCARIA__ODELEITE = 3.4
ALCARIA__FONTE_DO_PENEDO = 0.9
ALCOUTIM__CORTES_PEREIRAS = 6.0
ALCOUTIM__CORTE_TABELIAO = 5.0
ALCOUTIM__MONTINHO_DAS_LARANJEIRAS = 8.8
ALCOUTIM__PARQUE_EMPRESARIAL_ALCOUTIM = 5.0
ALMADA_DE_OURO__IC27_SAIDA_3 = 4.6
ALMADA_DE_OURO__AZINHAL = 4.3
ALTA_MORA__QUEBRADAS = 7.0
ALTA_MORA__VAQUEIROS = 21.1
AREA_REPOUSO_CASTRO_MARIM__PONTE_INTERNACIONAL_GUADIANA = 1.7
AZINHAL__IC27_SAIDA_2 = 2.7
AZINHAL_JUNQUEIRA = 4.4
BALURCO_DE_BAIXO__CORTE_DAS_DONAS = 6.8
BALURCO_DE_BAIXO__BALURCO_DE_CIMA = 1.6
BALURCO_DE_BAIXO__IC27_SAIDA_6 = 4.7
BALURCO_DE_BAIXO__PARQUE_EMPRESARIAL_ALCOUTIM = 1.5
BALURCO_DE_CIMA__IC27_SAIDA_7 = 1.1
BAR_DO_RIO__GUERREIROS_DO_RIO = 0.1
BARRAGEM_DE_ODELEITE__CHOCA_QUEIMADA = 1.0
BARRAGEM_DO_BELICHE__JUNQUEIRA = 5.8
BARRAGEM_DO_BELICHE__SENTINELA = 3.6
BARRANCO_DAS_PEREIRAS__FOZ_DE_ODELEITE = 2.4
BOAVISTA__ESPIRITO_SANTO = 6.6
BOAVISTA__PENHA_DA_AGUIA = 3.4
CAMPO_GOLFE_CASTRO_MARIM__IC27_SAIDA_1 = 2.2
CASA_BRANCA__CHOCA_QUEIMADA = 0.8
CASTRO_MARIM__VRSA = 3.5
CHOCA_QUEIMADA__QUEBRADAS = 2.2
CORTE_DAS_DONAS__ROTUNDA_DA_ARVORE = 2.1
CORTE_DAS_DONAS__IC27_SAIDA_6 = 6.9
CORTES_PEREIRAS__ENTRONCAMENTO_FIM_IC27 = 4.8
CORTE_TABELIAO__PARQUE_EMPRESARIAL_ALCOUTIM = 6.6
CORTE_TABELIAO__IC27_FIM = 5.9
EL_GRANADO__PUERTO_DE_LA_LAJA = 7.5
EL_GRANADO__SANLUCAR_DEL_GUADIANA = 7.8
EL_GRANADO__VILLANUEVA_DE_LOS_CASTILLEJOS = 14.4
ENTRONCAMENTO_FIM_IC27__IC27_FIM = 0.5
ENTRONCAMENTO_FIM_IC27__SANTA_MARTA = 1.8
ESPIRITO_SANTO__RIBEIRA_DO_VASCAO = 6.9
FONTE_DO_PENEDO__IC27_SAIDA_3 = 2.5
FURNAZINHAS__IC27_SAIDA_5 = 5.4
FURNAZINHAS__VAQUEIROS = 17.6
GIOES__MARTINLONGO = 9.4
GIOES__PEREIRO = 11.2
GUERREIROS_DO_RIO__LARANJEIRAS = 1.2
GUERREIROS_DO_RIO__ROTUNDA_DA_ARVORE = 0.7
IC27_FIM__IC27_SAIDA_7 = 6.1
IC27_INICIO__IC27_SAIDA_1 = 1.1
IC27_INICIO__MONTE_FRANCISCO = 0.5
IC27_INICIO__SAPAL = 2.0
IC27_SAIDA_1__IC27_SAIDA_2 = 8.1
IC27_SAIDA_1__JUNQUEIRA = 2.4
IC27_SAIDA_1__MONTE_FRANCISCO = 0.9
IC27_SAIDA_2__IC27_SAIDA_3 = 2.6
IC27_SAIDA_2__PICARRAL = 1.0
IC27_SAIDA_2__SENTINELA = 1.2
IC27_SAIDA_3__IC27_SAIDA_4 = 2.7
IC27_SAIDA_3__PORTELA_ALTA = 2.5
IC27_SAIDA_4__IC27_SAIDA_5 = 3.3
IC27_SAIDA_4__ODELEITE = 0.7
IC27_SAIDA_5__IC27_SAIDA_6 = 5.1
IC27_SAIDA_5__TENENCIA = 3.3
IC27_SAIDA_6__IC27_SAIDA_7 = 3.7
IC27_SAIDA_6__PALMEIRA = 0.7
IC27_SAIDA_7__PARQUE_EMPRESARIAL_ALCOUTIM = 3.0
IC27_SAIDA_7__PEREIRO = 6.1
LARANJEIRAS__MONTINHO_DAS_LARANJEIRAS = 0.5
MARTINLONGO__VAQUEIROS = 7.7
MERTOLA__MONTE_FERNANDES = 6.0
MONTE_FERNANDES__PICOITOS = 6.4
PICOITOS__SALGUEIROS = 2.0
POMARAO__PONTE_RIO_CHANCA = 0.2
POMARAO__SALGUEIROS = 4.6
PONTE_RIO_CHANCA__PUERTO_DE_LA_LAJA = 6.0
PORTELA_ALTA__QUEBRADAS = 1.2
QUEBRADAS__SENTINELA = 2.5
RIBEIRA_DO_VASCAO__SANTA_MARTA = 3.6
SAN_SILVESTRE_DE_GUZMAN__VILLANUEVA_DE_LOS_CASTILLEJOS = 14.6
SAN_SILVESTRE_DE_GUZMAN__SANLUCAR_DEL_GUADIANA = 17.6
SAN_SILVESTRE_DE_GUZMAN__VILLABLANCA = 9.6


class Locais:
    lista_locais = []

    def preencher_lista_locais(self):
        #  Criar os locais
        a_49_saida_125 = local.Local(A_49_SAIDA_125,
                                     {VILLABLANCA: [NORTE, A_49_SAIDA_125__VILLABLANCA, CARRO],
                                      A_49_SAIDA_129: [OESTE, A_49_SAIDA_125__A_49_SAIDA_129, CARRO]})

        a_49_saida_129 = local.Local(A_49_SAIDA_129,
                                     {A_49_SAIDA_125: [ESTE, A_49_SAIDA_125__A_49_SAIDA_129, CARRO],
                                      A_49_SAIDA_131: [OESTE, A_49_SAIDA_129__A_49_SAIDA_131, CARRO],
                                      AYAMONTE: [SUDOESTE, A_49_SAIDA_129__AYAMONTE, CARRO]})

        a_49_saida_131 = local.Local(A_49_SAIDA_131,
                                     {A_49_SAIDA_129: [ESTE, A_49_SAIDA_129__A_49_SAIDA_131, CARRO],
                                      AYAMONTE: [SUL, A_49_SAIDA_131__AYAMONTE, CARRO],
                                      COSTA_ESURI: [NORTE, A_49_SAIDA_131__COSTA_ESURI, CARRO]})

        alamo = local.Local(ALAMO,
                            {ROTUNDA_DA_ARVORE: [NORTE, ALAMO__ROTUNDA_DA_ARVORE, CARRO],
                             BARRANCO_DAS_PEREIRAS: [SUL, ALAMO__BARRANCO_DAS_PEREIRAS, CARRO]})

        alamo_mertola = local.Local(ALAMO_MERTOLA,
                                    {ESPIRITO_SANTO: [SUDESTE, ALAMO_MERTOLA__ESPIRITO_SANTO, CARRO],
                                     BOAVISTA: [ESTE, ALAMO_MERTOLA__BOAVISTA, CARRO],
                                     MERTOLA: [NORTE, ALAMO_MERTOLA__MERTOLA, CARRO]})

        alcaria = local.Local(ALCARIA,
                              {FOZ_DE_ODELEITE: [NORDESTE, ALCARIA__FOZ_DE_ODELEITE, CARRO],
                               ODELEITE: [OESTE, ALCARIA__ODELEITE, CARRO],
                               FONTE_DO_PENEDO: [SUL, ALCARIA__FONTE_DO_PENEDO, CARRO]})

        alcoutim = local.Local(ALCOUTIM,
                               {PARQUE_EMPRESARIAL_ALCOUTIM: [SUDOESTE, ALCOUTIM__PARQUE_EMPRESARIAL_ALCOUTIM, CARRO],
                                MONTINHO_DAS_LARANJEIRAS: [SUL, ALCOUTIM__MONTINHO_DAS_LARANJEIRAS, CARRO],
                                CORTE_TABELIAO: [SUDOESTE, ALCOUTIM__CORTE_TABELIAO, CARRO],
                                CORTES_PEREIRAS: [NOROESTE, ALCOUTIM__CORTES_PEREIRAS, CARRO],
                                SANLUCAR_DEL_GUADIANA: [NORDESTE, 0, BARCO],
                                LARANJEIRAS: [SUL, 0, BARCO]})

        almada_de_ouro = local.Local(ALMADA_DE_OURO,
                                     {IC27_SAIDA_3: [OESTE, ALMADA_DE_OURO__IC27_SAIDA_3, CARRO],
                                      AZINHAL: [SUDOESTE, ALMADA_DE_OURO__AZINHAL, CARRO],
                                      FOZ_DE_ODELEITE: [NORTE, 0, BARCO],
                                      COSTA_ESURI: [SUL, 0, BARCO]})

        alta_mora = local.Local(ALTA_MORA,
                                {QUEBRADAS: [ESTE, ALTA_MORA__QUEBRADAS, CARRO],
                                 VAQUEIROS: [NOROESTE, ALTA_MORA__VAQUEIROS, CARRO]})

        ayamonte = local.Local(AYAMONTE,
                               {A_49_SAIDA_129: [NORDESTE, A_49_SAIDA_129__AYAMONTE, CARRO],
                                A_49_SAIDA_131: [NORTE, A_49_SAIDA_131__AYAMONTE, CARRO],
                                COSTA_ESURI: [NORTE, 0, BARCO],
                                VRSA: [SUDOESTE, 0, BARCO]})

        azinhal = local.Local(AZINHAL,
                              {ALMADA_DE_OURO: [NORDESTE, ALMADA_DE_OURO__AZINHAL, CARRO],
                               IC27_SAIDA_2: [NOROESTE, AZINHAL__IC27_SAIDA_2, CARRO],
                               JUNQUEIRA: [SUL, AZINHAL_JUNQUEIRA, CARRO]})

        bar_do_rio = local.Local(BAR_DO_RIO,
                                 {GUERREIROS_DO_RIO: [OESTE, BAR_DO_RIO__GUERREIROS_DO_RIO, CARRO],
                                  LARANJEIRAS: [NOROESTE, 0, BARCO],
                                  FOZ_DE_ODELEITE: [SUL, 0, BARCO]})

        barragem_de_odeleite = local.Local(BARRAGEM_DE_ODELEITE,
                                           {CHOCA_QUEIMADA: [SUDESTE, BARRAGEM_DE_ODELEITE__CHOCA_QUEIMADA, CARRO]})

        barragem_do_beliche = local.Local(BARRAGEM_DO_BELICHE,
                                          {SENTINELA: [NORTE, BARRAGEM_DO_BELICHE__SENTINELA, CARRO],
                                           JUNQUEIRA: [SUDESTE, BARRAGEM_DO_BELICHE__JUNQUEIRA, CARRO]})

        barranco_das_pereiras = local.Local(BARRANCO_DAS_PEREIRAS,
                                            {ALAMO: [NORTE, ALAMO__BARRANCO_DAS_PEREIRAS, CARRO],
                                             FOZ_DE_ODELEITE: [SUL, BARRANCO_DAS_PEREIRAS__FOZ_DE_ODELEITE, CARRO]})

        balurco_de_baixo = local.Local(BALURCO_DE_BAIXO,
                                       {CORTE_DAS_DONAS: [SUDESTE, BALURCO_DE_BAIXO__CORTE_DAS_DONAS, CARRO],
                                        PARQUE_EMPRESARIAL_ALCOUTIM: [NORTE, BALURCO_DE_BAIXO__PARQUE_EMPRESARIAL_ALCOUTIM, CARRO],
                                        IC27_SAIDA_6: [SUDOESTE, BALURCO_DE_BAIXO__IC27_SAIDA_6, CARRO],
                                        BALURCO_DE_CIMA: [NOROESTE, BALURCO_DE_BAIXO__BALURCO_DE_CIMA, CARRO]})

        balurco_de_cima = local.Local(BALURCO_DE_CIMA,
                                      {IC27_SAIDA_7: [NOROESTE, BALURCO_DE_CIMA__IC27_SAIDA_7, CARRO],
                                       BALURCO_DE_BAIXO: [SUDESTE, BALURCO_DE_BAIXO__BALURCO_DE_CIMA, CARRO]})

        boavista = local.Local(BOAVISTA,
                               {ESPIRITO_SANTO: [SUDOESTE, BOAVISTA__ESPIRITO_SANTO, CARRO],
                                ALAMO_MERTOLA: [OESTE, ALAMO_MERTOLA__BOAVISTA, CARRO],
                                PENHA_DA_AGUIA: [NORDESTE, BOAVISTA__PENHA_DA_AGUIA, CARRO]})

        casa_branca = local.Local(CASA_BRANCA,
                                  {CHOCA_QUEIMADA: [NOROESTE, CASA_BRANCA__CHOCA_QUEIMADA, CARRO]})

        choca_queimada = local.Local(CHOCA_QUEIMADA,
                                     {QUEBRADAS: [SUL, CHOCA_QUEIMADA__QUEBRADAS, CARRO],
                                      CASA_BRANCA: [SUDESTE, CASA_BRANCA__CHOCA_QUEIMADA, CARRO],
                                      BARRAGEM_DE_ODELEITE: [NOROESTE, BARRAGEM_DE_ODELEITE__CHOCA_QUEIMADA, CARRO]})

        corte_das_donas = local.Local(CORTE_DAS_DONAS,
                                      {BALURCO_DE_BAIXO: [NOROESTE, BALURCO_DE_BAIXO__CORTE_DAS_DONAS, CARRO],
                                       ROTUNDA_DA_ARVORE: [ESTE, CORTE_DAS_DONAS__ROTUNDA_DA_ARVORE, CARRO],
                                       IC27_SAIDA_6: [NOROESTE, CORTE_DAS_DONAS__IC27_SAIDA_6, CARRO]})

        cortes_pereiras = local.Local(CORTES_PEREIRAS,
                                      {ENTRONCAMENTO_FIM_IC27: [OESTE, CORTES_PEREIRAS__ENTRONCAMENTO_FIM_IC27, CARRO],
                                       ALCOUTIM: [SUDESTE, ALCOUTIM__CORTES_PEREIRAS, CARRO]})

        corte_tabeliao = local.Local(CORTE_TABELIAO,
                                     {ALCOUTIM: [NORDESTE, ALCOUTIM__CORTE_TABELIAO, CARRO],
                                      PARQUE_EMPRESARIAL_ALCOUTIM: [SUL, CORTE_TABELIAO__PARQUE_EMPRESARIAL_ALCOUTIM, CARRO],
                                      IC27_FIM: [NOROESTE, CORTE_TABELIAO__IC27_FIM, CARRO]})

        costa_esuri = local.Local(COSTA_ESURI,
                                  {A_49_SAIDA_131: [SUL, A_49_SAIDA_131__COSTA_ESURI, CARRO],
                                   ALMADA_DE_OURO: [NORTE, 0, BARCO],
                                   AYAMONTE: [SUL, 0, BARCO]})

        el_granado = local.Local(EL_GRANADO,
                                 {SANLUCAR_DEL_GUADIANA: [SUDOESTE, EL_GRANADO__SANLUCAR_DEL_GUADIANA, CARRO],
                                  PUERTO_DE_LA_LAJA: [OESTE, EL_GRANADO__PUERTO_DE_LA_LAJA, CARRO],
                                  VILLANUEVA_DE_LOS_CASTILLEJOS: [ESTE, EL_GRANADO__VILLANUEVA_DE_LOS_CASTILLEJOS, CARRO]})

        entroncamento_fim_ic27 = local.Local(ENTRONCAMENTO_FIM_IC27,
                                             {IC27_FIM: [SUDESTE, ENTRONCAMENTO_FIM_IC27__IC27_FIM, CARRO],
                                              CORTES_PEREIRAS: [ESTE, CORTES_PEREIRAS__ENTRONCAMENTO_FIM_IC27, CARRO],
                                              SANTA_MARTA: [NOROESTE, ENTRONCAMENTO_FIM_IC27__SANTA_MARTA, CARRO]})

        espirito_santo = local.Local(ESPIRITO_SANTO,
                                     {RIBEIRA_DO_VASCAO: [SUDESTE, ESPIRITO_SANTO__RIBEIRA_DO_VASCAO, CARRO],
                                      ALAMO_MERTOLA: [NOROESTE, ALAMO_MERTOLA__ESPIRITO_SANTO, CARRO],
                                      BOAVISTA: [NORDESTE, BOAVISTA__ESPIRITO_SANTO, CARRO]})

        fonte_do_penedo = local.Local(FONTE_DO_PENEDO,
                                      {ALCARIA: [NORTE, ALCARIA__FONTE_DO_PENEDO, CARRO],
                                       IC27_SAIDA_3: [SUDOESTE, FONTE_DO_PENEDO__IC27_SAIDA_3, CARRO]})

        foz_de_odeleite = local.Local(FOZ_DE_ODELEITE,
                                      {BARRANCO_DAS_PEREIRAS: [NORTE, BARRANCO_DAS_PEREIRAS__FOZ_DE_ODELEITE, CARRO],
                                       ALCARIA: [SUDOESTE, ALCARIA__FOZ_DE_ODELEITE, CARRO],
                                       BAR_DO_RIO: [NORTE, 0, BARCO],
                                       ALMADA_DE_OURO: [SUL, 0, BARCO]})

        furnazinhas = local.Local(FURNAZINHAS,
                                  {IC27_SAIDA_5: [NOROESTE, FURNAZINHAS__IC27_SAIDA_5, CARRO],
                                   VAQUEIROS: [NOROESTE, FURNAZINHAS__VAQUEIROS, CARRO]})

        gioes = local.Local(GIOES,
                            {MARTINLONGO: [SUDOESTE, GIOES__MARTINLONGO, CARRO],
                             PEREIRO: [SUDESTE, GIOES__PEREIRO, CARRO]})

        guerreiros_do_rio = local.Local(GUERREIROS_DO_RIO,
                                        {LARANJEIRAS: [NOROESTE, GUERREIROS_DO_RIO__LARANJEIRAS, CARRO],
                                         ROTUNDA_DA_ARVORE: [SUL, GUERREIROS_DO_RIO__ROTUNDA_DA_ARVORE, CARRO],
                                         BAR_DO_RIO: [ESTE, BAR_DO_RIO__GUERREIROS_DO_RIO, CARRO]})

        ic27_fim = local.Local(IC27_FIM,
                               {CORTE_TABELIAO: [SUDESTE, CORTE_TABELIAO__IC27_FIM, CARRO],
                                IC27_SAIDA_7: [SUL, IC27_FIM__IC27_SAIDA_7, CARRO],
                                ENTRONCAMENTO_FIM_IC27: [NOROESTE, ENTRONCAMENTO_FIM_IC27__IC27_FIM, CARRO]})

        ic27_saida_1 = local.Local(IC27_SAIDA_1,
                                   {IC27_SAIDA_2: [NOROESTE, IC27_SAIDA_1__IC27_SAIDA_2, CARRO],
                                    JUNQUEIRA: [NOROESTE, IC27_SAIDA_1__JUNQUEIRA, CARRO]})

        ic27_saida_2 = local.Local(IC27_SAIDA_2,
                                   {IC27_SAIDA_3: [NORTE, IC27_SAIDA_2__IC27_SAIDA_3, CARRO],
                                    IC27_SAIDA_1: [SUDESTE, IC27_SAIDA_1__IC27_SAIDA_2, CARRO],
                                    AZINHAL: [SUDESTE, AZINHAL__IC27_SAIDA_2, CARRO],
                                    PICARRAL: [NORDESTE, IC27_SAIDA_2__PICARRAL, CARRO],
                                    SENTINELA: [OESTE, IC27_SAIDA_2__SENTINELA, CARRO]})

        ic27_saida_3 = local.Local(IC27_SAIDA_3,
                                   {IC27_SAIDA_2: [SUL, IC27_SAIDA_2__IC27_SAIDA_3, CARRO],
                                    IC27_SAIDA_4: [NORTE, IC27_SAIDA_3__IC27_SAIDA_4, CARRO],
                                    FONTE_DO_PENEDO: [NORDESTE, FONTE_DO_PENEDO__IC27_SAIDA_3, CARRO],
                                    ALMADA_DE_OURO: [ESTE, ALMADA_DE_OURO__IC27_SAIDA_3, CARRO],
                                    PORTELA_ALTA: [SUDOESTE, IC27_SAIDA_3__PORTELA_ALTA, CARRO]})

        ic27_saida_4 = local.Local(IC27_SAIDA_4,
                                   {IC27_SAIDA_5: [NOROESTE, IC27_SAIDA_4__IC27_SAIDA_5, CARRO],
                                    IC27_SAIDA_3: [SUL, IC27_SAIDA_3__IC27_SAIDA_4, CARRO],
                                    ODELEITE: [ESTE, IC27_SAIDA_4__ODELEITE, CARRO]})

        ic27_saida_5 = local.Local(IC27_SAIDA_5,
                                   {IC27_SAIDA_6: [NORTE, IC27_SAIDA_5__IC27_SAIDA_6, CARRO],
                                    IC27_SAIDA_4: [SUDESTE, IC27_SAIDA_4__IC27_SAIDA_5, CARRO],
                                    TENENCIA: [NORDESTE, IC27_SAIDA_5__TENENCIA, CARRO],
                                    FURNAZINHAS: [SUDESTE, FURNAZINHAS__IC27_SAIDA_5, CARRO]})

        ic27_saida_6 = local.Local(IC27_SAIDA_6,
                                   {CORTE_DAS_DONAS: [SUDESTE, CORTE_DAS_DONAS__IC27_SAIDA_6, CARRO],
                                    BALURCO_DE_BAIXO: [NORDESTE, BALURCO_DE_BAIXO__IC27_SAIDA_6, CARRO],
                                    PALMEIRA: [SUDOESTE, IC27_SAIDA_6__PALMEIRA, CARRO],
                                    IC27_SAIDA_7: [NORTE, IC27_SAIDA_6__IC27_SAIDA_7, CARRO],
                                    IC27_SAIDA_5: [SUL, IC27_SAIDA_5__IC27_SAIDA_6, CARRO]})

        ic27_saida_7 = local.Local(IC27_SAIDA_7,
                                   {IC27_SAIDA_6: [SUL, IC27_SAIDA_6__IC27_SAIDA_7, CARRO],
                                    IC27_FIM: [NORTE, IC27_FIM__IC27_SAIDA_7, CARRO],
                                    PARQUE_EMPRESARIAL_ALCOUTIM: [ESTE, IC27_SAIDA_7__PARQUE_EMPRESARIAL_ALCOUTIM, CARRO],
                                    BALURCO_DE_CIMA: [SUDESTE, BALURCO_DE_CIMA__IC27_SAIDA_7, CARRO],
                                    PEREIRO: [NOROESTE, IC27_SAIDA_7__PEREIRO, CARRO],})

        junqueira = local.Local(JUNQUEIRA,
                                {BARRAGEM_DO_BELICHE: [NOROESTE, BARRAGEM_DO_BELICHE__JUNQUEIRA, CARRO],
                                 AZINHAL: [NORTE, AZINHAL_JUNQUEIRA, CARRO],
                                 IC27_SAIDA_1: [SUDESTE, IC27_SAIDA_1__JUNQUEIRA, CARRO]})

        laranjeiras = local.Local(LARANJEIRAS,
                                  {GUERREIROS_DO_RIO: [SUDESTE, GUERREIROS_DO_RIO__LARANJEIRAS, CARRO],
                                   MONTINHO_DAS_LARANJEIRAS: [NOROESTE, LARANJEIRAS__MONTINHO_DAS_LARANJEIRAS, CARRO],
                                   ALCOUTIM: [NORTE, 0, BARCO],
                                   BAR_DO_RIO: [SUDESTE, 0, BARCO]})

        martinlongo = local.Local(MARTINLONGO,
                                  {VAQUEIROS: [SUDESTE, MARTINLONGO__VAQUEIROS, CARRO],
                                   GIOES: [NORDESTE, GIOES__MARTINLONGO, CARRO]})

        mertola = local.Local(MERTOLA,
                              {ALAMO_MERTOLA: [SUL, ALAMO_MERTOLA__MERTOLA, CARRO],
                               MONTE_FERNANDES: [SUDESTE, MERTOLA__MONTE_FERNANDES, CARRO],
                               PENHA_DA_AGUIA: [SUDESTE, 0, BARCO]})

        monte_fernandes = local.Local(MONTE_FERNANDES,
                                      {MERTOLA: [NOROESTE, MERTOLA__MONTE_FERNANDES, CARRO],
                                       PICOITOS: [SUDESTE, MONTE_FERNANDES__PICOITOS, CARRO]})

        montinho_das_laranjeiras = local.Local(MONTINHO_DAS_LARANJEIRAS,
                                               {ALCOUTIM: [NORTE, ALCOUTIM__MONTINHO_DAS_LARANJEIRAS, CARRO],
                                                LARANJEIRAS: [SUDESTE, LARANJEIRAS__MONTINHO_DAS_LARANJEIRAS, CARRO]})

        odeleite = local.Local(ODELEITE,
                               {ALCARIA: [ESTE, ALCARIA__ODELEITE, CARRO],
                                IC27_SAIDA_4: [OESTE, IC27_SAIDA_4__ODELEITE, CARRO]})

        palmeira = local.Local(PALMEIRA,
                               {IC27_SAIDA_6: [NORDESTE, IC27_SAIDA_6__PALMEIRA, CARRO]})

        parque_empresarial_alcoutim = local.Local(PARQUE_EMPRESARIAL_ALCOUTIM,
                                                  {ALCOUTIM: [NORDESTE, ALCOUTIM__PARQUE_EMPRESARIAL_ALCOUTIM, CARRO],
                                                   BALURCO_DE_BAIXO: [SUL, BALURCO_DE_BAIXO__PARQUE_EMPRESARIAL_ALCOUTIM, CARRO],
                                                   IC27_SAIDA_7: [OESTE, IC27_SAIDA_7__PARQUE_EMPRESARIAL_ALCOUTIM, CARRO],
                                                   CORTE_TABELIAO: [NORTE, CORTE_TABELIAO__PARQUE_EMPRESARIAL_ALCOUTIM, CARRO]})

        penha_da_aguia = local.Local(PENHA_DA_AGUIA,
                                     {BOAVISTA: [SUDOESTE, BOAVISTA__PENHA_DA_AGUIA, CARRO],
                                      POMARAO: [SUDESTE, 0, BARCO],
                                      MERTOLA: [NOROESTE, 0, BARCO]})

        pereiro = local.Local(PEREIRO,
                              {GIOES: [NOROESTE, GIOES__PEREIRO, CARRO],
                               IC27_SAIDA_7: [SUDESTE, IC27_SAIDA_7__PEREIRO, CARRO]})

        picarral = local.Local(PICARRAL,
                               {IC27_SAIDA_2: [SUDOESTE, IC27_SAIDA_2__PICARRAL, CARRO]})

        picoitos = local.Local(PICOITOS,
                               {MONTE_FERNANDES: [NOROESTE, MONTE_FERNANDES__PICOITOS, CARRO],
                                SALGUEIROS: [ESTE, PICOITOS__SALGUEIROS, CARRO]})

        pomarao = local.Local(POMARAO,
                              {PONTE_RIO_CHANCA: [SUDESTE, POMARAO__PONTE_RIO_CHANCA, CARRO],
                               SALGUEIROS: [NORTE, POMARAO__SALGUEIROS, CARRO],
                               PUERTO_DE_LA_LAJA: [SUL, 0, BARCO],
                               PENHA_DA_AGUIA: [NOROESTE, 0, BARCO]})

        ponte_rio_chanca = local.Local(PONTE_RIO_CHANCA,
                                       {PUERTO_DE_LA_LAJA: [SUDESTE, PONTE_RIO_CHANCA__PUERTO_DE_LA_LAJA, CARRO],
                                        POMARAO: [NOROESTE, POMARAO__PONTE_RIO_CHANCA, CARRO]})

        portela_alta = local.Local(PORTELA_ALTA,
                                   {IC27_SAIDA_3: [NORDESTE, IC27_SAIDA_3__PORTELA_ALTA, CARRO],
                                    QUEBRADAS: [OESTE, PORTELA_ALTA__QUEBRADAS, CARRO]})

        puerto_de_la_laja = local.Local(PUERTO_DE_LA_LAJA,
                                        {EL_GRANADO: [ESTE, EL_GRANADO__PUERTO_DE_LA_LAJA, CARRO],
                                         PONTE_RIO_CHANCA: [NOROESTE, PONTE_RIO_CHANCA__PUERTO_DE_LA_LAJA, CARRO],
                                         SANLUCAR_DEL_GUADIANA: [SUL, 0, BARCO],
                                         POMARAO: [NORTE, 0, BARCO]})

        quebradas = local.Local(QUEBRADAS,
                                {PORTELA_ALTA: [ESTE, PORTELA_ALTA__QUEBRADAS, CARRO],
                                 SENTINELA: [SUDESTE, QUEBRADAS__SENTINELA, CARRO],
                                 CHOCA_QUEIMADA: [NORTE, CHOCA_QUEIMADA__QUEBRADAS, CARRO],
                                 ALTA_MORA: [OESTE, ALTA_MORA__QUEBRADAS, CARRO]})

        ribeira_do_vascao = local.Local(RIBEIRA_DO_VASCAO,
                                        {SANTA_MARTA: [SUL, RIBEIRA_DO_VASCAO__SANTA_MARTA, CARRO],
                                         ESPIRITO_SANTO: [NOROESTE, ESPIRITO_SANTO__RIBEIRA_DO_VASCAO, CARRO]})

        rotunda_da_arvore = local.Local(ROTUNDA_DA_ARVORE,
                                        {GUERREIROS_DO_RIO: [NORTE, GUERREIROS_DO_RIO__ROTUNDA_DA_ARVORE, CARRO],
                                         CORTE_DAS_DONAS: [OESTE, CORTE_DAS_DONAS__ROTUNDA_DA_ARVORE, CARRO],
                                         ALAMO: [SUL, ALAMO__ROTUNDA_DA_ARVORE, CARRO]})

        salgueiros = local.Local(SALGUEIROS,
                                 {PICOITOS: [OESTE, PICOITOS__SALGUEIROS, CARRO],
                                  POMARAO: [SUL, POMARAO__SALGUEIROS, CARRO]})

        san_silvestre_de_guzman = local.Local(SAN_SILVESTRE_DE_GUZMAN,
                                              {SANLUCAR_DEL_GUADIANA: [NOROESTE, SAN_SILVESTRE_DE_GUZMAN__SANLUCAR_DEL_GUADIANA, CARRO],
                                               VILLANUEVA_DE_LOS_CASTILLEJOS: [NORDESTE, SAN_SILVESTRE_DE_GUZMAN__VILLANUEVA_DE_LOS_CASTILLEJOS, CARRO],
                                               VILLABLANCA: [SUL, SAN_SILVESTRE_DE_GUZMAN__VILLABLANCA, CARRO]})

        sanlucar_del_guadiana = local.Local(SANLUCAR_DEL_GUADIANA,
                                            {EL_GRANADO: [NORDESTE, EL_GRANADO__SANLUCAR_DEL_GUADIANA, CARRO],
                                             SAN_SILVESTRE_DE_GUZMAN: [SUDESTE, SAN_SILVESTRE_DE_GUZMAN__SANLUCAR_DEL_GUADIANA, CARRO],
                                             ALCOUTIM: [SUDOESTE, 0, BARCO],
                                             PUERTO_DE_LA_LAJA: [NORTE, 0, BARCO]})

        santa_marta = local.Local(SANTA_MARTA,
                                  {ENTRONCAMENTO_FIM_IC27: [SUDESTE, ENTRONCAMENTO_FIM_IC27__SANTA_MARTA, CARRO],
                                   RIBEIRA_DO_VASCAO: [NORTE, RIBEIRA_DO_VASCAO__SANTA_MARTA, CARRO]})

        sentinela = local.Local(SENTINELA,
                                {IC27_SAIDA_2: [ESTE, IC27_SAIDA_2__SENTINELA, CARRO],
                                 QUEBRADAS: [NOROESTE, QUEBRADAS__SENTINELA, CARRO],
                                 BARRAGEM_DO_BELICHE: [SUL, BARRAGEM_DO_BELICHE__SENTINELA, CARRO]})

        tenencia = local.Local(TENENCIA,
                               {IC27_SAIDA_5: [SUDOESTE, IC27_SAIDA_5__TENENCIA, CARRO]})

        vaqueiros = local.Local(VAQUEIROS,
                                {FURNAZINHAS: [SUDESTE, FURNAZINHAS__VAQUEIROS, CARRO],
                                 MARTINLONGO: [NOROESTE, MARTINLONGO__VAQUEIROS, CARRO],
                                 ALTA_MORA: [SUDESTE, ALTA_MORA__VAQUEIROS, CARRO]})

        vila_real_de_santo_antonio = local.Local(VRSA,
                                                 {AYAMONTE: [NORDESTE, 0, BARCO]})

        villablanca = local.Local(VILLABLANCA,
                                  {SAN_SILVESTRE_DE_GUZMAN: [NORTE, SAN_SILVESTRE_DE_GUZMAN__VILLABLANCA, CARRO],
                                   A_49_SAIDA_125: [SUL, A_49_SAIDA_125__VILLABLANCA, CARRO]})

        villanueva_de_los_castillejos = local.Local(VILLANUEVA_DE_LOS_CASTILLEJOS,
                                                    {EL_GRANADO: [OESTE, EL_GRANADO__VILLANUEVA_DE_LOS_CASTILLEJOS, CARRO],
                                                     SAN_SILVESTRE_DE_GUZMAN: [SUDOESTE, SAN_SILVESTRE_DE_GUZMAN__VILLANUEVA_DE_LOS_CASTILLEJOS, CARRO]})

        #  Adicionar os locais à lista
        self.lista_locais.append(a_49_saida_125)
        self.lista_locais.append(a_49_saida_129)
        self.lista_locais.append(a_49_saida_131)
        self.lista_locais.append(alamo)
        self.lista_locais.append(alamo_mertola)
        self.lista_locais.append(alcaria)
        self.lista_locais.append(alcoutim)
        self.lista_locais.append(almada_de_ouro)
        self.lista_locais.append(alta_mora)
        self.lista_locais.append(ayamonte)
        self.lista_locais.append(azinhal)
        self.lista_locais.append(balurco_de_baixo)
        self.lista_locais.append(balurco_de_cima)
        self.lista_locais.append(bar_do_rio)
        self.lista_locais.append(barragem_de_odeleite)
        self.lista_locais.append(barragem_do_beliche)
        self.lista_locais.append(barranco_das_pereiras)
        self.lista_locais.append(boavista)
        self.lista_locais.append(casa_branca)
        self.lista_locais.append(choca_queimada)
        self.lista_locais.append(corte_das_donas)
        self.lista_locais.append(cortes_pereiras)
        self.lista_locais.append(corte_tabeliao)
        self.lista_locais.append(costa_esuri)
        self.lista_locais.append(el_granado)
        self.lista_locais.append(entroncamento_fim_ic27)
        self.lista_locais.append(espirito_santo)
        self.lista_locais.append(fonte_do_penedo)
        self.lista_locais.append(foz_de_odeleite)
        self.lista_locais.append(furnazinhas)
        self.lista_locais.append(gioes)
        self.lista_locais.append(guerreiros_do_rio)
        self.lista_locais.append(ic27_fim)
        self.lista_locais.append(ic27_saida_1)
        self.lista_locais.append(ic27_saida_2)
        self.lista_locais.append(ic27_saida_3)
        self.lista_locais.append(ic27_saida_4)
        self.lista_locais.append(ic27_saida_5)
        self.lista_locais.append(ic27_saida_6)
        self.lista_locais.append(ic27_saida_7)
        self.lista_locais.append(junqueira)
        self.lista_locais.append(laranjeiras)
        self.lista_locais.append(martinlongo)
        self.lista_locais.append(mertola)
        self.lista_locais.append(monte_fernandes)
        self.lista_locais.append(montinho_das_laranjeiras)
        self.lista_locais.append(odeleite)
        self.lista_locais.append(palmeira)
        self.lista_locais.append(parque_empresarial_alcoutim)
        self.lista_locais.append(penha_da_aguia)
        self.lista_locais.append(pereiro)
        self.lista_locais.append(picarral)
        self.lista_locais.append(picoitos)
        self.lista_locais.append(pomarao)
        self.lista_locais.append(ponte_rio_chanca)
        self.lista_locais.append(portela_alta)
        self.lista_locais.append(puerto_de_la_laja)
        self.lista_locais.append(quebradas)
        self.lista_locais.append(ribeira_do_vascao)
        self.lista_locais.append(rotunda_da_arvore)
        self.lista_locais.append(salgueiros)
        self.lista_locais.append(san_silvestre_de_guzman)
        self.lista_locais.append(sanlucar_del_guadiana)
        self.lista_locais.append(santa_marta)
        self.lista_locais.append(sentinela)
        self.lista_locais.append(tenencia)
        self.lista_locais.append(vaqueiros)
        self.lista_locais.append(vila_real_de_santo_antonio)
        self.lista_locais.append(villablanca)
        self.lista_locais.append(villanueva_de_los_castillejos)

        #  Retornar a lista de locais
        return self.lista_locais
