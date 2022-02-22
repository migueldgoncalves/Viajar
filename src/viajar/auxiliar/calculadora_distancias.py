from typing import List, Set, Dict, Tuple

try:
    import osmium
except:
    print("Biblioteca osmium não instalada. Está a executar este ficheiro em Windows?")
    exit(1)

import viajar.auxiliar.vias as vias
import viajar.auxiliar.haversine as haversine

"""
Este módulo destina-se a calcular distâncias por estrada ou ferrovia entre dois pontos
"""

MARGEM_RECTANGULO_DISTANCIAS = 0.1  # 1 grau = muito aproximadamente 100 km na Península Ibérica

TAG_HIGHWAY: str = 'highway'  # No OpenStreetMap, estradas recebem a tag 'highway'
TAG_RAILWAY: str = 'railway'

VIA_FERROVIA = vias.VIA_FERROVIA
VIA_ESTRADA = vias.VIA_ESTRADA

AREA_URBANA = 'Urbana'
AREA_INTERCIDADES = 'Intercidades'

AVISO_TAMANHO_AREA_INTERCIDADES = 100
AVISO_TAMANHO_AREA_URBANA = 10

DISTANCIA_INFINITA: int = 999999  # km


class CalculadoraDistancias:
    """
    Classe principal para o cálculo de distâncias
    Como usar:
        Primeiro gerar o mapa processado
        Depois correr o algoritmo de Dijkstra para quantos pares (origem, destino) se queira
    """
    def __init__(self) -> None:
        self.mapa_processado: Dict[int, Node] = {}

    def gerar_mapa_processado(self, lista_coordenadas: List[Tuple[float, float]], via_tipo: str, area_tipo: str,
                              ficheiro_osm: str) -> None:
        """
        Cria um mapa que contém todas as coordenadas fornecidas, adequado para se correr nele o algoritmo de Dijkstra
        :param lista_coordenadas: As coordenadas a incluir no mapa
        :param via_tipo: Se a via é uma estrada ou uma ferrovia
        :param area_tipo: Se a área a cobrir é urbana ou geral
            Áreas gerais (intercidades) cobrem apenas as estradas principais, e são adequadas para auto-estradas e outras
                vias importantes em ambiente rural e urbano
            Áreas urbanas cobrem mais estradas, e são adequadas para cobrir ruas dentro da mesma cidade. Evitar usar para
                área com mais de alguns quilómetros quadrados, ou o processamento será muito lento
            A área não é tida em conta para ferrovias
        :param ficheiro_osm: Path para o ficheiro OSM onde ir buscar a informação
        :return:
        """
        print("A obter representação da área... Isto demorará uns minutos.")

        h = ObterNosVias(lista_coordenadas, via_tipo, area_tipo)
        h.apply_file(ficheiro_osm, locations=True)

        distancia_norte_sul = round(
            haversine.obter_distancia_haversine((h.min_latitude, h.min_longitude), (h.max_latitude, h.min_longitude)), 1)
        distancia_este_oeste = round(
            haversine.obter_distancia_haversine((h.min_latitude, h.min_longitude), (h.min_latitude, h.max_longitude)), 1)
        print(f"A área de interesse tem {distancia_norte_sul} km norte-sul e {distancia_este_oeste} km este-oeste")

        if area_tipo == AREA_INTERCIDADES and distancia_norte_sul * distancia_este_oeste > AVISO_TAMANHO_AREA_INTERCIDADES ** 2 or \
                area_tipo == AREA_URBANA and distancia_norte_sul * distancia_este_oeste > AVISO_TAMANHO_AREA_URBANA ** 2:
            print("Aviso: A área a cobrir é muito grande - Esta operação poderá ser muito demorada")

        # Assim que receber os nós circundantes, terá toda a informação para se correr o algoritmo de Dijkstra
        self.mapa_processado: Dict[int, Node] = h.nos

        # Adicionar nós circundantes
        print("A adicionar informação de nós circundantes...")
        for via_id in h.vias:
            via: Via = h.vias[via_id]
            if len(via.lista_nos) <= 1:
                continue
            for index, no in enumerate(via.lista_nos):  # Todos os nós da via, estejam ou não no rectângulo desejado
                if index == 0:
                    no_seguinte: Node = via.lista_nos[1]
                    if (h.min_latitude <= no_seguinte.latitude <= h.max_latitude) and \
                            (h.min_longitude <= no_seguinte.longitude <= h.max_longitude):  # Nó circundante está dentro do rectângulo
                        if self.mapa_processado.get(no.node_id, None):
                            self.mapa_processado[no.node_id].nos_circundantes.add(no_seguinte.node_id)
                elif index == len(via.lista_nos) - 1:  # Último nó da via
                    no_anterior: Node = via.lista_nos[index - 1]
                    if (h.min_latitude <= no_anterior.latitude <= h.max_latitude) and \
                            (h.min_longitude <= no_anterior.longitude <= h.max_longitude):  # Nó circundante está dentro do rectângulo
                        if self.mapa_processado.get(no.node_id, None):
                            self.mapa_processado[no.node_id].nos_circundantes.add(no_anterior.node_id)
                else:  # Nó a meio da via
                    no_seguinte: Node = via.lista_nos[index + 1]
                    if (h.min_latitude <= no_seguinte.latitude <= h.max_latitude) and \
                            (h.min_longitude <= no_seguinte.longitude <= h.max_longitude):  # Nó circundante está dentro do rectângulo
                        if self.mapa_processado.get(no.node_id, None):
                            self.mapa_processado[no.node_id].nos_circundantes.add(no_seguinte.node_id)
                    no_anterior: Node = via.lista_nos[index - 1]
                    if (h.min_latitude <= no_anterior.latitude <= h.max_latitude) and \
                            (h.min_longitude <= no_anterior.longitude <= h.max_longitude):  # Nó circundante está dentro do rectângulo
                        if self.mapa_processado.get(no.node_id, None):
                            self.mapa_processado[no.node_id].nos_circundantes.add(no_anterior.node_id)

        self.mapa_processado = {no_id: self.mapa_processado[no_id] for no_id in self.mapa_processado if
                                len(self.mapa_processado[no_id].nos_circundantes) > 0}  # Manter apenas nós que tenham nós circundantes

        print("Representação da área obtida")
        return

    def calcular_distancia(self, origem: Tuple[float, float], destino: Tuple[float, float]) -> float:
        """
        Tendo-se um mapa processado, retorna a distância por estrada ou ferrovia entre dois pontos
        Os pontos fornecidos são convertidos nos pontos em estrada ou ferrovia mais próximos
        :param origem:
        :param destino:
        :return: Distância calculada
        """
        if not self.mapa_processado:
            print("Não foi processado nenhum mapa")
            return 0.0

        origem_no_id: int = self._coordenadas_para_no(origem[0], origem[1]).node_id
        destino_no_id: int = self._coordenadas_para_no(destino[0], destino[1]).node_id

        # Algoritmo de Dijkstra
        nos_nao_visitados: Set[int] = set(self.mapa_processado.keys())
        distancias: Dict[int, float] = {no_id: 0 if no_id == origem_no_id else DISTANCIA_INFINITA for no_id in self.mapa_processado}
        no_actual: int = origem_no_id

        while destino_no_id in nos_nao_visitados:
            distancia_para_no: float = distancias[no_actual]
            nos_circundantes: Set[int] = self.mapa_processado[no_actual].nos_circundantes

            for no_circundante in nos_circundantes:
                if no_circundante not in nos_nao_visitados:
                    continue  # Nó já visitado - Distância mais curta já é conhecida
                coordenadas_no_actual: Tuple[float, float] = (
                    self.mapa_processado[no_actual].latitude, self.mapa_processado[no_actual].longitude)
                coordenadas_no_circundante: Tuple[float, float] = (
                    self.mapa_processado[no_circundante].latitude, self.mapa_processado[no_circundante].longitude)
                distancia_entre_nos: float = haversine.obter_distancia_haversine(coordenadas_no_actual, coordenadas_no_circundante)

                if distancia_entre_nos + distancia_para_no < distancias[no_circundante]:  # Distância obtida é menor - Actualizar
                    distancias[no_circundante] = distancia_entre_nos + distancia_para_no

            nos_nao_visitados.remove(no_actual)
            if all(distancias[no_id] == DISTANCIA_INFINITA for no_id in nos_nao_visitados) and no_actual != origem_no_id:
                break  # Se nesta fase todas as distâncias para nós não visitados sâo infinitas, esses nós são inalcançáveis - Terminar algoritmo

            menor_distancia_conhecida: float = DISTANCIA_INFINITA
            for no_id in nos_nao_visitados:
                if distancias[no_id] < menor_distancia_conhecida:
                    menor_distancia_conhecida = distancias[no_id]
                    no_actual = no_id

        distancia_para_destino: float = round(distancias[destino_no_id], 1)
        print(f'Distância entre origem e destino é {distancia_para_destino} km')

        return distancia_para_destino

    def _coordenadas_para_no(self, latitude: float, longitude: float):
        """
        Dadas coordenadas e considerando o mapa já processado, retorna o nó mais próximo das coordenadas indicadas
        O cálculo é aproximado - Usa-se o Teorema de Pitágoras em vez das distâncias de Haversine para mais rapidez
            Um grau de longitude em distância na Península Ibérica não corresponde exactamente a um grau de latitude
        """
        no_mais_proximo: Node = Node(0, 0.0, 0.0)
        distancia_pitagoras: float = 999999.0
        for no_id in self.mapa_processado:
            no: Node = self.mapa_processado[no_id]

            diferenca_latitude = abs(no.latitude - latitude)
            diferenca_longitude = abs(no.longitude - longitude)
            distancia = (diferenca_latitude ** 2 + diferenca_longitude ** 2) ** 1/2

            if distancia < distancia_pitagoras:
                no_mais_proximo = no
                distancia_pitagoras = distancia

        return no_mais_proximo


