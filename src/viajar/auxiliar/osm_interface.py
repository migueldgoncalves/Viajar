from typing import Optional, Union
import pprint
import requests
from xml.dom import minidom

import viajar.auxiliar.vias as vias
from viajar.auxiliar.coordenada import Coordenada

# Servidores
IP_DOCKER = '127.0.0.1'
ESPANHA_PORTO = 12345
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
                if xml_elem.nodeName == 'osm':
                    continue  # Sucesso
                else:
                    return False
        except:
            return False

        return True

    @staticmethod
    def obter_divisoes_administrativas_de_ponto(latitude: float, longitude: float, pais: str = None) -> dict[Union[str, int], str]:
        """
        A maior parte das divisões administrativas encontradas terão um número como identificador (entre 1 e 11), mas
            também poderão ter uma string como identificador (ex: historic_parish - Antiga freguesia portuguesa)
        """
        query = f'is_in({latitude},{longitude}); out geom;'
        if not pais:
            pais: str = OsmInterface.detectar_pais_por_coordenadas(latitude, longitude)
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
    def detectar_pais_por_coordenadas(latitude: float, longitude: float) -> Optional[str]:
        """
        Detecta automaticamente o país com base nos retornos a pedidos aos servidores existentes
        :return: Nome do país se for possível determinar, None caso contrário
        """
        for pais in [vias.PORTUGAL, vias.ESPANHA, vias.ANDORRA]:
            divisoes: dict[Union[str, int], str] = OsmInterface.obter_divisoes_administrativas_de_ponto(latitude, longitude, pais)

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
        if pais == vias.ESPANHA:
            porto = ESPANHA_PORTO
        elif pais == vias.PORTUGAL:
            porto = PORTUGAL_PORTO
        elif pais == vias.ANDORRA:
            porto = ANDORRA_PORTO
        elif pais == vias.GIBRALTAR:  # O servidor de Espanha tem a informação tanto de Espanha como de Gibraltar
            porto = ESPANHA_PORTO
        else:  # País não coberto
            return None

        url_servidor = f'http://{IP_DOCKER}:{porto}/api/interpreter'  # Usar https se o servidor não for local
        return url_servidor


class Node:
    """
    Classe para guardar dados de um nó
    """
    def __init__(self, node_id: int, latitude: float, longitude: float):
        self.node_id: int = node_id
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.nos_circundantes: set[int] = set()


class Via:
    """
    Classe para guardar dados de uma via
    """
    def __init__(self, via_id, lista_nos: list[Node]):
        self.via_id: int = via_id
        self.lista_nos: list[Node] = lista_nos


# a = OsmInterface.obter_divisoes_administrativas_de_ponto(37.35, -7.44)  # Ayamonte
# a = OsmInterface.obter_divisoes_administrativas_de_ponto(42.60, 1.47)  # Andorra
# a = OsmInterface.obter_divisoes_administrativas_de_ponto(39.0, -7.0)  # Portugal
# a = OsmInterface.obter_divisoes_administrativas_de_ponto(36.133772, -5.351501)  # Gibraltar
# pprint.pprint(a)

# nome_estrada = "Autoestrada da Costa do Estoril"
# nome_estrada = "Autovía del Suroeste"
# pprint.pprint(OsmInterface.obter_saidas_de_estrada(nome_estrada, pais=vias.ESPANHA))
# nome_linha = 'Linha de Cascais'
# nome_linha = "Tren C-3: Chamartín -> Sol -> Atocha -> Aranjuez"
# nome_linha = "Línea 8: Nuevos Ministerios-Aeropuerto T4"
# pprint.pprint(OsmInterface.obter_estacoes_de_linha_ferroviaria(nome_linha, pais=vias.ESPANHA))