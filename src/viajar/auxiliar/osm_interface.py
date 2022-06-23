from typing import Optional, Union
import requests
from xml.dom import minidom

import viajar.auxiliar.vias as vias
from viajar.auxiliar.coordenada import Coordenada

# Servidores
IP_DOCKER = '127.0.0.1'
ESPANHA_GIBRALTAR_PORTO = 12345
PORTUGAL_PORTO = 12346
ANDORRA_PORTO = 12347

##############################
# Constantes do OpenStreetMap
##############################

# Níveis administrativos do OpenStreetMap

# Geral
PAIS = 2

# Andorra
PAROQUIA = 7

# Espanha
COMUNIDADE_AUTONOMA = 4
PROVINCIA = 6
COMARCA = 7
MUNICIPIO = 8
DISTRITO_ES = 9

# Gibraltar
GIBRALTAR_NIVEL_ADMIN = 4

# Portugal
REGIAO_AUTONOMA = 4
DISTRITO_PT = 6
CONCELHO = 7
FREGUESIA = 8
FREGUESIA_HISTORICA = 'historic_parish'

##############################

VIA_FERROVIA = vias.VIA_FERROVIA
VIA_ESTRADA = vias.VIA_ESTRADA

NIVEL_DETALHE_INTERCIDADES = 1
NIVEL_DETALHE_URBANO = 2

MARGEM_RECTANGULO_DISTANCIAS = 0.1  # 1 grau = muito aproximadamente 100 km na Península Ibérica

# Estradas e caminhos com tags não incluídas nesta lista não costumam ser usadas no âmbito deste projecto
# Referência: https://wiki.openstreetmap.org/wiki/Key:highway
TAGS_ESTRADAS_PRETENDIDAS = {
    NIVEL_DETALHE_INTERCIDADES: [
        'motorway', 'trunk', 'primary', 'secondary', 'motorway_link', 'trunk_link', 'primary_link', 'secondary_link',
        'motorway_junction'],
    NIVEL_DETALHE_URBANO: [
        'motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified', 'residential', 'motorway_link',
        'trunk_link', 'primary_link', 'secondary_link', 'tertiary_link', 'living_street', 'service', 'motorway_junction'],
}


class PontosExtremos:
    """
    Classe para guardar pontos extremos de uma região
    """
    def __init__(self, nome: str, nivel_administrativo: int, pais: str,
                 norte: Coordenada, sul: Coordenada, este: Coordenada, oeste: Coordenada):
        self.nome: str = nome
        self.nivel_administrativo: int = nivel_administrativo
        self.pais: str = pais
        self.norte: Coordenada = norte
        self.sul: Coordenada = sul
        self.este: Coordenada = este
        self.oeste: Coordenada = oeste

    def __str__(self):
        return f'Nome: {self.nome}\n' \
               f'Nível administrativo: {self.nivel_administrativo}\n' \
               f'País: {self.pais}\n' \
               f'Norte: {self.norte}\n' \
               f'Sul: {self.sul}\n' \
               f'Este: {self.este}\n' \
               f'Oeste: {self.oeste}'


class Node:
    """
    Classe para guardar dados de um nó
    """
    def __init__(self, node_id: int, latitude: float, longitude: float):
        self.node_id: int = node_id
        self.latitude: float = float(latitude)
        self.longitude: float = float(longitude)
        self.nos_circundantes: set[int] = set()


class Via:
    """
    Classe para guardar dados de uma via
    """
    def __init__(self, via_id, lista_nos: list[Node]):
        self.via_id: int = via_id
        self.lista_nos: list[Node] = lista_nos


