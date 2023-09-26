import unittest
from xml.dom import minidom

from travel.support.osm_interface import OsmInterface
from travel.support import osm_interface
from travel.support import ways
from travel.support.coordinates import Coordinates
from test.travel.support import test_fail_if_servers_down


class TestOsmInterface(unittest.TestCase):

    def test_get_administrative_divisions_by_coordinates_invalid_parameters(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        # No coordinates
        with self.assertRaises(AssertionError):
            OsmInterface().get_administrative_divisions_by_coordinates(None, ways.PORTUGAL)  # Providing null country is accepted

        # Invalid country
        with self.assertRaises(AssertionError):
            OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(39.0, -5.0), 'Invalid country')

        # Coordinates outside covered countries
        self.assertEqual({}, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(0.0, 0.0), None))  # Gulf of Guinea
        self.assertEqual({}, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(0.0, 0.0), ways.PORTUGAL))  # Gulf of Guinea

        # Coordinates not matching provided country
        self.assertEqual({}, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(39.0, -5.0), ways.PORTUGAL))  # Coordinates belong to Spanish Extremadura

    def test_get_administrative_divisions_by_coordinates_successful(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        # Portugal, far from Spanish border
        expected_response = {
            2: 'Portugal',
            6: 'Lisboa',
            7: 'Vila Franca de Xira',
            8: 'Castanheira do Ribatejo e Cachoeiras',
            'historic_parish': 'Cachoeiras',
            'região;sub-região': 'Área Metropolitana de Lisboa',
            'timezone': 'Fuso Horário da Europa/Lisboa'
        }
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(39.0, -9.0), None))
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(39.0, -9.0), ways.PORTUGAL))

        # Portugal, close from Spanish border
        expected_response = {
            2: 'Portugal',
            6: 'Portalegre',
            7: 'Campo Maior',
            8: 'Nossa Senhora da Expectação',
            'protected_area': 'Caia',
            'região': 'Alentejo',
            'sub-região': 'Alto Alentejo',
            'timezone': 'Fuso Horário da Europa/Lisboa'
        }
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(39.0, -7.0), None))
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(39.0, -7.0), ways.PORTUGAL))

        # Portuguese Madeira Islands
        expected_response = {
            2: 'Portugal',
            4: 'Madeira',
            7: 'Porto Santo',
            8: 'Porto Santo',
            'ilha': 'Porto Santo',
            'lugar': 'Matas',
            'timezone': 'Atlantic/Madeira Timezone'
        }
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(33.058620, -16.339865), None))
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(33.058620, -16.339865), ways.PORTUGAL))

        # Portuguese Azores Islands
        expected_response = {
            2: 'Portugal',
            4: 'Açores',
            7: 'Velas',
            8: 'Norte Grande (Neves)',
            'ilha': 'São Jorge',
            'timezone': 'Atlantic/Azores Timezone'
        }
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(38.673701, -28.055517), None))
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(38.673701, -28.055517), ways.PORTUGAL))

        # Spain, close from Portuguese border
        expected_response = {
            2: 'España',
            4: 'Extremadura',
            6: 'Badajoz',
            8: 'Mérida',
            'timezone': 'Zona Horaria de Europa/Madrid'
        }
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(39.0, -6.5), None))
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(39.0, -6.5), ways.SPAIN))

        # Spain, far from all borders, with comarca and district info known
        expected_response = {
            2: 'España',
            4: 'Provincia Eclesiástica de Madrid',
            6: 'Archidiócesis de Madrid',
            8: 'Madrid',
            9: 'Moncloa-Aravaca',
            10: 'Ciudad Universitaria',
            'timezone': 'Zona Horaria de Europa/Madrid'
        }
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(40.45, -3.75), None))
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(40.45, -3.75), ways.SPAIN))

        # Spain, close from Gibraltar border
        expected_response = {
            2: 'España',
            4: 'Andalucía',
            6: 'Cádiz',
            7: 'Campo de Gibraltar',
            8: 'La Línea de la Concepción',
            'timezone': 'Zona Horaria de Europa/Madrid'
        }
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(36.168023, -5.350738), None))
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(36.168023, -5.350738), ways.SPAIN))

        # Spain, close from Andorran border
        expected_response = {
            2: 'España',
            4: 'Catalunya',
            6: 'Lleida',
            7: 'Alt Urgell',
            8: "la Seu d'Urgell",
            'political': 'Català com a llengua pròpia a Catalunya',
            'political_fraction': 'Alt Pirineu i Aran (Lleida)',
            'timezone': 'Zona Horaria de Europa/Madrid'
        }
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(42.358877, 1.456251), None))
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(42.358877, 1.456251), ways.SPAIN))

        # Spain, close from French border
        expected_response = {
            2: 'España',
            4: 'Euskadi',
            6: 'Gipuzkoa',
            8: 'Hondarribia/Fontarrabie',
            'historic': 'Bidasoa Beherea / Bajo Bidasoa',
            'timezone': 'Zona Horaria de Europa/Madrid'
        }
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(43.369574, -1.796590), None))
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(43.369574, -1.796590), ways.SPAIN))

        # Ceuta, Spain, close from Moroccan border
        expected_response = {
            2: 'España',
            4: 'Ceuta',
            8: 'Ceuta',
            'disputed': 'Alcance de las Reclamaciones Españolas en Ceuta'
        }
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(35.888740, -5.320993), None))
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(35.888740, -5.320993), ways.SPAIN))

        # Melilla, Spain, close from Moroccan border
        expected_response = {
            2: 'España',
            4: 'Melilla',
            8: 'Melilla',
            'disputed': 'Extent of Spanish Claim at Melilla'
        }
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(35.287817, -2.947612), None))
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(35.287817, -2.947612), ways.SPAIN))

        # Spanish Balearic Islands
        expected_response = {
            2: 'España',
            4: 'Illes Balears',
            6: 'Illes Balears',
            7: 'Menorca',
            8: 'Maó',
            'timezone': 'Zona Horaria de Europa/Madrid'
        }
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(39.888771, 4.260855), None))
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(39.888771, 4.260855), ways.SPAIN))

        # Spanish Canary Islands - Included in a separate server
        expected_response = {
            2: 'España',
            4: 'Canarias',
            6: 'Las Palmas',
            8: 'Las Palmas de Gran Canaria',
            'political': 'Gran Canaria',
            'region': 'Canary Islands',
            'timezone': 'Atlantic/Canary Timezone'
        }
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(28.117338, -15.437617), None))
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(28.117338, -15.437617), ways.CANARY_ISLANDS))

        # Gibraltar
        expected_response = {
            2: 'Gibraltar',
            4: 'Gibraltar',
            'administrative': 'British Overseas Territories'
        }
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(36.135510, -5.347506), None))
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(36.135510, -5.347506), ways.GIBRALTAR))

        # Andorra
        expected_response = {
            2: 'Andorra',
            7: 'Escaldes-Engordany',
        }
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(42.509215, 1.538949), None))
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(42.509215, 1.538949), ways.ANDORRA))

    def test_get_road_exits_invalid_parameters(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        # No parameters
        with self.assertRaises(AssertionError):
            OsmInterface().get_road_exits(None, None)

        # Invalid parameters
        with self.assertRaises(AssertionError):
            OsmInterface().get_road_exits('Invalid road', 'Invalid country')

        # No road name
        with self.assertRaises(AssertionError):
            OsmInterface().get_road_exits(None, ways.PORTUGAL)
        with self.assertRaises(AssertionError):
            OsmInterface().get_road_exits('', ways.PORTUGAL)

        # Invalid road name
        self.assertEqual({}, OsmInterface().get_road_exits('Invalid road', ways.PORTUGAL))

        # No country
        with self.assertRaises(AssertionError):
            OsmInterface().get_road_exits(ways.PT_A5.osm_name, None)
        with self.assertRaises(AssertionError):
            OsmInterface().get_road_exits(ways.PT_A5.osm_name, '')

        # Invalid country
        with self.assertRaises(AssertionError):
            OsmInterface().get_road_exits(ways.PT_A5.osm_name, 'Invalid country')

    def test_get_road_exits_successful(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        # Large Continental Portuguese freeway
        expected_response_keys = [
            '1', '10', '10A', '11', '12', '13', '14', '15', '16', '17', '18', '18A', '18B', '19', '19A', '1A', '2', '22',
            '23', '2A', '3', '3A', '4', '5', '5A', '6', '6 A', '7', '8', '9'
        ]
        response: dict[str, list[Coordinates]] = OsmInterface().get_road_exits(ways.PT_A1.osm_name, ways.PORTUGAL)

        self.assertEqual(expected_response_keys, list(response.keys()))
        for key in expected_response_keys:
            self.assertTrue((len(response[key]) > 0))
        self.assertEqual([Coordinates(38.7936469, -9.1126855), Coordinates(38.7844696, -9.1208711)], response['1'])
        self.assertEqual([Coordinates(41.0793433, -8.5817397), Coordinates(41.0726616, -8.5809713),
                          Coordinates(41.0669659, -8.5815887)], response['19'])
        self.assertEqual([Coordinates(39.7417361, -8.7432394), Coordinates(39.7395957, -8.7364531)], response['9'])

        # Small Continental Portuguese freeway
        expected_response_keys = [
            '1', '10', '11', '12', '2', '3', '4', '5', '6', '7', '8', '9'
        ]
        response: dict[str, list[Coordinates]] = OsmInterface().get_road_exits(ways.PT_A5.osm_name, ways.PORTUGAL)

        self.assertEqual(expected_response_keys, list(response.keys()))
        for key in expected_response_keys:
            self.assertTrue((len(response[key]) > 0))
        self.assertEqual([Coordinates(38.7248631, -9.1848642)], response['1'])
        self.assertEqual([Coordinates(38.7189712, -9.2115565), Coordinates(38.7207966, -9.2058737),
                          Coordinates(38.7212092, -9.2044865)], response['3'])
        self.assertEqual([Coordinates(38.7174199, -9.3854995), Coordinates(38.7177498, -9.3910173)], response['9'])

        # Freeway in the Portuguese Azores islands
        expected_response_keys = ['1', '2', '3', '4', '5', '6']
        response: dict[str, list[Coordinates]] = OsmInterface().get_road_exits(ways.PT_EN11A.osm_name, ways.PORTUGAL)

        self.assertEqual(expected_response_keys, list(response.keys()))
        for key in expected_response_keys:
            self.assertTrue((len(response[key]) > 0))
        self.assertEqual([Coordinates(37.7466258, -25.6986159)], response['1'])
        self.assertEqual([Coordinates(37.7568791, -25.6714952), Coordinates(37.7559955, -25.6744092)], response['4'])
        self.assertEqual([Coordinates(37.7506841, -25.6507245), Coordinates(37.745365, -25.7005975)], response['6'])

        # Freeway in the Portuguese Madeira islands
        expected_response_keys = [
            '1', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '2', '20', '21', '22', '23', '24', '25',
            '26', '27', '28', '3', '4', '5', '6', '7', '8', '9'
        ]
        response: dict[str, list[Coordinates]] = OsmInterface().get_road_exits(ways.PT_VR1.osm_name, ways.PORTUGAL)

        self.assertEqual(expected_response_keys, list(response.keys()))
        for key in expected_response_keys:
            self.assertTrue((len(response[key]) > 0))
        self.assertEqual([Coordinates(32.6842945, -17.0520903)], response['1'])
        self.assertEqual([Coordinates(32.684517, -16.7947839), Coordinates(32.6843973, -16.7947382)], response['20'])
        self.assertEqual([Coordinates(32.6579781, -16.9352209), Coordinates(32.6529814, -16.9405235),
                          Coordinates(32.6571532, -16.936037)], response['9'])

        # Portuguese road without exit numbers
        response: dict[str, list[Coordinates]] = OsmInterface().get_road_exits(ways.PT_IC27.osm_name, ways.PORTUGAL)
        self.assertEqual({}, response)

        # Large Peninsular Spanish freeway
        expected_response_keys = [
            '1', '1003', '1008', '1010', '1011', '1012', '1014', '1015', '1020', '1023', '1024', '103', '104', '105',
            '110A', '110B', '110b', '1110', '112', '113b',
            '115', '116', '117', '118', '119', '124', '127', '133', '153', '157', '160', '170', '172', '174',
            '175', '176', '181A', '183', '184', '185',
            '186', '187', '188', '192', '196', '197', '198', '206', '208', '209', '223', '226', '230', '232', '233', '237', '238', '239', '240',
            '241', '274', '277', '278', '279', '282', '283', '287A', '287B', '289', '293', '297', '298',
            '307', '311', '313', '315', '321', '322', '324', '325', '326', '328', '329', '331', '335', '336',
            '339', '341', '342', '344', '346', '351', '354', '355', '356', '357', '359', '371', '373', '375', '376',
            '379', '381', '383', '384', '385', '386', '389', '391',
            '395', '396', '398', '400', '402', '403', '404', '406', '409', '410', '411', '413', '414', '415', '416', '417',
            '418', '420', '421', '423', '424', '425', '429', '430', '431', '432', '435', '436', '438', '441',
            '442', '443', '446', '448', '449', '452', '453', '456', '459', '460', '464', '467', '468', '469', '471',
            '475', '479', '481', '482', '487', '489', '492', '494', '50', '504', '51', '510', '513', '514',
            '516', '518', '523', '525', '526', '528', '529', '535', '538', '541',
            '543', '545', '547', '549', '553', '555', '559', '559A', '559B', '563', '565', '567 AB', '571',
            '575', '578 A', '578 AB', '578 B', '578 BA', '581', '584', '585', '586', '588', '589', '591', '594', '596',
            '598', '6', '601', '609', '611', '616', '618', '622', '623', '628', '630', '633', '636', '640', '642',
            '644', '645', '646', '649', '651', '655',  '664', '666', '675', '692', '695A', '695B', '910', '920', '929',
            '933', '940', '948', '951', '953', '960', '967', '968', '970', '973', '978', '978A', '978B', '979', '981',
            '981A', '981B', '982', '988', '989', '992', '999'
        ]
        response: dict[str, list[Coordinates]] = OsmInterface().get_road_exits(ways.ES_A7.osm_name, ways.SPAIN)

        self.assertEqual(expected_response_keys, list(response.keys()))
        for key in expected_response_keys:
            self.assertTrue((len(response[key]) > 0))
        self.assertEqual([Coordinates(39.8955497, -0.1970601), Coordinates(39.8971608, -0.1970829)], response['1'])
        self.assertEqual([Coordinates(36.7741554, -3.5724422), Coordinates(36.7733459, -3.5811174)], response['322'])
        self.assertEqual([Coordinates(36.6248973, -4.5161178)], response['999'])

        # Small Peninsular Spanish freeway
        expected_response_keys = ['0A', '1', '10', '11', '12', '12B', '12C', '13', '14A', '14B', '16', '17', '19', '2', '20', '20A',
                                  '20B', '23', '23A', '23B', '24', '25', '26', '27', '28', '2A', '2B', '2C', '3',
                                  '3-4-5', '30', '31', '31B', '3BA', '4', '5', '5A', '5AB', '6', '6A', '6B', '7', '7-6',
                                  '7-8-9', '7A', '7B', '7BA', '8', '8-9', '8A', '9A', '9B'
                                  ]
        response: dict[str, list[Coordinates]] = OsmInterface().get_road_exits(ways.ES_M30.osm_name, ways.SPAIN)

        self.assertEqual(expected_response_keys, list(response.keys()))
        for key in expected_response_keys:
            self.assertTrue((len(response[key]) > 0))
        self.assertEqual([Coordinates(40.4813264, -3.673715)], response['0A'])
        self.assertEqual([Coordinates(40.4642921, -3.6667577)], response['2C'])
        self.assertEqual([Coordinates(40.4028638, -3.6664435)], response['9B'])

        # Freeway in the Spanish Balearic Islands
        expected_response_keys = [
            '12', '15', '17', '1B', '2', '22', '25', '27', '2B', '3', '30', '35', '36', '37', '4', '40', '6', '7', '8'
        ]
        response: dict[str, list[Coordinates]] = OsmInterface().get_road_exits(ways.ES_MA13.osm_name, ways.SPAIN)

        self.assertEqual(expected_response_keys, list(response.keys()))
        for key in expected_response_keys:
            self.assertTrue((len(response[key]) > 0))
        self.assertEqual([Coordinates(39.6386017, 2.7762271), Coordinates(39.6419962, 2.7832712)], response['12'])
        self.assertEqual([Coordinates(39.7032618, 2.8964112), Coordinates(39.7059107, 2.9025601)], response['25'])
        self.assertEqual([Coordinates(39.6305955, 2.7409232), Coordinates(39.6298699, 2.7374448)], response['8'])

        # Freeway in the Spanish Canary Islands
        expected_response_keys = [
            '0', '1', '10', '11', '12', '13', '15', '16', '17', '18', '2', '23', '25', '26', '28', '3', '31', '37', '4',
            '43', '45', '46', '48', '5', '50', '53', '56', '6', '62', '67', '68', '6A', '6B', '7', '7A', '7B', '7C', '8'
        ]
        response: dict[str, list[Coordinates]] = OsmInterface().get_road_exits(ways.ES_GC1.osm_name, ways.CANARY_ISLANDS)

        self.assertEqual(expected_response_keys, list(response.keys()))
        for key in expected_response_keys:
            self.assertTrue((len(response[key]) > 0))
        self.assertEqual([Coordinates(28.0722836, -15.4164624)], response['0'])
        self.assertEqual([Coordinates(27.7726755, -15.5548229), Coordinates(27.7687561, -15.5579072)], response['43'])
        self.assertEqual([Coordinates(28.0005451, -15.391823)], response['8'])

        # Spanish road without exit numbers
        response: dict[str, list[Coordinates]] = OsmInterface().get_road_exits(ways.ES_A483.osm_name, ways.SPAIN)
        self.assertEqual({}, response)
        response: dict[str, list[Coordinates]] = OsmInterface().get_road_exits(ways.ES_GC21.osm_name, ways.CANARY_ISLANDS)
        self.assertEqual({}, response)

        # No road in Andorra or Gibraltar is expected to have exit numbers

    def test_get_railway_stations_invalid_parameters(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        # No parameters
        with self.assertRaises(AssertionError):
            OsmInterface().get_railway_stations(None, None)

        # Invalid parameters
        with self.assertRaises(AssertionError):
            OsmInterface().get_railway_stations('Invalid railway', 'Invalid country')

        # No railway name
        with self.assertRaises(AssertionError):
            OsmInterface().get_railway_stations(None, ways.PORTUGAL)
        with self.assertRaises(AssertionError):
            OsmInterface().get_railway_stations('', ways.PORTUGAL)

        # Invalid railway name
        self.assertEqual({}, OsmInterface().get_railway_stations('Invalid railway', ways.PORTUGAL))

        # No country
        with self.assertRaises(AssertionError):
            OsmInterface().get_railway_stations(ways.PT_NORTH_LINE.osm_name, None)
        with self.assertRaises(AssertionError):
            OsmInterface().get_railway_stations(ways.PT_NORTH_LINE.osm_name, '')

        # Invalid country
        with self.assertRaises(AssertionError):
            OsmInterface().get_railway_stations(ways.PT_NORTH_LINE.osm_name, 'Invalid country')

    def test_get_railway_exits_successful(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        # Large Portuguese railway
        expected_response_keys = [
            'Braço de Prata', 'Ovar', 'Avanca', 'Vale de Santarém', 'Mato de Miranda', 'Bifurcação de Xabregas', 'Passagem de Nível da Adémia',
            'Litém', 'Azambuja', 'Riachos', 'Entroncamento', 'Lamarosa', 'Setil', 'Santarém', 'Reguengo-Vale da Pedra-Pontével',
            'Vale de Figueira', 'Virtudes', 'Santana-Cartaxo', 'Moscavide', 'Sacavém', 'Bobadela', 'Alverca',
            'Carvalheira-Maceda', 'Espadanal da Azambuja', 'Miramar', 'Espinho', 'Silvalde', 'Bencanta', 'Espadaneira',
            'Esmoriz', 'Paramos', 'Coimbrões', 'Gaia', 'Madalena', 'Valadares', 'Aguda', 'Francelos',
            'Cortegaça', 'Granja', 'Válega', 'Estarreja', 'Cacia', 'Canelas', 'Salreu', 'Aveiro', 'Oiã',
            'Oliveira do Bairro', 'Paraimo-Sangalhos', 'Quintãs', 'Aguim', 'Curia', 'Mealhada', 'Mogofores',
            'Pampilhosa', 'Souselas', 'Adémia', 'Coimbra-B', 'Vilela-Fornos', 'Alfarelos - Granja do Ulmeiro', 'Amial',
            'Casais', 'Taveiro', 'Formoselha', 'Pereira', 'Vila Pouca do Campo', 'Pelariga', 'Pombal', 'Simões',
            'Soure', 'Vila Nova de Anços', 'Albergaria dos Doze', 'Caxarias', 'Vermoil', 'Chão de Maçãs-Fátima',
            'Fungalvaz', 'Paialvo', 'Seiça-Ourém', 'Bifurcação Norte do Setil', 'Vila Nova da Rainha',
            'Carregado', 'Castanheira do Ribatejo', 'Vila Franca de Xira', 'Alhandra', 'Quinta das Torres',
            'General Torres', 'Gare do Oriente', 'Póvoa', 'Santa Iria', 'Porto - Campanhã', 'Lisboa - Santa Apolónia'
        ]
        response: dict[str, list[Coordinates]] = OsmInterface().get_railway_stations(ways.PT_NORTH_LINE.osm_name, ways.PORTUGAL)

        self.assertEqual(expected_response_keys, list(response.keys()))
        for key in expected_response_keys:
            self.assertTrue((len(response[key]) > 0))
        self.assertEqual([Coordinates(38.7470748, -9.1027308), Coordinates(38.7470648, -9.1026882)], response['Braço de Prata'])
        self.assertEqual([Coordinates(40.5910309, -8.612713), Coordinates(40.5910442, -8.6126654)], response['Quintãs'])
        self.assertEqual([Coordinates(38.7137802, -9.1229108), Coordinates(38.7138279, -9.1230008)], response['Lisboa - Santa Apolónia'])

        # Small Portuguese railway
        expected_response_keys = [
            'Algueirão-Mem Martins', 'Amadora', 'Campolide', 'Santa Cruz - Damaia', 'Queluz-Belas', 'Monte Abraão',
            'Massamá-Barcarena', 'Agualva - Cacém', 'Rio de Mouro', 'Portela de Sintra', 'Mercês', 'Sintra',
            'Benfica', 'Reboleira'
        ]
        response: dict[str, list[Coordinates]] = OsmInterface().get_railway_stations(ways.PT_SINTRA_LINE.osm_name, ways.PORTUGAL)

        self.assertEqual(expected_response_keys, list(response.keys()))
        for key in expected_response_keys:
            self.assertTrue((len(response[key]) > 0))
        self.assertEqual([Coordinates(38.7978927, -9.3399843), Coordinates(38.7975035, -9.3422101)], response['Algueirão-Mem Martins'])
        self.assertEqual([Coordinates(38.7845893, -9.3220953), Coordinates(38.7839355, -9.3197534)], response['Rio de Mouro'])
        self.assertEqual([Coordinates(38.7506498, -9.2215468), Coordinates(38.7506823, -9.2215326),
                          Coordinates(38.751105, -9.2239419), Coordinates(38.7511375, -9.2239275)], response['Reboleira'])

        # Neither Madeira nor Azores Islands have railways

        # Large Peninsular Spanish railway
        expected_response_keys = [
            'Cabeza Del Buey', 'Almadenejos-Almaden', 'Guadalmez-Los Pedroches', 'Villagonzalo'
        ]
        response: dict[str, list[Coordinates]] = OsmInterface().get_railway_stations(ways.ES_CIUDAD_REAL_BADAJOZ.osm_name, ways.SPAIN)

        self.assertEqual(expected_response_keys, list(response.keys()))
        for key in expected_response_keys:
            self.assertTrue((len(response[key]) > 0))
        self.assertEqual([Coordinates(38.7404341, -4.7303171)], response['Almadenejos-Almaden'])
        self.assertEqual([Coordinates(38.8641393, -6.2075556)], response['Villagonzalo'])

        # Small Peninsular Spanish railway
        expected_response_keys = [
            'Colombia', 'Aeropuerto T4', 'Barajas', 'Feria de Madrid', 'Aeropuerto T1-T2-T3', 'Mar de Cristal',
            'Pinar del Rey', 'Nuevos Ministerios'
        ]
        response: dict[str, list[Coordinates]] = OsmInterface().get_railway_stations(ways.ES_MADRID_METRO_LINE_8.osm_name, ways.SPAIN)

        self.assertEqual(expected_response_keys, list(response.keys()))
        for key in expected_response_keys:
            self.assertTrue((len(response[key]) > 0))
        self.assertEqual([Coordinates(40.4571282, -3.67706)], response['Colombia'])
        self.assertEqual([Coordinates(40.4677938, -3.5717894)], response['Aeropuerto T1-T2-T3'])
        self.assertEqual([Coordinates(40.4454819, -3.6915827)], response['Nuevos Ministerios'])

        # Railway in the Spanish Balearic Islands
        expected_response_keys = [
            'Sineu', "es Pont d'Inca", 'Enllaç', 'Petra', 'Manacor Estació', 'Santa Maria del Camí', 'Consell/Alaró',
            'Lloseta', 'Inca', 'Es Caülls', "Es Pont d'Inca Nou", 'Polígon de Marratxí', 'Son Costa - Son Fortesa',
            'Son Cladera - Es Vivero', 'Son Fuster', 'Marratxí', 'Jacint Verdaguer', 'Binissalem', 'Verge de Lluc',
            'Intermodal'
        ]
        response: dict[str, list[Coordinates]] = OsmInterface().get_railway_stations(ways.ES_SFM_T3.osm_name, ways.SPAIN)

        self.assertEqual(expected_response_keys, list(response.keys()))
        for key in expected_response_keys:
            self.assertTrue((len(response[key]) > 0))
        self.assertEqual([Coordinates(39.6436653, 3.0145261)], response['Sineu'])
        self.assertEqual([Coordinates(39.6044446, 2.7015167)], response["Es Pont d'Inca Nou"])
        self.assertEqual([Coordinates(39.5765349, 2.654482)], response['Intermodal'])

        # Railway in the Spanish Canary Islands
        expected_response_keys = [
            'Trinidad', 'Padre Anchieta', 'Cruz de Piedra', 'Museo de la Ciencia', 'Gracia', 'Teatro Guimerá', 'Fundación',
            'Intercambiador', 'Weyler', 'La Paz', 'Campus Guajara', 'Las Mantecas', 'Hospital Universitario', 'El Cardonal',
            'Taco', 'Hospital La Candelaria', 'Príncipes de España', 'Chimisay', 'Conservatorio', 'Cruz del Señor',
            'Puente Zurita'
        ]
        response: dict[str, list[Coordinates]] = OsmInterface().get_railway_stations(ways.ES_TENERIFE_TRAMWAY_T1.osm_name, ways.CANARY_ISLANDS)

        self.assertEqual(expected_response_keys, list(response.keys()))
        for key in expected_response_keys:
            self.assertTrue((len(response[key]) > 0))
        self.assertEqual([Coordinates(28.4858143, -16.3163949)], response['Trinidad'])
        self.assertEqual([Coordinates(28.4635534, -16.2969276)], response["Las Mantecas"])
        self.assertEqual([Coordinates(28.4678111, -16.2647475)], response['Puente Zurita'])

        # Neither Andorra nor Gibraltar have railways

    def test_process_area_for_distance_calculation_invalid_parameters(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        valid_coordinate_list = [Coordinates(1, 1), Coordinates(-1, -1)]

        # All invalid parameters
        with self.assertRaises(AssertionError):
            OsmInterface().process_area_for_distance_calculation([], None, 0, None)

        # Empty coordinate list
        with self.assertRaises(AssertionError):
            OsmInterface().process_area_for_distance_calculation([], ways.ROAD, osm_interface.DETAIL_LEVEL_URBAN, ways.PORTUGAL)

        # No way type
        with self.assertRaises(AssertionError):
            OsmInterface().process_area_for_distance_calculation(valid_coordinate_list, None, osm_interface.DETAIL_LEVEL_URBAN, ways.PORTUGAL)

        # Invalid way type
        with self.assertRaises(AssertionError):
            OsmInterface().process_area_for_distance_calculation(valid_coordinate_list, 'Invalid way type', osm_interface.DETAIL_LEVEL_URBAN, ways.PORTUGAL)

        # No detail level
        with self.assertRaises(AssertionError):
            OsmInterface().process_area_for_distance_calculation(valid_coordinate_list, ways.ROAD, 0, ways.PORTUGAL)

        # Invalid detail level
        with self.assertRaises(AssertionError):
            OsmInterface().process_area_for_distance_calculation(valid_coordinate_list, ways.ROAD, -1, ways.PORTUGAL)

        # No country
        with self.assertRaises(AssertionError):
            OsmInterface().process_area_for_distance_calculation(valid_coordinate_list, ways.ROAD, -1, None)

        # Invalid country
        with self.assertRaises(AssertionError):
            OsmInterface().process_area_for_distance_calculation(valid_coordinate_list, ways.ROAD, -1, 'Invalid country')

    def test_process_area_for_distance_calculation_successful(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        # This routine can be tested through calls to higher-level routines, with fewer lines of code
        # As such, this test will contain a single test case

        coordinate_list = [Coordinates(39.1, -8.9), Coordinates(38.9, -9.1)]  # An area north of Lisbon
        way_type = ways.ROAD
        detail = osm_interface.DETAIL_LEVEL_INTERCITY
        country = ways.PORTUGAL

        result = OsmInterface().process_area_for_distance_calculation(coordinate_list, way_type, detail, country)
        node_list = result[0]
        way_list = result[1]
        extreme_points = result[2]

        self.assertEqual(3, len(result))
        self.assertEqual(28145, len(node_list))  # Number of nodes
        self.assertEqual(3294, len(way_list))  # Number of ways

        for node in node_list:
            assert node
        for way in way_list:
            assert way

        node_id = 320080135
        self.assertEqual(39.121356, node_list.get(node_id).latitude)
        self.assertEqual(-8.9103214, node_list.get(node_id).longitude)
        self.assertEqual(node_id, node_list.get(node_id).node_id)
        self.assertEqual(set(), node_list.get(node_id).surrounding_node_ids)

        way_id = 4015552
        way_node_ids = [320080135, 320080136, 320080137]
        for i in range(3):
            self.assertEqual(way_node_ids[i], way_list.get(way_id).node_list[i].node_id)
        self.assertEqual(way_id, way_list.get(way_id).way_id)

        self.assertEqual(extreme_points, [38.8, 39.2, -9.2, -8.8])

    def test_process_way_for_distance_calculation_invalid_parameters(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        # All invalid parameters
        with self.assertRaises(AssertionError):
            OsmInterface().process_way_for_distance_calculation(None, None)

        # No way name
        with self.assertRaises(AssertionError):
            OsmInterface().process_way_for_distance_calculation(None, ways.PORTUGAL)

        # Invalid way name
        self.assertEqual(({}, {}), OsmInterface().process_way_for_distance_calculation('Invalid way name', ways.PORTUGAL))

        # No country
        with self.assertRaises(AssertionError):
            OsmInterface().process_way_for_distance_calculation('Autoestrada do Norte', None)

        # Invalid country
        with self.assertRaises(AssertionError):
            OsmInterface().process_way_for_distance_calculation('Autoestrada do Norte', 'Invalid country')

    def test_process_way_for_distance_calculation_successful(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        # This routine can be tested through calls to higher-level routines, with fewer lines of code
        # As such, this test will contain a single test case

        way_name = 'Autoestrada do Norte'  # EN - North freeway/motorway - Portuguese A1
        country = ways.PORTUGAL

        result = OsmInterface().process_way_for_distance_calculation(way_name, country)
        node_list = result[0]
        way_list = result[1]

        self.assertEqual(2, len(result))
        self.assertEqual(5595, len(node_list))  # Number of nodes
        self.assertEqual(851, len(way_list))  # Number of ways

        for node in node_list:
            assert node
        for way in way_list:
            assert way

        node_id = 25398450
        self.assertEqual(39.2031381, node_list.get(node_id).latitude)
        self.assertEqual(-8.7930774, node_list.get(node_id).longitude)
        self.assertEqual(node_id, node_list.get(node_id).node_id)
        self.assertEqual(set(), node_list.get(node_id).surrounding_node_ids)

        way_id = 4246625
        way_node_ids = [25398450, 4080875384, 25398453, 25398456, 25398458, 25398443, 680066405]
        for i in range(7):
            self.assertEqual(way_node_ids[i], way_list.get(way_id).node_list[i].node_id)
        self.assertEqual(way_id, way_list.get(way_id).way_id)

    def test_detect_country_by_coordinates(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        # Invalid parameters

        with self.assertRaises(AssertionError):
            OsmInterface().detect_country_by_coordinates(None)
        self.assertEqual(None, OsmInterface().detect_country_by_coordinates(Coordinates(0, 0)))  # Far from the Iberian Peninsula

        # Successful

        # Portugal
        self.assertEqual(ways.PORTUGAL, OsmInterface().detect_country_by_coordinates(Coordinates(39.0, -9.0)))  # North of Lisbon, far from the border with Spain
        self.assertEqual(ways.PORTUGAL, OsmInterface().detect_country_by_coordinates(Coordinates(39.0, -7.0)))  # Near Badajoz, close to the border with Spain
        self.assertEqual(ways.PORTUGAL, OsmInterface().detect_country_by_coordinates(Coordinates(37.743729, -25.673987)))  # Ponta Delgada, Azores
        self.assertEqual(ways.PORTUGAL, OsmInterface().detect_country_by_coordinates(Coordinates(33.062676, -16.347095)))  # Porto Santo Island, Madeira
        # Spain
        self.assertEqual(ways.SPAIN, OsmInterface().detect_country_by_coordinates(Coordinates(41.0, -4.0)))  # North of Madrid, far from all national borders
        self.assertEqual(ways.SPAIN, OsmInterface().detect_country_by_coordinates(Coordinates(39.0, -6.9)))  # Near Badajoz, close to the border with Portugal
        self.assertEqual(ways.SPAIN, OsmInterface().detect_country_by_coordinates(Coordinates(36.155877, -5.345686)))  # La Línea de la Concepción, close to the border with Gibraltar
        self.assertEqual(ways.SPAIN, OsmInterface().detect_country_by_coordinates(Coordinates(42.354588, 1.456754)))  # La Seu d'Urgell, close to the border with Andorra
        self.assertEqual(ways.SPAIN, OsmInterface().detect_country_by_coordinates(Coordinates(43.341914, -1.780583)))  # Irún, close to the border with France
        self.assertEqual(ways.SPAIN, OsmInterface().detect_country_by_coordinates(Coordinates(35.874293, -5.344738)))  # Ceuta, near Morocco
        self.assertEqual(ways.SPAIN, OsmInterface().detect_country_by_coordinates(Coordinates(35.274848, -2.936755)))  # Melilla, near Morocco
        self.assertEqual(ways.SPAIN, OsmInterface().detect_country_by_coordinates(Coordinates(38.910557, 1.416606)))  # Ibiza, Balearic Islands
        self.assertEqual(ways.CANARY_ISLANDS, OsmInterface().detect_country_by_coordinates(Coordinates(28.459231, -16.257192)))  # Santa Cruz de Tenerife, Canary Islands
        # Andorra
        self.assertEqual(ways.ANDORRA, OsmInterface().detect_country_by_coordinates(Coordinates(42.507051, 1.523456)))  # Andorra-a-Vella
        # Gibraltar
        self.assertEqual(ways.GIBRALTAR, OsmInterface().detect_country_by_coordinates(Coordinates(36.140909, -5.353565)))  # Main Street, Gibraltar

    def test_get_region_extreme_points_invalid_parameters(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        # All invalid parameters
        with self.assertRaises(AssertionError):
            OsmInterface().get_region_extreme_points(None, 0, None)

        # No region name
        with self.assertRaises(AssertionError):
            OsmInterface().get_region_extreme_points(None, osm_interface.PORTUGUESE_DISTRICT, ways.PORTUGAL)

        # Invalid region name
        result = OsmInterface().get_region_extreme_points('Invalid region', osm_interface.PORTUGUESE_DISTRICT, ways.PORTUGAL)
        self.assertEqual(-90.0, result.north.latitude)
        self.assertEqual(90.0, result.south.latitude)
        self.assertEqual(-180.0, result.east.longitude)
        self.assertEqual(180.0, result.west.longitude)

        # Invalid administrative level
        with self.assertRaises(AssertionError):
            OsmInterface().get_region_extreme_points('Lisboa', 0, ways.PORTUGAL)
        with self.assertRaises(AssertionError):
            OsmInterface().get_region_extreme_points('Lisboa', 12, ways.PORTUGAL)

        # No country
        with self.assertRaises(AssertionError):
            OsmInterface().get_region_extreme_points('Lisboa', osm_interface.PORTUGUESE_DISTRICT, None)

        # Invalid country
        with self.assertRaises(AssertionError):
            OsmInterface().get_region_extreme_points('Lisboa', osm_interface.PORTUGUESE_DISTRICT, 'Invalid country')

        # Region name not present in the country
        result = OsmInterface().get_region_extreme_points('Lisboa', osm_interface.PORTUGUESE_DISTRICT, ways.SPAIN)
        self.assertEqual(-90.0, result.north.latitude)
        self.assertEqual(90.0, result.south.latitude)
        self.assertEqual(-180.0, result.east.longitude)
        self.assertEqual(180.0, result.west.longitude)

    def test_get_region_extreme_points_successful(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        # Portugal
        result = OsmInterface().get_region_extreme_points('Portugal', osm_interface.COUNTRY, ways.PORTUGAL)
        self.assertEqual(42.1543112, result.north.latitude)
        self.assertEqual(-8.1987535, result.north.longitude)
        self.assertEqual(32.1995956, result.south.latitude)
        self.assertEqual(-16.4611945, result.south.longitude)
        self.assertEqual(41.5748318, result.east.latitude)
        self.assertEqual(-6.1891593, result.east.longitude)
        self.assertEqual(39.4456383, result.west.latitude)
        self.assertEqual(-31.5575303, result.west.longitude)

        # Portuguese district
        result = OsmInterface().get_region_extreme_points('Lisboa', osm_interface.PORTUGUESE_DISTRICT, ways.PORTUGAL)
        self.assertEqual(39.3177287, result.north.latitude)
        self.assertEqual(-9.2556097, result.north.longitude)
        self.assertEqual(38.6731469, result.south.latitude)
        self.assertEqual(-9.3238243, result.south.longitude)
        self.assertEqual(39.0583871, result.east.latitude)
        self.assertEqual(-8.781861, result.east.longitude)
        self.assertEqual(38.7807094, result.west.latitude)
        self.assertEqual(-9.5005266, result.west.longitude)

        # Portuguese autonomous region (either Azores or Madeira)
        result = OsmInterface().get_region_extreme_points('Açores', osm_interface.AUTONOMOUS_REGION, ways.PORTUGAL)
        self.assertEqual(39.7272503, result.north.latitude)
        self.assertEqual(-31.1129195, result.north.longitude)
        self.assertEqual(36.9276305, result.south.latitude)
        self.assertEqual(-25.0176849, result.south.longitude)
        self.assertEqual(37.2743015, result.east.latitude)
        self.assertEqual(-24.7798488, result.east.longitude)
        self.assertEqual(39.4954319, result.west.latitude)
        self.assertEqual(-31.2756316, result.west.longitude)

        # Portuguese municipality
        result = OsmInterface().get_region_extreme_points('Arruda dos Vinhos', osm_interface.PORTUGUESE_MUNICIPALITY, ways.PORTUGAL)
        self.assertEqual(39.0287911, result.north.latitude)
        self.assertEqual(-9.0933811, result.north.longitude)
        self.assertEqual(38.9214369, result.south.latitude)
        self.assertEqual(-9.1021505, result.south.longitude)
        self.assertEqual(38.97739, result.east.latitude)
        self.assertEqual(-9.0218938, result.east.longitude)
        self.assertEqual(38.9759003, result.west.latitude)
        self.assertEqual(-9.1785273, result.west.longitude)

        # Portuguese parish
        result = OsmInterface().get_region_extreme_points('Alcoutim e Pereiro', osm_interface.PORTUGUESE_PARISH, ways.PORTUGAL)
        self.assertEqual(37.5291307, result.north.latitude)
        self.assertEqual(-7.5741379, result.north.longitude)
        self.assertEqual(37.3689732, result.south.latitude)
        self.assertEqual(-7.4676604, result.south.longitude)
        self.assertEqual(37.3702988, result.east.latitude)
        self.assertEqual(-7.4370819, result.east.longitude)
        self.assertEqual(37.4337991, result.west.latitude)
        self.assertEqual(-7.6486614, result.west.longitude)

        # Spain
        result = OsmInterface().get_region_extreme_points('España', osm_interface.COUNTRY, ways.SPAIN)
        self.assertEqual(43.9933088, result.north.latitude)
        self.assertEqual(-7.6971085, result.north.longitude)
        self.assertEqual(35.2656282, result.south.latitude)
        self.assertEqual(-2.9505435, result.south.longitude)
        self.assertEqual(39.8782416, result.east.latitude)
        self.assertEqual(4.5918885, result.east.longitude)
        self.assertEqual(43.0458933, result.west.latitude)
        self.assertEqual(-9.5754539, result.west.longitude)

        # Spanish autonomous community
        result = OsmInterface().get_region_extreme_points('Andalucía', osm_interface.AUTONOMOUS_COMMUNITY, ways.SPAIN)
        self.assertEqual(38.7290874, result.north.latitude)
        self.assertEqual(-5.0469484, result.north.longitude)
        self.assertEqual(35.9376398, result.south.latitude)
        self.assertEqual(-3.0352337, result.south.longitude)
        self.assertEqual(37.3755316, result.east.latitude)
        self.assertEqual(-1.6298, result.east.longitude)
        self.assertEqual(37.5549122, result.west.latitude)
        self.assertEqual(-7.5226854, result.west.longitude)

        # Canary Islands
        result = OsmInterface().get_region_extreme_points('Canarias', osm_interface.AUTONOMOUS_COMMUNITY, ways.CANARY_ISLANDS)
        self.assertEqual(29.4160647, result.north.latitude)
        self.assertEqual(-13.5057679, result.north.longitude)
        self.assertEqual(27.6377389, result.south.latitude)
        self.assertEqual(-17.9867651, result.south.longitude)
        self.assertEqual(29.27778, result.east.latitude)
        self.assertEqual(-13.3320145, result.east.longitude)
        self.assertEqual(27.7188457, result.west.latitude)
        self.assertEqual(-18.1611809, result.west.longitude)

        # Spanish province
        result = OsmInterface().get_region_extreme_points('Cáceres', osm_interface.PROVINCE, ways.SPAIN)
        self.assertEqual(40.4866514, result.north.latitude)
        self.assertEqual(-6.2312683, result.north.longitude)
        self.assertEqual(39.0315802, result.south.latitude)
        self.assertEqual(-6.1420985, result.south.longitude)
        self.assertEqual(39.3949928, result.east.latitude)
        self.assertEqual(-4.9525129, result.east.longitude)
        self.assertEqual(39.6636796, result.west.latitude)
        self.assertEqual(-7.5416802, result.west.longitude)

        # Spanish comarca
        result = OsmInterface().get_region_extreme_points('Costa Occidental', osm_interface.COMARCA, ways.SPAIN)
        self.assertEqual(37.4136052, result.north.latitude)
        self.assertEqual(-7.4083091, result.north.longitude)
        self.assertEqual(37.1661936, result.south.latitude)
        self.assertEqual(-7.3948663, result.south.longitude)
        self.assertEqual(37.2083792, result.east.latitude)
        self.assertEqual(-7.0517745, result.east.longitude)
        self.assertEqual(37.402284, result.west.latitude)
        self.assertEqual(-7.4511209, result.west.longitude)

        # Spanish municipality
        result = OsmInterface().get_region_extreme_points('Madrid', osm_interface.SPANISH_MUNICIPALITY, ways.SPAIN)
        self.assertEqual(40.6437293, result.north.latitude)
        self.assertEqual(-3.6542196, result.north.longitude)
        self.assertEqual(40.3119774, result.south.latitude)
        self.assertEqual(-3.5986952, result.south.longitude)
        self.assertEqual(40.40265, result.east.latitude)
        self.assertEqual(-3.5179163, result.east.longitude)
        self.assertEqual(40.5708516, result.west.latitude)
        self.assertEqual(-3.8889539, result.west.longitude)

        # Spanish district
        result = OsmInterface().get_region_extreme_points('Barajas', osm_interface.SPANISH_DISTRICT, ways.SPAIN)
        self.assertEqual(40.5123682, result.north.latitude)
        self.assertEqual(-3.5721062, result.north.longitude)
        self.assertEqual(40.4464812, result.south.latitude)
        self.assertEqual(-3.5354915, result.south.longitude)
        self.assertEqual(40.4677375, result.east.latitude)
        self.assertEqual(-3.5250873, result.east.longitude)
        self.assertEqual(40.4684978, result.west.latitude)
        self.assertEqual(-3.6279521, result.west.longitude)

        # Andorra
        result = OsmInterface().get_region_extreme_points('Andorra', osm_interface.COUNTRY, ways.ANDORRA)
        self.assertEqual(42.6559357, result.north.latitude)
        self.assertEqual(1.5492987, result.north.longitude)
        self.assertEqual(42.4288238, result.south.latitude)
        self.assertEqual(1.5157512, result.south.longitude)
        self.assertEqual(42.5741828, result.east.latitude)
        self.assertEqual(1.786664, result.east.longitude)
        self.assertEqual(42.4951007, result.west.latitude)
        self.assertEqual(1.407225, result.west.longitude)

        # Andorran parish
        result = OsmInterface().get_region_extreme_points('Escaldes-Engordany', osm_interface.ANDORRAN_PARISH, ways.ANDORRA)
        self.assertEqual(42.5237965, result.north.latitude)
        self.assertEqual(1.5460477, result.north.longitude)
        self.assertEqual(42.449886, result.south.latitude)
        self.assertEqual(1.5788543, result.south.longitude)
        self.assertEqual(42.4815295, result.east.latitude)
        self.assertEqual(1.6632892, result.east.longitude)
        self.assertEqual(42.5228745, result.west.latitude)
        self.assertEqual(1.5215643, result.west.longitude)

        # Gibraltar
        result = OsmInterface().get_region_extreme_points('Gibraltar', osm_interface.COUNTRY, ways.GIBRALTAR)
        self.assertEqual(36.1550376, result.north.latitude)
        self.assertEqual(-5.3453466, result.north.longitude)
        self.assertEqual(36.058755, result.south.latitude)
        self.assertEqual(-5.347109, result.south.longitude)
        self.assertEqual(36.1420809, result.east.latitude)
        self.assertEqual(-5.2766611, result.east.longitude)
        self.assertEqual(36.1483668, result.west.latitude)
        self.assertEqual(-5.4006553, result.west.longitude)

    def test_query_server_invalid_parameters(self):
        # All invalid parameters
        with self.assertRaises(AssertionError):
            OsmInterface()._query_server('', '')

        # Invalid query
        with self.assertRaises(AssertionError):
            OsmInterface()._query_server('', ways.PORTUGAL)

        # Invalid country
        with self.assertRaises(AssertionError):
            OsmInterface()._query_server('A query', '')  # While 'query' parameter is not a valid query, it will pass the assert
        with self.assertRaises(AssertionError):
            OsmInterface()._query_server('A query', 'Invalid country')

    def test_query_server_successful(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        sample_query = f'is_in(39.0,-5.0); out geom;'  # Returns administrative divisions of location (39.0, -5.0), in Spanish Extremadura
        sample_raw_response_start = '<osm version="0.6" generator="Overpass API 0.7.57.1 74a55df1">\n'
        sample_raw_response_excerpt = '<tag k="admin_level" v="8"/>\n'
        sample_raw_response_end = '</osm>'

        result: minidom.Element = OsmInterface()._query_server(sample_query, ways.SPAIN)
        self.assertTrue(result.toxml().startswith(sample_raw_response_start))
        self.assertTrue(sample_raw_response_excerpt in result.toxml())
        self.assertTrue(result.toxml().endswith(sample_raw_response_end))
        self.assertEqual(62, result.toxml().find('\n'))  # Number of lines

    def test_parse_xml_response_invalid_parameters(self):
        self.assertIsNone(OsmInterface()._parse_raw_response(None))
        self.assertIsNone(OsmInterface()._parse_raw_response(''))

    def test_parse_xml_response_successful(self):
        xml_string = '<xml><value>A Value</value><another_value>Another Value</another_value></xml>'
        xml_object: minidom.Element = OsmInterface()._parse_raw_response(xml_string)
        self.assertEqual('value', xml_object.childNodes[0].nodeName)
        self.assertEqual('another_value', xml_object.childNodes[1].nodeName)
        self.assertEqual('A Value', xml_object.childNodes[0].childNodes[0].data)
        self.assertEqual('Another Value', xml_object.childNodes[1].childNodes[0].data)

        # Remaining tests will call routine _parse_raw_response() with more complex data - If they pass, routine is working properly

    def test_get_server_url_invalid_parameters(self):
        self.assertIsNone(OsmInterface()._get_server_url(None))
        self.assertIsNone(OsmInterface()._get_server_url(''))
        self.assertIsNone(OsmInterface()._get_server_url('Invalid country'))

    def test_get_server_url_successful(self):
        self.assertEqual('http://127.0.0.1:12347/api/interpreter', OsmInterface()._get_server_url(ways.ANDORRA))
        self.assertEqual('http://127.0.0.1:12345/api/interpreter', OsmInterface()._get_server_url(ways.GIBRALTAR))
        self.assertEqual('http://127.0.0.1:12346/api/interpreter', OsmInterface()._get_server_url(ways.PORTUGAL))
        self.assertEqual('http://127.0.0.1:12345/api/interpreter', OsmInterface()._get_server_url(ways.SPAIN))
        self.assertEqual('http://127.0.0.1:12348/api/interpreter', OsmInterface()._get_server_url(ways.CANARY_ISLANDS))
