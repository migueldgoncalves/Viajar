from travel.support import ways
from travel.support import osm_interface
from travel.support.osm_interface import OsmInterface

SAIR = 0
PORTUGAL = 1
ESPANHA = 2
ILHAS_CANARIAS = 3
ANDORRA = 4
GIBRALTAR = 5


def sair_por_opcao() -> None:
    print("Escolheu sair")
    print("Até à próxima!")
    exit(0)


def imprimir_pontos_extremos_e_sair(nome: str, nivel_admin: int, pais_desejado: str) -> None:
    output = OsmInterface().get_region_extreme_points(name=nome, admin_level=nivel_admin, country=pais_desejado)
    print(output)
    exit(0)


def obter_pontos_extremos():
    """
    Rotina principal
    """
    try:
        sucesso = OsmInterface().test_connections()
        if not sucesso:  # Pelo menos um servidor desligado
            print("Os servidores estão desligados")
            print("Ligue-os e volte a executar este script")
            exit(0)

        print("Bem-vindo/a ao delimitador de regiões")
        print("Irá obter os pontos extremos de uma região")

        pais: str = ''

        # Escolher país

        print(f'{SAIR} - Sair, {PORTUGAL} - Portugal, {ESPANHA} - Espanha Peninsular + Baleares + Ceuta + Melilla, {ILHAS_CANARIAS} - Ilhas Canárias, {ANDORRA} - Andorra, {GIBRALTAR} - Gibraltar')
        while True:
            try:
                opcao: int = int(input("Indique o país ao qual pertence a região pretendida: "))
            except ValueError:
                print("Deve introduzir um número")
                continue

            if opcao == SAIR:
                sair_por_opcao()

            elif opcao == PORTUGAL:
                pais = ways.PORTUGAL
                print("Escolheu Portugal")
                break
            elif opcao == ESPANHA:
                pais = ways.SPAIN
                print("Escolheu a Espanha Peninsular, Baleares, Ceuta, Melilla")
                break
            elif opcao == ILHAS_CANARIAS:
                pais = ways.CANARY_ISLANDS
                print("Escolheu as Ilhas Canárias")
                break
            elif opcao == ANDORRA:
                pais = ways.ANDORRA
                print("Escolheu Andorra")
                break
            elif opcao == GIBRALTAR:
                pais = ways.GIBRALTAR
                print("Escolheu Gibraltar, território ultramarino do Reino Unido")
                break

        # Escolher região

        if pais == ways.GIBRALTAR:  # Não tem subdivisões, calcular extremos do território de Gibraltar
            imprimir_pontos_extremos_e_sair("Gibraltar", osm_interface.GIBRALTAR_ADMIN_LEVEL, pais)

        elif pais == ways.ANDORRA:
            print(f'{SAIR} - Sair, {osm_interface.COUNTRY} - País inteiro, {osm_interface.ANDORRAN_PARISH} - Paróquia')
            while True:
                try:
                    opcao = int(input("Indique o tipo de região pretendido: "))
                except ValueError:
                    continue

                if opcao == SAIR:
                    sair_por_opcao()

                elif opcao == osm_interface.COUNTRY:  # País inteiro — Não é preciso pedir nome da região
                    nivel_regiao = osm_interface.COUNTRY
                    imprimir_pontos_extremos_e_sair("Andorra", nivel_regiao, pais)

                elif opcao == osm_interface.ANDORRAN_PARISH:
                    nivel_regiao = osm_interface.ANDORRAN_PARISH

                    nome_regiao = input("Indique o nome da paróquia: ").strip()
                    if not nome_regiao:
                        continue
                    imprimir_pontos_extremos_e_sair(nome_regiao, nivel_regiao, pais)

        elif pais in [ways.SPAIN, ways.CANARY_ISLANDS]:
            print(f'{SAIR} - Sair, {osm_interface.COUNTRY} - País/Região, {osm_interface.AUTONOMOUS_COMMUNITY} - Comunidade Autónoma, '
                  f'{osm_interface.PROVINCE} - Província, {osm_interface.COMARCA} - Comarca, {osm_interface.SPANISH_MUNICIPALITY} - Município, '
                  f'{osm_interface.SPANISH_DISTRICT} - Distrito')

            while True:
                try:
                    opcao = int(input("Indique o tipo de região pretendido: "))
                except ValueError:
                    continue

                if opcao == SAIR:
                    sair_por_opcao()

                elif opcao == osm_interface.COUNTRY:  # País inteiro — Não é preciso pedir nome da região
                    nivel_regiao = osm_interface.COUNTRY
                    imprimir_pontos_extremos_e_sair("España", nivel_regiao, pais)

                elif opcao in [osm_interface.AUTONOMOUS_COMMUNITY, osm_interface.PROVINCE, osm_interface.COMARCA,
                               osm_interface.SPANISH_MUNICIPALITY, osm_interface.SPANISH_DISTRICT]:
                    nivel_regiao = opcao

                    nome_regiao = input("Indique o nome da região: ").strip()
                    if not nome_regiao:
                        continue
                    imprimir_pontos_extremos_e_sair(nome_regiao, nivel_regiao, pais)

        elif pais == ways.PORTUGAL:
            print(f'{SAIR} - Sair, {osm_interface.COUNTRY} - País, {osm_interface.PORTUGUESE_DISTRICT} - Distrito, '
                  f'{osm_interface.PORTUGUESE_MUNICIPALITY} - Concelho, {osm_interface.PORTUGUESE_PARISH} - Freguesia')

            while True:
                try:
                    opcao = int(input("Indique o tipo de região pretendido: "))
                except ValueError:
                    continue

                if opcao == SAIR:
                    sair_por_opcao()

                elif opcao == osm_interface.COUNTRY:  # País inteiro — Não é preciso pedir nome da região
                    nivel_regiao = osm_interface.COUNTRY
                    imprimir_pontos_extremos_e_sair("Portugal", nivel_regiao, pais)

                elif opcao in [osm_interface.PORTUGUESE_DISTRICT, osm_interface.PORTUGUESE_MUNICIPALITY, osm_interface.PORTUGUESE_PARISH]:
                    nivel_regiao = opcao

                    nome_regiao = input("Indique o nome da região: ").strip()
                    if not nome_regiao:
                        continue
                    imprimir_pontos_extremos_e_sair(nome_regiao, nivel_regiao, pais)

    except Exception as e:
        print("Ocorreu uma excepção")
        print(e.args)
        print("A sair...")
        exit(1)