class OsmInterface:

    @staticmethod
    def testar_ligacao() -> bool:
        """
        Retorna True se se conseguiu estabelecer ligação com todos os servidores, False caso contrário
        """
        try:
            for pais in [vias.PORTUGAL, vias.ESPANHA, vias.ANDORRA]:
                url_servidor: str = OsmInterface._obter_url_servidor(pais)
                query = "out;"

                raw_response: str = requests.get(url_servidor + "?" + query).content.decode()
                xml_elem: minidom.Element = OsmInterface._parse_response(raw_response)
                if xml_elem.tagName == 'osm':
                    continue  # Sucesso
                else:
                    return False
        except:
            return False

        return True

    @staticmethod
    def obter_divisoes_administrativas_de_ponto(coordenadas: Coordenada, pais: str = None) -> dict[Union[str, int], str]:
        """
        A maior parte das divisões administrativas encontradas terão um número como identificador (entre 1 e 11), mas
            também poderão ter uma string como identificador (ex: historic_parish - Antiga freguesia portuguesa)
        """
        query = f'is_in({coordenadas.latitude},{coordenadas.longitude}); out geom;'
        if not pais:
            pais: str = OsmInterface.detectar_pais_por_coordenadas(coordenadas)
        if not pais:
            return {}

        raw_result: minidom.Element = OsmInterface._query(query, pais)
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
    def obter_saidas_de_estrada(nome_estrada: str, pais: str) -> dict[str, list[Coordenada]]:
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

        raw_result: minidom.Element = OsmInterface._query(query, pais)
        if not raw_result:
            return {}

        resposta = {}
        for no in raw_result.childNodes:
            if no.nodeName == 'node':
                coordenadas: Coordenada = Coordenada(float(no.getAttribute('lat')), float(no.getAttribute('lon')))
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
            if OsmInterface.testar_ligacao():
                print("A estrada fornecida não tem saídas com identificadores")
            return {}

        return dict(sorted(resposta.items(), key=lambda item: item[0]))  # Ordena resposta pelo identificador da saída

    @staticmethod
    def obter_estacoes_de_linha_ferroviaria(nome_linha_ferroviaria: str, pais: str) -> dict[str, list[Coordenada]]:
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

        raw_result: minidom.Element = OsmInterface._query(query, pais)
        if not raw_result:
            return {}

        resposta = {}
        for no in raw_result.childNodes:
            if no.nodeName == 'node':
                coordenadas: Coordenada = Coordenada(float(no.getAttribute('lat')), float(no.getAttribute('lon')))
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
            if OsmInterface.testar_ligacao():
                print("Não se encontraram estações ou apeadeiros para a linha ou ramal fornecido")
            return {}

        return resposta

    @staticmethod
    def processar_area_para_calculo_distancias(lista_coordenadas: list[Coordenada], via_tipo: str, detalhe: int,
                                               pais: str) -> tuple[dict[int, Node], dict[int, Via], list[float]]:
        """
        Retorna objectos Node e Via para uso no cálculo de distâncias dentro de uma determinada área rectangular
        :param lista_coordenadas: Lista de coordenadas que delimitam a área pretendida
        :param via_tipo: Se se devem considerar apenas estradas ou apenas linhas ferroviárias
        :param detalhe: Apenas considerado se se considerarem estradas. Quanto mais detalhe, mais tipos de estradas se processam
        :param pais: País da área a cobrir. Determina o servidor ao qual se farão pedidos
        :return Lista de objectos Node, lista de objecto Via, e extremos da área a cobrir
        """
        tags: list[str] = TAGS_ESTRADAS_PRETENDIDAS[detalhe]

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
        min_latitude -= MARGEM_RECTANGULO_DISTANCIAS
        max_latitude += MARGEM_RECTANGULO_DISTANCIAS
        min_longitude -= MARGEM_RECTANGULO_DISTANCIAS
        max_longitude += MARGEM_RECTANGULO_DISTANCIAS

        area_extremos: list[float] = [min_latitude, max_latitude, min_longitude, max_longitude]

        if via_tipo == VIA_ESTRADA:  # Todas as estradas marcadas com as tags pretendidas na área pretendida
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
        elif via_tipo == VIA_FERROVIA:  # Todas as linhas ferroviárias na área pretendida
            query = 'rel[railway]->.r1;' \
                    '(way(r.r1);' \
                    'way[railway];);' \
                    'out geom;'
        else:
            return {}, {}, []

        raw_result: minidom.Element = OsmInterface._query(query, pais)
        if not raw_result:
            return {}, {}, []

        lista_nos: dict[int, Node] = {}
        lista_vias: dict[int, Via] = {}
        for no in raw_result.childNodes:
            if no.nodeName == 'way' and no.hasAttribute('id'):
                via_id: int = no.getAttribute('id')
                lista_nos_via: list[Node] = []
                for n2 in no.childNodes:
                    if n2.nodeName == 'nd' and n2.hasAttribute('ref') and n2.hasAttribute('lat') and n2.hasAttribute('lon'):
                        no_id: int = n2.getAttribute('ref')
                        lat: float = n2.getAttribute('lat')
                        lon: float = n2.getAttribute('lon')
                        lista_nos_via.append(Node(no_id, lat, lon))
                        lista_nos[no_id] = Node(no_id, lat, lon)
                if lista_nos_via:
                    lista_vias[via_id] = Via(via_id, lista_nos_via)

        if not lista_nos or not lista_vias:
            if OsmInterface.testar_ligacao():
                print("Não se encontraram relações nem vias OSM para a estrada/ferrovia fornecida")
            return {}, {}, []

        return lista_nos, lista_vias, area_extremos

    @staticmethod
    def processar_via_para_calculo_distancias(nome_via: str, pais: str) -> tuple[dict[int, Node], dict[int, Via]]:
        """
        Dado o nome de uma estrada ou ferrovia, retorna objectos Node e Via para uso no cálculo de distâncias nessa
            estrada ou ferrovia
        """
        query = f'rel[name="{nome_via}"]->.r1;' \
                f'(way(r.r1);' \
                f'way[name="{nome_via}"];);' \
                'out geom;'

        raw_result: minidom.Element = OsmInterface._query(query, pais)
        if not raw_result:
            return {}, {}

        lista_nos: dict[int, Node] = {}
        lista_vias: dict[int, Via] = {}
        for no in raw_result.childNodes:
            if no.nodeName == 'way' and no.hasAttribute('id'):
                via_id: int = no.getAttribute('id')
                lista_nos_via: list[Node] = []
                for n2 in no.childNodes:
                    if n2.nodeName == 'nd' and n2.hasAttribute('ref') and n2.hasAttribute('lat') and n2.hasAttribute('lon'):
                        no_id: int = n2.getAttribute('ref')
                        lat: float = n2.getAttribute('lat')
                        lon: float = n2.getAttribute('lon')
                        lista_nos_via.append(Node(no_id, lat, lon))
                        lista_nos[no_id] = Node(no_id, lat, lon)
                if lista_nos_via:
                    lista_vias[via_id] = Via(via_id, lista_nos_via)

        if not lista_nos or not lista_vias:
            if OsmInterface.testar_ligacao():
                print("Não se encontraram relações nem vias OSM para a estrada/ferrovia fornecida")
            return {}, {}

        return lista_nos, lista_vias

    @staticmethod
    def detectar_pais_por_coordenadas(coordenadas: Coordenada) -> Optional[str]:
        """
        Detecta automaticamente o país com base nos retornos a pedidos aos servidores existentes
        :return: Nome do país se for possível determinar, None caso contrário
        """
        for pais_servidor in [vias.PORTUGAL, vias.ESPANHA, vias.ANDORRA]:
            divisoes: dict[Union[str, int], str] = OsmInterface.obter_divisoes_administrativas_de_ponto(coordenadas, pais_servidor)

            if divisoes.get(PAIS):  # Espera-se que cubra Portugal, Andorra e Gibraltar
                pais = divisoes[PAIS]
                if pais == 'Portugal':
                    return vias.PORTUGAL
                elif pais == 'Andorra':
                    return vias.ANDORRA
                elif pais == 'Gibraltar':
                    return vias.GIBRALTAR
                elif pais == 'Spain':
                    return vias.ESPANHA
                else:  # País não coberto
                    return None

            elif divisoes.get(COMUNIDADE_AUTONOMA):  # Espera-se que cubra Espanha
                comunidade_autonoma = divisoes[COMUNIDADE_AUTONOMA]

                if comunidade_autonoma not in ['Azores', 'Madeira', 'Gibraltar']:  # Nível é usado em Portugal e Gibraltar também
                    return vias.ESPANHA
        else:
            return None

    @staticmethod
    def obter_pontos_extremos_regiao(nome: str, nivel_administrativo: int, pais: str) -> Optional[PontosExtremos]:
        # Freguesias históricas portuguesas não têm nível associado
        query = f'rel[name="{nome}"][admin_level="{nivel_administrativo}"];' \
                'out geom;'

        raw_result: minidom.Element = OsmInterface._query(query, pais)
        if not raw_result:
            print("Nenhum resultado obtido")
            return None

        max_norte: Coordenada = Coordenada(-90.0, 0.0)
        max_sul: Coordenada = Coordenada(90.0, 0.0)
        max_oeste: Coordenada = Coordenada(0.0, 180.0)
        max_este: Coordenada = Coordenada(0.0, -180.0)
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

        pontos_extremos = PontosExtremos(nome, nivel_administrativo, pais, max_norte, max_sul, max_este, max_oeste)
        return pontos_extremos

    @staticmethod
    def _query(query: str, pais: str, debug: bool = False) -> Optional[minidom.Element]:
        try:
            url_servidor: str = OsmInterface._obter_url_servidor(pais)
            raw_response = requests.get(url_servidor + "?data=" + query).content.decode()
            if debug:
                print(raw_response)
            return OsmInterface._parse_response(raw_response)

        except requests.exceptions.ConnectionError:
            print("A ligação não pôde ser estabelecida - O servidor local está ligado?")
            return None
        except Exception as e:
            print("Erro ao enviar uma query Overpass QL para o servidor local")
            print(e)
            return None

    @staticmethod
    def _parse_response(raw_response: str) -> Optional[minidom.Element]:
        if raw_response:
            return minidom.parseString(raw_response).childNodes[0]  # Elemento base - Sempre delimitado por <osm> </osm>
        else:
            return None

    @staticmethod
    def _obter_url_servidor(pais: str) -> Optional[str]:
        if pais == vias.ESPANHA:  # Os mapas de Espanha e de Gibraltar estão no mesmo servidor
            porto = ESPANHA_GIBRALTAR_PORTO
        elif pais == vias.PORTUGAL:
            porto = PORTUGAL_PORTO
        elif pais == vias.ANDORRA:
            porto = ANDORRA_PORTO
        elif pais == vias.GIBRALTAR:
            porto = ESPANHA_GIBRALTAR_PORTO
        else:  # País não coberto
            return None

        url_servidor = f'http://{IP_DOCKER}:{porto}/api/interpreter'  # Usar https se o servidor não for local
        return url_servidor

print(OsmInterface.obter_pontos_extremos_regiao("Sierra Norte", COMARCA, vias.ESPANHA))