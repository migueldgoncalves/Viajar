import os
import sys
import io
import unittest
import unittest.mock

from travel.support import ways
from travel.support.information_generator import InformationGenerator
from travel.main import paths_and_files

# Note - Altitudes are being fetched from Google using a paid API. First few thousands of requests in a given month are free
# To reduce costs, all tested ways here are small
all_ways_to_analise = [ways.PT_A26, ways.ES_MADRID_METRO_LINE_8]
encoding = 'utf-8'


def _delete_test_files():
    placeholder_filepaths_to_delete = [paths_and_files.TMP_CSV_LOCATION_PATH, paths_and_files.TMP_CSV_CONNECTION_PATH,
                                       paths_and_files.TMP_CSV_LOCATION_SPAIN_PATH, paths_and_files.TMP_CSV_MUNICIPIO_PATH,
                                       paths_and_files.TMP_CSV_COMARCA_PATH, paths_and_files.TMP_CSV_LOCATION_PORTUGAL_PATH,
                                       paths_and_files.TMP_CSV_CONCELHO_PATH, paths_and_files.TMP_CSV_DESTINATION_PATH]
    for way in all_ways_to_analise:
        information_generator = InformationGenerator(way)
        for placeholder in placeholder_filepaths_to_delete:
            actual_filepath: str = information_generator.get_filepath(placeholder)
            if os.path.exists(actual_filepath):
                os.remove(actual_filepath)


def _redirect_output() -> io.StringIO:
    """
    Redirects stdout to be monitorable inside tests

    :return: Object to where stdout is now being redirected
    """
    stdout_redirect: io.StringIO = io.StringIO()
    sys.stdout = stdout_redirect
    return stdout_redirect


