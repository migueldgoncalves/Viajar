from typing import Optional, Union
import pprint

import requests
from xml.dom import minidom

IP_DOCKER = '127.0.0.1'
PORTO_DOCKER = 12345
URL_BASE = f'http://{IP_DOCKER}:{PORTO_DOCKER}/api/interpreter'  # Usar https se o servidor não for local


class OsmInterface:

    @staticmethod
    def testar_ligacao() -> bool:
        """
        Retorna True se se conseguiu estabelecer ligação, False caso contrário
        """
        try:
            query = "out;"
            raw_response: str = requests.get(URL_BASE + "?" + query).content.decode()
            xml_elem: minidom.Element = OsmInterface._parse_response(raw_response)
            if xml_elem.nodeName == 'osm':
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def obter_divisoes_administrativas_de_ponto(latitude: float, longitude: float) -> dict[Union[str, int], str]:
        query = 'way[name="Estació Nacional d\'Autobussos"];' \
                'out geom;'  # Funciona!
        query = 'area[name="Andorra la Vella"][admin_level=7];' \
                'out geom;'  # Funciona!

        query = f'is_in({latitude},{longitude}); out geom;'
        raw_result: minidom.Element = OsmInterface._query(query)

        resposta = {}
        for no in raw_result.childNodes:
            if no.nodeName == 'area':  # Divisão administrativa encontrada
                chave: Optional[str] = None
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
                    resposta[chave] = nome
        return dict(sorted(resposta.items(), key=lambda item: item[0]))  # Ordena resposta pela chave

    @staticmethod
    def _query(query: str, debug: bool = False) -> Optional[minidom.Element]:
        try:
            raw_response = requests.get(URL_BASE + "?data=" + query).content.decode()
            if debug:
                print(raw_response)
            return OsmInterface._parse_response(raw_response)

        except requests.exceptions.ConnectionError:
            print("A ligação não pôde ser estabelecida - O servidor local está ligado?")
            return None
        except:
            print("Erro ao enviar uma query Overpass QL para o servidor local")
            return None

    @staticmethod
    def _parse_response(raw_response: str) -> Optional[minidom.Element]:
        if raw_response:
            return minidom.parseString(raw_response).childNodes[0]  # Elemento base - Sempre delimitado por <osm> </osm>
        else:
            return None


a = OsmInterface.obter_divisoes_administrativas_de_ponto(38.3, -2.0)
pprint.pprint(a)
