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
ALCOUTIM = "Alcoutim"
BALURCO_DE_BAIXO = "Balurco de Baixo"
BALURCO_DE_CIMA = "Balurco de Cima"
BAR_DO_RIO = "Bar do Rio"
CORTE_DAS_DONAS = "Corte das Donas"
CORTES_PEREIRAS = "Cortes Pereiras"
CORTE_TABELIAO = "Corte Tabelião"
ENTRONCAMENTO_FIM_IC27 = "Entroncamento a seguir ao IC27"
FOZ_DE_ODELEITE = "Foz de Odeleite"
FURNAZINHAS = "Furnazinhas"
GIOES = "Giões"
GUERREIROS_DO_RIO = "Guerreiros do Rio"
IC27_FIM = "IC27-Fim"
IC27_SAIDA_1 = "IC27-Saída 1"
IC27_SAIDA_2 = "IC27-Saída 2"
IC27_SAIDA_3 = "IC27-Saída 3"
IC27_SAIDA_4 = "IC27-Saída 4"
IC27_SAIDA_5 = "IC27-Saída 5"
IC27_SAIDA_6 = "IC27-Saída 6"
IC27_SAIDA_7 = "IC27-Saída 7"
LARANJEIRAS = "Laranjeiras"
MARTINLONGO = "Martinlongo"
MONTINHO_DAS_LARANJEIRAS = "Montinho das Laranjeiras"
PALMEIRA = "Palmeira"
PARQUE_EMPRESARIAL_ALCOUTIM = "Parque Empresarial de Alcoutim"
PEREIRO = "Pereiro"
RIBEIRA_DO_VASCAO = "Ribeira do Vascão"
ROTUNDA_DA_ARVORE = "Rotunda da Árvore"
SANLUCAR_DEL_GUADIANA = "Sanlúcar del Guadiana"
SANTA_MARTA = "Santa Marta"
TENENCIA = "Tenência"
VAQUEIROS = "Vaqueiros"

#  Distâncias (km)
ALAMO__ROTUNDA_DA_ARVORE = 0.5
ALAMO__FOZ_DE_ODELEITE = 3.7
ALCOUTIM__CORTES_PEREIRAS = 6.0
ALCOUTIM__CORTE_TABELIAO = 5.0
ALCOUTIM__MONTINHO_DAS_LARANJEIRAS = 8.8
ALCOUTIM__PARQUE_EMPRESARIAL_ALCOUTIM = 5.0
BALURCO_DE_BAIXO__CORTE_DAS_DONAS = 6.8
BALURCO_DE_BAIXO__BALURCO_DE_CIMA = 1.6
BALURCO_DE_BAIXO__IC27_SAIDA_6 = 4.7
BALURCO_DE_BAIXO__PARQUE_EMPRESARIAL_ALCOUTIM = 1.5
BALURCO_DE_CIMA__IC27_SAIDA_7 = 1.1
BAR_DO_RIO__GUERREIROS_DO_RIO = 0.1
CORTE_DAS_DONAS__ROTUNDA_DA_ARVORE = 2.1
CORTE_DAS_DONAS__IC27_SAIDA_6 = 6.9
CORTES_PEREIRAS__ENTRONCAMENTO_FIM_IC27 = 4.8
CORTE_TABELIAO__PARQUE_EMPRESARIAL_ALCOUTIM = 6.6
CORTE_TABELIAO__IC27_FIM = 5.9
ENTRONCAMENTO_FIM_IC27__IC27_FIM = 0.5
ENTRONCAMENTO_FIM_IC27__SANTA_MARTA = 1.8
FURNAZINHAS__IC27_SAIDA_5 = 5.4
FURNAZINHAS__VAQUEIROS = 17.6
GIOES__MARTINLONGO = 9.4
GIOES__PEREIRO = 11.2
GUERREIROS_DO_RIO__LARANJEIRAS = 1.2
GUERREIROS_DO_RIO__ROTUNDA_DA_ARVORE = 0.7
IC27_FIM__IC27_SAIDA_7 = 6.1
IC27_SAIDA_5__IC27_SAIDA_6 = 5.1
IC27_SAIDA_5__TENENCIA = 3.3
IC27_SAIDA_6__IC27_SAIDA_7 = 3.7
IC27_SAIDA_6__PALMEIRA = 0.7
IC27_SAIDA_7__PARQUE_EMPRESARIAL_ALCOUTIM = 3.0
IC27_SAIDA_7__PEREIRO = 6.1
LARANJEIRAS__MONTINHO_DAS_LARANJEIRAS = 0.5
MARTINLONGO__VAQUEIROS = 7.7
RIBEIRA_DO_VASCAO__SANTA_MARTA = 3.6


