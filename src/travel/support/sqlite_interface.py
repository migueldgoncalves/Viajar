import sqlite3
import os

from travel.main import paths_and_files
from travel.support.sorter import split_by_commas, csv_to_list

"""
This module allows to create a SQLite DB from the .csv files of this project
It allows to quickly update the DB of the associated Android project
"""


class SQLiteDBInterface:

    def __init__(self, return_instead_of_exit=False):
        self.cursor = None

        print("Starting creation and population of the SQLite DB...")

        try:
            self.delete_existing_db()
            with sqlite3.connect(paths_and_files.ANDROID_DB_FILE_PATH) as conn:
                self.cursor = conn.cursor()
                self.create_db()
                self.populate_db()
        except Exception as e:
            print(e)
            print("An error occurred while creating and populating the DB. Exiting...")
            if return_instead_of_exit:
                return
            else:
                exit(1)

        print("DB successfully created and populated")
        if return_instead_of_exit:
            return
        else:
            exit(0)

    def delete_existing_db(self):
        try:
            os.remove(paths_and_files.ANDROID_DB_FILE_PATH)
            print("Existing DB was successfully deleted")
        except FileNotFoundError:
            print("No DB exists yet - Nothing to delete")

    def create_db(self):
        print("Creating DB...")
        with open(paths_and_files.DB_SCRIPT_PATH, mode='r') as file:
            queries = file.read().split(';\n')
        for query in queries:
            self.cursor.execute(query)
        print("DB successfully created")

    def populate_db(self):
        def populate_table(path_csv: str, query_sql: str):
            print(f"Populating table from file {path_csv}...")

            content: list[str] = csv_to_list(path_csv)
            for i, line in enumerate(content):
                if i == 0:  # Header - Not needed here
                    continue

                line = split_by_commas([line])  # "Álamo, Alcoutim",37.386987 -> ["Álamo, Alcoutim", 37.386987]
                for j, field in enumerate(line):
                    if line[j] == 'False':  # .csv files include boolean fields, which must be converted as SQLite does not support booleans
                        line[j] = '0'
                    elif line[j] == 'True':
                        line[j] = '1'
                    if type(line[j]) is str and '"' in line[j]:  # Remove quote chars - Not needed when populating the DB
                        line[j] = line[j].replace("\"", "")  # "Álamo, Alcoutim" -> Álamo, Alcoutim
                self.cursor.execute(query_sql, line)

        print("Starting population of the DB...")

        populate_table(paths_and_files.CSV_LOCATION_PATH, "INSERT INTO Location(name, latitude, longitude, altitude, protected_area, island, batch) VALUES(?, ?, ?, ?, ?, ?, ?);")
        populate_table(paths_and_files.CSV_CONCELHO_PATH, "INSERT INTO Concelho(concelho, intermunicipal_entity, district, region) VALUES(?, ?, ?, ?);")
        populate_table(paths_and_files.CSV_PROVINCE_PATH, "INSERT INTO Province(province, autonomous_community) VALUES(?, ?);")
        populate_table(paths_and_files.CSV_MUNICIPIO_PATH, "INSERT INTO Municipio(municipio, comarca, province) VALUES(?, ?, ?);")
        populate_table(paths_and_files.CSV_LOCATION_PORTUGAL_PATH, "INSERT INTO LocationPortugal(name, parish, concelho) VALUES(?, ?, ?);")
        populate_table(paths_and_files.CSV_LOCATION_SPAIN_PATH, "INSERT INTO LocationSpain(name, municipio, province, district) VALUES(?, ?, ?, ?);")
        populate_table(paths_and_files.CSV_LOCATION_GIBRALTAR_PATH, "INSERT INTO LocationGibraltar(name) VALUES(?);")
        populate_table(paths_and_files.CSV_CONNECTION_PATH, "INSERT INTO Connection(location_a, location_b, means_transport, distance, way, cardinal_point, order_a, order_b) VALUES(?, ?, ?, ?, ?, ?, ?, ?);")
        populate_table(paths_and_files.CSV_DESTINATION_PATH, "INSERT INTO Destination(location_a, location_b, means_transport, starting_point, destination) VALUES(?, ?, ?, ?, ?)")

        print("DB successfully populated")
