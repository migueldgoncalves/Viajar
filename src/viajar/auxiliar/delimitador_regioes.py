from viajar.auxiliar import vias
from viajar.auxiliar import osm_interface
from viajar.auxiliar.osm_interface import OsmInterface

SAIR = 0
PORTUGAL = 1
ESPANHA = 2
ANDORRA = 3
GIBRALTAR = 4


def sair_por_opcao() -> None:
    print("Escolheu sair")
    print("Até à próxima!")
    exit(0)


def imprimir_pontos_extremos_e_sair(nome: str, nivel_admin: int, pais_desejado: str) -> None:
    output = OsmInterface().obter_pontos_extremos_regiao(nome=nome, nivel_administrativo=nivel_admin, pais=pais_desejado)
    print(output)
    exit(0)


def obter_pontos_extremos():
    """
    Rotina principal
    """
    try:
        sucesso = OsmInterface().testar_ligacao()
        if not sucesso:  # Pelo menos um servidor desligado
            print("Os servidores estão desligados")
            print("Ligue-os e volte a executar este script")
            exit(0)

        print("Bem-vindo/a ao delimitador de regiões")
        print("Irá obter os pontos extremos de uma região")

        pais: str = ''

        # Escolher país

        print(f'{SAIR} - Sair, {PORTUGAL} - Portugal, {ESPANHA} - Espanha, {ANDORRA} - Andorra, {GIBRALTAR} - Gibraltar')
        while True:
            try:
                opcao: int = int(input("Indique o país ao qual pertence a região pretendida: "))
            except ValueError:
                print("Deve introduzir um número")
                continue

            if opcao == SAIR:
                sair_por_opcao()

            elif opcao == PORTUGAL:
                pais = vias.PORTUGAL
                print("Escolheu Portugal")
                break
            elif opcao == ESPANHA:
                pais = vias.ESPANHA
                print("Escolheu Espanha")
                break
            elif opcao == ANDORRA:
                pais = vias.ANDORRA
                print("Escolheu Andorra")
                break
            elif opcao == GIBRALTAR:
                pais = vias.GIBRALTAR
                print("Escolheu Gibraltar, território ultramarino do Reino Unido")
                break

        # Escolher região

        if pais == vias.GIBRALTAR:  # Não tem subdivisões, calcular extremos do território de Gibraltar
            imprimir_pontos_extremos_e_sair("Gibraltar", osm_interface.GIBRALTAR_NIVEL_ADMIN, pais)

        elif pais == vias.ANDORRA:
            print(f'{SAIR} - Sair, {osm_interface.PAIS} - País inteiro, {osm_interface.PAROQUIA} - Paróquia')
            while True:
                try:
                    opcao = int(input("Indique o tipo de região pretendido: "))
                except ValueError:
                    continue

                if opcao == SAIR:
                    sair_por_opcao()

                elif opcao == osm_interface.PAIS:  # País inteiro — Não é preciso pedir nome da região
                    nivel_regiao = osm_interface.PAIS
                    imprimir_pontos_extremos_e_sair("Andorra", nivel_regiao, pais)

                elif opcao == osm_interface.PAROQUIA:
                    nivel_regiao = osm_interface.PAROQUIA

                    nome_regiao = input("Indique o nome da paróquia: ").strip()
                    if not nome_regiao:
                        continue
                    imprimir_pontos_extremos_e_sair(nome_regiao, nivel_regiao, pais)

        elif pais == vias.ESPANHA:
            print(f'{SAIR} - Sair, {osm_interface.PAIS} - País, {osm_interface.COMUNIDADE_AUTONOMA} - Comunidade Autónoma, '
                  f'{osm_interface.PROVINCIA} - Província, {osm_interface.COMARCA} - Comarca, {osm_interface.MUNICIPIO} - Município, '
                  f'{osm_interface.DISTRITO_ES} - Distrito')

            while True:
                try:
                    opcao = int(input("Indique o tipo de região pretendido: "))
                except ValueError:
                    continue

                if opcao == SAIR:
                    sair_por_opcao()

                elif opcao == osm_interface.PAIS:  # País inteiro — Não é preciso pedir nome da região
                    nivel_regiao = osm_interface.PAIS
                    imprimir_pontos_extremos_e_sair("España", nivel_regiao, pais)

                elif opcao in [osm_interface.COMUNIDADE_AUTONOMA, osm_interface.PROVINCIA, osm_interface.COMARCA,
                               osm_interface.MUNICIPIO, osm_interface.DISTRITO_ES]:
                    nivel_regiao = opcao

                    nome_regiao = input("Indique o nome da região: ").strip()
                    if not nome_regiao:
                        continue
                    imprimir_pontos_extremos_e_sair(nome_regiao, nivel_regiao, pais)

        elif pais == vias.PORTUGAL:
            print(f'{SAIR} - Sair, {osm_interface.PAIS} - País, {osm_interface.DISTRITO_PT} - Distrito, '
                  f'{osm_interface.CONCELHO} - Concelho, {osm_interface.FREGUESIA} - Freguesia')

            while True:
                try:
                    opcao = int(input("Indique o tipo de região pretendido: "))
                except ValueError:
                    continue

                if opcao == SAIR:
                    sair_por_opcao()

                elif opcao == osm_interface.PAIS:  # País inteiro — Não é preciso pedir nome da região
                    nivel_regiao = osm_interface.PAIS
                    imprimir_pontos_extremos_e_sair("Portugal", nivel_regiao, pais)

                elif opcao in [osm_interface.DISTRITO_PT, osm_interface.CONCELHO, osm_interface.FREGUESIA]:
                    nivel_regiao = opcao

                    nome_regiao = input("Indique o nome da região: ").strip()
                    if not nome_regiao:
                        continue
                    imprimir_pontos_extremos_e_sair(nome_regiao, nivel_regiao, pais)

    except Exception as e:
        print("Ocurreu uma excepção")
        print(e.args)
        print("A sair...")
        exit(1)
