"""
Main - Executar para aceder a todos os scripts disponíveis
"""

import viajar.auxiliar.vias as vias
# INSERIR AQUI estrada ou linha ferroviária para ser analisada pelo gerador
VIA = vias.PT_A23

OPCAO_SAIR = 0

OPCAO_VIAJAR = 1
OPCAO_CARRO = 2
OPCAO_COMBATE = 3

OPCAO_GERADOR = 4
OPCAO_ORDENADOR = 5
OPCAO_SQLITE = 6

print("===============================")
print("Bem-vindo/a ao projecto Viajar")
print("===============================")

print("Que script deseja correr?")
print("")
while True:
    print(f"{OPCAO_SAIR} - Sair")

    print("Scripts principais")
    print(f'{OPCAO_VIAJAR} - Viajar')
    print(f'{OPCAO_CARRO} - Carro')
    print(f'{OPCAO_COMBATE} - Combate')

    print("Scripts auxiliares")
    print(f'{OPCAO_GERADOR} - Gerador automático de informação')
    print(f'{OPCAO_ORDENADOR} - Ordenador de ficheiros .csv')
    print(f'{OPCAO_SQLITE} - Criador de bases de dados SQLite')

    try:
        opcao = int(input("Insira o número pretendido e depois prima ENTER: "))
    except:
        opcao = ''

    if opcao == OPCAO_SAIR:
        print("Escolheu sair")
        print("Até à próxima")
        exit(0)

    # Colocar os imports junto do respectivo código permite correr o script com Linux e Windows

    elif opcao == OPCAO_VIAJAR:
        from viajar import viajar
        viajar.Viajar.realizar_viagem(viajar.Viajar())
    elif opcao == OPCAO_CARRO:
        from carro import carro
        carro.Carro.viajar(carro.Carro(), distancia_a_percorrer=0, destino="")
        '''
        README CARRO

        É necessário correr este script num terminal normal do Windows ou equivalente
        Isso deve-se ao uso da biblioteca msvcrt para detectar e ler teclas pressionadas

        O comando Run do IDE PyCharm apenas irá funcionar se
        Em Run > Edit Configurations se seleccione a opção Emulate terminal in output console
        Porém, com esse comando todos os caracteres não-ASCII irão aparecer desformatados
        '''
    elif opcao == OPCAO_COMBATE:
        from combate import ronda
        ronda.Ronda.ronda_loop(ronda.Ronda())

    elif opcao == OPCAO_GERADOR:
        import viajar.auxiliar.gerador_informacao as gerador
        gerador.GeradorInformacao(VIA)
    elif opcao == OPCAO_ORDENADOR:
        from viajar.auxiliar import ordenador
        ordenador.ordenar_ficheiros_csv()
    elif opcao == OPCAO_SQLITE:
        from viajar.auxiliar import sqlite_interface
        sqlite_interface.SQLiteBDInterface()
