from typing import Optional

import os
import subprocess

import psycopg2
from psycopg2 import OperationalError, sql

from travel.main import location_portugal, location_spain, location_gibraltar
from travel.main.cardinal_points import get_opposite_cardinal_point
from travel.main import paths_and_files


class DBInterface:
    """
    Interface to the creation and population of the PostgreSQL database in use by this program
    """

    database_name: str = 'travel'
    username: str = 'postgres'
    password: str = 'postgres'
    host: str = 'localhost'
    sql_port: int = 5432

    def __init__(self):
        self.connection: Optional[psycopg2.connection] = None
        self.cursor: Optional[psycopg2.cursor] = None

    def create_and_populate_travel_db(self) -> bool:
        """
        Main routine - Should be called in order to create the DB, if it does not exist, and then populate it
        Returns True on success, False on failure
        """
        try:
            if not DBInterface.is_db_created(DBInterface.database_name):
                success = DBInterface.create_database(DBInterface.database_name)
                if not success:
                    print(f"Failed to create the {DBInterface.database_name} database")
                    return False
        except Exception as e:
            print(f"Exception while checking if {DBInterface.database_name} exists")
            print(''.join(e.args))
            return False

        try:
            self.connection = psycopg2.connect(
                database=DBInterface.database_name,
                user=DBInterface.username,
                password=DBInterface.password,
                host=DBInterface.host,
                port=DBInterface.sql_port
            )
            self.connection.autocommit = True
            self.cursor: psycopg2.cursor = self.connection.cursor()

            # Creates and populates the DB
            sql_script_path: str = paths_and_files.DB_SCRIPT_PATH
            with open(sql_script_path, mode='r') as file:
                queries: list[str] = file.read().split(';\n')
            for query in queries:
                query = DBInterface.convert_sqlite_to_postgresql(query)
                self.cursor.execute(query + ';')
            self.preencher_base_dados()
        except OperationalError as e:
            print(f"Ocorreu o erro '{e}'")

    @staticmethod
    def is_db_created(db_name: str) -> bool:
        """
        Returns True if database with provided name exists, False otherwise, raises exception if any problem occurs
        """
        if not db_name:
            raise Exception("No DB name provided")
        elif len(db_name.strip()) == 0:
            raise Exception("Empty DB name provided")

        # Note: Environmental variable set only for this Python process, not system-wide
        # Allows call to psql to not show prompt for password
        # TODO: Improve security - See https://www.postgresql.org/docs/current/libpq-pgpass.html
        env_variable: str = "PGPASSWORD"
        try:
            os.environ[env_variable] = DBInterface.password
        except Exception as e:
            print(f"Error while setting {env_variable} environmental variable")
            raise Exception(''.join(e.args))

        psql_command: list[str] = ['\\l', f'{db_name}']
        command: list[str] = ['psql', '-U', f'{DBInterface.username}', '-c']
        command.extend(psql_command)

        try:
            # Note: Will print error message if DB is not found - Nothing to worry about
            p: subprocess.Popen = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            p.stdin.close()
            p.wait()
        except Exception as e:
            print(f"Error while running psql command to check if {db_name} database exists")
            raise Exception(''.join(e.args))

        if p.stderr:
            stderr = p.stderr.read()
            p.stderr.close()
            raise Exception(f'{stderr}')
        elif not p.stdout:
            raise Exception(f"No output obtained from psql command to check if {db_name} database exists")

        success_indicator = db_name  # If command result includes DB name, DB exists
        output: str = f'{p.stdout.read()}'
        p.stdout.close()
        return success_indicator in output

    @staticmethod
    def create_database(db_name: str):
        """
        Given a string, creates a database with the provided name. Returns True on success, False otherwise
        Database creation will fail if it already exists, so checking beforehand is required
        """
        return DBInterface._create_or_delete_database(db_name, create=True)

    @staticmethod
    def delete_database(db_name: str):
        """
        Given a string, deletes the database with the provided name. Returns True on success, False otherwise
        Database deletion will fail if it does not exist, so checking beforehand is required

        Deletion will fail if another session (for example, in pgAdmin) is opened in the DB
        """
        return DBInterface._create_or_delete_database(db_name, create=False)

    @staticmethod
    def _create_or_delete_database(db_name: str, create: bool = True) -> bool:
        """
        Returns True on success, False otherwise
        """
        try:
            # Connects to PostgreSQL - No database name needs to be provided at this point
            connection: psycopg2.connection = psycopg2.connect(
                user=DBInterface.username,
                password=DBInterface.password,
                host=DBInterface.host,
                port=DBInterface.sql_port
            )
            connection.autocommit = True
            cursor: psycopg2.cursor = connection.cursor()

            # Creates or deletes the database
            if create:
                db_query: str = sql.SQL("CREATE DATABASE {};").format(sql.Identifier(db_name))
            else:  # Delete
                db_query: str = sql.SQL("DROP DATABASE {};").format(sql.Identifier(db_name))
            cursor.execute(db_query)
            connection.close()

            return True

        except Exception as e:
            if create:
                print(f"Exception while creating the database {db_name}")
            else:
                print(f"Exception while deleting the database {db_name}")
            print(''.join(e.args))

            return False

    @staticmethod
    def convert_sqlite_to_postgresql(query: str) -> str:
        """
        Converts a query in the database.sql from SQLite to PostgreSQL
        File database.sql is written in SQLite as scheme is dictated by Android and therefore more restrictive
        Example conversions: PostgreSQL support boolean values, while in SQLite integers must be used

        Most of the file can be used for both SQL dialects
        """
        # Add CASCADE to queries dropping tables for PostgreSQL
        if query.startswith("DROP"):  # Ex: DROP TABLE IF EXISTS Location; -> DROP TABLE IF EXISTS Location CASCADE;
            query = f'{query} CASCADE'

        # While in SQLite the REAL datatype uses 8 bytes, in PostgreSQL it uses 4 bytes and is limited to a precision of 6 digits
        if 'REAL' in query:
            query = query.replace('REAL', 'NUMERIC')

        # Defines boolean table columns in PostgreSQL - In SQLite there is no boolean data type
        if 'starting_point' in query and 'Destination' in query:  # Ex: starting_point INTEGER NOT NULL, -> starting_point BOOLEAN NOT NULL,
            query_parts: list[str] = query.split(',')
            updated_query_parts: list[str] = []
            for query_part in query_parts:
                if "starting_point" in query_part:
                    query_part = query_part.replace('INTEGER', 'BOOLEAN')
                updated_query_parts.append(query_part)
            query = ','.join(updated_query_parts)

        return query

    #  Retorna um local com todas as suas informações
    def obter_local(self, nome):
        #  Determinar o país
        query = "SELECT COUNT(name) FROM LocationPortugal WHERE name = '" + nome + "';"
        self.cursor.execute(query)
        resultado = self.cursor.fetchall()[0][0]
        if resultado == 1:  # Local de Portugal
            pais = 'Portugal'
        else:
            query = "SELECT COUNT(name) FROM LocationSpain WHERE name = '" + nome + "';"
            self.cursor.execute(query)
            resultado = self.cursor.fetchall()[0][0]
            if resultado == 1:  # Local de Espanha
                pais = 'Espanha'
            else:
                query = "SELECT COUNT(name) FROM LocationGibraltar WHERE name = '" + nome + "';"
                self.cursor.execute(query)
                resultado = self.cursor.fetchall()[0][0]
                if resultado == 1:  # Local de Gibraltar
                    pais = 'Gibraltar'
                else:
                    return None  # Local inválido

        #  Determinar os locais circundantes
        query = "SELECT * FROM Connection WHERE location_a = '" + nome + "' OR location_b = '" + nome + "';"
        self.cursor.execute(query)
        resultado = self.cursor.fetchall()
        locais_circundantes = {}
        ordem = []
        sentidos_info_extra = {}
        for linha in resultado:
            if linha[0].strip() == nome:  # Local A
                ordem.append(linha[6])  # Ordem A
                local_circundante = linha[1].strip()
                ponto_cardeal = linha[5].strip()
            else:  # Local B
                ordem.append(linha[7])  # Ordem B
                local_circundante = linha[0].strip()
                ponto_cardeal = get_opposite_cardinal_point(linha[5].strip())
            distancia = float(linha[3])
            meio_transporte = linha[2].strip()
            if linha[4] is not None:
                sentidos_info_extra[(local_circundante, meio_transporte)] = linha[4].strip()
            locais_circundantes[(local_circundante, meio_transporte)] = [ponto_cardeal, distancia, meio_transporte]
        locais_circundantes = DBInterface.ordenar_dicionario(locais_circundantes, ordem)

        #  Determinar os destinos por sentido
        query = "SELECT * FROM Destination WHERE " \
                "(location_a = '" + nome + "' AND starting_point = 'true') OR (location_b = '" + nome + "' AND starting_point = 'false');"
        self.cursor.execute(query)
        resultado = self.cursor.fetchall()
        sentidos = {}
        for local_circundante in locais_circundantes:
            nome_local = local_circundante[0]
            meio_transporte = local_circundante[1]
            destinos = []
            for linha in resultado:
                if (nome_local in [linha[0], linha[1]]) & (meio_transporte == linha[2]):
                    destinos.append(linha[4].strip())
            if len(destinos) > 0:
                sentidos[(nome_local, meio_transporte)] = destinos

        #  Determinar os restantes parâmetros gerais
        query = "SELECT * FROM Location WHERE name = '" + nome + "';"
        self.cursor.execute(query)
        resultado = self.cursor.fetchall()
        latitude = float(resultado[0][1])
        longitude = float(resultado[0][2])
        altitude = int(resultado[0][3])
        info_extra = ''
        if resultado[0][4] is not None:
            info_extra = resultado[0][4].strip()
        lote = int(resultado[0][5])

        #  Determinar os parâmetros específicos do país
        if pais == 'Portugal':
            query = "SELECT LocationPortugal.name, parish, Concelho.concelho, intermunicipal_entity, district, region " \
                    "FROM LocationPortugal, Concelho " \
                    "WHERE LocationPortugal.concelho = Concelho.concelho AND LocationPortugal.name = '" + nome + "';"
            self.cursor.execute(query)
            resultado = self.cursor.fetchall()
            freguesia = resultado[0][1].strip()
            concelho = resultado[0][2].strip()
            distrito = resultado[0][4].strip()
            entidade_intermunicipal = resultado[0][3].strip()
            regiao = resultado[0][5].strip()
        elif pais == 'Espanha':
            query = "SELECT name, municipio, district, Province.province, autonomous_community " \
                    "FROM LocationSpain, Province " \
                    "WHERE LocationSpain.province = Province.province AND LocationSpain.name = '" + nome + "';"
            self.cursor.execute(query)
            resultado = self.cursor.fetchall()
            distrito = ''
            if resultado[0][2] is not None:
                distrito = resultado[0][2].strip()
            municipio = resultado[0][1].strip()
            provincia = resultado[0][3].strip()
            comunidade_autonoma = resultado[0][4].strip()
            query = "SELECT * FROM Comarca WHERE municipio = '" + municipio + "' AND province = '" + provincia + "';"
            self.cursor.execute(query)
            resultado = self.cursor.fetchall()
            comarcas = []
            for linha in resultado:
                comarcas.append(linha[1].strip())
        elif pais == 'Gibraltar':
            query = "SELECT name, major_residential_area FROM LocationGibraltar WHERE name = '" + nome + "';"
            self.cursor.execute(query)
            resultado = self.cursor.fetchall()
            major_residential_areas = []
            for linha in resultado:
                major_residential_areas.append(linha[1].strip())
        else:
            return None

        #  Criar o local
        if pais == 'Portugal':
            local = location_portugal.LocationPortugal(nome, locais_circundantes, latitude, longitude, altitude, freguesia,
                                                       concelho, distrito, entidade_intermunicipal, regiao)
        elif pais == 'Espanha':
            local = location_spain.LocationSpain(nome, locais_circundantes, latitude, longitude, altitude, municipio,
                                                 comarcas, provincia, comunidade_autonoma)
            local.set_district(distrito)
        elif pais == 'Gibraltar':
            local = location_gibraltar.LocationGibraltar(nome, locais_circundantes, latitude, longitude, altitude,
                                                         major_residential_areas)
        else:
            return None
        local.set_destinations(sentidos)
        local.set_ways(sentidos_info_extra)
        local.set_protected_area(info_extra)
        local.set_batch(lote)

        return local

    #  Preenche a base de dados
    def preencher_base_dados(self):
        path_csv = paths_and_files.CSV_LOCATION_PATH
        query = "COPY Location(name, latitude, longitude, altitude, protected_area, batch) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = paths_and_files.CSV_CONCELHO_PATH
        query = "COPY Concelho(concelho, intermunicipal_entity, district, region) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = paths_and_files.CSV_PROVINCE_PATH
        query = "COPY Province(province, autonomous_community) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = paths_and_files.CSV_MUNICIPIO_PATH
        query = "COPY Municipio(municipio, province) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = paths_and_files.CSV_LOCATION_PORTUGAL_PATH
        query = "COPY LocationPortugal(name, parish, concelho) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = paths_and_files.CSV_LOCATION_SPAIN_PATH
        query = "COPY LocationSpain(name, municipio, province, district) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = paths_and_files.CSV_LOCATION_GIBRALTAR_PATH
        query = "COPY LocationGibraltar(name, major_residential_area) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = paths_and_files.CSV_COMARCA_PATH
        query = "COPY Comarca(municipio, comarca, province) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = paths_and_files.CSV_CONNECTION_PATH
        query = "COPY Connection(location_a, location_b, means_transport, distance, way, cardinal_point, order_a, order_b)" \
                " FROM '" + path_csv + "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = paths_and_files.CSV_DESTINATION_PATH
        query = "COPY Destination(location_a, location_b, means_transport, starting_point, destination) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

    #  Retorna o número de locais da base de dados
    def obter_numero_locais(self):
        query = "SELECT COUNT(name) FROM Location;"
        self.cursor.execute(query)
        return self.cursor.fetchall()[0][0]

    #  Ordena os elementos de um dicionário de acordo com uma ordem fornecida
    @staticmethod
    def ordenar_dicionario(dicionario, ordem):
        novo_dic = {}
        for i in range(len(dicionario)):
            for j in range(len(dicionario)):
                if ordem[j] == len(novo_dic) + 1:
                    chave = list(dicionario)[j]
                    novo_dic[chave] = dicionario[chave]
        return novo_dic
