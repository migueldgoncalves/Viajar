from typing import Union, Optional
import os
import requests

from travel.support import ways
from travel.support.ways import Way
import travel.support.sorter as sorter
import travel.support.haversine as haversine
import travel.support.distance_calculator as distance_calculator
import travel.support.osm_interface as osm_interface
from travel.support.coordinates import Coordinates
from travel.main import paths_and_files
from travel.main import menu

COORDINATES_DECIMAL_PLACES: int = 6
ENCODING: str = 'utf-8'

OPTION_LOCATION_INFO = 1
OPTION_CONNECTIONS_AND_DESTINATIONS = 2
OPTION_TOP_DOWN = 1
OPTION_BOTTOM_UP = 2


class InformationGenerator:
    """
    This class generates .csv files with info covering a freeway/motorway or a railway
        How to use:
            First, generate the location info for the desired way, by calling this class
            Then, manually sort the exits/stations, if needed. This step might be skipped for roads, but is virtually always necessary for railways
            Finally, generate the connection and destination info for the desired way, by calling again this class
    """

    def __init__(self, way_to_analise: Way, get_altitude_info=False) -> None:
        """
        Important: Altitude info is fetched from Google Cloud. While the first thousands of requests are free, this is a paid API
            For safety, get_altitude_info defaults to False
        """
        self.way_type: str = way_to_analise.way_type  # Road or railway
        self.way_display_name: str = way_to_analise.display_name  # Name to be displayed in the filenames, ex: "North Line"
        self.way_osm_name: str = way_to_analise.osm_name  # OSM name, ex: "Linha do Norte" (Portuguese for "North Line")
        self.country: str = way_to_analise.country

        self.get_altitude_info: bool = get_altitude_info

        self.google_api_key: Optional[str] = self._get_google_api_key()  # Will be None if key is missing

    def present_main_menu(self) -> None:
        """
        Main entry point - Presents the main menu of the information generator
        """
        print("Welcome to the automatic information generator of the Viajar project")

        option_labels: list[str] = [
            f'Generate location info for {self.way_display_name}',
            f'Generate connection and destination info for {self.way_display_name}'
        ]
        menu_introduction: list[str] = ['Which option do you want to select?']

        # Guaranteed to be valid non-exit option
        user_option = menu.present_numeric_menu(option_labels, menu_introduction)

        # Processes user option
        if user_option == OPTION_LOCATION_INFO:
            print(f"You have chosen to generate location info for {self.way_display_name}")
            self.process_option_get_location_info()
        elif user_option == OPTION_CONNECTIONS_AND_DESTINATIONS:
            print(f"You have chosen to generate connection and destination info for {self.way_display_name}")
            self.process_option_get_connections_and_destinations()

    def process_option_get_connections_and_destinations(self) -> None:
        """
        Assuming that there is already a file for the locations of the desired way, this routine creates the files
            containing the respective connections and destination info
        """
        if self.country not in ways.ALL_SUPPORTED_COUNTRIES:
            print(f'Invalid country - Cancelling processing of {self.way_display_name}')
            exit(1)

        if not os.path.exists(self._get_filepath(paths_and_files.TMP_CSV_LOCATION_PATH)):
            print(f'Location info file for {self.way_display_name} does not exist.')
            print(f'Please run this program again, then select option {OPTION_LOCATION_INFO} to generate the location info for {self.way_display_name}.')
            exit(0)

        warning: str = f'A connection info file already exists for {self.way_display_name}'
        self._repeated_file_detector(self._get_filepath(paths_and_files.TMP_CSV_CONNECTION_PATH), warning)
        # It can be assumed that either there is a connections file and a destinations file, or none of them, as they are generated at the same time
        #   Therefore, the user can be presented with a single confirmation dialog

        menu_introduction: list[str] = [f'How do you wish to list {self.way_display_name} connections and destinations?']
        option_labels = [
            'Top-Down',
            'Bottom-Up'
        ]

        # Guaranteed to be valid non-exit option
        option: int = menu.present_numeric_menu(option_labels, menu_introduction)

        inverted: bool = False
        if option == OPTION_TOP_DOWN:
            print(f'{self.way_display_name} connections and destinations will be listed from start to end')
            # inverted is already False
        elif option == OPTION_BOTTOM_UP:
            print(f'{self.way_display_name} connections and destinations will be listed from end to start')
            inverted = True

        self.create_connections_and_destinations_files(inverted=inverted)

        print(f'{self.way_display_name} has been processed')
        print("Have a safe trip!")

    def process_option_get_location_info(self) -> None:
        """
        Collects information regarding either the exits of a freeway / motorway or the stations of a railway using OSM
            and Google, then stores this info in dedicated files
        """
        warning: str = f'{self.way_display_name} seems to have been processed before'
        self._repeated_file_detector(self._get_filepath(paths_and_files.TMP_CSV_LOCATION_PATH), warning)

        if self.country not in ways.ALL_SUPPORTED_COUNTRIES:
            print(f'Invalid country - Cancelling processing of {self.way_display_name}')
            exit(1)

        self.create_locations_files()

        print(f'{self.way_display_name} has been processed')
        print("Have a safe trip!")

    def create_locations_files(self) -> None:
        """
        Assuming that a way name was previously provided, this routine processes it and generates the following files:
        Always - location.csv
        If the way is in Spain - location_spain.csv, municipio.csv, and comarca.csv
        If the way is in Portugal - location_portugal.csv, and concelho.csv
        There is no support for Gibraltar nor for Andorra
        """
        print("################")
        print(f"Starting processing of {self.way_display_name}...")
        print("################\n")  # The \n adds an extra line as a visual separator

        saidas_estacoes_coordenadas: dict[str, Coordinates] = self.get_saidas_estacoes()
        saidas_estacoes_ordenadas: list[str] = list(saidas_estacoes_coordenadas.keys())
        saidas_estacoes_ordenadas.sort()

        if self.way_type == ways.RAILWAY:
            print(f'{len(saidas_estacoes_ordenadas)} estações encontradas')
        else:
            print(f'{len(saidas_estacoes_ordenadas)} saídas encontradas')
        if len(saidas_estacoes_ordenadas) == 0:
            print(f'Processamento da {self.way_display_name} cancelado')
            exit(1)

        if not os.path.exists(paths_and_files.TMP_FOLDER_PATH):
            os.makedirs(paths_and_files.TMP_FOLDER_PATH)

        with open(os.path.join(self._get_filepath(paths_and_files.TMP_CSV_LOCATION_PATH)), 'w', encoding=ENCODING) as f:
            for saida_ou_estacao in saidas_estacoes_ordenadas:  # Ex: 2 para uma auto-estrada, "Cascais" para uma ferrovia
                latitude: float = saidas_estacoes_coordenadas[saida_ou_estacao].get_latitude()
                longitude: float = saidas_estacoes_coordenadas[saida_ou_estacao].get_longitude()
                altitude: int = 0
                info_extra: str = ''
                lote: int = 0
                if self.get_altitude_info:
                    if self.way_type == ways.RAILWAY:
                        print(f'A obter a altitude da estação {saida_ou_estacao}...')
                    else:
                        print(f'A obter a altitude da saída {saida_ou_estacao}...')
                    altitude: int = self.get_altitude(latitude, longitude)
                if self.way_type == ways.RAILWAY:
                    f.write(f'Estação de {saida_ou_estacao},{latitude},{longitude},{altitude},{info_extra},{lote}\n')
                else:
                    f.write(f'{self.way_display_name} - Saída {saida_ou_estacao},{latitude},{longitude},{altitude},{info_extra},{lote}\n')
        sorter.ordenar_ficheiros_csv(ficheiro_a_ordenar=self._get_filepath(paths_and_files.TMP_CSV_LOCATION_PATH), cabecalho=False)
        print(f'Ficheiro de locais criado')

        saidas_estacoes_terminadas: int = 0

        if self.country == ways.SPAIN:
            municipios: set[str] = set()
            comarcas: set[str] = set()

            divisoes_pretendidas: list[int] = [osm_interface.PROVINCE, osm_interface.COMARCA, osm_interface.SPANISH_MUNICIPALITY, osm_interface.SPANISH_DISTRICT]
            divisoes_saidas_estacoes: dict[Coordinates, dict[Union[str, int], Optional[str]]] = self.get_divisoes_administrativas(
                list(saidas_estacoes_coordenadas.values()), divisoes_pretendidas)  # {(37.1, -7.5): {6: 'Alcoutim', 7: 'Alcoutim', 8: 'Faro'}}

            with open(self._get_filepath(paths_and_files.TMP_CSV_LOCATION_SPAIN_PATH), 'w', encoding=ENCODING) as f:
                for saida_ou_estacao in saidas_estacoes_ordenadas:
                    ponto: Coordinates = saidas_estacoes_coordenadas[saida_ou_estacao]

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

            with open(self._get_filepath(paths_and_files.TMP_CSV_MUNICIPIO_PATH), 'w', encoding=ENCODING) as f:
                for municipio in municipios:
                    f.write(municipio)

            with open(self._get_filepath(paths_and_files.TMP_CSV_COMARCA_PATH), 'w', encoding=ENCODING) as f:
                for comarca in comarcas:
                    f.write(comarca)

            sorter.ordenar_ficheiros_csv(ficheiro_a_ordenar=self._get_filepath(paths_and_files.TMP_CSV_LOCATION_SPAIN_PATH), cabecalho=False)
            print("Ficheiro de locais de Espanha terminado")
            sorter.ordenar_ficheiros_csv(ficheiro_a_ordenar=self._get_filepath(paths_and_files.TMP_CSV_MUNICIPIO_PATH), cabecalho=False)
            print("Ficheiro de municípios terminado")
            sorter.ordenar_ficheiros_csv(ficheiro_a_ordenar=self._get_filepath(paths_and_files.TMP_CSV_COMARCA_PATH), cabecalho=False)
            print("Ficheiro de comarcas terminado")

        elif self.country == ways.PORTUGAL:
            concelhos: set[str] = set()

            divisoes_pretendidas: list[Union[str, int]] = [
                osm_interface.PORTUGUESE_DISTRICT, osm_interface.PORTUGUESE_MUNICIPALITY, osm_interface.PORTUGUESE_PARISH, osm_interface.PORTUGUESE_HISTORIC_PARISH]
            divisoes_saidas_estacoes:  dict[Coordinates, dict[Union[str, int], Optional[str]]] = self.get_divisoes_administrativas(
                list(saidas_estacoes_coordenadas.values()), divisoes_pretendidas)  # {(37.1, -7.5): {6: 'Alcoutim', 7: 'Alcoutim', 8: 'Faro'}}

            with open(self._get_filepath(paths_and_files.TMP_CSV_LOCATION_PORTUGAL_PATH), 'w', encoding=ENCODING) as f:
                for saida_ou_estacao in saidas_estacoes_ordenadas:
                    ponto: Coordinates = saidas_estacoes_coordenadas[saida_ou_estacao]

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

            with open(self._get_filepath(paths_and_files.TMP_CSV_CONCELHO_PATH), 'w', encoding=ENCODING) as f:
                for concelho in concelhos:
                    f.write(concelho)

            sorter.ordenar_ficheiros_csv(ficheiro_a_ordenar=self._get_filepath(paths_and_files.TMP_CSV_LOCATION_PORTUGAL_PATH), cabecalho=False)
            print("Ficheiro de locais de Portugal terminado")
            sorter.ordenar_ficheiros_csv(ficheiro_a_ordenar=self._get_filepath(paths_and_files.TMP_CSV_CONCELHO_PATH), cabecalho=False)
            print("Ficheiro de concelhos terminado")

        else:
            pass

    def create_connections_and_destinations_files(self, inverted: bool) -> None:
        with open(self._get_filepath(paths_and_files.TMP_CSV_LOCATION_PATH), 'r', encoding=ENCODING) as f:
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

        if inverted:
            conteudo = list(reversed(conteudo))

        # Gerar mapa para depois com ele se calcularem as distâncias
        todas_coordenadas: list[Coordinates] = []
        for idx, local in enumerate(conteudo):
            if idx <= len(conteudo) - 2:  # Índice não é o do último elemento
                linha_a: str = conteudo[idx]
                linha_b: str = conteudo[idx + 1]
                elementos_a: list[str] = linha_a.split(",")
                elementos_b: list[str] = linha_b.split(",")
                elementos_a: list[str] = sorter.separar_por_virgulas(lista=elementos_a)  # '"Álamo', 'Alcoutim"' -> '"Álamo, Alcoutim"'
                elementos_b: list[str] = sorter.separar_por_virgulas(lista=elementos_b)

                if conteudo[idx + 1].strip() == '':  # Linha vazia - Parar processamento aqui
                    break

                latitude_a, longitude_a = float(elementos_a[1]), float(elementos_a[2])
                latitude_b, longitude_b = float(elementos_b[1]), float(elementos_b[2])
                if not Coordinates(latitude_a, longitude_a) in todas_coordenadas:
                    todas_coordenadas.append(Coordinates(latitude_a, longitude_a))
                if not Coordinates(latitude_b, longitude_b) in todas_coordenadas:
                    todas_coordenadas.append(Coordinates(latitude_b, longitude_b))

        calc_dist: distance_calculator.DistanceCalculator = distance_calculator.DistanceCalculator()
        calc_dist.generate_processed_map(todas_coordenadas, self.way_type, self.country, way_name=self.way_osm_name)

        origem = sorter.separar_por_virgulas(lista=conteudo[0].split(','))[0]
        destino = sorter.separar_por_virgulas(lista=conteudo[-1].split(','))[0]
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
                elementos_a: list[str] = sorter.separar_por_virgulas(lista=elementos_a)  # '"Álamo', 'Alcoutim"' -> '"Álamo, Alcoutim"'
                elementos_b: list[str] = sorter.separar_por_virgulas(lista=elementos_b)

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
                ponto_cardeal: str = haversine.get_cardinal_point(
                    source=Coordinates(latitude_a, longitude_a), destination=Coordinates(latitude_b, longitude_b))
                ordem_a = 2
                ordem_b = 1

                distancia: float = calc_dist.calculate_distance_with_adjusts(
                    Coordinates(latitude_a, longitude_a), Coordinates(latitude_b, longitude_b))
                if distancia == distance_calculator.INFINITE_DISTANCE:
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

        with open(self._get_filepath(paths_and_files.TMP_CSV_CONNECTION_PATH), 'w', encoding=ENCODING) as f:
            f.writelines(ligacoes)
        with open(self._get_filepath(paths_and_files.TMP_CSV_DESTINATION_PATH), 'w', encoding=ENCODING) as f:
            f.writelines(destinos)

    def get_altitude(self, latitude: float, longitude: float) -> int:
        if not self.google_api_key:  # File containing the key is missing?
            return 0  # Return default

        try:
            url: str = f'https://maps.googleapis.com/maps/api/elevation/json?locations={latitude},{longitude}&key={self.google_api_key}'
            return int(requests.get(url=url).json()['results'][0]['elevation'])
        except Exception as e:
            print(str(e))
            return 0

    def get_divisoes_administrativas(self, locais: list[Coordinates], divisoes_pretendidas: list[Union[str, int]]
                                     ) -> dict[Coordinates, dict[Union[str, int], Optional[str]]]:
        """
        Dado uma lista de coordenadas, retorna dicionário com, para cada local, os nomes das divisões administrativas pretendidas
        """
        print("A obter divisões administrativas...")

        divisoes_admins_por_pontos: dict[Coordinates, dict[Union[str, int], Optional[str]]] = {}
        for coordenadas in locais:
            divisoes_admins_de_ponto: dict[Union[str, int], Optional[str]] = {}

            retorno: dict[Union[str, int], str] = osm_interface.OsmInterface.get_administrative_divisions_by_coordinates(coordenadas)

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

    def get_saidas_estacoes(self) -> dict[str, Coordinates]:
        if self.way_type == ways.RAILWAY:
            print("A obter nós correspondentes a estações...")
        else:
            print("A obter nós correspondentes a saídas...")

        if self.way_type == ways.RAILWAY:
            saidas_estacoes_temp: dict[str, list[Coordinates]] = osm_interface.OsmInterface.get_railway_stations(
                self.way_osm_name, self.country)
        else:
            saidas_estacoes_temp: dict[str, list[Coordinates]] = osm_interface.OsmInterface.get_road_exits(
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

        saidas_ou_estacoes: dict[str, Coordinates] = {}  # Contém apenas o "centro" de cada estação ou saída
        for saida_ou_estacao in saidas_estacoes_temp:
            latitude = 0.0
            longitude = 0.0
            for ponto in saidas_estacoes_temp[saida_ou_estacao]:
                latitude += ponto.get_latitude()
                longitude += ponto.get_longitude()
            latitude = round(latitude / len(saidas_estacoes_temp[saida_ou_estacao]), COORDINATES_DECIMAL_PLACES)
            longitude = round(longitude / len(saidas_estacoes_temp[saida_ou_estacao]), COORDINATES_DECIMAL_PLACES)
            saidas_ou_estacoes[saida_ou_estacao] = Coordinates(latitude, longitude)

        if self.way_type == ways.RAILWAY:
            print("Coordenadas de estações obtidas\n")
        else:
            print("Coordenadas de saídas obtidas\n")

        return saidas_ou_estacoes

    def _repeated_file_detector(self, path: str, warning_message: str) -> None:
        """
        Given a filepath, detects if the file exists. If so, prints the provided warning message, and allows the user
            to cancel operation or to continue anyway.
        """
        if os.path.exists(path):
            menu_introduction: list[str] = [warning_message, 'If you proceed, you will overwrite the existing file. Do you wish to proceed?']
            proceed: bool = menu.present_boolean_menu(menu_introduction)

            if not proceed:
                print(f'Processing of {self.way_display_name} has been cancelled. Exiting')
                exit(0)

            # In case user has agreed to proceed nevertheless, do nothing and just return

    def _get_google_api_key(self) -> Optional[str]:
        """
        Returns Google API key into memory - It is used to get altitude info
        Google API key is expected to be in a dedicated .txt file
        IMPORTANT: Do not add this .txt file to any VCS repository
        """
        try:
            if not os.path.exists(paths_and_files.GOOGLE_API_KEY_FILEPATH):
                print(f"Google API key not found - Expected path is: {paths_and_files.GOOGLE_API_KEY_FILEPATH}")
                return None

            with open(paths_and_files.GOOGLE_API_KEY_FILEPATH, 'r', encoding=ENCODING) as f:
                api_key = f.readlines()[0]
                return api_key
        except:
            print("Error while getting Google API key")
            return None

    def _get_filepath(self, filepath_with_placeholder: str) -> str:
        """
        Given a filepath with a placeholder, returns the final filepath, with the way name replacing the placeholder
        Ex: 'D:\foo\\placeholder_location.csv' -> 'D:\foo\freeway_name_location.csv'
        """
        return filepath_with_placeholder.replace(paths_and_files.TMP_CSV_WAY_NAME_PLACEHOLDER, self.way_display_name)