class TestInformationGenerator(unittest.TestCase):

    def setUp(self):
        _delete_test_files()

    def test_road_in_portugal(self):
        way_to_analise = ways.PT_A26
        get_altitude_info = True
        information_generator = InformationGenerator(way_to_analise, get_altitude_info)

        information_generator.process_option_get_location_info()

        destinations_to_provide: list[str] = ["1", "Grândola,Beja", "Sines"]
        _redirect_output()
        with unittest.mock.patch('builtins.input', side_effect=destinations_to_provide):  # Simulates user input
            information_generator.process_option_get_connections_and_destinations()

        expected_file_content: list[str] = [
            'A26 - Exit 1,37.97146,-8.824538,24,,,0\n',
            'A26 - Exit 2,37.974813,-8.807394,54,,,0\n',
            'A26 - Exit 3,37.997563,-8.753134,87,,,0\n'
        ]
        with open(information_generator.get_filepath(paths_and_files.TMP_CSV_LOCATION_PATH), 'r', encoding=encoding) as f:
            actual_file_content = f.readlines()
        self.assertEqual(expected_file_content, actual_file_content)

        expected_file_content: list[str] = [
            'A26 - Exit 1,A26 - Exit 2,Car,1.5,A26,E,2,1\n',
            'A26 - Exit 2,A26 - Exit 3,Car,5.4,A26,E,2,1\n'
        ]
        with open(information_generator.get_filepath(paths_and_files.TMP_CSV_CONNECTION_PATH), 'r', encoding=encoding) as f:
            actual_file_content = f.readlines()
        self.assertEqual(expected_file_content, actual_file_content)

        expected_file_content: list[str] = [
            'A26 - Exit 1,A26 - Exit 2,Car,False,Grândola\n',
            'A26 - Exit 1,A26 - Exit 2,Car,False,Beja\n',
            'A26 - Exit 1,A26 - Exit 2,Car,False,\n',
            'A26 - Exit 1,A26 - Exit 2,Car,True,Sines\n',
            'A26 - Exit 1,A26 - Exit 2,Car,True,\n',
            'A26 - Exit 2,A26 - Exit 3,Car,False,Grândola\n',
            'A26 - Exit 2,A26 - Exit 3,Car,False,Beja\n',
            'A26 - Exit 2,A26 - Exit 3,Car,False,\n',
            'A26 - Exit 2,A26 - Exit 3,Car,True,Sines\n',
            'A26 - Exit 2,A26 - Exit 3,Car,True,\n'
        ]
        with open(information_generator.get_filepath(paths_and_files.TMP_CSV_DESTINATION_PATH), 'r', encoding=encoding) as f:
            actual_file_content = f.readlines()
        self.assertEqual(expected_file_content, actual_file_content)

        expected_file_content: list[str] = [
            'A26 - Exit 1,Sines,Sines\n',
            'A26 - Exit 2,Sines,Sines\n',
            'A26 - Exit 3,"Santiago do Cacém, Santa Cruz e São Bartolomeu da Serra",Santiago do Cacém\n'
        ]
        with open(information_generator.get_filepath(paths_and_files.TMP_CSV_LOCATION_PORTUGAL_PATH), 'r', encoding=encoding) as f:
            actual_file_content = f.readlines()
        self.assertEqual(expected_file_content, actual_file_content)

        expected_file_content: list[str] = [
            'Santiago do Cacém,,Setúbal,\n',
            'Sines,,Setúbal,\n'
        ]
        with open(information_generator.get_filepath(paths_and_files.TMP_CSV_CONCELHO_PATH), 'r', encoding=encoding) as f:
            actual_file_content = f.readlines()
        self.assertEqual(expected_file_content, actual_file_content)

    def test_railway_in_spain(self):
        way_to_analise = ways.ES_MADRID_METRO_LINE_8
        get_altitude_info = True
        information_generator = InformationGenerator(way_to_analise, get_altitude_info)

        information_generator.process_option_get_location_info()

        destinations_to_provide: list[str] = ["2", "", "Madrid City Centre"]
        _redirect_output()
        with unittest.mock.patch('builtins.input', side_effect=destinations_to_provide):  # Simulates user input
            information_generator.process_option_get_connections_and_destinations()

        expected_file_content: list[str] = [
            'Aeropuerto T1-T2-T3 Station,40.467794,-3.571789,605,,,0\n',
            'Aeropuerto T4 Station,40.492395,-3.593248,615,,,0\n',
            'Barajas Station,40.47616,-3.583413,623,,,0\n',
            'Colombia Station,40.457128,-3.67706,707,,,0\n',
            'Feria de Madrid Station,40.463936,-3.615554,672,,,0\n',
            'Mar de Cristal Station,40.469888,-3.638573,679,,,0\n',
            'Nuevos Ministerios Station,40.445482,-3.691583,680,,,0\n',
            'Pinar del Rey Station,40.467858,-3.64869,704,,,0\n'
        ]
        with open(information_generator.get_filepath(paths_and_files.TMP_CSV_LOCATION_PATH), 'r', encoding=encoding) as f:
            actual_file_content = f.readlines()
        self.assertEqual(expected_file_content, actual_file_content)

        expected_file_content: list[str] = [
            'Pinar del Rey Station,Nuevos Ministerios Station,Train,4.6,Madrid Metro - Line 8,SW,2,1\n',
            'Nuevos Ministerios Station,Mar de Cristal Station,Train,5.5,Madrid Metro - Line 8,E,2,1\n',
            'Mar de Cristal Station,Feria de Madrid Station,Train,2.1,Madrid Metro - Line 8,E,2,1\n',
            'Feria de Madrid Station,Colombia Station,Train,5.8,Madrid Metro - Line 8,W,2,1\n',
            'Colombia Station,Barajas Station,Train,11.4,Madrid Metro - Line 8,E,2,1\n',
            'Barajas Station,Aeropuerto T4 Station,Train,2.1,Madrid Metro - Line 8,NW,2,1\n',
            'Aeropuerto T4 Station,Aeropuerto T1-T2-T3 Station,Train,3.5,Madrid Metro - Line 8,SE,2,1\n'
        ]
        with open(information_generator.get_filepath(paths_and_files.TMP_CSV_CONNECTION_PATH), 'r', encoding=encoding) as f:
            actual_file_content = f.readlines()
        self.assertEqual(expected_file_content, actual_file_content)

        expected_file_content: list[str] = [
            'Pinar del Rey Station,Nuevos Ministerios Station,Train,False,\n',
            'Pinar del Rey Station,Nuevos Ministerios Station,Train,False,\n',
            'Pinar del Rey Station,Nuevos Ministerios Station,Train,True,Madrid City Centre\n',
            'Pinar del Rey Station,Nuevos Ministerios Station,Train,True,\n',
            'Nuevos Ministerios Station,Mar de Cristal Station,Train,False,\n',
            'Nuevos Ministerios Station,Mar de Cristal Station,Train,False,\n',
            'Nuevos Ministerios Station,Mar de Cristal Station,Train,True,Madrid City Centre\n',
            'Nuevos Ministerios Station,Mar de Cristal Station,Train,True,\n',
            'Mar de Cristal Station,Feria de Madrid Station,Train,False,\n',
            'Mar de Cristal Station,Feria de Madrid Station,Train,False,\n',
            'Mar de Cristal Station,Feria de Madrid Station,Train,True,Madrid City Centre\n',
            'Mar de Cristal Station,Feria de Madrid Station,Train,True,\n',
            'Feria de Madrid Station,Colombia Station,Train,False,\n',
            'Feria de Madrid Station,Colombia Station,Train,False,\n',
            'Feria de Madrid Station,Colombia Station,Train,True,Madrid City Centre\n',
            'Feria de Madrid Station,Colombia Station,Train,True,\n',
            'Colombia Station,Barajas Station,Train,False,\n',
            'Colombia Station,Barajas Station,Train,False,\n',
            'Colombia Station,Barajas Station,Train,True,Madrid City Centre\n',
            'Colombia Station,Barajas Station,Train,True,\n',
            'Barajas Station,Aeropuerto T4 Station,Train,False,\n',
            'Barajas Station,Aeropuerto T4 Station,Train,False,\n',
            'Barajas Station,Aeropuerto T4 Station,Train,True,Madrid City Centre\n',
            'Barajas Station,Aeropuerto T4 Station,Train,True,\n',
            'Aeropuerto T4 Station,Aeropuerto T1-T2-T3 Station,Train,False,\n',
            'Aeropuerto T4 Station,Aeropuerto T1-T2-T3 Station,Train,False,\n',
            'Aeropuerto T4 Station,Aeropuerto T1-T2-T3 Station,Train,True,Madrid City Centre\n',
            'Aeropuerto T4 Station,Aeropuerto T1-T2-T3 Station,Train,True,\n']
        with open(information_generator.get_filepath(paths_and_files.TMP_CSV_DESTINATION_PATH), 'r', encoding=encoding) as f:
            actual_file_content = f.readlines()
        self.assertEqual(expected_file_content, actual_file_content)

        expected_file_content: list[str] = [
            'Aeropuerto T1-T2-T3 Station,Madrid,Archidiócesis de Madrid,Barajas\n',
            'Aeropuerto T4 Station,Madrid,Archidiócesis de Madrid,Barajas\n',
            'Barajas Station,Madrid,Archidiócesis de Madrid,Barajas\n',
            'Colombia Station,Madrid,Archidiócesis de Madrid,Chamartín\n',
            'Feria de Madrid Station,Madrid,Archidiócesis de Madrid,Barajas\n',
            'Mar de Cristal Station,Madrid,Archidiócesis de Madrid,Hortaleza\n',
            'Nuevos Ministerios Station,Madrid,Archidiócesis de Madrid,Chamberí\n',
            'Pinar del Rey Station,Madrid,Archidiócesis de Madrid,Hortaleza\n'
        ]
        with open(information_generator.get_filepath(paths_and_files.TMP_CSV_LOCATION_SPAIN_PATH), 'r', encoding=encoding) as f:
            actual_file_content = f.readlines()
        self.assertEqual(expected_file_content, actual_file_content)

        expected_file_content: list[str] = [
            'Madrid,Archidiócesis de Madrid\n'
        ]
        with open(information_generator.get_filepath(paths_and_files.TMP_CSV_MUNICIPIO_PATH), 'r', encoding=encoding) as f:
            actual_file_content = f.readlines()
        self.assertEqual(expected_file_content, actual_file_content)

        expected_file_content: list[str] = []
        with open(information_generator.get_filepath(paths_and_files.TMP_CSV_COMARCA_PATH), 'r', encoding=encoding) as f:
            actual_file_content = f.readlines()
        self.assertEqual(expected_file_content, actual_file_content)

    def tearDown(self):
        _delete_test_files()
