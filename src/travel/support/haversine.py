from math import sin, cos, sqrt, asin, pi

from travel.main.cardinal_points import NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH, SOUTHWEST, WEST, NORTHWEST

RAIO_TERRA = 6371  # km


def obter_ponto_cardeal(origem: (float, float), destino: (float, float)) -> str:
    """
    Dada uma origem e um destino, retorna o ponto cardeal do destino em relação à origem
    Ex: Se origem = (39.0, 0.0) e destino = (40.0, 0.0), retorno será "N"
    :param origem: Coordenadas decimais
    :param destino: Idem
    :return: Abreviatura do ponto cardeal, ou "" se origem e destino forem iguais
    """
    if origem == destino:  # Mesmo ponto
        return ""

    distancia_norte_sul: float = obter_distancia_haversine((origem[0], 0), (destino[0], 0))  # Será sempre >= 0
    distancia_este_oeste: float = obter_distancia_haversine((0, origem[1]), (0, destino[1]))  # Será sempre >= 0

    diff_lat: float = float(destino[0]) - float(origem[0])
    diff_lon: float = float(destino[1]) - float(origem[1])

    if diff_lat == 0:
        if diff_lon > 0:
            return EAST
        elif diff_lon < 0:
            return WEST
    elif diff_lon == 0:
        if diff_lat > 0:
            return NORTH
        elif diff_lat < 0:
            return SOUTH
    elif diff_lat == diff_lon:
        if diff_lat > 0 and diff_lon > 0:
            return NORTHEAST
        elif diff_lat < 0 and diff_lon > 0:
            return SOUTHEAST
        elif diff_lat < 0 and diff_lon < 0:
            return SOUTHWEST
        elif diff_lat > 0 and diff_lon < 0:
            return NORTHWEST
    else:
        if diff_lat > 0 and diff_lon > 0:  # N, NE, E
            if abs(distancia_norte_sul) > 2 * abs(distancia_este_oeste):
                return NORTH
            elif abs(distancia_norte_sul) < 0.5 * abs(distancia_este_oeste):
                return EAST
            else:
                return NORTHEAST
        elif diff_lat < 0 and diff_lon > 0:  # E, SE, S
            if abs(distancia_norte_sul) > 2 * abs(distancia_este_oeste):
                return SOUTH
            elif abs(distancia_norte_sul) < 0.5 * abs(distancia_este_oeste):
                return EAST
            else:
                return SOUTHEAST
        elif diff_lat < 0 and diff_lon < 0:  # S, SO, O
            if abs(distancia_norte_sul) > 2 * abs(distancia_este_oeste):
                return SOUTH
            elif abs(distancia_norte_sul) < 0.5 * abs(distancia_este_oeste):
                return WEST
            else:
                return SOUTHWEST
        elif diff_lat > 0 and diff_lon < 0:  # O, NO, N
            if abs(distancia_norte_sul) > 2 * abs(distancia_este_oeste):
                return NORTH
            elif abs(distancia_norte_sul) < 0.5 * abs(distancia_este_oeste):
                return WEST
            else:
                return NORTHWEST

    return ""


def obter_distancia_haversine(origem: (float, float), destino: (float, float)) -> float:
    """
    Retorna distância em linha recta em km entre origem e destino. Erro até 0.5%
    """
    def _para_radianos(decimal: float) -> float:
        return decimal * pi / 180

    latitude_origem, longitude_destino = origem
    latitude_destino, longitude_destino = destino
    diff_lat: float = float(destino[0]) - float(origem[0])
    diff_lon: float = float(destino[1]) - float(origem[1])

    parametro_1: float = sin(_para_radianos(diff_lat / 2)) ** 2
    parametro_2: float = cos(_para_radianos(float(latitude_origem))) * cos(_para_radianos(float(latitude_destino))) * (
            sin(_para_radianos(diff_lon / 2)) ** 2)
    distancia: float = 2 * RAIO_TERRA * asin(sqrt(parametro_1 + parametro_2))

    return distancia
