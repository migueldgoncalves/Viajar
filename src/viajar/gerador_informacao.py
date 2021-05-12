import os

import requests
import overpy

import vias

# Inserir aqui auto-estrada para ser analisada pelo gerador
AUTO_ESTRADA_PARA_ANALISAR = vias.ES_EXA1

PATH_BASE = os.path.dirname(os.path.realpath(__file__))
NOME_AUTO_ESTRADA = AUTO_ESTRADA_PARA_ANALISAR[0]
CHAVE_API_PATH = os.path.join(PATH_BASE, '../api_key.txt')
PASTA_FICHEIROS_TEMP = os.path.join(PATH_BASE, 'tmp')
LOCAL_PATH = PASTA_FICHEIROS_TEMP + f'/{NOME_AUTO_ESTRADA}_local.csv'
LOCAL_ESPANHA_PATH = PASTA_FICHEIROS_TEMP + f'/{NOME_AUTO_ESTRADA}_local_espanha.csv'
LOCAL_PORTUGAL_PATH = PASTA_FICHEIROS_TEMP + f'/{NOME_AUTO_ESTRADA}_local_portugal.csv'
MUNICIPIO_PATH = PASTA_FICHEIROS_TEMP + f'/{NOME_AUTO_ESTRADA}_municipio.csv'
COMARCA_PATH = PASTA_FICHEIROS_TEMP + f'/{NOME_AUTO_ESTRADA}_comarca.csv'

"""
Gera ficheiros .csv com informação de saídas de auto-estradas
"""


class GeradorInformacao:

    def __init__(self):
        self.api = overpy.Overpass()
        with open(CHAVE_API_PATH, 'r') as f:
            self.api_key = f.readlines()[0]

    def create_ficheiros(self, auto_estrada_tuplo):
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

        if self.get_auto_estrada_pais(auto_estrada_tuplo) == vias.ESPANHA:
            municipios = set()
            with open(LOCAL_ESPANHA_PATH, 'w') as f:
                for saida in saidas_ordenadas:
                    latitude = saidas[saida][0]
                    longitude = saidas[saida][1]
                    municipio = self.get_divisao_administractiva(latitude, longitude, vias.MUNICIPIO)
                    provincia = self.get_divisao_administractiva(latitude, longitude, vias.PROVINCIA)
                    f.write(f'{auto_estrada_numero} - Saída {saida},{municipio},{provincia}\n')
                    municipios.add(f'{municipio},{provincia},\n')
                    print(f'Saída {saida} terminada')
            # with open(MUNICIPIO_PATH, 'w') as f:
            #     for municipio in municipios:
            #         f.write(municipio)

        elif self.get_auto_estrada_pais(auto_estrada_tuplo) == vias.PORTUGAL:
            with open(LOCAL_PORTUGAL_PATH, 'w') as f:
                for saida in saidas_ordenadas:
                    latitude = saidas[saida][0]
                    longitude = saidas[saida][1]
                    freguesia = self.get_divisao_administractiva(latitude, longitude, vias.ANTIGA_FREGUESIA)
                    if not freguesia:  # Freguesia já existia antes de 2013
                        freguesia = self.get_divisao_administractiva(latitude, longitude, vias.FREGUESIA)
                    concelho = self.get_divisao_administractiva(latitude, longitude, vias.CONCELHO)
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
        if len(resultado.nodes) == 0:
            # Auto-estradas mais pequenas não têm associada uma relação no OSM, são um conjunto de vias com o mesmo nome
            resultado = self.api.query(f'way["name"="{auto_estrada_nome}"];(._;>;);out;')
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


GeradorInformacao().create_ficheiros(AUTO_ESTRADA_PARA_ANALISAR)
