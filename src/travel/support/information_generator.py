import os
from typing import Union, Optional

import requests
import matplotlib.pyplot as plt

from travel.support import ways
from travel.support.ways import Way
import travel.support.sorter as ordenador
import travel.support.haversine as haversine
import travel.support.distance_calculator as calculadora_distancias
import travel.support.osm_interface as osm_interface
from travel.support.coordinate import Coordinate
from travel.main import paths_and_files


class Path:

    def __init__(self, *args):
        path_list: list = []
        for arg in args:
            if type(arg) == Path:
                arg = arg.path
            path_list.append(arg)
        self.path: str = os.path.join(*path_list)

    def get_path(self) -> str:
        return self.path


COORDENADAS_CASAS_DECIMAIS: int = 6
ENCODING: str = 'utf-8'

CHAVE_API_PATH: Path = Path(paths_and_files.GOOGLE_API_KEY_FILEPATH)
PASTA_TEMP: Path = Path(paths_and_files.TMP_FOLDER_PATH)

OPCAO_SAIR = 0
OPCAO_LOCAIS_DIV_ADMIN = 1
OPCAO_LIGACOES_DESTINOS = 2
OPCAO_CIMA_BAIXO = 1
OPCAO_BAIXO_CIMA = 2
OPCAO_AREA_INTERCIDADES = 1
OPCAO_AREA_URBANA = 2

"""
Gera ficheiros .csv com informação de saídas de auto-estradas e linhas ferroviárias, e suas ligações
"""


