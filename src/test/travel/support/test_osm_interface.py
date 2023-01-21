import unittest
from xml.dom import minidom

from travel.support.osm_interface import OsmInterface
from travel.support.osm_interface import DETAIL_LEVEL_URBAN, DETAIL_LEVEL_INTERCITY
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
            'região': 'Área Metropolitana de Lisboa',
            'sub-região': 'Grande Lisboa',
            'timezone': 'Europe/Lisbon Timezone'
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
            'timezone': 'Europe/Lisbon Timezone'
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
            4: 'Extremadura',
            6: 'Badajoz',
            8: 'Mérida'
        }
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(39.0, -6.5), None))
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(39.0, -6.5), ways.SPAIN))

        # Spain, far from all borders, with comarca and district info known
        expected_response = {
            4: 'Provincia Eclesiástica de Madrid',
            6: 'Archidiócesis de Madrid',
            7: 'Área metropolitana de Madrid y Corredor del Henares',
            8: 'Madrid',
            9: 'Moncloa-Aravaca',
            10: 'Ciudad Universitaria'
        }
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(40.45, -3.75), None))
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(40.45, -3.75), ways.SPAIN))

        # Spain, close from Gibraltar border
        expected_response = {
            4: 'Andalucía',
            6: 'Cádiz',
            7: 'Campo de Gibraltar',
            8: 'La Línea de la Concepción'
        }
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(36.168023, -5.350738), None))
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(36.168023, -5.350738), ways.SPAIN))

        # Spain, close from Andorran border
        expected_response = {
            4: 'Catalunya',
            6: 'Lleida',
            7: 'Alt Urgell',
            8: "la Seu d'Urgell",
            'political': 'Català com a llengua pròpia a Catalunya',
            'political_fraction': 'Alt Pirineu i Aran (Lleida)'
        }
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(42.358877, 1.456251), None))
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(42.358877, 1.456251), ways.SPAIN))

        # Spain, close from French border
        expected_response = {
            4: 'Euskadi',
            6: 'Gipuzkoa',
            7: 'Bidasoa Beherea / Bajo Bidasoa',
            8: 'Hondarribia/Fontarrabie'
        }
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(43.369574, -1.796590), None))
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(43.369574, -1.796590), ways.SPAIN))

        # Ceuta, Spain, close from Moroccan border
        expected_response = {
            4: 'Ceuta',
            8: 'Ceuta'
        }
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(35.888740, -5.320993), None))
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(35.888740, -5.320993), ways.SPAIN))

        # Melilla, Spain, close from Moroccan border
        expected_response = {
            4: 'Melilla',
            8: 'Melilla'
        }
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(35.287817, -2.947612), None))
        self.assertEqual(expected_response, OsmInterface().get_administrative_divisions_by_coordinates(Coordinates(35.287817, -2.947612), ways.SPAIN))

        # Spanish Balearic Islands
        expected_response = {
            4: 'Illes Balears',
            6: 'Illes Balears',
            7: 'Menorca',
            8: 'Maó'
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

        # Large Portuguese freeway
        expected_response_keys = [
            '1', '10', '10A', '11', '12', '13', '14', '15', '16', '17', '18', '18A', '18B', '19', '19A', '1A', '2', '22',
            '23', '2A', '3', '3A', '4', '5', '5A', '6', '6 A', '6A', '7', '8', '9'
        ]
        response: dict[str, list[Coordinates]] = OsmInterface().get_road_exits(ways.PT_A1.osm_name, ways.PORTUGAL)

        self.assertEqual(expected_response_keys, list(response.keys()))
        for key in expected_response_keys:
            self.assertTrue((len(response[key]) > 0))
        self.assertEqual([Coordinates(38.7936469, -9.1126855), Coordinates(38.7844696, -9.1208711)], response['1'])
        self.assertEqual([Coordinates(41.0061416, -8.5822318), Coordinates(41.0793433, -8.5817397),
                          Coordinates(41.0725807, -8.5810286), Coordinates(41.0667503, -8.5815289)], response['19'])
        self.assertEqual([Coordinates(39.7417361, -8.7432394), Coordinates(39.7395957, -8.7364531)], response['9'])

        # Small Portuguese freeway
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

        # Portuguese road without exit numbers
        response: dict[str, list[Coordinates]] = OsmInterface().get_road_exits(ways.PT_IC27.osm_name, ways.PORTUGAL)
        self.assertEqual({}, response)

        # Large Spanish freeway
        expected_response_keys = [
            '1', '103', '104', '105', '110A', '110B', '110b', '112', '1123', '1129', '1131', '1138', '113b', '1143',
            '1146', '1148', '115', '1151', '1152', '1153', '1154', '1155', '1156', '1158', '116', '1160', '1160A',
            '1160B', '1161', '1162', '1163', '1164', '1168', '117', '118', '119', '124', '127', '133', '135', '136',
            '138', '153', '155', '157', '160', '170', '172', '175', '176', '181A', '181B', '182', '183', '184', '185',
            '186', '187', '188', '192', '196', '197', '198', '201', '205', '206', '208', '209', '210', '212', '213',
            '214', '217', '222', '223', '225', '226', '230', '232', '233', '234', '235', '236', '237', '238', '240',
            '241', '242', '243', '244', '245', '246', '246-A', '246-B', '251', '254', '256', '258', '265', '272', '274',
            '276', '277', '278', '279', '282', '283', '285', '287A', '287B', '289', '292', '293', '295', '297', '305',
            '307', '311', '313', '314', '315', '321', '322', '324', '325', '326', '328', '329', '331', '335', '336',
            '339', '341', '342', '344', '346', '351', '354', '355', '356', '357', '358', '359', '361', '363', '366',
            '367', '369', '371', '373', '375', '376', '379', '381', '383', '384', '385', '386', '389', '391', '394',
            '395', '396', '398', '400', '402', '403', '404', '406', '409', '410', '411', '413', '414', '415', '416',
            '418', '419', '420', '422', '423', '424', '425', '429', '430', '431', '432', '435', '436', '438', '441',
            '442', '443', '446', '448', '449', '452', '453', '456', '459', '460', '464', '467', '468', '469', '471',
            '475', '479', '481', '482', '487', '489', '491', '494', '50', '504', '50A', '51', '510', '513', '514',
            '516', '518', '520', '523', '525', '526', '528', '529', '534', '534a', '534b', '535', '537', '538', '541',
            '543', '545', '547', '549', '553', '555', '559', '559A', '559B', '563', '565', '567 AB', '570', '571',
            '575', '578 A', '578 AB', '578 B', '578 BA', '581', '584', '585', '586', '588', '589', '591', '594', '596',
            '598', '6', '601', '609', '611', '616', '618', '622', '623', '628', '630', '633', '636', '640', '642',
            '644', '645', '646', '649', '651', '655', '7'
        ]
        response: dict[str, list[Coordinates]] = OsmInterface().get_road_exits(ways.ES_A7.osm_name, ways.SPAIN)

        self.assertEqual(expected_response_keys, list(response.keys()))
        for key in expected_response_keys:
            self.assertTrue((len(response[key]) > 0))
        self.assertEqual([Coordinates(39.8955497, -0.1970601), Coordinates(39.8971608, -0.1970829)], response['1'])
        self.assertEqual([Coordinates(36.7741554, -3.5724422), Coordinates(36.7733459, -3.5811174)], response['322'])
        self.assertEqual([Coordinates(36.7023358, -4.4576572)], response['7'])

        # Small Spanish freeway
        expected_response_keys = ['0A', '1', '10', '11', '12', '12B', '12C', '13', '16', '17', '19', '2', '20', '20A',
                                  '20B', '23', '23A', '23B', '24', '25', '26', '27', '28', '2A', '2B', '2C', '3',
                                  '3-4-5', '30', '31', '31B', '3BA', '4', '5', '5A', '5AB', '6', '6A', '6B', '7-6',
                                  '7-8-9', '7A', '7B', '7BA', '8', '8A', '9A', '9B'
                                  ]
        response: dict[str, list[Coordinates]] = OsmInterface().get_road_exits(ways.ES_M30.osm_name, ways.SPAIN)

        self.assertEqual(expected_response_keys, list(response.keys()))
        for key in expected_response_keys:
            self.assertTrue((len(response[key]) > 0))
        self.assertEqual([Coordinates(40.4813264, -3.673715)], response['0A'])
        self.assertEqual([Coordinates(40.4638637, -3.6665504)], response['2C'])
        self.assertEqual([Coordinates(40.4028638, -3.6664435)], response['9B'])

        # Spanish road without exit numbers
        response: dict[str, list[Coordinates]] = OsmInterface().get_road_exits(ways.ES_A483.osm_name, ways.PORTUGAL)
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
            'Braço de Prata', 'Ovar', 'Avanca', 'Vale de Santarém', 'Mato de Miranda', 'Passagem de Nível da Adémia',
            'Litém', 'Riachos', 'Entroncamento', 'Lamarosa', 'Setil', 'Santarém', 'Reguengo-Vale da Pedra-Pontével',
            'Vale de Figueira', 'Virtudes', 'Santana-Cartaxo', 'Moscavide', 'Sacavém', 'Bobadela', 'Alverca',
            'Carvalheira-Maceda', 'Espadanal da Azambuja', 'Miramar', 'Espinho', 'Silvalde', 'Bencanta', 'Espadaneira',
            'Esmoriz', 'Paramos', 'Coimbrões', 'Vila Nova de Gaia', 'Madalena', 'Valadares', 'Aguda', 'Francelos',
            'Cortegaça', 'Granja', 'Válega', 'Estarreja', 'Cacia', 'Canelas', 'Salreu', 'Aveiro', 'Oiã',
            'Oliveira do Bairro', 'Paraimo-Sangalhos', 'Quintãs', 'Aguim', 'Curia', 'Mealhada', 'Mogofores',
            'Pampilhosa', 'Souselas', 'Adémia', 'Coimbra-B', 'Vilela-Fornos', 'Alfarelos - Granja do Ulmeiro', 'Amial',
            'Casais', 'Taveiro', 'Formoselha', 'Pereira', 'Vila Pouca do Campo', 'Pelariga', 'Pombal', 'Simões',
            'Soure', 'Vila Nova de Anços', 'Albergaria dos Doze', 'Caxarias', 'Vermoil', 'Chão de Maçãs-Fátima',
            'Fungalvaz', 'Paialvo', 'Seiça-Ourém', 'Bifurcação Norte-Setil', 'Azambuja', 'Vila Nova da Rainha',
            'Carregado', 'Castanheira do Ribatejo', 'Vila Franca de Xira', 'Alhandra', 'Quinta das Torres',
            'General Torres', 'Gare do Oriente', 'Póvoa', 'Santa Iria', 'Porto - Campanhã', 'Lisboa Santa Apolónia'
        ]
        response: dict[str, list[Coordinates]] = OsmInterface().get_railway_stations(ways.PT_NORTH_LINE.osm_name, ways.PORTUGAL)

        self.assertEqual(expected_response_keys, list(response.keys()))
        for key in expected_response_keys:
            self.assertTrue((len(response[key]) > 0))
        self.assertEqual([Coordinates(38.7478486, -9.1024336), Coordinates(38.7461963, -9.1030306)], response['Braço de Prata'])
        self.assertEqual([Coordinates(40.5910309, -8.612713), Coordinates(40.5910442, -8.6126654)], response['Quintãs'])
        self.assertEqual([Coordinates(38.7137802, -9.1229108), Coordinates(38.7138279, -9.1230008)], response['Lisboa Santa Apolónia'])

        # Small Portuguese railway
        expected_response_keys = [
            'Algueirão/Mem Martins', 'Amadora', 'Campolide', 'Santa Cruz - Damaia', 'Queluz/Belas', 'Monte Abraão',
            'Massamá-Barcarena', 'Agualva - Cacém', 'Rio de Mouro', 'Portela de Sintra', 'Mercês', 'Sintra', 'Rossio',
            'Benfica', 'Reboleira'
        ]
        response: dict[str, list[Coordinates]] = OsmInterface().get_railway_stations(ways.PT_SINTRA_LINE.osm_name, ways.PORTUGAL)

        self.assertEqual(expected_response_keys, list(response.keys()))
        for key in expected_response_keys:
            self.assertTrue((len(response[key]) > 0))
        self.assertEqual([Coordinates(38.7978927, -9.3399843), Coordinates(38.7975035, -9.3422101)], response['Algueirão/Mem Martins'])
        self.assertEqual([Coordinates(38.7845691, -9.3221058), Coordinates(38.7839253, -9.3197594)], response['Rio de Mouro'])
        self.assertEqual([Coordinates(38.7506398, -9.2215502), Coordinates(38.750677, -9.2215338),
                          Coordinates(38.7511027, -9.2239415), Coordinates(38.7511335, -9.2239302)], response['Reboleira'])

        # Large Spanish railway
        expected_response_keys = [
            'Garrovilla-Las Vegas', 'Cabeza Del Buey', 'Almadenejos-Almaden', 'Guadalmez-Los Pedroches', 'Villagonzalo'
        ]
        response: dict[str, list[Coordinates]] = OsmInterface().get_railway_stations(ways.ES_CIUDAD_REAL_BADAJOZ.osm_name, ways.SPAIN)

        self.assertEqual(expected_response_keys, list(response.keys()))
        for key in expected_response_keys:
            self.assertTrue((len(response[key]) > 0))
        self.assertEqual([Coordinates(38.9154013, -6.4772448)], response['Garrovilla-Las Vegas'])
        self.assertEqual([Coordinates(38.7404341, -4.7303171)], response['Almadenejos-Almaden'])
        self.assertEqual([Coordinates(38.8641393, -6.2075556)], response['Villagonzalo'])

        # Small Spanish railway
        expected_response_keys = [
            'Colombia', 'Aeropuerto T4', 'Barajas', 'Feria de Madrid', 'Aeropuerto T1-T2-T3', 'Mar de Cristal',
            'Pinar del Rey', 'Nuevos Ministerios'
        ]
        response: dict[str, list[Coordinates]] = OsmInterface().get_railway_stations(ways.ES_MADRID_METRO_LINE_8.osm_name, ways.SPAIN)

        self.assertEqual(expected_response_keys, list(response.keys()))
        for key in expected_response_keys:
            self.assertTrue((len(response[key]) > 0))
        self.assertEqual([Coordinates(40.4571282, -3.67706)], response['Colombia'])
        self.assertEqual([Coordinates(40.4678852, -3.5718088)], response['Aeropuerto T1-T2-T3'])
        self.assertEqual([Coordinates(40.4454819, -3.6915827)], response['Nuevos Ministerios'])

        # Neither Andorra nor Gibraltar have railways

    def test_process_area_for_distance_calculation_invalid_parameters(self):
        test_fail_if_servers_down.TestFailIfServersDown().test_fail_if_servers_down()  # Will fail this test if OSM servers are down

        valid_coordinate_list = [Coordinates(1, 1), Coordinates(-1, -1)]

        # All invalid parameters
        with self.assertRaises(AssertionError):
            OsmInterface().process_area_for_distance_calculation([], None, 0, None)

        # Empty coordinate list
        with self.assertRaises(AssertionError):
            OsmInterface().process_area_for_distance_calculation([], ways.ROAD, DETAIL_LEVEL_URBAN, ways.PORTUGAL)

        # No way type
        with self.assertRaises(AssertionError):
            OsmInterface().process_area_for_distance_calculation(valid_coordinate_list, None, DETAIL_LEVEL_URBAN, ways.PORTUGAL)

        # Invalid way type
        with self.assertRaises(AssertionError):
            OsmInterface().process_area_for_distance_calculation(valid_coordinate_list, 'Invalid way type', DETAIL_LEVEL_URBAN, ways.PORTUGAL)

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
        detail = DETAIL_LEVEL_INTERCITY
        country = ways.PORTUGAL

        result = OsmInterface().process_area_for_distance_calculation(coordinate_list, way_type, detail, country)
        node_list = result[0]
        way_list = result[1]
        extreme_points = result[2]

        self.assertEqual(3, len(result))
        self.assertEqual(29190, len(node_list))  # Number of nodes
        self.assertEqual(3464, len(way_list))  # Number of ways

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
        self.assertEqual(5504, len(node_list))  # Number of nodes
        self.assertEqual(770, len(way_list))  # Number of ways

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
        sample_raw_response = f'<?xml version="1.0" encoding="UTF-8"?>\n' \
                              f'<osm version="0.6" generator="Overpass API 0.7.57.1 74a55df1">\n' \
                              f'<note>The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.</note>\n' \
                              f'<meta osm_base="2022-03-22T21:20:37Z" areas="2022-03-22T21:20:37Z"/>\n\n' \
                              f'  <area id="3600340004">\n' \
                              f'    <tag k="admin_level" v="8"/>\n' \
                              f'    <tag k="boundary" v="administrative"/>\n' \
                              f'    <tag k="idee:name" v="Siruela"/>\n' \
                              f'    <tag k="ine:municipio" v="06125"/>\n' \
                              f'    <tag k="name" v="Siruela"/>\n' \
                              f'    <tag k="population" v="2199"/>\n' \
                              f'    <tag k="population:date" v="2009"/>\n' \
                              f'    <tag k="source" v="BDLL25, EGRN, Instituto Geográfico Nacional"/>\n' \
                              f'    <tag k="type" v="boundary"/>\n' \
                              f'    <tag k="wikidata" v="Q1372816"/>\n' \
                              f'    <tag k="wikipedia" v="es:Siruela"/>\n' \
                              f'  </area>\n' \
                              f'  <area id="3600348994">\n' \
                              f'    <tag k="ISO3166-2" v="ES-BA"/>\n' \
                              f'    <tag k="admin_level" v="6"/>\n' \
                              f'    <tag k="alt_name:ar" v="باداخوز"/>\n' \
                              f'    <tag k="boundary" v="administrative"/>\n' \
                              f'    <tag k="ine:provincia" v="06"/>\n' \
                              f'    <tag k="name" v="Badajoz"/>\n' \
                              f'    <tag k="name:ar" v="بطليوس"/>\n' \
                              f'    <tag k="name:ast" v="Badaxoz"/>\n' \
                              f'    <tag k="name:be" v="Бадахас"/>\n' \
                              f'    <tag k="name:ca" v="Badajoz"/>\n' \
                              f'    <tag k="name:de" v="Badajoz"/>\n' \
                              f'    <tag k="name:el" v="Μπαδαχόθ"/>\n' \
                              f'    <tag k="name:en" v="Badajoz"/>\n' \
                              f'    <tag k="name:eo" v="Badaĥozo"/>\n' \
                              f'    <tag k="name:es" v="Badajoz"/>\n' \
                              f'    <tag k="name:eu" v="Badajoz"/>\n' \
                              f'    <tag k="name:ext" v="Baajós"/>\n' \
                              f'    <tag k="name:fa" v="باداخوس"/>\n' \
                              f'    <tag k="name:fr" v="Badajoz"/>\n' \
                              f'    <tag k="name:gl" v="Badaxoz"/>\n' \
                              f'    <tag k="name:ja" v="バダホス"/>\n' \
                              f'    <tag k="name:ko" v="바다호스"/>\n' \
                              f'    <tag k="name:pt" v="Badajoz"/>\n' \
                              f'    <tag k="name:ru" v="Бадахос"/>\n' \
                              f'    <tag k="name:sr" v="Бадахоз"/>\n' \
                              f'    <tag k="name:uk" v="Бадахос"/>\n' \
                              f'    <tag k="name:ur" v="بطليوس"/>\n' \
                              f'    <tag k="name:zh" v="巴達霍斯"/>\n' \
                              f'    <tag k="official_name:be" v="Правінцыя Бадахас"/>\n' \
                              f'    <tag k="ref:nuts" v="ES431"/>\n' \
                              f'    <tag k="ref:nuts:3" v="ES431"/>\n' \
                              f'    <tag k="source" v="BDLL25, EGRN, Instituto Geográfico Nacional"/>\n' \
                              f'    <tag k="type" v="boundary"/>\n' \
                              f'    <tag k="wikidata" v="Q81803"/>\n' \
                              f'    <tag k="wikipedia" v="es:Provincia de Badajoz"/>\n' \
                              f'  </area>\n' \
                              f'  <area id="3600349050">\n' \
                              f'    <tag k="ISO3166-2" v="ES-EX"/>\n' \
                              f'    <tag k="admin_level" v="4"/>\n' \
                              f'    <tag k="border_type" v="region"/>\n' \
                              f'    <tag k="boundary" v="administrative"/>\n' \
                              f'    <tag k="ine:ccaa" v="11"/>\n' \
                              f'    <tag k="name" v="Extremadura"/>\n' \
                              f'    <tag k="name:ar" v="إكستريمادورا"/>\n' \
                              f'    <tag k="name:ast" v="Estremadura"/>\n' \
                              f'    <tag k="name:be" v="Эстрэмадура"/>\n' \
                              f'    <tag k="name:ca" v="Extremadura"/>\n' \
                              f'    <tag k="name:cs" v="Extremadura"/>\n' \
                              f'    <tag k="name:el" v="Εξτρεμαδούρα"/>\n' \
                              f'    <tag k="name:en" v="Extremadura"/>\n' \
                              f'    <tag k="name:es" v="Extremadura"/>\n' \
                              f'    <tag k="name:eu" v="Extremadura"/>\n' \
                              f'    <tag k="name:ext" v="Estremaúra"/>\n' \
                              f'    <tag k="name:fr" v="Estrémadure"/>\n' \
                              f'    <tag k="name:hu" v="Extremadura"/>\n' \
                              f'    <tag k="name:ja" v="エストレマドゥーラ州"/>\n' \
                              f'    <tag k="name:pl" v="Estremadura"/>\n' \
                              f'    <tag k="name:pt" v="Estremadura"/>\n' \
                              f'    <tag k="name:ru" v="Эстремадура"/>\n' \
                              f'    <tag k="name:sk" v="Extremadura"/>\n' \
                              f'    <tag k="official_name" v="Extremadura"/>\n' \
                              f'    <tag k="ref:nuts" v="ES43"/>\n' \
                              f'    <tag k="ref:nuts:2" v="ES43"/>\n' \
                              f'    <tag k="source" v="BDLL25, EGRN, Instituto Geográfico Nacional"/>\n' \
                              f'    <tag k="type" v="boundary"/>\n' \
                              f'    <tag k="wikidata" v="Q5777"/>\n' \
                              f'    <tag k="wikipedia" v="es:Extremadura"/>\n' \
                              f'  </area>\n\n' \
                              f'</osm>\n'

        result: minidom.Element = OsmInterface()._query_server(sample_query, ways.SPAIN)
        expected_result: minidom.Element = minidom.parseString(sample_raw_response).childNodes[0]
        self.assertEqual(expected_result.toxml(), result.toxml())  # Directly comparing the objects will return False, even if source XML is the same

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