class Locais:
    lista_locais = []

    def preencher_lista_locais(self):
        #  Criar os locais
        alamo = local.Local(ALAMO,
                            {ROTUNDA_DA_ARVORE: [NORTE, ALAMO__ROTUNDA_DA_ARVORE, CARRO],
                             FOZ_DE_ODELEITE: [SUL, ALAMO__FOZ_DE_ODELEITE, CARRO]})

        alcoutim = local.Local(ALCOUTIM,
                               {PARQUE_EMPRESARIAL_ALCOUTIM: [SUDOESTE, ALCOUTIM__PARQUE_EMPRESARIAL_ALCOUTIM, CARRO],
                                MONTINHO_DAS_LARANJEIRAS: [SUL, ALCOUTIM__MONTINHO_DAS_LARANJEIRAS, CARRO],
                                CORTE_TABELIAO: [SUDOESTE, ALCOUTIM__CORTE_TABELIAO, CARRO],
                                CORTES_PEREIRAS: [NOROESTE, ALCOUTIM__CORTES_PEREIRAS, CARRO],
                                SANLUCAR_DEL_GUADIANA: [NORDESTE, 0, BARCO],
                                LARANJEIRAS: [SUL, 0, BARCO]})

        bar_do_rio = local.Local(BAR_DO_RIO,
                                 {GUERREIROS_DO_RIO: [OESTE, BAR_DO_RIO__GUERREIROS_DO_RIO, CARRO],
                                  LARANJEIRAS: [NOROESTE, 0, BARCO],
                                  FOZ_DE_ODELEITE: [SUL, 0, BARCO]})

        balurco_de_baixo = local.Local(BALURCO_DE_BAIXO,
                                       {CORTE_DAS_DONAS: [SUDESTE, BALURCO_DE_BAIXO__CORTE_DAS_DONAS, CARRO],
                                        PARQUE_EMPRESARIAL_ALCOUTIM: [NORTE, BALURCO_DE_BAIXO__PARQUE_EMPRESARIAL_ALCOUTIM, CARRO],
                                        IC27_SAIDA_6: [SUDOESTE, BALURCO_DE_BAIXO__IC27_SAIDA_6, CARRO],
                                        BALURCO_DE_CIMA: [NOROESTE, BALURCO_DE_BAIXO__BALURCO_DE_CIMA, CARRO]})

        balurco_de_cima = local.Local(BALURCO_DE_CIMA,
                                      {IC27_SAIDA_7: [NOROESTE, BALURCO_DE_CIMA__IC27_SAIDA_7, CARRO],
                                       BALURCO_DE_BAIXO: [SUDESTE, BALURCO_DE_BAIXO__BALURCO_DE_CIMA, CARRO]})

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

        entroncamento_fim_ic27 = local.Local(ENTRONCAMENTO_FIM_IC27,
                                             {IC27_FIM: [SUDESTE, ENTRONCAMENTO_FIM_IC27__IC27_FIM, CARRO],
                                              CORTES_PEREIRAS: [ESTE, CORTES_PEREIRAS__ENTRONCAMENTO_FIM_IC27, CARRO],
                                              SANTA_MARTA: [NOROESTE, ENTRONCAMENTO_FIM_IC27__SANTA_MARTA, CARRO]})

        foz_de_odeleite = local.Local(FOZ_DE_ODELEITE,
                                      {ALAMO: [NORTE, ALAMO__FOZ_DE_ODELEITE, CARRO],
                                       BAR_DO_RIO: [NORTE, 0, BARCO]})

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

        ic27_saida_5 = local.Local(IC27_SAIDA_5,
                                   {IC27_SAIDA_6: [NORTE, IC27_SAIDA_5__IC27_SAIDA_6, CARRO],
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

        laranjeiras = local.Local(LARANJEIRAS,
                                  {GUERREIROS_DO_RIO: [SUDESTE, GUERREIROS_DO_RIO__LARANJEIRAS, CARRO],
                                   MONTINHO_DAS_LARANJEIRAS: [NOROESTE, LARANJEIRAS__MONTINHO_DAS_LARANJEIRAS, CARRO],
                                   ALCOUTIM: [NORTE, 0, BARCO],
                                   BAR_DO_RIO: [SUDESTE, 0, BARCO]})

        martinlongo = local.Local(MARTINLONGO,
                                  {VAQUEIROS: [SUDESTE, MARTINLONGO__VAQUEIROS, CARRO],
                                   GIOES: [NORDESTE, GIOES__MARTINLONGO, CARRO]})

        montinho_das_laranjeiras = local.Local(MONTINHO_DAS_LARANJEIRAS,
                                               {ALCOUTIM: [NORTE, ALCOUTIM__MONTINHO_DAS_LARANJEIRAS, CARRO],
                                                LARANJEIRAS: [SUDESTE, LARANJEIRAS__MONTINHO_DAS_LARANJEIRAS, CARRO]})

        palmeira = local.Local(PALMEIRA,
                               {IC27_SAIDA_6: [NORDESTE, IC27_SAIDA_6__PALMEIRA, CARRO]})

        parque_empresarial_alcoutim = local.Local(PARQUE_EMPRESARIAL_ALCOUTIM,
                                                  {ALCOUTIM: [NORDESTE, ALCOUTIM__PARQUE_EMPRESARIAL_ALCOUTIM, CARRO],
                                                   BALURCO_DE_BAIXO: [SUL, BALURCO_DE_BAIXO__PARQUE_EMPRESARIAL_ALCOUTIM, CARRO],
                                                   IC27_SAIDA_7: [OESTE, IC27_SAIDA_7__PARQUE_EMPRESARIAL_ALCOUTIM, CARRO],
                                                   CORTE_TABELIAO: [NORTE, CORTE_TABELIAO__PARQUE_EMPRESARIAL_ALCOUTIM, CARRO]})

        pereiro = local.Local(PEREIRO,
                              {GIOES: [NOROESTE, GIOES__PEREIRO, CARRO],
                               IC27_SAIDA_7: [SUDESTE, IC27_SAIDA_7__PEREIRO, CARRO]})

        ribeira_do_vascao = local.Local(RIBEIRA_DO_VASCAO,
                                        {SANTA_MARTA: [SUL, RIBEIRA_DO_VASCAO__SANTA_MARTA, CARRO]})

        rotunda_da_arvore = local.Local(ROTUNDA_DA_ARVORE,
                                        {GUERREIROS_DO_RIO: [NORTE, GUERREIROS_DO_RIO__ROTUNDA_DA_ARVORE, CARRO],
                                         CORTE_DAS_DONAS: [OESTE, CORTE_DAS_DONAS__ROTUNDA_DA_ARVORE, CARRO],
                                         ALAMO: [SUL, ALAMO__ROTUNDA_DA_ARVORE, CARRO]})

        sanlucar_del_guadiana = local.Local(SANLUCAR_DEL_GUADIANA,
                                            {ALCOUTIM: [SUDOESTE, 0, BARCO]})

        santa_marta = local.Local(SANTA_MARTA,
                                  {ENTRONCAMENTO_FIM_IC27: [SUDESTE, ENTRONCAMENTO_FIM_IC27__SANTA_MARTA, CARRO],
                                   RIBEIRA_DO_VASCAO: [NORTE, RIBEIRA_DO_VASCAO__SANTA_MARTA, CARRO]})

        tenencia = local.Local(TENENCIA,
                               {IC27_SAIDA_5: [SUDOESTE, IC27_SAIDA_5__TENENCIA, CARRO]})

        vaqueiros = local.Local(VAQUEIROS,
                                {FURNAZINHAS: [SUDESTE, FURNAZINHAS__VAQUEIROS, CARRO],
                                 MARTINLONGO: [NOROESTE, MARTINLONGO__VAQUEIROS, CARRO]})

        #  Adicionar os locais à lista
        self.lista_locais.append(alamo)
        self.lista_locais.append(alcoutim)
        self.lista_locais.append(balurco_de_baixo)
        self.lista_locais.append(balurco_de_cima)
        self.lista_locais.append(bar_do_rio)
        self.lista_locais.append(corte_das_donas)
        self.lista_locais.append(cortes_pereiras)
        self.lista_locais.append(corte_tabeliao)
        self.lista_locais.append(entroncamento_fim_ic27)
        self.lista_locais.append(foz_de_odeleite)
        self.lista_locais.append(furnazinhas)
        self.lista_locais.append(gioes)
        self.lista_locais.append(guerreiros_do_rio)
        self.lista_locais.append(ic27_fim)
        self.lista_locais.append(ic27_saida_5)
        self.lista_locais.append(ic27_saida_6)
        self.lista_locais.append(ic27_saida_7)
        self.lista_locais.append(laranjeiras)
        self.lista_locais.append(martinlongo)
        self.lista_locais.append(montinho_das_laranjeiras)
        self.lista_locais.append(palmeira)
        self.lista_locais.append(parque_empresarial_alcoutim)
        self.lista_locais.append(pereiro)
        self.lista_locais.append(ribeira_do_vascao)
        self.lista_locais.append(rotunda_da_arvore)
        self.lista_locais.append(sanlucar_del_guadiana)
        self.lista_locais.append(santa_marta)
        self.lista_locais.append(tenencia)
        self.lista_locais.append(vaqueiros)

        #  Retornar a lista de locais
        return self.lista_locais
