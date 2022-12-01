import unittest
from xml.dom import minidom

from travel.support.osm_interface import OsmInterface
from travel.support import ways
from test.travel.support import test_fail_if_servers_down


class TestOsmInterface(unittest.TestCase):

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
