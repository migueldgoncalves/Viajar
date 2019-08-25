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

#  Nomes dos locais
GUERREIROS_DO_RIO = "Guerreiros do Rio"
LARANJEIRAS = "Laranjeiras"
ROTUNDA_DA_ARVORE = "Rotunda da Árvore"
ALAMO = "Álamo"
MONTINHO_DAS_LARANJEIRAS = "Montinho das Laranjeiras"
CORTE_DAS_DONAS = "Corte das Donas"
ALCOUTIM = "Alcoutim"
BALURCOS = "Balurcos"
FOZ_DE_ODELEITE = "Foz de Odeleite"
IC27_SAIDA_1 = "IC27 - Saída 1"
IC27_SAIDA_2 = "IC27 - Saída 2"
IC27_SAIDA_3 = "IC27 - Saída 3"
IC27_SAIDA_4 = "IC27 - Saída 4"
IC27_SAIDA_5 = "IC27 - Saída 5"
IC27_SAIDA_6 = "IC27 - Saída 6"
IC27_SAIDA_7 = "IC27 - Saída 7"

#  Distâncias (km)
GUERREIROS_DO_RIO__LARANJEIRAS = 1.2
GUERREIROS_DO_RIO__ROTUNDA_DA_ARVORE = 0.7
ROTUNDA_DA_ARVORE__ALAMO = 0.5
ROTUNDA_DA_ARVORE__CORTE_DAS_DONAS = 2.1
CORTE_DAS_DONAS__BALURCOS = 6.8
BALURCOS__ALCOUTIM = 6.7
ALCOUTIM__MONTINHO_DAS_LARANJEIRAS = 8.8
MONTINHO_DAS_LARANJEIRAS__LARANJEIRAS = 0.5
ALAMO__FOZ_DE_ODELEITE = 3.7


class Locais:

    lista_locais = []

    def preencher_lista_locais(self):
        #  Criar os locais
        guerreiros_do_rio = local.Local(GUERREIROS_DO_RIO,
                                        {LARANJEIRAS: [NOROESTE, GUERREIROS_DO_RIO__LARANJEIRAS],
                                         ROTUNDA_DA_ARVORE: [SUL, GUERREIROS_DO_RIO__ROTUNDA_DA_ARVORE]})
        laranjeiras = local.Local(LARANJEIRAS,
                                  {GUERREIROS_DO_RIO: [SUDESTE, GUERREIROS_DO_RIO__LARANJEIRAS],
                                   MONTINHO_DAS_LARANJEIRAS: [NOROESTE, MONTINHO_DAS_LARANJEIRAS__LARANJEIRAS]})
        rotunda_da_arvore = local.Local(ROTUNDA_DA_ARVORE,
                                        {GUERREIROS_DO_RIO: [NORTE, GUERREIROS_DO_RIO__ROTUNDA_DA_ARVORE],
                                         CORTE_DAS_DONAS: [OESTE, ROTUNDA_DA_ARVORE__CORTE_DAS_DONAS],
                                         ALAMO: [SUL, ROTUNDA_DA_ARVORE__ALAMO]})
        alamo = local.Local(ALAMO,
                            {ROTUNDA_DA_ARVORE: [NORTE, ROTUNDA_DA_ARVORE__ALAMO],
                             FOZ_DE_ODELEITE: [SUL, ALAMO__FOZ_DE_ODELEITE]})
        corte_das_donas = local.Local(CORTE_DAS_DONAS,
                                      {BALURCOS: [NOROESTE, CORTE_DAS_DONAS__BALURCOS],
                                       ROTUNDA_DA_ARVORE: [ESTE, ROTUNDA_DA_ARVORE__CORTE_DAS_DONAS]})
        montinho_das_laranjeiras = local.Local(MONTINHO_DAS_LARANJEIRAS,
                                               {ALCOUTIM: [NORTE, ALCOUTIM__MONTINHO_DAS_LARANJEIRAS],
                                                LARANJEIRAS: [SUDESTE, MONTINHO_DAS_LARANJEIRAS__LARANJEIRAS]})
        alcoutim = local.Local(ALCOUTIM,
                               {BALURCOS: [SUDOESTE, BALURCOS__ALCOUTIM],
                                MONTINHO_DAS_LARANJEIRAS: [SUL, ALCOUTIM__MONTINHO_DAS_LARANJEIRAS]})
        balurcos = local.Local(BALURCOS,
                               {CORTE_DAS_DONAS: [SUDESTE, CORTE_DAS_DONAS__BALURCOS],
                                ALCOUTIM: [NORDESTE, BALURCOS__ALCOUTIM]})
        foz_de_odeleite = local.Local(FOZ_DE_ODELEITE,
                                      {ALAMO: [NORTE, ALAMO__FOZ_DE_ODELEITE]})

        #  Adicionar os locais à lista
        self.lista_locais.append(guerreiros_do_rio)
        self.lista_locais.append(laranjeiras)
        self.lista_locais.append(rotunda_da_arvore)
        self.lista_locais.append(alamo)
        self.lista_locais.append(corte_das_donas)
        self.lista_locais.append(montinho_das_laranjeiras)
        self.lista_locais.append(alcoutim)
        self.lista_locais.append(balurcos)
        self.lista_locais.append(foz_de_odeleite)

        #  Retornar a lista de locais
        return self.lista_locais
