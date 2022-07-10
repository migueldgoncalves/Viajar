import sqlite3
import os
import csv

"""
Este módulo permite criar uma base de dados SQLite a partir dos ficheiros .csv deste projecto
Permite actualizar a base de dados do projecto Android de uma forma rápida
"""

DELIMITER = ','
QUOTECHAR = '"'
QUOTING = csv.QUOTE_NONE
ENCODING = 'utf-8'
ESCAPECHAR = ''

# ALTERAR AQUI PATHS
# Devem estar fora da drive C: - Pode haver problemas de permissões
PASTA_DESTINO = 'D:\\AndroidStudioProjects\\Viajar\\app\\src\\main\\assets'  # A pasta do projecto Android onde colocar a BD
PASTA_CSV = 'D:\\PycharmProjects\\Viajar\\src\\travel\\database'  # A pasta do projecto Python onde estão os ficheiros .csv
FICHEIRO_BD = 'Travel'  # Sem extensão - Nome do ficheiro de BD a ser criado

PATH_BD = os.path.join(PASTA_DESTINO, FICHEIRO_BD)

SCRIPT_SQLITE = 'database_sqlite.sql'
PATH_SCRIPT = os.path.join(PASTA_CSV, SCRIPT_SQLITE)


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
            with open(PATH_SCRIPT, mode='r') as file:
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
        def preencher_tabela(ficheiro, query_sql):
            print(f"A criar tabela a partir do ficheiro {ficheiro}...")

            path_csv = os.path.join(PASTA_CSV, ficheiro)
            with open(path_csv, mode='r', encoding=ENCODING) as ficheiro:
                conteudo = csv.reader(ficheiro, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=QUOTING, escapechar=ESCAPECHAR)
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

        preencher_tabela('location.csv', "INSERT INTO Location(name, latitude, longitude, altitude, extra_info, batch) VALUES(?, ?, ?, ?, ?, ?);")
        preencher_tabela('concelho.csv', "INSERT INTO Concelho(concelho, intermunicipal_entity, district, region) VALUES(?, ?, ?, ?);")
        preencher_tabela('province.csv', "INSERT INTO Province(province, autonomous_community) VALUES(?, ?);")
        preencher_tabela('municipio.csv', "INSERT INTO Municipio(municipio, province) VALUES(?, ?);")
        preencher_tabela('location_portugal.csv', "INSERT INTO LocationPortugal(name, parish, concelho) VALUES(?, ?, ?);")
        preencher_tabela('location_spain.csv', "INSERT INTO LocationSpain(name, municipio, province, district) VALUES(?, ?, ?, ?);")
        preencher_tabela('location_gibraltar.csv', "INSERT INTO LocationGibraltar(name, major_residential_area) VALUES(?, ?);")
        preencher_tabela('comarca.csv', "INSERT INTO Comarca(municipio, comarca, province) VALUES(?, ?, ?);")
        preencher_tabela('connection.csv', "INSERT INTO Connection(location_a, location_b, means_transport, distance, extra_info, cardinal_point, order_a, order_b) VALUES(?, ?, ?, ?, ?, ?, ?, ?);")
        preencher_tabela('destination.csv', "INSERT INTO Destination(location_a, location_b, means_transport, starting_point, destination) VALUES(?, ?, ?, ?, ?)")

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
