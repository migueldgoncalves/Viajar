import pathlib
import psycopg2
from psycopg2 import OperationalError
import os

from travel.main import location_portugal, location_spain, location_gibraltar
from travel.main.cardinal_points import get_opposite_cardinal_point


class DBInterface:
    # DB folder path
    folder_name: str = 'database'
    folder_path: str = os.path.join(str(pathlib.Path(__file__).parent.absolute()), '', f'../{folder_name}')
    database_file: str = 'database.sql'

    database_name: str = 'travel'
    username: str = 'postgres'
    password: str = 'postgres'
    host: str = 'localhost'
    sql_port: int = 5432

    def __init__(self):
        try:
            self.connection: psycopg2.connection = psycopg2.connect(
                database=self.database_name,
                user=DBInterface.username,
                password=DBInterface.password,
                host=DBInterface.host,
                port=DBInterface.sql_port
            )
            self.connection.autocommit = True
            self.cursor: psycopg2.cursor = self.connection.cursor()

            # Creates and populates the DB
            sql_script_path: str = os.path.join(DBInterface.folder_path, DBInterface.database_file)
            with open(sql_script_path, mode='r') as file:
                queries: list[str] = file.read().split(';\n')
            for query in queries:
                query = DBInterface._convert_sqlite_to_postgresql(query)
                self.cursor.execute(query + ';')
            self.preencher_base_dados()
        except OperationalError as e:
            print(f"Ocorreu o erro '{e}'")

    @staticmethod
    def _convert_sqlite_to_postgresql(query: str) -> str:
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
        path_csv = os.path.join(self.folder_path, 'location.csv')
        query = "COPY Location(name, latitude, longitude, altitude, protected_area, batch) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = os.path.join(self.folder_path, 'concelho.csv')
        query = "COPY Concelho(concelho, intermunicipal_entity, district, region) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = os.path.join(self.folder_path, 'province.csv')
        query = "COPY Province(province, autonomous_community) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = os.path.join(self.folder_path, 'municipio.csv')
        query = "COPY Municipio(municipio, province) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = os.path.join(self.folder_path, 'location_portugal.csv')
        query = "COPY LocationPortugal(name, parish, concelho) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = os.path.join(self.folder_path, 'location_spain.csv')
        query = "COPY LocationSpain(name, municipio, province, district) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = os.path.join(self.folder_path, 'location_gibraltar.csv')
        query = "COPY LocationGibraltar(name, major_residential_area) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = os.path.join(self.folder_path, 'comarca.csv')
        query = "COPY Comarca(municipio, comarca, province) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = os.path.join(self.folder_path, 'connection.csv')
        query = "COPY Connection(location_a, location_b, means_transport, distance, way, cardinal_point, order_a, order_b)" \
                " FROM '" + path_csv + "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = os.path.join(self.folder_path, 'destination.csv')
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
