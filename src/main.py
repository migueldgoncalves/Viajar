import travel.support.ways as vias

"""
Main - Executar para aceder a todos os scripts disponíveis
"""

# INSERIR AQUI estrada ou linha ferroviária para ser analisada pelo gerador
VIA = vias.ES_A2

OPCAO_SAIR = 0

OPCAO_VIAJAR = 1
OPCAO_CARRO = 2
OPCAO_COMBATE = 3

OPCAO_GERADOR = 4
OPCAO_ORDENADOR = 5
OPCAO_SQLITE = 6
OPCAO_DELIMITADOR = 7

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
    print(f'{OPCAO_DELIMITADOR} - Calculadora de pontos extremos de uma região')

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
        from travel.main import travel
        travel.Viajar().realizar_viagem()
    elif opcao == OPCAO_CARRO:
        from car import car
        car.Carro().viajar(distancia_a_percorrer=0, destino="")
        '''
        README CARRO

        É necessário correr este script num terminal normal do Windows ou equivalente
        Isso deve-se ao uso da biblioteca msvcrt para detectar e ler teclas pressionadas

        O comando Run do IDE PyCharm apenas irá funcionar se
        Em Run > Edit Configurations se seleccione a opção Emulate terminal in output console
        Porém, com esse comando todos os caracteres não-ASCII irão aparecer desformatados
        '''
    elif opcao == OPCAO_COMBATE:
        from combat import round
        round.Ronda().ronda_loop()

    elif opcao == OPCAO_GERADOR:
        import travel.support.information_generator as gerador
        gerador.GeradorInformacao(VIA)
    elif opcao == OPCAO_ORDENADOR:
        from travel.support import sorter
        sorter.ordenar_ficheiros_csv()
    elif opcao == OPCAO_SQLITE:
        from travel.support import sqlite_interface
        sqlite_interface.SQLiteBDInterface()
    elif opcao == OPCAO_DELIMITADOR:
        from travel.support import region_bounds_finder
        region_bounds_finder.obter_pontos_extremos()
