from typing import Optional, Union
import requests
from xml.dom import minidom

from travel.support import ways
from travel.support.coordinate import Coordinate

"""
Interface to OpenStreetMap API
Machines running instances of OSM can be Dockers running locally
"""

# Servers
DOCKER_IP = '127.0.0.1'  # Localhost
PORT_GIBRALTAR_SPAIN = 12345  # Same Docker instance contains maps of Spain and Gibraltar
PORT_PORTUGAL = 12346
PORT_ANDORRA = 12347

##############################
# OpenStreetMap administrative levels

# General
COUNTRY = 2  # Applies to countries. Gibraltar and its waters are covered by a level-2 relation as well

# Andorra
ANDORRAN_PARISH = 7  # In Catalan, "parròquia"

# Spain
AUTONOMOUS_COMMUNITY = 4
PROVINCE = 6
COMARCA = 7
SPANISH_MUNICIPALITY = 8  # In Spanish, "municipio"
SPANISH_DISTRICT = 9  # In Spanish, "distrito"

# Gibraltar
GIBRALTAR_ADMIN_LEVEL = 4  # Covers the territory of Gibraltar. The sum of Gibraltar territory and waters is covered by a level-2 relation

# Portugal
AUTONOMOUS_REGION = 4  # Azores and Madeira
PORTUGUESE_DISTRICT = 6  # In Portuguese, "distrito", same as in Spanish
PORTUGUESE_MUNICIPALITY = 7  # In Portuguese, "concelho"
PORTUGUESE_PARISH = 8  # In Portuguese, "freguesia"
PORTUGUESE_HISTORIC_PARISH = 'historic_parish'  # Former Portuguese parishes (pre-2013), in the past were associated with level 9
##############################

# Detail levels allow to balance between the accuracy of the results and the time spent calculating them
DETAIL_LEVEL_INTERCITY = 1
DETAIL_LEVEL_URBAN = 2

DISTANCE_RECTANGLE_MARGIN = 0.1  # Degrees. 1 degree = Very approximately 100 km in the Iberian Peninsula

# Some or all of the most relevant road and path types are expected to be present below
# Reference: https://wiki.openstreetmap.org/wiki/Key:highway
TAGS_DETAIL_LEVEL_INTERCITY = [
    'motorway', 'trunk', 'primary', 'secondary', 'motorway_link', 'trunk_link', 'primary_link', 'secondary_link',
    'motorway_junction',
]
TAGS_DETAIL_LEVEL_URBAN = TAGS_DETAIL_LEVEL_INTERCITY + [
    'tertiary', 'unclassified', 'residential', 'tertiary_link', 'living_street', 'service',
]
TAGS_DESIRED_ROADS = {
    DETAIL_LEVEL_INTERCITY: TAGS_DETAIL_LEVEL_INTERCITY,
    DETAIL_LEVEL_URBAN: TAGS_DETAIL_LEVEL_URBAN,
}


class ExtremePoints:
    """
    Data access object to store the extreme points of a region
    """
    def __init__(self, name: str, admin_level: int, country: str,
                 north: Coordinate, south: Coordinate, east: Coordinate, west: Coordinate):
        assert name
        assert admin_level >= COUNTRY
        assert country in ways.ALL_SUPPORTED_COUNTRIES
        assert north
        assert south
        assert east
        assert west
        assert len({north, south, east, west}) == 4  # No coordinates should be repeated

        self.name: str = name
        self.admin_level: int = admin_level
        self.country: str = country
        self.north: Coordinate = north
        self.south: Coordinate = south
        self.east: Coordinate = east
        self.west: Coordinate = west

    def __str__(self):
        return f'Name: {self.name}\n' \
               f'Administrative level: {self.admin_level}\n' \
               f'Country: {self.country}\n' \
               f'North: {self.north}\n' \
               f'South: {self.south}\n' \
               f'East: {self.east}\n' \
               f'West: {self.west}'


class OsmNode:
    """
    Data access object to store the data of an OSM node
    """
    def __init__(self, node_id: int, latitude: float, longitude: float):
        assert node_id >= 0  # Node ID == 0 - Default node ID, used in distance calculation
        assert -90 <= latitude <= 90
        assert -180 <= longitude <= 180

        self.node_id: int = node_id
        self.latitude: float = float(latitude)
        self.longitude: float = float(longitude)
        self.surrounding_node_ids: set[int] = set()  # Contains IDs of nodes that are next to this node in ways and relations


