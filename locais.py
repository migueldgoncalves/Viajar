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

#  Nomes dos locais
ALAMO = "Álamo"
ALCOUTIM_CIMO = "Alcoutim-Cimo"
BALURCOS = "Balurcos"
CORTE_DAS_DONAS = "Corte das Donas"
FOZ_DE_ODELEITE = "Foz de Odeleite"
GUERREIROS_DO_RIO = "Guerreiros do Rio"
IC27_SAIDA_1 = "IC27-Saída 1"
IC27_SAIDA_2 = "IC27-Saída 2"
IC27_SAIDA_3 = "IC27-Saída 3"
IC27_SAIDA_4 = "IC27-Saída 4"
IC27_SAIDA_5 = "IC27-Saída 5"
IC27_SAIDA_6 = "IC27-Saída 6"
IC27_SAIDA_7 = "IC27-Saída 7"
LARANJEIRAS = "Laranjeiras"
MONTINHO_DAS_LARANJEIRAS = "Montinho das Laranjeiras"
PALMEIRA = "Palmeira"
PARQUE_EMPRESARIAL_ALCOUTIM = "Parque Empresarial de Alcoutim"
ROTUNDA_DA_ARVORE = "Rotunda da Árvore"

#  Distâncias (km)
ALAMO__ROTUNDA_DA_ARVORE = 0.5
ALAMO__FOZ_DE_ODELEITE = 3.7
ALCOUTIM_CIMO__PARQUE_EMPRESARIAL_ALCOUTIM = 5.0
ALCOUTIM_CIMO__MONTINHO_DAS_LARANJEIRAS = 8.8
BALURCOS__CORTE_DAS_DONAS = 6.8
BALURCOS__IC27_SAIDA_6 = 4.7
BALURCOS__PARQUE_EMPRESARIAL_ALCOUTIM = 1.5
CORTE_DAS_DONAS__ROTUNDA_DA_ARVORE = 2.1
CORTE_DAS_DONAS__IC27_SAIDA_6 = 6.9
GUERREIROS_DO_RIO__LARANJEIRAS = 1.2
GUERREIROS_DO_RIO__ROTUNDA_DA_ARVORE = 0.7
IC27_SAIDA_6__PALMEIRA = 0.7
LARANJEIRAS__MONTINHO_DAS_LARANJEIRAS = 0.5


