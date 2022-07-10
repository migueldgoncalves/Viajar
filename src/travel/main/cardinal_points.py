"""
Wrapper module for cardinal point constants and utils
"""

NORTE = "N"
NORDESTE = "NE"
ESTE = "E"
SUDESTE = "SE"
SUL = "S"
SUDOESTE = "SO"
OESTE = "O"
NOROESTE = "NO"


def obter_ponto_cardeal_oposto(cardinal_point: str) -> str:
    if cardinal_point == NORTE:
        return SUL
    elif cardinal_point == NORDESTE:
        return SUDOESTE
    elif cardinal_point == ESTE:
        return OESTE
    elif cardinal_point == SUDESTE:
        return NOROESTE
    elif cardinal_point == SUL:
        return NORTE
    elif cardinal_point == SUDOESTE:
        return NORDESTE
    elif cardinal_point == OESTE:
        return ESTE
    elif cardinal_point == NOROESTE:
        return SUDESTE
    else:
        return ''
