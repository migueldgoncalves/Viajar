from typing import Optional, Union
import pprint
import requests
from xml.dom import minidom

import viajar.auxiliar.vias as vias

IP_DOCKER = '127.0.0.1'
ESPANHA_PORTO = 12345
PORTUGAL_PORTO = 12346
ANDORRA_PORTO = 12347


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
        query = 'way[name="Estació Nacional d\'Autobussos"];' \
                'out geom;'  # Funciona!
        query = 'area[name="Andorra la Vella"][admin_level=7];' \
                'out geom;'  # Funciona!

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

    @staticmethod
    def detectar_pais_por_coordenadas(latitude: float, longitude: float) -> Optional[str]:
        return OsmInterface._detectar_pais(latitude, longitude)

    @staticmethod
    def _detectar_pais(latitude: float = 0.0, longitude: float = 0.0):
        """
        Detecta automaticamente o país com base nos retornos a pedidos aos servidores existentes
        :param latitude: Deve ser fornecida com a longitude
        :param longitude: Deve ser fornecida com a latitude (pode ser 0.0)
        :return: Nome do país se for possível determinar, None caso contrário
        """
        if longitude or latitude:   # Coordenadas (0.0, 0.0) estão muito afastadas de Península Ibérica
            for pais in [vias.PORTUGAL, vias.ESPANHA, vias.ANDORRA]:
                divisoes: dict[str, str] = OsmInterface.obter_divisoes_administrativas_de_ponto(latitude, longitude, pais)

                if divisoes.get(vias.PAIS):  # Espera-se que cubra Portugal, Andorra e Gibraltar
                    pais = divisoes[vias.PAIS]
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

                elif divisoes.get(vias.COMUNIDADE_AUTONOMA):  # Espera-se que cubra Espanha
                    comunidade_autonoma = divisoes[vias.COMUNIDADE_AUTONOMA]

                    if comunidade_autonoma not in ['Azores', 'Madeira', 'Gibraltar']:  # Nível é usado em Portugal e Gibraltar também
                        return vias.ESPANHA

            else:
                return None
        else:
            return None


# a = OsmInterface.obter_divisoes_administrativas_de_ponto(37.35, -7.44)  # Ayamonte
# a = OsmInterface.obter_divisoes_administrativas_de_ponto(42.60, 1.47)  # Andorra
a = OsmInterface.obter_divisoes_administrativas_de_ponto(39.0, -7.0)  # Portugal
# a = OsmInterface.obter_divisoes_administrativas_de_ponto(36.133772, -5.351501)  # Gibraltar
pprint.pprint(a)