class Locais:
    lista_locais = []

    def preencher_lista_locais(self):
        #  Criar os locais
        alamo = local.Local(ALAMO,
                            {ROTUNDA_DA_ARVORE: [NORTE, ALAMO__ROTUNDA_DA_ARVORE, CARRO],
                             FOZ_DE_ODELEITE: [SUL, ALAMO__FOZ_DE_ODELEITE, CARRO]})

        alcoutim_cimo = local.Local(ALCOUTIM_CIMO,
                                    {PARQUE_EMPRESARIAL_ALCOUTIM: [SUDOESTE,
                                                                   ALCOUTIM_CIMO__PARQUE_EMPRESARIAL_ALCOUTIM, CARRO],
                                     MONTINHO_DAS_LARANJEIRAS: [SUL, ALCOUTIM_CIMO__MONTINHO_DAS_LARANJEIRAS, CARRO]})

        balurcos = local.Local(BALURCOS,
                               {CORTE_DAS_DONAS: [SUDESTE, BALURCOS__CORTE_DAS_DONAS, CARRO],
                                PARQUE_EMPRESARIAL_ALCOUTIM: [NORTE, BALURCOS__PARQUE_EMPRESARIAL_ALCOUTIM, CARRO],
                                IC27_SAIDA_6: [SUDOESTE, BALURCOS__IC27_SAIDA_6, CARRO]})

        corte_das_donas = local.Local(CORTE_DAS_DONAS,
                                      {BALURCOS: [NOROESTE, BALURCOS__CORTE_DAS_DONAS, CARRO],
                                       ROTUNDA_DA_ARVORE: [ESTE, CORTE_DAS_DONAS__ROTUNDA_DA_ARVORE, CARRO],
                                       IC27_SAIDA_6: [NOROESTE, CORTE_DAS_DONAS__IC27_SAIDA_6, CARRO]})

        foz_de_odeleite = local.Local(FOZ_DE_ODELEITE,
                                      {ALAMO: [NORTE, ALAMO__FOZ_DE_ODELEITE, CARRO]})

        guerreiros_do_rio = local.Local(GUERREIROS_DO_RIO,
                                        {LARANJEIRAS: [NOROESTE, GUERREIROS_DO_RIO__LARANJEIRAS, CARRO],
                                         ROTUNDA_DA_ARVORE: [SUL, GUERREIROS_DO_RIO__ROTUNDA_DA_ARVORE, CARRO]})

        ic27_saida_6 = local.Local(IC27_SAIDA_6,
                                   {CORTE_DAS_DONAS: [SUDESTE, CORTE_DAS_DONAS__IC27_SAIDA_6, CARRO],
                                    BALURCOS: [NORDESTE, BALURCOS__IC27_SAIDA_6, CARRO],
                                    PALMEIRA: [SUDOESTE, IC27_SAIDA_6__PALMEIRA, CARRO]})

        laranjeiras = local.Local(LARANJEIRAS,
                                  {GUERREIROS_DO_RIO: [SUDESTE, GUERREIROS_DO_RIO__LARANJEIRAS, CARRO],
                                   MONTINHO_DAS_LARANJEIRAS: [NOROESTE, LARANJEIRAS__MONTINHO_DAS_LARANJEIRAS, CARRO]})

        montinho_das_laranjeiras = local.Local(MONTINHO_DAS_LARANJEIRAS,
                                               {ALCOUTIM_CIMO: [NORTE, ALCOUTIM_CIMO__MONTINHO_DAS_LARANJEIRAS, CARRO],
                                                LARANJEIRAS: [SUDESTE, LARANJEIRAS__MONTINHO_DAS_LARANJEIRAS, CARRO]})

        palmeira = local.Local(PALMEIRA,
                               {IC27_SAIDA_6: [NORDESTE, IC27_SAIDA_6__PALMEIRA, CARRO]})

        parque_empresarial_alcoutim = local.Local(PARQUE_EMPRESARIAL_ALCOUTIM,
                                                  {ALCOUTIM_CIMO: [NORDESTE,
                                                                   ALCOUTIM_CIMO__PARQUE_EMPRESARIAL_ALCOUTIM, CARRO],
                                                   BALURCOS: [SUL, BALURCOS__PARQUE_EMPRESARIAL_ALCOUTIM, CARRO]})

        rotunda_da_arvore = local.Local(ROTUNDA_DA_ARVORE,
                                        {GUERREIROS_DO_RIO: [NORTE, GUERREIROS_DO_RIO__ROTUNDA_DA_ARVORE, CARRO],
                                         CORTE_DAS_DONAS: [OESTE, CORTE_DAS_DONAS__ROTUNDA_DA_ARVORE, CARRO],
                                         ALAMO: [SUL, ALAMO__ROTUNDA_DA_ARVORE, CARRO]})

        #  Adicionar os locais à lista
        self.lista_locais.append(alamo)
        self.lista_locais.append(alcoutim_cimo)
        self.lista_locais.append(balurcos)
        self.lista_locais.append(corte_das_donas)
        self.lista_locais.append(foz_de_odeleite)
        self.lista_locais.append(guerreiros_do_rio)
        self.lista_locais.append(ic27_saida_6)
        self.lista_locais.append(laranjeiras)
        self.lista_locais.append(montinho_das_laranjeiras)
        self.lista_locais.append(palmeira)
        self.lista_locais.append(parque_empresarial_alcoutim)
        self.lista_locais.append(rotunda_da_arvore)

        #  Retornar a lista de locais
        return self.lista_locais
