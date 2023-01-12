import unittest
from xml.dom import minidom

from travel.support.osm_interface import OsmInterface
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