class ObterNosVias(osmium.SimpleHandler):
    """
    Dado um conjunto de coordenadas, calcula um rectângulo que contenha todos os pontos fornecidos, com uma margem
        ajustável, e obtém os pontos que estejam dentro do rectângulo e as vias com pelo menos 1 ponto no seu interior
    """
    def __init__(self, lista_coordenadas: List[Tuple[float, float]], via_tipo: str, area_tipo: str):
        super(ObterNosVias, self).__init__()

        self.nos: Dict[int, Node] = {}
        self.vias: Dict[int, Via] = {}
        self.via_tipo: str = via_tipo
        self.area_tipo: str = area_tipo
        self.tags: list = []

        self.min_latitude: float = 90.0
        self.max_latitude: float = -90.0
        self.min_longitude: float = 180.0
        self.max_longitude: float = -180.0

        # Estradas e caminhos com tags não incluídas nesta lista não costumam ser usadas no âmbito deste projecto
        # Referência: https://wiki.openstreetmap.org/wiki/Key:highway
        self.tags_estradas_pretendidas_intercidades: list = [
            'motorway', 'trunk', 'primary', 'secondary', 'motorway_link', 'trunk_link', 'primary_link', 'secondary_link',
            'motorway_junction']
        self.tags_estradas_pretendidas_urbana: list = [
            'motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified', 'residential', 'motorway_link',
            'trunk_link', 'primary_link', 'secondary_link', 'tertiary_link', 'living_street', 'service', 'motorway_junction']

        if self.area_tipo == AREA_INTERCIDADES:
            self.tags = self.tags_estradas_pretendidas_intercidades
        elif self.area_tipo == AREA_URBANA:
            self.tags = self.tags_estradas_pretendidas_urbana

        # Calcula os extremos do rectângulo
        for coordenadas in lista_coordenadas:
            latitude: float = coordenadas[0]
            longitude: float = coordenadas[1]
            if latitude < self.min_latitude:
                self.min_latitude = latitude
            if latitude > self.max_latitude:
                self.max_latitude = latitude
            if longitude < self.min_longitude:
                self.min_longitude = longitude
            if longitude > self.max_longitude:
                self.max_longitude = longitude

        # Acrescenta a margem ao rectângulo, em graus decimais
        self.min_latitude -= MARGEM_RECTANGULO_DISTANCIAS
        self.max_latitude += MARGEM_RECTANGULO_DISTANCIAS
        self.min_longitude -= MARGEM_RECTANGULO_DISTANCIAS
        self.max_longitude += MARGEM_RECTANGULO_DISTANCIAS

    def node(self, n):
        """
        Nós dentro do rectângulo desejado
        """
        if (self.min_latitude <= n.location.lat <= self.max_latitude) and \
                (self.min_longitude <= n.location.lon <= self.max_longitude):
            novo_no = Node(n.id, n.location.lat, n.location.lon)
            self.nos[n.id] = novo_no

    def way(self, w):
        """
        Vias com pelo menos um nó dentro do rectângulo desejado
        """
        # Está-se à procura de estradas e a via é uma estrada do tipo desejado OU está-se à procura de ferrovias e a via é uma ferrovia
        if self.via_tipo == VIA_ESTRADA and w.tags.get(TAG_HIGHWAY) and w.tags.get(TAG_HIGHWAY) in self.tags or \
                self.via_tipo == VIA_FERROVIA and w.tags.get(TAG_RAILWAY):
            lista_nos: List[Node] = []
            via_cruza_rectangulo: bool = False  # Via pode também estar contida no rectângulo
            for node_ref in w.nodes:
                try:
                    novo_no = Node(node_ref.ref, node_ref.lat, node_ref.lon)
                except:  # É possível para node refs não terem coordenadas - Descartar
                    continue
                lista_nos.append(novo_no)
                if (self.min_latitude <= node_ref.lat <= self.max_latitude) and \
                        (self.min_longitude <= node_ref.lon <= self.max_longitude):  # Nó está dentro do rectângulo
                    via_cruza_rectangulo = True

            if via_cruza_rectangulo:
                nova_via = Via(w.id, lista_nos)
                self.vias[w.id] = nova_via


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
    def __init__(self, via_id, lista_nos: List[Node]):
        self.via_id: int = via_id
        self.lista_nos: List[Node] = lista_nos