class OsmWay:
    """
    Data access object to store the data of an OSM way
    """
    def __init__(self, way_id: int, node_list: list[OsmNode]):
        assert way_id > 0
        assert node_list

        self.way_id: int = way_id
        self.node_list: list[OsmNode] = node_list


class OsmInterface:

    @staticmethod
    def test_connections() -> bool:
        """
        Returns True if connection could be established with all OSM servers, False otherwise
        """
        try:
            for country in ways.ALL_SUPPORTED_COUNTRIES:
                server_url: str = OsmInterface._get_server_url(country)
                query: str = "out;"  # Simplest query - Just to check if server replies

                raw_response: str = requests.get(f'{server_url}?{query}').content.decode()  # Will raise ConnectionError if server is down
                xml_elem: minidom.Element = OsmInterface._parse_raw_response(raw_response)
                if xml_elem.tagName == 'osm':
                    continue  # Success - Check next server URL
                else:
                    return False  # Server down
        except requests.exceptions.ConnectionError:
            print(f'At least one OSM server is down')
            return False
        except Exception as e:
            print("An exception occurred while checking if OSM servers are running")
            print(e.args)
            return False

        return True

    @staticmethod
    def obter_divisoes_administrativas_de_ponto(coordenadas: Coordinate, pais: str = None) -> dict[Union[str, int], str]:
        """
        A maior parte das divisões administrativas encontradas terão um número como identificador (entre 1 e 11), mas
            também poderão ter uma string como identificador (ex: historic_parish - Antiga freguesia portuguesa)
        """
        query = f'is_in({coordenadas.latitude},{coordenadas.longitude}); out geom;'
        if not pais:
            pais: str = OsmInterface.detectar_pais_por_coordenadas(coordenadas)
        if not pais:
            return {}

        raw_result: minidom.Element = OsmInterface._query_server(query, pais)
        if not raw_result:
            return {}

        resposta = {}
        for no in raw_result.childNodes:
            if no.nodeName == 'area':  # Divisão administrativa encontrada
                chave: Optional[Union[str, int]] = None
                nome: Optional[str] = None
                for n in no.childNodes:
                    if n.nodeName == 'tag':
                        if n.hasAttribute('k') and n.getAttribute('k') == 'admin_level':  # Nível da divisão encontrado
                            chave = n.getAttribute('v')
                        elif n.hasAttribute('k') and n.getAttribute('k') in [  # Nível não encontrado, mas sim nome (ex: antigas freguesias)
                                'political_division', 'border_type', 'boundary'] and not chave:
                            chave = n.getAttribute('v')
                        elif n.hasAttribute('k') and n.getAttribute('k') == 'name':  # Nome da divisão administrativa
                            nome = n.getAttribute('v')
                if chave and nome:
                    try:
                        chave = int(chave)
                    except:  # Não é inteiro — Ex: 'historic_parish'
                        pass
                    resposta[chave] = nome

        return dict(sorted(resposta.items(), key=lambda item: str(item[0])))  # Ordena resposta pela chave

    @staticmethod
    def obter_saidas_de_estrada(nome_estrada: str, pais: str) -> dict[str, list[Coordinate]]:
        """
        Dado o nome de uma estrada e o respectivo país, retorna as saídas e respectivas coordenadas
        Destina-se sobretudo a auto-estradas e vias rápidas
        """
        # A query obtém tanto relações como vias com o nome da estrada
        query = f'rel[name="{nome_estrada}"];' \
                f'way(r)->.w1;' \
                f'way[name="{nome_estrada}"]->.w2;' \
                f'(node(w.w1);' \
                f'node(w.w2);)->.n1;' \
                f'node.n1[highway="motorway_junction"];' \
                f'out geom;'

        raw_result: minidom.Element = OsmInterface._query_server(query, pais)
        if not raw_result:
            return {}

        resposta = {}
        for no in raw_result.childNodes:
            if no.nodeName == 'node':
                coordenadas: Coordinate = Coordinate(float(no.getAttribute('lat')), float(no.getAttribute('lon')))
                saida_id: Optional[str] = None
                for n in no.childNodes:
                    if n.nodeName == 'tag':
                        if n.hasAttribute('k') and n.getAttribute('k') == 'ref':  # Saída tem identificador
                            saida_id = n.getAttribute('v')
                if saida_id:
                    if saida_id not in resposta:
                        resposta[saida_id] = []
                    resposta[saida_id].append(coordenadas)

        if not resposta:
            if OsmInterface.test_connections():
                print("A estrada fornecida não tem saídas com identificadores")
            return {}

        return dict(sorted(resposta.items(), key=lambda item: item[0]))  # Ordena resposta pelo identificador da saída

    @staticmethod
    def obter_estacoes_de_linha_ferroviaria(nome_linha_ferroviaria: str, pais: str) -> dict[str, list[Coordinate]]:
        """
        Dado o nome de uma linha ferroviária e o respectivo país, retorna as estações e respectivas coordenadas
        """
        # A query obtém tanto relações como vias com o nome da linha ferroviária
        query = f'rel[name="{nome_linha_ferroviaria}"];' \
                f'way(r)->.w1;' \
                f'way[name="{nome_linha_ferroviaria}"]->.w2;' \
                f'(node(w.w1);' \
                f'node(w.w2);)->.n1;' \
                f'node.n1[name];' \
                f'out geom;'

        raw_result: minidom.Element = OsmInterface._query_server(query, pais)
        if not raw_result:
            return {}

        resposta = {}
        for no in raw_result.childNodes:
            if no.nodeName == 'node':
                coordenadas: Coordinate = Coordinate(float(no.getAttribute('lat')), float(no.getAttribute('lon')))
                estacao: Optional[str] = None
                for n in no.childNodes:
                    if n.nodeName == 'tag':
                        if n.hasAttribute('k') and n.getAttribute('k') == 'name':  # Nó tem nome - Provável estação ou apeadeiro
                            estacao = n.getAttribute('v')
                if estacao:
                    if estacao not in resposta:
                        resposta[estacao] = []
                    resposta[estacao].append(coordenadas)

        if not resposta:
            if OsmInterface.test_connections():
                print("Não se encontraram estações ou apeadeiros para a linha ou ramal fornecido")
            return {}

        return resposta

    @staticmethod
    def processar_area_para_calculo_distancias(lista_coordenadas: list[Coordinate], via_tipo: str, detalhe: int,
                                               pais: str) -> tuple[dict[int, OsmNode], dict[int, OsmWay], list[float]]:
        """
        Retorna objectos Node e Via para uso no cálculo de distâncias dentro de uma determinada área rectangular
        :param lista_coordenadas: Lista de coordenadas que delimitam a área pretendida
        :param via_tipo: Se se devem considerar apenas estradas ou apenas linhas ferroviárias
        :param detalhe: Apenas considerado se se considerarem estradas. Quanto mais detalhe, mais tipos de estradas se processam
        :param pais: País da área a cobrir. Determina o servidor ao qual se farão pedidos
        :return Lista de objectos Node, lista de objecto Via, e extremos da área a cobrir
        """
        tags: list[str] = TAGS_DESIRED_ROADS[detalhe]

        min_latitude: float = 90.0
        max_latitude: float = -90.0
        min_longitude: float = 180.0
        max_longitude: float = -180.0

        # Calcula os extremos do rectângulo
        for coordenadas in lista_coordenadas:
            latitude: float = coordenadas.latitude
            longitude: float = coordenadas.longitude
            if latitude < min_latitude:
                min_latitude = latitude
            if latitude > max_latitude:
                max_latitude = latitude
            if longitude < min_longitude:
                min_longitude = longitude
            if longitude > max_longitude:
                max_longitude = longitude

        # Acrescenta a margem ao rectângulo, em graus decimais
        min_latitude -= DISTANCE_RECTANGLE_MARGIN
        max_latitude += DISTANCE_RECTANGLE_MARGIN
        min_longitude -= DISTANCE_RECTANGLE_MARGIN
        max_longitude += DISTANCE_RECTANGLE_MARGIN

        area_extremos: list[float] = [min_latitude, max_latitude, min_longitude, max_longitude]

        if via_tipo == ways.ROAD:  # Todas as estradas marcadas com as tags pretendidas na área pretendida
            query = f'[bbox:{min_latitude},{min_longitude},{max_latitude},{max_longitude}];' \
                    '('
            for tag in tags:
                query += f'rel[highway={tag}];'
            query += ')->.r1;' \
                     f'(way(r.r1);'
            for tag in tags:
                query += f'way[highway={tag}];'
            query += ');' \
                     'out geom;'
        elif via_tipo == ways.RAILWAY:  # Todas as linhas ferroviárias na área pretendida
            query = 'rel[railway]->.r1;' \
                    '(way(r.r1);' \
                    'way[railway];);' \
                    'out geom;'
        else:
            return {}, {}, []

        raw_result: minidom.Element = OsmInterface._query_server(query, pais)
        if not raw_result:
            return {}, {}, []

        lista_nos: dict[int, OsmNode] = {}
        lista_vias: dict[int, OsmWay] = {}
        for no in raw_result.childNodes:
            if no.nodeName == 'way' and no.hasAttribute('id'):
                via_id: int = no.getAttribute('id')
                lista_nos_via: list[OsmNode] = []
                for n2 in no.childNodes:
                    if n2.nodeName == 'nd' and n2.hasAttribute('ref') and n2.hasAttribute('lat') and n2.hasAttribute('lon'):
                        no_id: int = n2.getAttribute('ref')
                        lat: float = n2.getAttribute('lat')
                        lon: float = n2.getAttribute('lon')
                        lista_nos_via.append(OsmNode(no_id, lat, lon))
                        lista_nos[no_id] = OsmNode(no_id, lat, lon)
                if lista_nos_via:
                    lista_vias[via_id] = OsmWay(via_id, lista_nos_via)

        if not lista_nos or not lista_vias:
            if OsmInterface.test_connections():
                print("Não se encontraram relações nem vias OSM para a estrada/ferrovia fornecida")
            return {}, {}, []

        return lista_nos, lista_vias, area_extremos

    @staticmethod
    def processar_via_para_calculo_distancias(nome_via: str, pais: str) -> tuple[dict[int, OsmNode], dict[int, OsmWay]]:
        """
        Dado o nome de uma estrada ou ferrovia, retorna objectos Node e Via para uso no cálculo de distâncias nessa
            estrada ou ferrovia
        """
        query = f'rel[name="{nome_via}"]->.r1;' \
                f'(way(r.r1);' \
                f'way[name="{nome_via}"];);' \
                'out geom;'

        raw_result: minidom.Element = OsmInterface._query_server(query, pais)
        if not raw_result:
            return {}, {}

        lista_nos: dict[int, OsmNode] = {}
        lista_vias: dict[int, OsmWay] = {}
        for no in raw_result.childNodes:
            if no.nodeName == 'way' and no.hasAttribute('id'):
                via_id: int = no.getAttribute('id')
                lista_nos_via: list[OsmNode] = []
                for n2 in no.childNodes:
                    if n2.nodeName == 'nd' and n2.hasAttribute('ref') and n2.hasAttribute('lat') and n2.hasAttribute('lon'):
                        no_id: int = n2.getAttribute('ref')
                        lat: float = n2.getAttribute('lat')
                        lon: float = n2.getAttribute('lon')
                        lista_nos_via.append(OsmNode(no_id, lat, lon))
                        lista_nos[no_id] = OsmNode(no_id, lat, lon)
                if lista_nos_via:
                    lista_vias[via_id] = OsmWay(via_id, lista_nos_via)

        if not lista_nos or not lista_vias:
            if OsmInterface.test_connections():
                print("Não se encontraram relações nem vias OSM para a estrada/ferrovia fornecida")
            return {}, {}

        return lista_nos, lista_vias

    @staticmethod
    def detectar_pais_por_coordenadas(coordenadas: Coordinate) -> Optional[str]:
        """
        Detecta automaticamente o país com base nos retornos a pedidos aos servidores existentes
        :return: Nome do país se for possível determinar, None caso contrário
        """
        for pais_servidor in ways.ALL_SUPPORTED_COUNTRIES:
            divisoes: dict[Union[str, int], str] = OsmInterface.obter_divisoes_administrativas_de_ponto(coordenadas, pais_servidor)

            if divisoes.get(COUNTRY):  # Espera-se que cubra Portugal, Andorra e Gibraltar
                pais = divisoes[COUNTRY]
                if pais == 'Portugal':
                    return ways.PORTUGAL
                elif pais == 'Andorra':
                    return ways.ANDORRA
                elif pais == 'Gibraltar':
                    return ways.GIBRALTAR
                elif pais == 'Spain':
                    return ways.SPAIN
                else:  # País não coberto
                    return None

            elif divisoes.get(AUTONOMOUS_COMMUNITY):  # Espera-se que cubra Espanha
                comunidade_autonoma = divisoes[AUTONOMOUS_COMMUNITY]

                if comunidade_autonoma not in ['Azores', 'Madeira', 'Gibraltar']:  # Nível é usado em Portugal e Gibraltar também
                    return ways.SPAIN
        else:
            return None

    @staticmethod
    def obter_pontos_extremos_regiao(nome: str, nivel_administrativo: int, pais: str) -> Optional[ExtremePoints]:
        # Freguesias históricas portuguesas não têm nível associado
        query = f'rel[name="{nome}"][admin_level="{nivel_administrativo}"];' \
                'out geom;'

        raw_result: minidom.Element = OsmInterface._query_server(query, pais)
        if not raw_result:
            print("Nenhum resultado obtido")
            return None

        max_norte: Coordinate = Coordinate(-90.0, 0.0)
        max_sul: Coordinate = Coordinate(90.0, 0.0)
        max_oeste: Coordinate = Coordinate(0.0, 180.0)
        max_este: Coordinate = Coordinate(0.0, -180.0)
        for no in raw_result.childNodes:
            if no.nodeName == 'relation' and no.hasAttribute('id'):  # Região pretendida
                for n2 in no.childNodes:
                    if n2.nodeName == 'member' and n2.hasAttribute('type') and n2.getAttribute('type') == 'node' and \
                            n2.hasAttribute('lat') and n2.hasAttribute('lon'):  # Nó que delimita a região
                        lat = float(n2.getAttribute('lat'))
                        lon = float(n2.getAttribute('lon'))
                        if lat > max_norte.latitude:
                            max_norte.set_latitude(lat)
                            max_norte.set_longitude(lon)
                        if lat < max_sul.latitude:
                            max_sul.set_latitude(lat)
                            max_sul.set_longitude(lon)
                        if lon > max_este.longitude:
                            max_este.set_latitude(lat)
                            max_este.set_longitude(lon)
                        if lon < max_oeste.longitude:
                            max_oeste.set_latitude(lat)
                            max_oeste.set_longitude(lon)
                    elif n2.nodeName == 'member' and n2.hasAttribute('type') and n2.getAttribute('type') == 'way':  # Via que delimita a região
                        for n3 in n2.childNodes:
                            if n3.nodeName == 'nd' and n3.hasAttribute('lat') and n3.hasAttribute('lon'):
                                lat = float(n3.getAttribute('lat'))
                                lon = float(n3.getAttribute('lon'))
                                if lat > max_norte.latitude:
                                    max_norte.set_latitude(lat)
                                    max_norte.set_longitude(lon)
                                if lat < max_sul.latitude:
                                    max_sul.set_latitude(lat)
                                    max_sul.set_longitude(lon)
                                if lon > max_este.longitude:
                                    max_este.set_latitude(lat)
                                    max_este.set_longitude(lon)
                                if lon < max_oeste.longitude:
                                    max_oeste.set_latitude(lat)
                                    max_oeste.set_longitude(lon)

        pontos_extremos = ExtremePoints(nome, nivel_administrativo, pais, max_norte, max_sul, max_este, max_oeste)
        return pontos_extremos

    @staticmethod
    def _query_server(query: str, country: str) -> Optional[minidom.Element]:
        """
        Base method to send a query to an OSM server and return the parsed response
        :param query: Query string to send to the server
        :param country: Desired country - It is expected that the query applies to a single country
        :return: A Python representation of the response XML on success, None otherwise
        """
        assert query
        assert country in ways.ALL_SUPPORTED_COUNTRIES

        try:
            server_url: str = OsmInterface._get_server_url(country)
            raw_response: str = requests.get(f'{server_url}?data={query}').content.decode()  # An XML encoded as a string
            return OsmInterface._parse_raw_response(raw_response)  # From string to a representation of the response XML

        except requests.exceptions.ConnectionError:
            print(f"Connection with OSM server for country {country} failed to be established - Is server running?")
            return None
        except Exception as e:
            print(f'Error while sending Overpass QL query {query} to OSM server for country {country}')
            print(e)
            return None

    @staticmethod
    def _parse_raw_response(raw_response: str) -> Optional[minidom.Element]:
        """
        Given the raw string response from the OSM servers (always formatted as an XML), returns the essential part of the response
            as a Python XML object
        """
        if raw_response:
            return minidom.parseString(raw_response).childNodes[0]  # Base element - Always delimited by <osm> </osm>
        else:
            return None

    @staticmethod
    def _get_server_url(country: str) -> Optional[str]:
        """
        Given a target country, returns the full OSM server URL, or None if country is unsupported
        """
        if country == ways.ANDORRA:
            port: int = PORT_ANDORRA
        elif country in [ways.GIBRALTAR, ways.SPAIN]:  # Spain and Gibraltar maps are in the same server
            port: int = PORT_GIBRALTAR_SPAIN
        elif country == ways.PORTUGAL:
            port: int = PORT_PORTUGAL
        else:  # Unsupported country
            return None

        server_url = f'http://{DOCKER_IP}:{port}/api/interpreter'  # Please change to https if server is remote
        return server_url
