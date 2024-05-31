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

        coordinates: dict[str, Coordinates] = self.get_exits_or_stations_coordinates()
        sorted_exits_or_stations: list[str] = list(coordinates.keys())
        sorted_exits_or_stations.sort()

        if self.way_type == ways.RAILWAY:
            print(f'{len(sorted_exits_or_stations)} stations were found')
        else:
            print(f'{len(sorted_exits_or_stations)} exits were found')
        if len(sorted_exits_or_stations) == 0:
            print(f'No exits or stations were found - Cancelling processing of {self.way_display_name}')
            exit(1)

        if not os.path.exists(paths_and_files.TMP_FOLDER_PATH):
            os.makedirs(paths_and_files.TMP_FOLDER_PATH)

        with open(os.path.join(self._get_filepath(paths_and_files.TMP_CSV_LOCATION_PATH)), 'w', encoding=ENCODING) as f:
            for location_name in sorted_exits_or_stations:  # Ex: "2" for a freeway/motorway, or "Santa Apolónia" for a railway
                latitude: float = coordinates[location_name].get_latitude()
                longitude: float = coordinates[location_name].get_longitude()
                altitude: int = 0
                protected_area: str = ''
                batch: int = 0
                if self.get_altitude_info:
                    if self.way_type == ways.RAILWAY:
                        print(f'Getting altitude for {location_name} station...')
                    else:
                        print(f'Getting altitude for exit {location_name}...')
                    altitude: int = self.get_altitude(latitude, longitude)
                if self.way_type == ways.RAILWAY:
                    f.write(f'{location_name} Station,{latitude},{longitude},{altitude},{protected_area},{batch}\n')
                else:
                    f.write(f'{self.way_display_name} - Exit {location_name},{latitude},{longitude},{altitude},{protected_area},{batch}\n')
        sorter.ordenar_ficheiros_csv(ficheiro_a_ordenar=self._get_filepath(paths_and_files.TMP_CSV_LOCATION_PATH), cabecalho=False)
        print(f'Created locations file')

        processed_locations: int = 0

        # Get country-specific info
        if self.country == ways.SPAIN:
            municipios: set[str] = set()  # Spanish municipalities
            comarcas: set[str] = set()  # Spanish subdivision bigger than a municipality and smaller than a province

            desired_administrative_divisions: list[int] = [osm_interface.PROVINCE, osm_interface.COMARCA, osm_interface.SPANISH_MUNICIPALITY, osm_interface.SPANISH_DISTRICT]
            # Ex: {(37.1, -7.5): {6: 'Sevilla', 7: 'Comarca Metropolitana de Sevilla', 8: 'Sevilla', 9: 'Triana'}}
            administrative_divisions: dict[Coordinates, dict[Union[str, int], Optional[str]]] = self.get_administrative_divisions(list(coordinates.values()), desired_administrative_divisions)

            with open(self._get_filepath(paths_and_files.TMP_CSV_LOCATION_SPAIN_PATH), 'w', encoding=ENCODING) as f:
                for location_name in sorted_exits_or_stations:
                    location: Coordinates = coordinates[location_name]

                    municipio: str = administrative_divisions.get(location, {}).get(osm_interface.SPANISH_MUNICIPALITY, "")
                    province: str = administrative_divisions.get(location, {}).get(osm_interface.PROVINCE, "")
                    comarca: str = administrative_divisions.get(location, {}).get(osm_interface.COMARCA, '')  # Is not always available
                    district_es: str = administrative_divisions.get(location, {}).get(osm_interface.SPANISH_DISTRICT, '')  # Only available in the largest cities

                    if self.way_type == ways.RAILWAY:
                        if district_es:
                            f.write(f'{location_name} Station,{municipio},{province},{district_es}\n')
                        else:
                            f.write(f'{location_name} Station,{municipio},{province},\n')
                    else:
                        if district_es:
                            f.write(f'{self.way_display_name} - Exit {location_name},{municipio},{province},{district_es}\n')
                        else:
                            f.write(f'{self.way_display_name} - Exit {location_name},{municipio},{province},\n')

                    municipios.add(f'{municipio},{province}\n')
                    if comarca:
                        comarcas.add(f'{municipio},{comarca},{province}\n')

                    processed_locations += 1
                    if self.way_type == ways.RAILWAY:
                        print(f'{location_name} Station processed - {processed_locations}/{len(sorted_exits_or_stations)} processed stations')
                    else:
                        print(f'Exit {location_name} processed - {processed_locations}/{len(sorted_exits_or_stations)} processed exits')

            with open(self._get_filepath(paths_and_files.TMP_CSV_MUNICIPIO_PATH), 'w', encoding=ENCODING) as f:
                for municipio in municipios:
                    f.write(municipio)

            with open(self._get_filepath(paths_and_files.TMP_CSV_COMARCA_PATH), 'w', encoding=ENCODING) as f:
                for comarca in comarcas:
                    f.write(comarca)

            sorter.ordenar_ficheiros_csv(ficheiro_a_ordenar=self._get_filepath(paths_and_files.TMP_CSV_LOCATION_SPAIN_PATH), cabecalho=False)
            print("Finished Spanish locations file")
            sorter.ordenar_ficheiros_csv(ficheiro_a_ordenar=self._get_filepath(paths_and_files.TMP_CSV_MUNICIPIO_PATH), cabecalho=False)
            print("Finished Spanish municipalities file")
            sorter.ordenar_ficheiros_csv(ficheiro_a_ordenar=self._get_filepath(paths_and_files.TMP_CSV_COMARCA_PATH), cabecalho=False)
            print("Finished comarcas file")

        elif self.country == ways.PORTUGAL:
            concelhos: set[str] = set()  # Portuguese municipalities

            desired_administrative_divisions: list[Union[str, int]] = [osm_interface.PORTUGUESE_DISTRICT, osm_interface.PORTUGUESE_MUNICIPALITY, osm_interface.PORTUGUESE_PARISH, osm_interface.PORTUGUESE_HISTORIC_PARISH]
            # {(37.1, -7.5): {6: 'Alcoutim e Pereiro', 7: 'Alcoutim', 8: 'Faro', 'historic_parish': 'Pereiro'}}
            administrative_divisions:  dict[Coordinates, dict[Union[str, int], Optional[str]]] = self.get_administrative_divisions(list(coordinates.values()), desired_administrative_divisions)

            with open(self._get_filepath(paths_and_files.TMP_CSV_LOCATION_PORTUGAL_PATH), 'w', encoding=ENCODING) as f:
                for location_name in sorted_exits_or_stations:
                    location: Coordinates = coordinates[location_name]

                    parish: str = administrative_divisions.get(location, {}).get(osm_interface.PORTUGUESE_HISTORIC_PARISH, "")  # Historic parish, if it exists
                    if not parish:
                        parish = administrative_divisions.get(location, {}).get(osm_interface.PORTUGUESE_PARISH, "")  # Current parish
                    concelho: str = administrative_divisions.get(location, {}).get(osm_interface.PORTUGUESE_MUNICIPALITY, "")
                    district_pt: str = administrative_divisions.get(location, {}).get(osm_interface.PORTUGUESE_DISTRICT, "")

                    if self.way_type == ways.RAILWAY:
                        f.write(f'{location_name} Station,{parish},{concelho}\n')
                    else:
                        f.write(f'{self.way_display_name} - Exit {location_name},{parish},{concelho}\n')

                    concelhos.add(f'{concelho},,{district_pt},\n')  # The intermunicipal entity and the historic region must be manually inserted

                    processed_locations += 1
                    if self.way_type == ways.RAILWAY:
                        print(f'{location_name} Station processed - {processed_locations}/{len(sorted_exits_or_stations)} processed stations')
                    else:
                        print(f'Exit {location_name} processed - {processed_locations}/{len(sorted_exits_or_stations)} processed exits')

            with open(self._get_filepath(paths_and_files.TMP_CSV_CONCELHO_PATH), 'w', encoding=ENCODING) as f:
                for concelho in concelhos:
                    f.write(concelho)

            sorter.ordenar_ficheiros_csv(ficheiro_a_ordenar=self._get_filepath(paths_and_files.TMP_CSV_LOCATION_PORTUGAL_PATH), cabecalho=False)
            print("Finished Portuguese locations file")
            sorter.ordenar_ficheiros_csv(ficheiro_a_ordenar=self._get_filepath(paths_and_files.TMP_CSV_CONCELHO_PATH), cabecalho=False)
            print("Finished Portuguese municipalities file")

        else:
            pass

    def create_connections_and_destinations_files(self, inverted: bool) -> None:
        with open(self._get_filepath(paths_and_files.TMP_CSV_LOCATION_PATH), 'r', encoding=ENCODING) as f:
            content: list[str] = f.readlines()

        if len(content) == 0:
            print(f'Locations file for {self.way_display_name} is empty.')
            print("Exiting.")
            exit(1)
        elif len(content) == 1:
            print(f'Locations file for {self.way_display_name} has only 1 location.')
            print("It is not possible to create connections and destinations.")
            print("Exiting.")
            exit(1)

        if inverted:
            content = list(reversed(content))

        # Generates map in order to later get the connection distances from it
        locations: list[Coordinates] = []
        for idx, location in enumerate(content):
            if idx <= len(content) - 2:  # Not the last location in the file
                line_a: str = content[idx]
                line_b: str = content[idx + 1]
                elements_a: list[str] = line_a.split(",")
                elements_b: list[str] = line_b.split(",")
                elements_a = sorter.separar_por_virgulas(lista=elements_a)  # '"Álamo', 'Alcoutim"' -> '"Álamo, Alcoutim"'
                elements_b = sorter.separar_por_virgulas(lista=elements_b)

                if content[idx + 1].strip() == '':  # Empty line - Stop processing here
                    break

                latitude_a, longitude_a = float(elements_a[1]), float(elements_a[2])
                latitude_b, longitude_b = float(elements_b[1]), float(elements_b[2])
                if not Coordinates(latitude_a, longitude_a) in locations:
                    locations.append(Coordinates(latitude_a, longitude_a))
                if not Coordinates(latitude_b, longitude_b) in locations:
                    locations.append(Coordinates(latitude_b, longitude_b))

        dist_calc: distance_calculator.DistanceCalculator = distance_calculator.DistanceCalculator()
        dist_calc.generate_processed_map(locations, self.way_type, self.country, way_name=self.way_osm_name)

        source: str = sorter.separar_por_virgulas(lista=content[0].split(','))[0]
        destination: str = sorter.separar_por_virgulas(lista=content[-1].split(','))[0]
        print("\nInsert the already known destinations split by commas, then press ENTER")
        print("Or press ENTER without destinations to generate a file without pre-populated destinations")
        destinations_towards_source: list[str] = input(f"Insert the destinations from {destination} towards {source}: ").split(",")
        destinations_towards_destination: list[str] = input(f"Insert the destinations from {source} towards {destination}: ").split(",")

        connections: list[str] = []
        destinations: list[str] = []
        for idx, location in enumerate(content):
            if idx <= len(content) - 2:  # Not the last location in the file
                line_a: str = content[idx]
                line_b: str = content[idx + 1]
                elements_a: list[str] = line_a.split(",")
                elements_b: list[str] = line_b.split(",")
                elements_a = sorter.separar_por_virgulas(lista=elements_a)  # '"Álamo', 'Alcoutim"' -> '"Álamo, Alcoutim"'
                elements_b = sorter.separar_por_virgulas(lista=elements_b)

                location_a: str = elements_a[0]
                location_b: str = elements_b[0].strip()

                if location_b == '':  # Empty line - Stop processing here
                    print("Empty line found - Processing will be partial only")
                    break

                if self.way_type == ways.RAILWAY:
                    means_transport: str = 'Train'
                else:
                    means_transport: str = 'Car'

                way_name: str = self.way_display_name
                latitude_a, longitude_a = float(elements_a[1]), float(elements_a[2])
                latitude_b, longitude_b = float(elements_b[1]), float(elements_b[2])
                cardinal_point: str = haversine.get_cardinal_point(source=Coordinates(latitude_a, longitude_a), destination=Coordinates(latitude_b, longitude_b))
                order_a = 2
                order_b = 1

                distance: float = dist_calc.calculate_distance_with_adjusts(Coordinates(latitude_a, longitude_a), Coordinates(latitude_b, longitude_b))
                if distance == distance_calculator.INFINITE_DISTANCE:
                    print("Unable to calculate distance - Continuing...")
                    distance = 0.0

                connection: str = f'{location_a},{location_b},{means_transport},{distance},{way_name},{cardinal_point},{order_a},{order_b}\n'
                connections.append(connection)

                if destinations_towards_source:
                    for destination in destinations_towards_source:
                        destination_string: str = f'{location_a},{location_b},{means_transport},False,{destination}\n'
                        destinations.append(destination_string)
                destination_string: str = f'{location_a},{location_b},{means_transport},False,\n'  # Empty line to make it easier to add more destinations
                destinations.append(destination_string)

                if destinations_towards_destination:
                    for destination in destinations_towards_destination:
                        destination_string: str = f'{location_a},{location_b},{means_transport},True,{destination}\n'
                        destinations.append(destination_string)
                destination_string: str = f'{location_a},{location_b},{means_transport},True,\n'  # Empty line to make it easier to add more destinations
                destinations.append(destination_string)

                print(f'{idx + 1}/{len(content) - 1} processed connections')  # Counts every line, including empty lines in the middle of the file

        with open(self._get_filepath(paths_and_files.TMP_CSV_CONNECTION_PATH), 'w', encoding=ENCODING) as f:
            f.writelines(connections)
        with open(self._get_filepath(paths_and_files.TMP_CSV_DESTINATION_PATH), 'w', encoding=ENCODING) as f:
            f.writelines(destinations)

    def get_altitude(self, latitude: float, longitude: float) -> int:
        if not self.google_api_key:  # File containing the key is missing?
            return 0  # Return default

        try:
            url: str = f'https://maps.googleapis.com/maps/api/elevation/json?locations={latitude},{longitude}&key={self.google_api_key}'
            return int(requests.get(url=url).json()['results'][0]['elevation'])
        except Exception as e:
            print(str(e))
            return 0

    def get_administrative_divisions(self, locations: list[Coordinates], desired_administrative_divisions: list[Union[str, int]]) -> dict[Coordinates, dict[Union[str, int], Optional[str]]]:
        """
        Returns a dictionary with the desired administrative divisions for each provided location
        """
        print("Getting administrative divisions...")

        administrative_divisions_by_location: dict[Coordinates, dict[Union[str, int], Optional[str]]] = {}
        for location in locations:
            administrative_divisions: dict[Union[str, int], Optional[str]] = {}

            return_value: dict[Union[str, int], str] = osm_interface.OsmInterface.get_administrative_divisions_by_coordinates(location)

            for key in return_value:
                if key not in desired_administrative_divisions:
                    continue

                administrative_division: Union[str, int] = return_value[key]
                administrative_divisions[key] = administrative_division

            for key in desired_administrative_divisions:
                if key not in administrative_divisions:  # Administrative division was not found for that location
                    administrative_divisions[key] = None

            administrative_divisions_by_location[location] = administrative_divisions

        print("Got administrative divisions\n")
        return administrative_divisions_by_location

    def get_exits_or_stations_coordinates(self) -> dict[str, Coordinates]:
        """
        Returns the coordinates for either the exits of the provided freeway / motorway or the stations of the provided railway
        No parameters are expected - Instead, class instance is set with the desired way to be processed, either a road or a railway
        """
        if self.way_type == ways.RAILWAY:
            print("Getting nodes for railway stations...")
        else:
            print("Getting nodes for freeway/motorway exits...")

        if self.way_type == ways.RAILWAY:
            all_coordinates: dict[str, list[Coordinates]] = osm_interface.OsmInterface.get_railway_stations(self.way_osm_name, self.country)
        else:
            all_coordinates: dict[str, list[Coordinates]] = osm_interface.OsmInterface.get_road_exits(self.way_osm_name, self.country)

        if len(all_coordinates) == 0:
            if self.way_type == ways.RAILWAY:
                print(f'No node was found for the stations of {self.way_display_name}. Is the railway in {self.country}?')
                print('It is also possible that this railway has no associated stations in OpenStreetMap')
            else:
                print(f'No node was found for the exits of {self.way_display_name}. Is the road in {self.country}?')
                print('It is also possible that this road has no associated exits in OpenStreetMap')
            exit(0)

        centre_coordinates: dict[str, Coordinates] = {}  # Contain only the "center" of each station or exit
        for exit_or_station in all_coordinates:
            latitude: float = 0.0
            longitude: float = 0.0
            for coordinates in all_coordinates[exit_or_station]:
                latitude += coordinates.get_latitude()
                longitude += coordinates.get_longitude()
            latitude = round(latitude / len(all_coordinates[exit_or_station]), COORDINATES_DECIMAL_PLACES)
            longitude = round(longitude / len(all_coordinates[exit_or_station]), COORDINATES_DECIMAL_PLACES)
            centre_coordinates[exit_or_station] = Coordinates(latitude, longitude)

        if self.way_type == ways.RAILWAY:
            print("Got coordinates for all railway stations\n")
        else:
            print("Got coordinates for all road exits\n")

        return centre_coordinates

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
        Returns Google API key - It is used to get altitude info
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
