import sqlite3
import os
import csv

from travel.main import paths_and_files

"""
Este módulo permite criar uma base de dados SQLite a partir dos ficheiros .csv deste projecto
Permite actualizar a base de dados do projecto Android de uma forma rápida
"""

DELIMITER = ','
QUOTECHAR = '"'
QUOTING = csv.QUOTE_NONE
ENCODING = 'utf-8'

PATH_BD = paths_and_files.ANDROID_DB_FILE_PATH
PATH_SQL_SCRIPT = paths_and_files.DB_SCRIPT_PATH


class SQLiteBDInterface:

    def __init__(self):
        self.cursor = None

        print("A iniciar criação e preenchimento da base de dados SQLite...")

        try:
            self.apagar_bd_existente()
            with sqlite3.connect(PATH_BD) as conn:
                self.cursor = conn.cursor()
                self.criar_base_dados()
                self.preencher_base_dados()
        except Exception as e:
            print(e)
            print("Ocorreu um erro ao criar e preencher a base de dados. A sair...")
            exit(1)

        print("Base de dados criada e preenchida com sucesso")
        input("Prima qualquer tecla para sair")
        exit(0)

    def apagar_bd_existente(self):
        try:
            os.remove(PATH_BD)
            print("Base de dados existente removida")
        except FileNotFoundError:
            print("Não existe ainda uma base de dados")

    def criar_base_dados(self):
        try:
            print("A criar base de dados...")
            with open(PATH_SQL_SCRIPT, mode='r') as file:
                queries = file.read().split(';\n')
            for query in queries:
                self.cursor.execute(query)
            print("Base de dados criada")

        except Exception as e:
            print(e)
            print("Ocorreu um erro ao criar a base de dados. A sair...")
            exit(1)

    #  Preenche a base de dados
    def preencher_base_dados(self):
        def preencher_tabela(path_csv, query_sql):
            print(f"A criar tabela a partir do ficheiro {path_csv}...")

            with open(path_csv, mode='r', encoding=ENCODING) as ficheiro:
                conteudo = csv.reader(ficheiro, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=QUOTING)
                for i, linha in enumerate(conteudo):
                    if i == 0:  # Cabeçalho
                        continue

                    linha = self._separar_por_virgulas(linha)  # "Álamo, Alcoutim",37.386987 -> ["Álamo, Alcoutim", 37.386987]
                    for j, elemento in enumerate(linha):
                        if linha[j] == 'False':
                            linha[j] = 0
                        elif linha[j] == 'True':
                            linha[j] = 1
                        if type(linha[j]) == str and '"' in linha[j]:
                            linha[j] = linha[j].replace("\"", "")  # "Álamo, Alcoutim" -> Álamo, Alcoutim
                    self.cursor.execute(query_sql, linha)

        print("A iniciar preenchimento da base de dados...")

        preencher_tabela(paths_and_files.CSV_LOCATION_PATH, "INSERT INTO Location(name, latitude, longitude, altitude, protected_area, batch) VALUES(?, ?, ?, ?, ?, ?);")
        preencher_tabela(paths_and_files.CSV_CONCELHO_PATH, "INSERT INTO Concelho(concelho, intermunicipal_entity, district, region) VALUES(?, ?, ?, ?);")
        preencher_tabela(paths_and_files.CSV_PROVINCE_PATH, "INSERT INTO Province(province, autonomous_community) VALUES(?, ?);")
        preencher_tabela(paths_and_files.CSV_MUNICIPIO_PATH, "INSERT INTO Municipio(municipio, province) VALUES(?, ?);")
        preencher_tabela(paths_and_files.CSV_LOCATION_PORTUGAL_PATH, "INSERT INTO LocationPortugal(name, parish, concelho) VALUES(?, ?, ?);")
        preencher_tabela(paths_and_files.CSV_LOCATION_SPAIN_PATH, "INSERT INTO LocationSpain(name, municipio, province, district) VALUES(?, ?, ?, ?);")
        preencher_tabela(paths_and_files.CSV_LOCATION_GIBRALTAR_PATH, "INSERT INTO LocationGibraltar(name, major_residential_area) VALUES(?, ?);")
        preencher_tabela(paths_and_files.CSV_COMARCA_PATH, "INSERT INTO Comarca(municipio, comarca, province) VALUES(?, ?, ?);")
        preencher_tabela(paths_and_files.CSV_CONNECTION_PATH, "INSERT INTO Connection(location_a, location_b, means_transport, distance, way, cardinal_point, order_a, order_b) VALUES(?, ?, ?, ?, ?, ?, ?, ?);")
        preencher_tabela(paths_and_files.CSV_DESTINATION_PATH, "INSERT INTO Destination(location_a, location_b, means_transport, starting_point, destination) VALUES(?, ?, ?, ?, ?)")

        print("Base de dados preenchida")

    def _separar_por_virgulas(self, lista):
        lista_temp = []
        for palavra in lista:
            lista_temp.extend(palavra.split(','))

        lista_retornar = []
        continuar = False
        for i in range(len(lista_temp)):
            if continuar:
                continuar = False
                continue

            palavra = lista_temp[i]
            if QUOTECHAR in palavra and i < len(lista_temp) - 1:
                lista_retornar.append(palavra + "," + lista_temp[i + 1])  # '"Álamo', 'Alcoutim"' -> '"Álamo, Alcoutim"'
                continuar = True
            else:
                lista_retornar.append(palavra.strip())

        return lista_retornar