class GeradorInformacao:

    def __init__(self, way_to_analise: Way, obter_altitudes=True) -> None:
        self.way_type: str = way_to_analise.way_type  # Road or railway
        self.way_display_name: str = way_to_analise.display_name  # Name to be displayed in the filenames, ex: "North Line"
        self.way_osm_name: str = way_to_analise.osm_name  # OSM name, ex: "Linha do Norte"
        self.country: str = way_to_analise.country

        self.obter_altitudes: bool = obter_altitudes

        self.api_key = None

        self.local_path: Path = Path(PASTA_TEMP, f'{self.way_display_name}_local.csv')
        self.local_espanha_path: Path = Path(PASTA_TEMP, f'{self.way_display_name}_local_espanha.csv')
        self.local_portugal_path: Path = Path(PASTA_TEMP, f'{self.way_display_name}_local_portugal.csv')
        self.local_gibraltar_path: Path = Path(PASTA_TEMP, f'{self.way_display_name}_local_gibraltar.csv')
        self.municipio_path: Path = Path(PASTA_TEMP, f'{self.way_display_name}_municipio.csv')
        self.comarca_path: Path = Path(PASTA_TEMP, f'{self.way_display_name}_comarca.csv')
        self.concelho_path: Path = Path(PASTA_TEMP, f'{self.way_display_name}_concelho.csv')
        self.ligacao_path: Path = Path(PASTA_TEMP, f'{self.way_display_name}_ligacao.csv')
        self.destino_path: Path = Path(PASTA_TEMP, f'{self.way_display_name}_destino.csv')

        print("Bem-vindo/a ao gerador automático de informação.")
        print("Escreva a opção desejada e pressione ENTER.")
        print(f"{OPCAO_SAIR} - Sair do programa")
        print(f"{OPCAO_LOCAIS_DIV_ADMIN} - Gerar locais e divisões administrativas da {self.way_display_name}")
        print(f"{OPCAO_LIGACOES_DESTINOS} - Gerar ligações e destinos da {self.way_display_name}")
        while True:
            opcao = input("Escreva a opção desejada e pressione ENTER: ")
            if opcao == str(OPCAO_SAIR):
                print("Escolheu sair.")
                print("Boa viagem!")
                exit(0)
            elif opcao == str(OPCAO_LOCAIS_DIV_ADMIN):
                print(f"Escolheu gerar os locais e divisões administrativas da {self.way_display_name}.")
                self.opcao_obter_locais_divisoes_admins()
                break
            elif opcao == str(OPCAO_LIGACOES_DESTINOS):
                print(f"Escolheu gerar as ligações e destinos da {self.way_display_name}.")
                self.opcao_obter_ligacoes_destinos()
                break
        exit(0)

    def opcao_obter_ligacoes_destinos(self) -> None:
        """
        A partir de um ficheiro de locais de uma via, cria os ficheiros de ligações e de destinos correspondentes
        """
        if self.country not in ways.ALL_SUPPORTED_COUNTRIES:
            print(f'País inválido - Processamento da {self.way_display_name} cancelado')
            exit(1)

        if not os.path.exists(self.local_path.path):
            print(f'O ficheiro de locais da {self.way_display_name} não existe.')
            print(f'Execute este programa novamente e seleccione a opção {OPCAO_LOCAIS_DIV_ADMIN}.')
            exit(0)
        aviso: str = f'A {self.way_display_name} parece já ter um ficheiro de ligações.'
        self._detector_ficheiro_repetido(self.ligacao_path.path, aviso)
        aviso: str = f'A {self.way_display_name} parece já ter um ficheiro de destinos.'
        self._detector_ficheiro_repetido(self.destino_path.path, aviso)

        print(f'Como deseja que a {self.way_display_name} seja ordenada?')
        print("Escreva a opção desejada e pressione ENTER")
        print(f"{OPCAO_SAIR} - Sair do programa")
        print(f"{OPCAO_CIMA_BAIXO} - De cima para baixo")
        print(f"{OPCAO_BAIXO_CIMA} - De baixo para cima")
        while True:
            opcao = input("Escreva a opção desejada e pressione ENTER: ")
            if opcao == str(OPCAO_SAIR):
                print("Escolheu sair.")
                print("Boa viagem!")
                exit(0)
            elif opcao == str(OPCAO_LOCAIS_DIV_ADMIN):
                print(f"A {self.way_display_name} será ordenada de cima para baixo")
                invertido: bool = False
                break
            elif opcao == str(OPCAO_LIGACOES_DESTINOS):
                print(f"A {self.way_display_name} será ordenada de baixo para cima")
                invertido: bool = True
                break

        self.create_ficheiros_ligacoes_destinos(invertido=invertido)
        print(f'{self.way_display_name} processada')
        print("Boa viagem!")

    def opcao_obter_locais_divisoes_admins(self) -> None:
        """
        Recolhe informação sobre as saídas de uma auto-estrada / estações de uma linha ferroviária usando o OSM e cria
        os respectivos ficheiros de locais e de divisões administrativas
        """
        aviso: str = f'A {self.way_display_name} parece já ter sido processada antes.'
        self._detector_ficheiro_repetido(self.local_path.path, aviso)

        if self.country not in ways.ALL_SUPPORTED_COUNTRIES:
            print(f'País inválido - Processamento da {self.way_display_name} cancelado')
            exit(1)

        # Chave da API da Google - Usada para obter altitudes
        with open(CHAVE_API_PATH.path, 'r', encoding=ENCODING) as f:
            self.api_key: str = f.readlines()[0]

        self.create_ficheiros_locais_divisoes_admins()
        print(f'{self.way_display_name} processada')
        print("Boa viagem!")

    def create_ficheiros_locais_divisoes_admins(self) -> None:
        print("################")
        print(f'A iniciar processamento da {self.way_display_name}...')
        print("################\n")

        saidas_estacoes_coordenadas: dict[str, Coordinate] = self.get_saidas_estacoes()
        saidas_estacoes_ordenadas: list[str] = list(saidas_estacoes_coordenadas.keys())
        saidas_estacoes_ordenadas.sort()

        if self.way_type == ways.RAILWAY:
            print(f'{len(saidas_estacoes_ordenadas)} estações encontradas')
        else:
            print(f'{len(saidas_estacoes_ordenadas)} saídas encontradas')
        if len(saidas_estacoes_ordenadas) == 0:
            print(f'Processamento da {self.way_display_name} cancelado')
            exit(1)

        if not os.path.exists(PASTA_TEMP.path):
            os.makedirs(PASTA_TEMP.path)

        with open(os.path.join(self.local_path.path), 'w', encoding=ENCODING) as f:
            for saida_ou_estacao in saidas_estacoes_ordenadas:  # Ex: 2 para uma auto-estrada, "Cascais" para uma ferrovia
                latitude: float = saidas_estacoes_coordenadas[saida_ou_estacao].get_latitude()
                longitude: float = saidas_estacoes_coordenadas[saida_ou_estacao].get_longitude()
                altitude: int = 0
                info_extra: str = ''
                lote: int = 0
                if self.obter_altitudes:
                    if self.way_type == ways.RAILWAY:
                        print(f'A obter a altitude da estação {saida_ou_estacao}...')
                    else:
                        print(f'A obter a altitude da saída {saida_ou_estacao}...')
                    altitude: int = self.get_altitude(latitude, longitude)
                if self.way_type == ways.RAILWAY:
                    f.write(f'Estação de {saida_ou_estacao},{latitude},{longitude},{altitude},{info_extra},{lote}\n')
                else:
                    f.write(f'{self.way_display_name} - Saída {saida_ou_estacao},{latitude},{longitude},{altitude},{info_extra},{lote}\n')
        ordenador.ordenar_ficheiros_csv(ficheiro_a_ordenar=self.local_path.path, cabecalho=False)
        print(f'Ficheiro de locais criado')

        saidas_estacoes_terminadas: int = 0

        if self.country == ways.SPAIN:
            municipios: set[str] = set()
            comarcas: set[str] = set()

            divisoes_pretendidas: list[int] = [osm_interface.PROVINCE, osm_interface.COMARCA, osm_interface.SPANISH_MUNICIPALITY, osm_interface.SPANISH_DISTRICT]
            divisoes_saidas_estacoes: dict[Coordinate, dict[Union[str, int], Optional[str]]] = self.get_divisoes_administrativas(
                list(saidas_estacoes_coordenadas.values()), divisoes_pretendidas)  # {(37.1, -7.5): {6: 'Alcoutim', 7: 'Alcoutim', 8: 'Faro'}}

            with open(self.local_espanha_path.path, 'w', encoding=ENCODING) as f:
                for saida_ou_estacao in saidas_estacoes_ordenadas:
                    ponto: Coordinate = saidas_estacoes_coordenadas[saida_ou_estacao]

                    municipio: str = divisoes_saidas_estacoes.get(ponto, {}).get(osm_interface.SPANISH_MUNICIPALITY, "")
                    provincia: str = divisoes_saidas_estacoes.get(ponto, {}).get(osm_interface.PROVINCE, "")
                    comarca: str = divisoes_saidas_estacoes.get(ponto, {}).get(osm_interface.COMARCA, '')  # Nem sempre está disponível
                    distrito_es: str = divisoes_saidas_estacoes.get(ponto, {}).get(osm_interface.SPANISH_DISTRICT, '')  # Só disponível nas grandes cidades

                    if self.way_type == ways.RAILWAY:
                        if distrito_es:
                            f.write(f'Estação de {saida_ou_estacao},{municipio},{provincia},{distrito_es}\n')
                        else:
                            f.write(f'Estação de {saida_ou_estacao},{municipio},{provincia},\n')
                    else:
                        if distrito_es:
                            f.write(f'{self.way_display_name} - Saída {saida_ou_estacao},{municipio},{provincia},{distrito_es}\n')
                        else:
                            f.write(f'{self.way_display_name} - Saída {saida_ou_estacao},{municipio},{provincia},\n')

                    municipios.add(f'{municipio},{provincia}\n')
                    if comarca:
                        comarcas.add(f'{municipio},{comarca},{provincia}\n')

                    saidas_estacoes_terminadas += 1
                    if self.way_type == ways.RAILWAY:
                        print(f'Estação {saida_ou_estacao} terminada - '
                              f'{saidas_estacoes_terminadas}/{len(saidas_estacoes_ordenadas)} estações processadas')
                    else:
                        print(f'Saída {saida_ou_estacao} terminada - '
                              f'{saidas_estacoes_terminadas}/{len(saidas_estacoes_ordenadas)} saídas processadas')

            with open(self.municipio_path.path, 'w', encoding=ENCODING) as f:
                for municipio in municipios:
                    f.write(municipio)

            with open(self.comarca_path.path, 'w', encoding=ENCODING) as f:
                for comarca in comarcas:
                    f.write(comarca)

            ordenador.ordenar_ficheiros_csv(ficheiro_a_ordenar=self.local_espanha_path.path, cabecalho=False)
            print("Ficheiro de locais de Espanha terminado")
            ordenador.ordenar_ficheiros_csv(ficheiro_a_ordenar=self.municipio_path.path, cabecalho=False)
            print("Ficheiro de municípios terminado")
            ordenador.ordenar_ficheiros_csv(ficheiro_a_ordenar=self.comarca_path.path, cabecalho=False)
            print("Ficheiro de comarcas terminado")

        elif self.country == ways.PORTUGAL:
            concelhos: set[str] = set()

            divisoes_pretendidas: list[Union[str, int]] = [
                osm_interface.PORTUGUESE_DISTRICT, osm_interface.PORTUGUESE_MUNICIPALITY, osm_interface.PORTUGUESE_PARISH, osm_interface.PORTUGUESE_HISTORIC_PARISH]
            divisoes_saidas_estacoes:  dict[Coordinate, dict[Union[str, int], Optional[str]]] = self.get_divisoes_administrativas(
                list(saidas_estacoes_coordenadas.values()), divisoes_pretendidas)  # {(37.1, -7.5): {6: 'Alcoutim', 7: 'Alcoutim', 8: 'Faro'}}

            with open(self.local_portugal_path.path, 'w', encoding=ENCODING) as f:
                for saida_ou_estacao in saidas_estacoes_ordenadas:
                    ponto: Coordinate = saidas_estacoes_coordenadas[saida_ou_estacao]

                    freguesia: str = divisoes_saidas_estacoes.get(ponto, {}).get(osm_interface.PORTUGUESE_HISTORIC_PARISH, "")  # Antiga freguesia, se existir
                    if not freguesia:
                        freguesia = divisoes_saidas_estacoes.get(ponto, {}).get(osm_interface.PORTUGUESE_PARISH, "")
                    concelho: str = divisoes_saidas_estacoes.get(ponto, {}).get(osm_interface.PORTUGUESE_MUNICIPALITY, "")
                    distrito: str = divisoes_saidas_estacoes.get(ponto, {}).get(osm_interface.PORTUGUESE_DISTRICT, "")

                    if self.way_type == ways.RAILWAY:
                        f.write(f'Estação de {saida_ou_estacao},{freguesia},{concelho}\n')
                    else:
                        f.write(f'{self.way_display_name} - Saída {saida_ou_estacao},{freguesia},{concelho}\n')

                    concelhos.add(f'{concelho},,{distrito},\n')  # Inserir manualmente entidade intermunicipal e região histórica

                    saidas_estacoes_terminadas += 1
                    if self.way_type == ways.RAILWAY:
                        print(f'Estação {saida_ou_estacao} terminada - '
                              f'{saidas_estacoes_terminadas}/{len(saidas_estacoes_ordenadas)} estações processadas')
                    else:
                        print(f'Saída {saida_ou_estacao} terminada - '
                              f'{saidas_estacoes_terminadas}/{len(saidas_estacoes_ordenadas)} saídas processadas')

            with open(self.concelho_path.path, 'w', encoding=ENCODING) as f:
                for concelho in concelhos:
                    f.write(concelho)

            ordenador.ordenar_ficheiros_csv(ficheiro_a_ordenar=self.local_portugal_path.path, cabecalho=False)
            print("Ficheiro de locais de Portugal terminado")
            ordenador.ordenar_ficheiros_csv(ficheiro_a_ordenar=self.concelho_path.path, cabecalho=False)
            print("Ficheiro de concelhos terminado")

        else:
            pass

    def create_ficheiros_ligacoes_destinos(self, invertido: bool) -> None:
        with open(self.local_path.path, 'r', encoding=ENCODING) as f:
            conteudo: list[str] = f.readlines()

        if len(conteudo) == 0:
            print(f'O ficheiro de locais da {self.way_display_name} está vazio.')
            print("A sair.")
            exit(0)
        elif len(conteudo) == 1:
            print(f'O ficheiro de locais da {self.way_display_name} só tem 1 local.')
            print("Não é possível criar ligações nem destinos.")
            print("A sair.")
            exit(0)

        if invertido:
            conteudo = list(reversed(conteudo))

        # Gerar mapa para depois com ele se calcularem as distâncias
        todas_coordenadas: list[Coordinate] = []
        for idx, local in enumerate(conteudo):
            if idx <= len(conteudo) - 2:  # Índice não é o do último elemento
                linha_a: str = conteudo[idx]
                linha_b: str = conteudo[idx + 1]
                elementos_a: list[str] = linha_a.split(",")
                elementos_b: list[str] = linha_b.split(",")
                elementos_a: list[str] = ordenador.separar_por_virgulas(lista=elementos_a)  # '"Álamo', 'Alcoutim"' -> '"Álamo, Alcoutim"'
                elementos_b: list[str] = ordenador.separar_por_virgulas(lista=elementos_b)

                if conteudo[idx + 1].strip() == '':  # Linha vazia - Parar processamento aqui
                    break

                latitude_a, longitude_a = float(elementos_a[1]), float(elementos_a[2])
                latitude_b, longitude_b = float(elementos_b[1]), float(elementos_b[2])
                if not Coordinate(latitude_a, longitude_a) in todas_coordenadas:
                    todas_coordenadas.append(Coordinate(latitude_a, longitude_a))
                if not Coordinate(latitude_b, longitude_b) in todas_coordenadas:
                    todas_coordenadas.append(Coordinate(latitude_b, longitude_b))

        # Mostrar via a cobrir num gráfico
        latitudes = [coordenadas.latitude for coordenadas in todas_coordenadas]
        longitudes = [coordenadas.longitude for coordenadas in todas_coordenadas]
        plt.plot(longitudes, latitudes)
        plt.ylabel('Latitude')
        plt.xlabel('Longitude')
        intervalo_latitudes = max(latitudes) - min(latitudes)
        intervalo_longitudes = max(longitudes) - min(longitudes)
        intervalo = max((intervalo_latitudes, intervalo_longitudes))
        if intervalo_longitudes == intervalo:
            plt.xlim(min(longitudes), min(longitudes) + intervalo)
        else:  # Centrar gráfico
            margem = (intervalo - intervalo_longitudes) / 2
            plt.xlim(min(longitudes) - margem, max(longitudes) + margem)
        if intervalo_latitudes == intervalo:
            plt.ylim(min(latitudes), min(latitudes) + intervalo)
        else:  # Centrar gráfico
            margem = (intervalo - intervalo_latitudes) / 2
            plt.ylim(min(latitudes) - margem, max(latitudes) + margem)
        plt.show()

        calc_dist: calculadora_distancias.CalculadoraDistancias = calculadora_distancias.CalculadoraDistancias()
        calc_dist.gerar_mapa_processado(todas_coordenadas, self.way_type, self.country, via_nome=self.way_osm_name)

        origem = ordenador.separar_por_virgulas(lista=conteudo[0].split(','))[0]
        destino = ordenador.separar_por_virgulas(lista=conteudo[-1].split(','))[0]
        print("\nIntroduza os destinos já conhecidos separados por vírgulas, depois pressione ENTER.")
        print("Ou pressione ENTER sem destinos para gerar um ficheiro sem destinos pré-preenchidos.")
        destinos_para_inicio: list[str] = input(f"Introduza os destinos desde {destino} em direcção a {origem}: ").split(",")
        destinos_para_fim: list[str] = input(f"Introduza os destinos desde {origem} em direcção a {destino}: ").split(",")

        ligacoes: list[str] = []
        destinos: list[str] = []
        for idx, local in enumerate(conteudo):
            if idx <= len(conteudo) - 2:  # Índice não é o do último elemento
                linha_a: str = conteudo[idx]
                linha_b: str = conteudo[idx + 1]
                elementos_a: list[str] = linha_a.split(",")
                elementos_b: list[str] = linha_b.split(",")
                elementos_a: list[str] = ordenador.separar_por_virgulas(lista=elementos_a)  # '"Álamo', 'Alcoutim"' -> '"Álamo, Alcoutim"'
                elementos_b: list[str] = ordenador.separar_por_virgulas(lista=elementos_b)

                local_a: str = elementos_a[0]
                local_b: str = elementos_b[0].strip()

                if local_b == '':  # Linha vazia - Parar processamento aqui
                    print("Linha vazia encontrada - Processamento será apenas parcial")
                    break

                if self.way_type == ways.RAILWAY:
                    meio_transporte: str = 'Train'
                else:
                    meio_transporte: str = 'Car'

                info_extra: str = self.way_display_name
                latitude_a, longitude_a = float(elementos_a[1]), float(elementos_a[2])
                latitude_b, longitude_b = float(elementos_b[1]), float(elementos_b[2])
                ponto_cardeal: str = haversine.obter_ponto_cardeal(origem=(latitude_a, longitude_a), destino=(latitude_b, longitude_b))
                ordem_a = 2
                ordem_b = 1

                distancia: float = calc_dist.calcular_distancia_com_ajustes(
                    Coordinate(latitude_a, longitude_a), Coordinate(latitude_b, longitude_b))
                if distancia == calculadora_distancias.DISTANCIA_INFINITA:
                    print("Não foi possível calcular distância - Continuando...")
                    distancia = 0.0

                ligacao: str = f'{local_a},{local_b},{meio_transporte},{distancia},{info_extra},{ponto_cardeal},{ordem_a},{ordem_b}\n'
                ligacoes.append(ligacao)

                if destinos_para_inicio:
                    for destino in destinos_para_inicio:
                        destino_false: str = f'{local_a},{local_b},{meio_transporte},False,{destino}\n'
                        destinos.append(destino_false)
                destino_false: str = f'{local_a},{local_b},{meio_transporte},False,\n'  # Linha vazia para facilitar o adicionar de mais destinos
                destinos.append(destino_false)

                if destinos_para_fim:
                    for destino in destinos_para_fim:
                        destino_true: str = f'{local_a},{local_b},{meio_transporte},True,{destino}\n'
                        destinos.append(destino_true)
                destino_true: str = f'{local_a},{local_b},{meio_transporte},True,\n'  # Linha vazia para facilitar o adicionar de mais destinos
                destinos.append(destino_true)

                print(f'{idx + 1}/{len(conteudo) - 1} ligações processadas')  # Conta todas as linhas mesmo com linhas vazias pelo meio

        with open(self.ligacao_path.path, 'w', encoding=ENCODING) as f:
            f.writelines(ligacoes)
        with open(self.destino_path.path, 'w', encoding=ENCODING) as f:
            f.writelines(destinos)

    def get_altitude(self, latitude: float, longitude: float) -> int:
        try:
            url: str = f'https://maps.googleapis.com/maps/api/elevation/json?locations={latitude},{longitude}&key={self.api_key}'
            return int(requests.get(url=url).json()['results'][0]['elevation'])
        except Exception as e:
            print(str(e))
            return 0

    def get_divisoes_administrativas(self, locais: list[Coordinate], divisoes_pretendidas: list[Union[str, int]]
                                     ) -> dict[Coordinate, dict[Union[str, int], Optional[str]]]:
        """
        Dado uma lista de coordenadas, retorna dicionário com, para cada local, os nomes das divisões administrativas pretendidas
        """
        print("A obter divisões administrativas...")

        divisoes_admins_por_pontos: dict[Coordinate, dict[Union[str, int], Optional[str]]] = {}
        for coordenadas in locais:
            divisoes_admins_de_ponto: dict[Union[str, int], Optional[str]] = {}

            retorno: dict[Union[str, int], str] = osm_interface.OsmInterface.obter_divisoes_administrativas_de_ponto(coordenadas)

            for chave in retorno:
                if chave not in divisoes_pretendidas:
                    continue

                divisao_admin: Union[str, int] = retorno[chave]
                divisoes_admins_de_ponto[chave] = divisao_admin

            for chave in divisoes_pretendidas:
                if chave not in divisoes_admins_de_ponto:  # Se divisão pretendida não foi encontrada para aquele ponto, inserir None
                    divisoes_admins_de_ponto[chave] = None

            divisoes_admins_por_pontos[coordenadas] = divisoes_admins_de_ponto

        print("Divisões administrativas obtidas\n")
        return divisoes_admins_por_pontos

    def get_saidas_estacoes(self) -> dict[str, Coordinate]:
        if self.way_type == ways.RAILWAY:
            print("A obter nós correspondentes a estações...")
        else:
            print("A obter nós correspondentes a saídas...")

        if self.way_type == ways.RAILWAY:
            saidas_estacoes_temp: dict[str, list[Coordinate]] = osm_interface.OsmInterface.obter_estacoes_de_linha_ferroviaria(
                self.way_osm_name, self.country)
        else:
            saidas_estacoes_temp: dict[str, list[Coordinate]] = osm_interface.OsmInterface.obter_saidas_de_estrada(
                self.way_osm_name, self.country)

        if len(saidas_estacoes_temp) == 0:
            if self.way_type == ways.RAILWAY:
                print(f"Não foi encontrado nenhum nó associado às estações da {self.way_display_name}. "
                      f"A ferrovia está em {self.country}?")
                print(f"Pode também ser uma ferrovia sem estações associadas no OpenStreetMap")
            else:
                print(f'Não foi encontrado nenhum nó associado às saídas da {self.way_display_name}. '
                      f'A auto-estrada está em {self.country}?')
                print(f'Pode também ser uma auto-estrada sem números de saída no OpenStreetMap')
            exit(0)

        saidas_ou_estacoes: dict[str, Coordinate] = {}  # Contém apenas o "centro" de cada estação ou saída
        for saida_ou_estacao in saidas_estacoes_temp:
            latitude = 0.0
            longitude = 0.0
            for ponto in saidas_estacoes_temp[saida_ou_estacao]:
                latitude += ponto.get_latitude()
                longitude += ponto.get_longitude()
            latitude = round(latitude / len(saidas_estacoes_temp[saida_ou_estacao]), COORDENADAS_CASAS_DECIMAIS)
            longitude = round(longitude / len(saidas_estacoes_temp[saida_ou_estacao]), COORDENADAS_CASAS_DECIMAIS)
            saidas_ou_estacoes[saida_ou_estacao] = Coordinate(latitude, longitude)

        if self.way_type == ways.RAILWAY:
            print("Coordenadas de estações obtidas\n")
        else:
            print("Coordenadas de saídas obtidas\n")

        return saidas_ou_estacoes

    def _detector_ficheiro_repetido(self, path: str, aviso: str) -> None:
        """
        Detecta se o ficheiro fornecido existe. Se existe, apresenta o aviso ao utilizador e dá opção de escolha.
        Se a opção for de cancelar, sai do programa, caso contrário continua
        :param path: Path do ficheiro
        :param aviso: String de aviso que indique qual o ficheiro já existente
        :return:
        """
        if os.path.exists(path):
            print(aviso)
            print(f'Se continuar, irá reescrever o ficheiro criado. Deseja prosseguir?')
            while True:
                opcao = repr(input(f'Escreva S para prosseguir ou N para cancelar a operação, depois pressione ENTER:'))
                if 's' in opcao.lower():
                    print()
                    break
                elif 'n' in opcao.lower():
                    print(f'Processamento da {self.way_display_name} cancelado.')
                    exit(0)
