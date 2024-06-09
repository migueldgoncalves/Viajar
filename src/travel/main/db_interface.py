from typing import Optional

import os
import subprocess

import psycopg2
from psycopg2 import sql

from travel.main import location, location_portugal, location_spain, location_gibraltar, location_andorra, location_beyond_iberian_peninsula
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
        # Create the DB if it does not exist
        try:
            if not DBInterface.is_db_created(DBInterface.database_name):
                success: bool = DBInterface.create_database(DBInterface.database_name)
                if not success:
                    print(f"Failed to create the {DBInterface.database_name} database")
                    return False
        except Exception as e:
            print(f"Exception while checking if {DBInterface.database_name} database exists and creating it if needed")
            print(''.join(e.args))
            return False

        # Connect to the DB
        try:
            self.connection = psycopg2.connect(
                database=DBInterface.database_name,
                user=DBInterface.username,
                password=DBInterface.password,
                host=DBInterface.host,
                port=DBInterface.sql_port
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(f"Exception while creating the cursor to access the {DBInterface.database_name} database")
            print(''.join(e.args))
            return False

        # Create the tables of the DB
        success: bool = self.create_db_tables()
        if not success:
            print(f'Failed to create the tables of the {DBInterface.database_name} database')
            return False

        # Populate the DB
        success: bool = self.populate_travel_db()
        if not success:
            print(f'Failed to populate the {DBInterface.database_name} database')
            return False

        return True

    def create_db_tables(self) -> bool:
        """
        Returns True if tables were successfully created in the database with provided name, False otherwise
        """
        try:
            # Creates and populates the DB
            sql_script_path: str = paths_and_files.DB_SCRIPT_PATH
            with open(sql_script_path, mode='r') as file:
                queries: list[str] = file.read().split(';\n')
            for query in queries:
                query = DBInterface.convert_sqlite_to_postgresql(query)
                self.cursor.execute(query + ';')
            return True

        except Exception as e:
            print(f"Exception while creating the tables of the database {DBInterface.database_name}")
            print(''.join(e.args))
            return False

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

        success_indicator: str = db_name  # If command result includes DB name, DB exists
        output: str = f'{p.stdout.read()}'
        p.stdout.close()
        return success_indicator in output

    @staticmethod
    def create_database(db_name: str) -> bool:
        """
        Given a string, creates a database with the provided name. Returns True on success, False otherwise
        Database creation will fail if it already exists, so checking beforehand is required
        """
        return DBInterface._create_or_delete_database(db_name, create=True)

    @staticmethod
    def delete_database(db_name: str) -> bool:
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
                db_query: sql.SQL = sql.SQL("CREATE DATABASE {};").format(sql.Identifier(db_name))
            else:  # Delete
                db_query: sql.SQL = sql.SQL("DROP DATABASE {};").format(sql.Identifier(db_name))
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

    def get_location_object(self, name) -> Optional[location.Location]:
        """
        Given a location name, returns a country-specific location object with the respective information
        """
        try:
            country: str = self.get_location_country(name)
            if not country:
                print(f"Location {name} is not in any country table - Failed to determine country")
                return None

            # Determine the surrounding locations and connections info
            query: sql.SQL = sql.SQL("SELECT * FROM Connection WHERE location_a = {} OR location_b = {};").format(sql.Literal(name), sql.Literal(name))
            self.cursor.execute(query)
            result: list[tuple] = self.cursor.fetchall()
            surrounding_locations: dict[tuple[str, str], tuple[str, float, str]] = {}
            orders: list[int] = []
            ways: dict[tuple[str, str], str] = {}
            for line in result:
                if line[0].strip() == name:  # Location A
                    orders.append(line[6])  # Order A
                    surrounding_location: str = line[1].strip()
                    cardinal_point: str = line[5].strip()
                else:  # Location B
                    orders.append(line[7])  # Order B
                    surrounding_location: str = line[0].strip()
                    cardinal_point: str = get_opposite_cardinal_point(line[5].strip())
                distance: float = float(line[3])
                means_transport: str = line[2].strip()
                if line[4] is not None:
                    ways[(surrounding_location, means_transport)] = line[4].strip()
                surrounding_locations[(surrounding_location, means_transport)] = (cardinal_point, distance, means_transport)
            surrounding_locations = DBInterface.order_dictionary(surrounding_locations, orders)

            # Determine destinations per combination surrounding location/means of transport
            query = sql.SQL("SELECT * FROM Destination WHERE (location_a = {} AND starting_point = 'true') OR (location_b = {} AND starting_point = 'false');").format(sql.Literal(name), sql.Literal(name))
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            all_destinations: dict[tuple[str, str], list[str]] = {}
            for surrounding_location in surrounding_locations:
                surrounding_location_name: str = surrounding_location[0]
                means_transport: str = surrounding_location[1]
                destinations: list[str] = []
                for line in result:
                    if (surrounding_location_name in [line[0], line[1]]) & (means_transport == line[2]):
                        destinations.append(line[4].strip())
                if len(destinations) > 0:
                    all_destinations[(surrounding_location_name, means_transport)] = destinations

            # Determine the remainder of the general location parameters
            query = sql.SQL("SELECT * FROM Location WHERE name = {};").format(sql.Literal(name))
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            latitude: float = float(result[0][1])
            longitude: float = float(result[0][2])
            altitude: int = int(result[0][3])
            protected_area: str = ''
            island: str = ''
            if result[0][4] is not None:
                protected_area = result[0][4].strip()
            if result[0][5] is not None:
                island = result[0][5].strip()
            batch: int = int(result[0][6])

            # Determine the country-specific parameters, then create the location object
            if country == location_portugal.COUNTRY:
                query = sql.SQL("SELECT LocationPortugal.name, parish, Concelho.concelho, intermunicipal_entity, district, region "
                                "FROM LocationPortugal, Concelho "
                                "WHERE LocationPortugal.concelho = Concelho.concelho AND LocationPortugal.name = {};").format(sql.Literal(name))
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                parish: str = result[0][1].strip()
                concelho: str = result[0][2].strip()
                district: str = result[0][4].strip()
                intermunicipal_entity: str = result[0][3].strip()
                region: str = result[0][5].strip()
                location_object: location_portugal.LocationPortugal = location_portugal.LocationPortugal(
                    name, surrounding_locations, latitude, longitude, altitude, parish, concelho, district,
                    intermunicipal_entity, region)

            elif country == location_spain.COUNTRY:
                query = sql.SQL("SELECT name, municipio, district, Province.province, autonomous_community "
                                "FROM LocationSpain, Province "
                                "WHERE LocationSpain.province = Province.province AND LocationSpain.name = {};").format(sql.Literal(name))
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                district: str = ''
                if result[0][2] is not None:
                    district = result[0][2].strip()
                municipio: str = result[0][1].strip()
                province: str = result[0][3].strip()
                autonomous_community: str = result[0][4].strip()

                # Get comarca info
                query = sql.SQL("SELECT * FROM Municipio WHERE municipio = {} AND province = {};").format(sql.Literal(municipio), sql.Literal(province))
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                comarca: str = result[0][1].strip()

                location_object: location_spain.LocationSpain = location_spain.LocationSpain(
                    name, surrounding_locations, latitude, longitude, altitude, municipio, comarca, province, autonomous_community)
                location_object.set_district(district)

            elif country == location_gibraltar.COUNTRY:
                query = sql.SQL("SELECT name FROM LocationGibraltar WHERE name = {};").format(sql.Literal(name))
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                location_object: location_gibraltar.LocationGibraltar = location_gibraltar.LocationGibraltar(
                    name, surrounding_locations, latitude, longitude, altitude)

            elif country == location_andorra.COUNTRY:
                query = sql.SQL("SELECT * FROM LocationAndorra WHERE name = {};").format(sql.Literal(name))
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                parish: str = result[0][1].strip()
                location_object: location_andorra.LocationAndorra = location_andorra.LocationAndorra(
                    name, surrounding_locations, latitude, longitude, altitude, parish)

            else:  # Location beyond Iberian Peninsula
                query = sql.SQL("SELECT * FROM LocationBeyondIberianPeninsula WHERE name = {};").format(sql.Literal(name))
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                country: str = result[0][1].strip()
                osm_admin_level_3: str = result[0][2].strip() if result[0][2] else ''
                osm_admin_level_4: str = result[0][3].strip() if result[0][3] else ''
                osm_admin_level_5: str = result[0][4].strip() if result[0][4] else ''
                osm_admin_level_6: str = result[0][5].strip() if result[0][5] else ''
                osm_admin_level_7: str = result[0][6].strip() if result[0][6] else ''
                osm_admin_level_8: str = result[0][7].strip() if result[0][7] else ''
                osm_admin_level_9: str = result[0][8].strip() if result[0][8] else ''
                location_object: location_beyond_iberian_peninsula.LocationBeyondIberianPeninsula = location_beyond_iberian_peninsula.LocationBeyondIberianPeninsula(
                    name, surrounding_locations, latitude, longitude, altitude, country, osm_admin_level_3, osm_admin_level_4,
                    osm_admin_level_5, osm_admin_level_6, osm_admin_level_7, osm_admin_level_8, osm_admin_level_9)

            location_object.set_destinations(all_destinations)
            location_object.set_ways(ways)
            location_object.set_protected_area(protected_area)
            location_object.set_island(island)
            location_object.set_batch(batch)

            return location_object

        except Exception as e:
            print(f"Exception while getting info for location {name}")
            print(''.join(e.args))
            return None

    def get_location_country(self, location_name: str) -> str:
        """
        Given a location name, returns the respective country
        """
        default_country_name = 'Default'
        table_names: dict[str, str] = {
            location_portugal.COUNTRY: 'LocationPortugal',
            location_spain.COUNTRY: 'LocationSpain',
            location_gibraltar.COUNTRY: 'LocationGibraltar',
            location_andorra.COUNTRY: 'LocationAndorra',
            default_country_name: 'LocationBeyondIberianPeninsula'
        }

        for country_name in table_names:
            table_name: str = table_names[country_name]
            query_template: str = "SELECT COUNT(name) FROM %s WHERE name = {};" % table_name  # Table name would be quoted if inserted using sql.Identifier, causing query to fail
            country_query: psycopg2.sql.SQL = sql.SQL(query_template).format(sql.Literal(location_name))

            self.cursor.execute(country_query)
            location_count: int = self.cursor.fetchall()[0][0]
            is_in_country = location_count
            if is_in_country == 1:  # Location will appear at most once in a country table
                if country_name == default_country_name:  # Location beyond Iberian Peninsula - Country name is instead inside the table
                    get_country_query_template: str = "SELECT country FROM %s WHERE name = {};" % table_name  # Table name would be quoted if inserted using sql.Identifier, causing query to fail
                    get_country_query: psycopg2.sql.SQL = sql.SQL(get_country_query_template).format(sql.Literal(location_name))
                    self.cursor.execute(get_country_query)
                    country_name = self.cursor.fetchall()[0][0]
                return country_name

        return ''  # Location is not part of any country table - It should

    def populate_travel_db(self) -> bool:
        """
        Populates the DB. Returns True on success, False otherwise
        """
        delimiter: str = ','
        encoding: str = 'utf8'

        try:
            csv_path: str = paths_and_files.CSV_LOCATION_PATH
            query = sql.SQL("COPY Location(name, latitude, longitude, altitude, protected_area, island, batch) FROM {} "
                            "DELIMITER {} CSV HEADER ENCODING {};").format(sql.Literal(csv_path), sql.Literal(delimiter), sql.Literal(encoding))
            self.cursor.execute(query)

            csv_path = paths_and_files.CSV_CONCELHO_PATH
            query = sql.SQL("COPY Concelho(concelho, intermunicipal_entity, district, region) FROM {} DELIMITER {} "
                            "CSV HEADER ENCODING {};").format(sql.Literal(csv_path), sql.Literal(delimiter), sql.Literal(encoding))
            self.cursor.execute(query)

            csv_path = paths_and_files.CSV_PROVINCE_PATH
            query = sql.SQL("COPY Province(province, autonomous_community) FROM {} DELIMITER {} "
                            "CSV HEADER ENCODING {};").format(sql.Literal(csv_path), sql.Literal(delimiter), sql.Literal(encoding))
            self.cursor.execute(query)

            csv_path = paths_and_files.CSV_MUNICIPIO_PATH
            query = sql.SQL("COPY Municipio(municipio, comarca, province) FROM {} DELIMITER {} "
                            "CSV HEADER ENCODING {};").format(sql.Literal(csv_path), sql.Literal(delimiter), sql.Literal(encoding))
            self.cursor.execute(query)

            csv_path = paths_and_files.CSV_LOCATION_PORTUGAL_PATH
            query = sql.SQL("COPY LocationPortugal(name, parish, concelho) FROM {} DELIMITER {} "
                            "CSV HEADER ENCODING {};").format(sql.Literal(csv_path), sql.Literal(delimiter), sql.Literal(encoding))
            self.cursor.execute(query)

            csv_path = paths_and_files.CSV_LOCATION_SPAIN_PATH
            query = sql.SQL("COPY LocationSpain(name, municipio, province, district) FROM {} DELIMITER {} "
                            "CSV HEADER ENCODING {};").format(sql.Literal(csv_path), sql.Literal(delimiter), sql.Literal(encoding))
            self.cursor.execute(query)

            csv_path = paths_and_files.CSV_LOCATION_GIBRALTAR_PATH
            query = sql.SQL("COPY LocationGibraltar(name) FROM {} DELIMITER {} "
                            "CSV HEADER ENCODING {};").format(sql.Literal(csv_path), sql.Literal(delimiter), sql.Literal(encoding))
            self.cursor.execute(query)

            csv_path = paths_and_files.CSV_LOCATION_ANDORRA_PATH
            query = sql.SQL("COPY LocationAndorra(name, parish) FROM {} DELIMITER {} "
                            "CSV HEADER ENCODING {};").format(sql.Literal(csv_path), sql.Literal(delimiter), sql.Literal(encoding))
            self.cursor.execute(query)

            csv_path = paths_and_files.CSV_LOCATION_BEYOND_IBERIAN_PENINSULA_PATH
            query = sql.SQL("COPY LocationBeyondIberianPeninsula(name, country, osm_admin_level_3, osm_admin_level_4, osm_admin_level_5, osm_admin_level_6, osm_admin_level_7, osm_admin_level_8, osm_admin_level_9) FROM {} DELIMITER {} "
                            "CSV HEADER ENCODING {};").format(sql.Literal(csv_path), sql.Literal(delimiter), sql.Literal(encoding))
            self.cursor.execute(query)

            csv_path = paths_and_files.CSV_CONNECTION_PATH
            query = sql.SQL("COPY Connection(location_a, location_b, means_transport, distance, way, cardinal_point, order_a, order_b) "
                            "FROM {} DELIMITER {} CSV HEADER ENCODING {};").format(sql.Literal(csv_path), sql.Literal(delimiter), sql.Literal(encoding))
            self.cursor.execute(query)

            csv_path = paths_and_files.CSV_DESTINATION_PATH
            query = sql.SQL("COPY Destination(location_a, location_b, means_transport, starting_point, destination) "
                            "FROM {} DELIMITER {} CSV HEADER ENCODING {};").format(sql.Literal(csv_path), sql.Literal(delimiter), sql.Literal(encoding))
            self.cursor.execute(query)

            return True

        except Exception as e:
            print(f"Exception while populating the {DBInterface.database_name} database")
            print(''.join(e.args))
            return False

    def get_total_location_number(self) -> int:
        """
        Returns the number of locations in the DB
        """
        query = "SELECT COUNT(name) FROM Location;"
        self.cursor.execute(query)
        return self.cursor.fetchall()[0][0]

    # Orders elements of a dictionary according to a supplied order
    @staticmethod
    def order_dictionary(dictionary: dict, order: list[int]) -> dict:
        """
        Orders elements of the provided dictionary according to the supplied order, returns ordered dictionary
        """
        new_dict: dict = {}
        for i in range(len(dictionary)):
            for j in range(len(dictionary)):
                if order[j] == len(new_dict) + 1:
                    dict_key = list(dictionary)[j]
                    new_dict[dict_key] = dictionary[dict_key]
        return new_dict

    def exit(self):
        # Close the connection
        try:
            self.connection.close()
            return True
        except Exception as e:
            print(f"Exception while closing the connection to the {DBInterface.database_name} database")
            print(''.join(e.args))
            return False
