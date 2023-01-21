import travel.support.haversine as haversine
import travel.support.osm_interface as osm_interface
from travel.support.coordinates import Coordinates

"""
Este módulo destina-se a calcular distâncias por estrada ou ferrovia entre dois pontos
Suporta 3 modos de funcionamento:
    -Distâncias dentro da mesma estrada/ferrovia
    -Distâncias dentro de uma dada área, tendo em conta as estradas mais importantes
    -Distâncias dentro de uma área urbana, tendo em conta mais ruas e estradas
"""

AVISO_TAMANHO_AREA_INTERCIDADES = 100
AVISO_TAMANHO_AREA_URBANA = 10

DISTANCIA_INFINITA: int = 999999  # km

# Ajuste feito às coordenadas para se tentar obter a distância mais curta
AJUSTE_COORDENADAS = 0.0005  # 0.001 graus = muito aproximadamente 100 metros na Península Ibérica


class CalculadoraDistancias:
    """
    Classe principal para o cálculo de distâncias
    Como usar:
        Primeiro gerar o mapa processado OU processar a estrada/ferrovia com o nome desejado
        Depois correr o algoritmo de Dijkstra para quantos pares (origem, destino) se queira
    """
    def __init__(self) -> None:
        self.mapa_processado: dict[int, osm_interface.OsmNode] = {}

    def gerar_mapa_processado(self, lista_coordenadas: list[Coordinates], via_tipo: str, pais: str,
                              detalhe_area: int = None, via_nome: str = None) -> None:
        """
        Cria um mapa que contém todas as coordenadas fornecidas, adequado para se correr nele o algoritmo de Dijkstra
        :param lista_coordenadas: As coordenadas a incluir no mapa
        :param via_tipo: Se a via é uma estrada ou uma ferrovia
        :param pais: País da área ou via a processar
        :param detalhe_area: Facultativo - Nível de detalhe da área a cobrir. Quanto mais detalhe, mais estradas se consideram
            Com menos detalhe cobrem-se apenas as estradas principais
            Um detalhe elevado é adequado para cobrir ruas dentro da mesma cidade. Evitar usar para áreas com mais de
                alguns quilómetros quadrados, ou o processamento será muito lento
            A área não é tida em conta para ferrovias, nem se se fornecer o nome da via
        :param via_nome: Facultativo - Nome da via (Ex: Linha do Norte). Se for fornecido, só se considerará essa via
            Fornecer nome de via em vez do detalhe da área se se desejar cobrir uma única estrada ou ferrovia
        :return:
        """
        if not via_nome and not detalhe_area:
            print("Não se forneceu nome da via nem detalhe da área a processar - A sair")
            exit(1)

        print("A obter representação da área...")

        if detalhe_area:  # Pretende-se cobrir uma área
            lista_nos, vias_a_considerar, area_extremos = osm_interface.OsmInterface.process_area_for_distance_calculation(
                lista_coordenadas, via_tipo, detalhe_area, pais)

            min_latitude: float = area_extremos[0]
            max_latitude: float = area_extremos[1]
            min_longitude: float = area_extremos[2]
            max_longitude: float = area_extremos[3]

            distancia_norte_sul = round(
                haversine.obter_distancia_haversine((min_latitude, min_longitude), (max_latitude, min_longitude)), 1)
            distancia_este_oeste = round(
                haversine.obter_distancia_haversine((min_latitude, min_longitude), (min_latitude, max_longitude)), 1)
            print(f"A área de interesse tem {distancia_norte_sul} km norte-sul e {distancia_este_oeste} km este-oeste")

            if detalhe_area == osm_interface.DETAIL_LEVEL_INTERCITY and distancia_norte_sul * distancia_este_oeste > AVISO_TAMANHO_AREA_INTERCIDADES ** 2 or \
                    detalhe_area == osm_interface.DETAIL_LEVEL_URBAN and distancia_norte_sul * distancia_este_oeste > AVISO_TAMANHO_AREA_URBANA ** 2:
                print("Aviso: A área a cobrir é muito grande - Esta operação poderá ser muito demorada")

            # Assim que se receber os nós circundantes, haverá toda a informação para se correr o algoritmo de Dijkstra
            self.mapa_processado: dict[int, osm_interface.OsmNode] = lista_nos

        else:  # Pretende-se cobrir uma estrada/ferrovia individual

            # Assim que se receber os nós circundantes, haverá toda a informação para se correr o algoritmo de Dijkstra
            retorno = osm_interface.OsmInterface.process_way_for_distance_calculation(via_nome, pais)
            self.mapa_processado: dict[int, osm_interface.OsmNode] = retorno[0]

            vias_a_considerar: dict[int, osm_interface.OsmWay] = retorno[1]
            min_latitude: float = -90.0  # As coordenadas neste caso não serão consideradas
            max_latitude: float = 90.0
            min_longitude: float = -180.0
            max_longitude: float = 180.0

        # Adicionar nós circundantes
        print("A adicionar informação de nós circundantes...")
        for via_id in vias_a_considerar:
            via: osm_interface.OsmWay = vias_a_considerar[via_id]
            if len(via.node_list) <= 1:
                continue
            for index, no in enumerate(via.node_list):  # Todos os nós da via, estejam ou não no rectângulo desejado
                if index == 0:
                    no_seguinte: osm_interface.OsmNode = via.node_list[1]
                    if (min_latitude <= no_seguinte.latitude <= max_latitude) and \
                            (min_longitude <= no_seguinte.longitude <= max_longitude):  # Nó circundante está dentro do rectângulo
                        if self.mapa_processado.get(no.node_id, None):
                            self.mapa_processado[no.node_id].surrounding_node_ids.add(no_seguinte.node_id)
                elif index == len(via.node_list) - 1:  # Último nó da via
                    no_anterior: osm_interface.OsmNode = via.node_list[index - 1]
                    if (min_latitude <= no_anterior.latitude <= max_latitude) and \
                            (min_longitude <= no_anterior.longitude <= max_longitude):  # Nó circundante está dentro do rectângulo
                        if self.mapa_processado.get(no.node_id, None):
                            self.mapa_processado[no.node_id].surrounding_node_ids.add(no_anterior.node_id)
                else:  # Nó a meio da via
                    no_seguinte: osm_interface.OsmNode = via.node_list[index + 1]
                    if (min_latitude <= no_seguinte.latitude <= max_latitude) and \
                            (min_longitude <= no_seguinte.longitude <= max_longitude):  # Nó circundante está dentro do rectângulo
                        if self.mapa_processado.get(no.node_id, None):
                            self.mapa_processado[no.node_id].surrounding_node_ids.add(no_seguinte.node_id)
                    no_anterior: osm_interface.OsmNode = via.node_list[index - 1]
                    if (min_latitude <= no_anterior.latitude <= max_latitude) and \
                            (min_longitude <= no_anterior.longitude <= max_longitude):  # Nó circundante está dentro do rectângulo
                        if self.mapa_processado.get(no.node_id, None):
                            self.mapa_processado[no.node_id].surrounding_node_ids.add(no_anterior.node_id)

        self.mapa_processado = {no_id: self.mapa_processado[no_id] for no_id in self.mapa_processado if
                                len(self.mapa_processado[no_id].surrounding_node_ids) > 0}  # Manter apenas nós que tenham nós circundantes

        print("Representação da área obtida")
        return

    def calcular_distancia_com_ajustes(self, origem: Coordinates, destino: Coordinates, menos_verificacoes=True) -> float:
        """
        Repete o cálculo das distâncias ajustando ligeiramente as coordenadas de origem e destino. Permite superar o
            haver duas vias OSM paralelas numa mesma auto-estrada, por exemplo
        Destina-se sobretudo ao cálculo de distâncias dentro de uma mesma estrada/ferrovia
        """
        def _calcular_distancia_com_ajustes(origem: Coordinates, destino: Coordinates,
                                            ajuste_1: float, ajuste_2: float, ajuste_3: float, ajuste_4: float,
                                            verboso=False):
            latitude_origem = origem.latitude + ajuste_1
            longitude_origem = origem.longitude + ajuste_2
            latitude_destino = destino.latitude + ajuste_3
            longitude_destino = destino.longitude + ajuste_4

            origem = Coordinates(latitude_origem, longitude_origem)
            destino = Coordinates(latitude_destino, longitude_destino)

            distancia: float = self.calcular_distancia(origem, destino, verboso=verboso)
            return distancia

        if menos_verificacoes:  # 9 verificações
            for ajuste_1 in [-AJUSTE_COORDENADAS, 0, AJUSTE_COORDENADAS]:
                for ajuste_2 in [-AJUSTE_COORDENADAS, 0, AJUSTE_COORDENADAS]:
                    distancia: float = _calcular_distancia_com_ajustes(origem, destino, ajuste_1, ajuste_1, ajuste_2, ajuste_2, verboso=False)
                    if distancia < DISTANCIA_INFINITA:
                        return distancia
        else:  # 81 verificações
            for ajuste_1 in [-AJUSTE_COORDENADAS, 0, AJUSTE_COORDENADAS]:
                for ajuste_2 in [-AJUSTE_COORDENADAS, 0, AJUSTE_COORDENADAS]:
                    for ajuste_3 in [-AJUSTE_COORDENADAS, 0, AJUSTE_COORDENADAS]:
                        for ajuste_4 in [-AJUSTE_COORDENADAS, 0, AJUSTE_COORDENADAS]:
                            distancia: float = _calcular_distancia_com_ajustes(origem, destino, ajuste_1, ajuste_2, ajuste_3, ajuste_4, verboso=False)
                            if distancia < DISTANCIA_INFINITA:
                                return distancia

        return DISTANCIA_INFINITA

    def calcular_distancia(self, origem: Coordinates, destino: Coordinates, verboso: bool = True) -> float:
        """
        Tendo-se um mapa processado, retorna a distância por estrada ou ferrovia entre dois pontos
        Os pontos fornecidos são convertidos nos pontos em estrada ou ferrovia mais próximos
        :param origem:
        :param destino:
        :param verboso:
        :return: Distância calculada
        """
        if not self.mapa_processado:
            if verboso:
                print("Não foi processado nenhum mapa")
            return 0.0

        origem_no_id: int = self._coordenadas_para_no(origem).node_id
        destino_no_id: int = self._coordenadas_para_no(destino).node_id

        # Algoritmo de Dijkstra
        nos_nao_visitados: set[int] = set(self.mapa_processado.keys())
        distancias: dict[int, float] = {no_id: 0 if no_id == origem_no_id else DISTANCIA_INFINITA for no_id in self.mapa_processado}
        no_actual: int = origem_no_id

        while destino_no_id in nos_nao_visitados:
            distancia_para_no: float = distancias[no_actual]
            nos_circundantes: set[int] = self.mapa_processado[no_actual].surrounding_node_ids

            for no_circundante in nos_circundantes:
                if no_circundante not in nos_nao_visitados:
                    continue  # Nó já visitado - Distância mais curta já é conhecida
                coordenadas_no_actual: tuple[float, float] = (
                    self.mapa_processado[no_actual].latitude, self.mapa_processado[no_actual].longitude)
                coordenadas_no_circundante: tuple[float, float] = (
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
        if verboso:
            print(f'Distância entre origem e destino é {distancia_para_destino} km')

        return distancia_para_destino

    def _coordenadas_para_no(self, coordenadas: Coordinates):
        """
        Dadas coordenadas e considerando o mapa já processado, retorna o nó mais próximo das coordenadas indicadas
        O cálculo é aproximado - Usa-se o Teorema de Pitágoras em vez das distâncias de Haversine para mais rapidez
            Um grau de longitude em distância na Península Ibérica não corresponde exactamente a um grau de latitude
        """
        no_mais_proximo: osm_interface.OsmNode = osm_interface.OsmNode(0, 0.0, 0.0)
        distancia_pitagoras: float = DISTANCIA_INFINITA
        for no_id in self.mapa_processado:
            no: osm_interface.OsmNode = self.mapa_processado[no_id]

            diferenca_latitude = abs(no.latitude - coordenadas.latitude)
            diferenca_longitude = abs(no.longitude - coordenadas.longitude)
            distancia = (diferenca_latitude ** 2 + diferenca_longitude ** 2) ** 1/2

            if distancia < distancia_pitagoras:
                no_mais_proximo = no
                distancia_pitagoras = distancia

        return no_mais_proximo
