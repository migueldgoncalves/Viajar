import os

import requests
import overpy

# País

ANDORRA = "AD"
ESPANHA = "ES"
GIBRALTAR = "GI"
PORTUGAL = "PT"

# Sistema

PATH_BASE = os.path.dirname(os.path.realpath(__file__))
CHAVE_API_PATH = os.path.join(PATH_BASE, '../api_key.txt')
PASTA_FICHEIROS_TEMP = os.path.join(PATH_BASE, 'tmp')
LOCAL_PATH = PASTA_FICHEIROS_TEMP + '/local.csv'
LOCAL_ESPANHA_PATH = PASTA_FICHEIROS_TEMP + '/local_espanha.csv'
LOCAL_PORTUGAL_PATH = PASTA_FICHEIROS_TEMP + '/local_portugal.csv'
MUNICIPIO_PATH = PASTA_FICHEIROS_TEMP + '/municipio.csv'
COMARCA_PATH = PASTA_FICHEIROS_TEMP + '/comarca.csv'

# Níveis administractivos do OpenStreetMap

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
ENTIDADE_INTERMUNICIPAL = 5  # Nos Açores e na Madeira identificam ilhas
DISTRITO_PT = 6
CONCELHO = 7
FREGUESIA = 8
ANTIGA_FREGUESIA = 9  # Existe dentro de uniões de antigas freguesias

# Auto-estradas

ES_A49 = ("A-49", "Autopista del Quinto Centenario", ESPANHA)
ES_A5 = ("A-5", "Autovía del Suroeste", ESPANHA)
ES_M40 = ("M-40", "Autopista de Circunvalación M-40", ESPANHA)
PT_A2 = ("A2", "Autoestrada do Sul", PORTUGAL)
PT_A5 = ("A5", "Autoestrada da Costa do Estoril", PORTUGAL)

# Linhas ferroviárias

LINHA_DO_NORTE = ("Linha do Norte", PORTUGAL)

"""
Gera ficheiros .csv com informação de saídas de auto-estradas
"""


class GeradorInformacao:

    def __init__(self):
        self.api = overpy.Overpass()
        with open(CHAVE_API_PATH, 'r') as f:
            self.api_key = f.readlines()[0]

    def create_locais_ficheiros(self, auto_estrada_tuplo):
        auto_estrada_numero = self.get_auto_estrada_numero(auto_estrada_tuplo)
        saidas = self.get_auto_estradas_saidas(auto_estrada_tuplo)
        saidas_ordenadas = list(saidas.keys())
        saidas_ordenadas.sort()

        if not os.path.exists(PASTA_FICHEIROS_TEMP):
            os.makedirs(PASTA_FICHEIROS_TEMP)

        with open(os.path.join(LOCAL_PATH), 'w') as f:
            for saida in saidas_ordenadas:
                latitude = saidas[saida][0]
                longitude = saidas[saida][1]
                altitude = self.get_altitude(latitude, longitude)
                f.write(f'{auto_estrada_numero} - Saída {saida},{latitude},{longitude},{altitude},\n')

        if self.get_auto_estrada_pais(auto_estrada_tuplo) == ESPANHA:
            municipios = set()
            with open(LOCAL_ESPANHA_PATH, 'w') as f:
                for saida in saidas_ordenadas:
                    latitude = saidas[saida][0]
                    longitude = saidas[saida][1]
                    municipio = self.get_divisao_administractiva(latitude, longitude, MUNICIPIO)
                    provincia = self.get_divisao_administractiva(latitude, longitude, PROVINCIA)
                    f.write(f'{auto_estrada_numero} - Saída {saida},{municipio},{provincia}\n')
                    municipios.add(f'{municipio},{provincia},\n')
                    print(f'Saída {saida} terminada')
            with open(MUNICIPIO_PATH, 'w') as f:
                for municipio in municipios:
                    f.write(municipio)

        elif self.get_auto_estrada_pais(auto_estrada_tuplo) == PORTUGAL:
            with open(LOCAL_PORTUGAL_PATH, 'w') as f:
                for saida in saidas_ordenadas:
                    latitude = saidas[saida][0]
                    longitude = saidas[saida][1]
                    freguesia = self.get_divisao_administractiva(latitude, longitude, ANTIGA_FREGUESIA)
                    if not freguesia:  # Freguesia já existia antes de 2013
                        freguesia = self.get_divisao_administractiva(latitude, longitude, FREGUESIA)
                    concelho = self.get_divisao_administractiva(latitude, longitude, CONCELHO)
                    f.write(f'{auto_estrada_numero} - Saída {saida},{freguesia},{concelho}\n')
                    print(f'Saída {saida} terminada')

    def get_altitude(self, latitude, longitude):
        url = f'https://maps.googleapis.com/maps/api/elevation/json?locations={latitude},{longitude}&key={self.api_key}'
        return int(requests.get(url=url).json()['results'][0]['elevation'])

    def get_divisao_administractiva(self, latitude, longitude, divisao):
        result = self.api.query(f'is_in({latitude},{longitude});relation(pivot)[admin_level = {divisao}];(._;>;);out;')
        try:
            return result.relations[0].tags['name']
        except IndexError:
            return None

    def get_auto_estradas_saidas(self, auto_estrada_tuplo):
        auto_estrada_nome = self.get_auto_estrada_nome(auto_estrada_tuplo)

        saidas_temp = {}
        resultado = self.api.query(f'relation["name"="{auto_estrada_nome}"];(._;>;);out;')
        for node in resultado.nodes:
            if len(node.tags) > 0:
                if node.tags.__contains__('highway') and node.tags['highway'] == 'motorway_junction':
                    if node.tags.__contains__('ref'):
                        saida_numero = node.tags['ref']
                        if saida_numero not in saidas_temp:
                            saidas_temp[saida_numero] = []
                        saidas_temp[saida_numero].append((float(node.lat), float(node.lon)))
        saidas = {}
        for saida in saidas_temp:
            latitude = 0.0
            longitude = 0.0
            for coordenadas in saidas_temp[saida]:
                latitude += coordenadas[0]
                longitude += coordenadas[1]
            latitude = round(latitude / len(saidas_temp[saida]), 6)
            longitude = round(longitude / len(saidas_temp[saida]), 6)
            saidas[saida] = (latitude, longitude)
        return saidas

    def get_auto_estrada_numero(self, tuplo):
        return tuplo[0]  # Ex: A-5

    def get_auto_estrada_nome(self, tuplo):  # De acordo com o OpenStreetMap
        return tuplo[1]  # Ex: Autovía del Suroeste

    def get_auto_estrada_pais(self, tuplo):
        return tuplo[2]  # Ex: ES


GeradorInformacao().create_locais_ficheiros(ES_A5)
