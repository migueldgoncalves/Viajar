import os
import time

import requests
import overpy

import viajar.vias as vias
import viajar.ordenador as ordenador

# Inserir aqui auto-estrada para ser analisada pelo gerador
AUTO_ESTRADA_PARA_ANALISAR = vias.ES_GR30

PATH_BASE = os.path.dirname(os.path.realpath(__file__))
NOME_AUTO_ESTRADA = AUTO_ESTRADA_PARA_ANALISAR[0]
CHAVE_API_PATH = os.path.join(PATH_BASE, '../api_key.txt')
PASTA_FICHEIROS_TEMP = os.path.join(PATH_BASE, 'tmp')

LOCAL_PATH = os.path.join(PASTA_FICHEIROS_TEMP, f'{NOME_AUTO_ESTRADA}_local.csv')
LOCAL_ESPANHA_PATH = os.path.join(PASTA_FICHEIROS_TEMP, f'{NOME_AUTO_ESTRADA}_local_espanha.csv')
LOCAL_PORTUGAL_PATH = os.path.join(PASTA_FICHEIROS_TEMP, f'{NOME_AUTO_ESTRADA}_local_portugal.csv')
MUNICIPIO_PATH = os.path.join(PASTA_FICHEIROS_TEMP, f'{NOME_AUTO_ESTRADA}_municipio.csv')
COMARCA_PATH = os.path.join(PASTA_FICHEIROS_TEMP, f'/{NOME_AUTO_ESTRADA}_comarca.csv')
CONCELHO_PATH = os.path.join(PASTA_FICHEIROS_TEMP, f'{NOME_AUTO_ESTRADA}_concelho.csv')

COORDENADAS_CASAS_DECIMAIS = 6
ENCODING = 'utf-8'

"""
Gera ficheiros .csv com informação de saídas de auto-estradas
"""


class GeradorInformacao:

    def __init__(self):
        self.api = overpy.Overpass()
        with open(CHAVE_API_PATH, 'r', encoding=ENCODING) as f:
            self.api_key = f.readlines()[0]

    def create_ficheiros(self, auto_estrada_tuplo):
        auto_estrada_numero = self.get_auto_estrada_numero(auto_estrada_tuplo)

        print("################")
        print(f'A iniciar processamento da auto-estrada {auto_estrada_numero}...')
        print("################")

        saidas = self.get_auto_estradas_saidas(auto_estrada_tuplo)
        saidas_ordenadas = list(saidas.keys())
        saidas_ordenadas.sort()

        print(f'{len(saidas_ordenadas)} saídas encontradas')
        if len(saidas_ordenadas) == 0:
            print("Processamento cancelado")
            exit(1)

        if not os.path.exists(PASTA_FICHEIROS_TEMP):
            os.makedirs(PASTA_FICHEIROS_TEMP)

        with open(os.path.join(LOCAL_PATH), 'w', encoding=ENCODING) as f:
            for saida in saidas_ordenadas:
                latitude = saidas[saida][0]
                longitude = saidas[saida][1]
                altitude = self.get_altitude(latitude, longitude)
                f.write(f'{auto_estrada_numero} - Saída {saida},{latitude},{longitude},{altitude},\n')
        ordenador.ordenar_ficheiros_csv(ficheiro_a_ordenar=LOCAL_PATH, cabecalho=False)
        print(f'Ficheiro de locais criado')

        saidas_terminadas = 0

        if self.get_auto_estrada_pais(auto_estrada_tuplo) == vias.ESPANHA:
            municipios = set()
            comarcas = set()

            with open(LOCAL_ESPANHA_PATH, 'w', encoding=ENCODING) as f:
                for saida in saidas_ordenadas:
                    latitude = saidas[saida][0]
                    longitude = saidas[saida][1]

                    municipio = self.get_divisao_administractiva(latitude, longitude, vias.MUNICIPIO)
                    time.sleep(1)

                    provincia = self.get_divisao_administractiva(latitude, longitude, vias.PROVINCIA)
                    time.sleep(1)

                    comarca = self.get_divisao_administractiva(latitude, longitude, vias.COMARCA)
                    time.sleep(1)

                    distrito_es = self.get_divisao_administractiva(latitude, longitude, vias.DISTRITO_ES)
                    time.sleep(1)

                    if distrito_es:
                        f.write(f'{auto_estrada_numero} - Saída {saida},{municipio},{provincia},{distrito_es}\n')
                    else:
                        f.write(f'{auto_estrada_numero} - Saída {saida},{municipio},{provincia},\n')

                    municipios.add(f'{municipio},{provincia}\n')
                    if comarca:
                        comarcas.add(f'{municipio},{comarca},{provincia}\n')

                    saidas_terminadas += 1
                    print(f'Saída {saida} terminada - {saidas_terminadas}/{len(saidas_ordenadas)} saídas processadas')

            with open(MUNICIPIO_PATH, 'w', encoding=ENCODING) as f:
                for municipio in municipios:
                    f.write(municipio)

            with open(COMARCA_PATH, 'w', encoding=ENCODING) as f:
                for comarca in comarcas:
                    f.write(comarca)

            ordenador.ordenar_ficheiros_csv(ficheiro_a_ordenar=LOCAL_ESPANHA_PATH, cabecalho=False)
            print("Ficheiro de locais de Espanha terminado")
            ordenador.ordenar_ficheiros_csv(ficheiro_a_ordenar=MUNICIPIO_PATH, cabecalho=False)
            print("Ficheiro de municípios terminado")
            ordenador.ordenar_ficheiros_csv(ficheiro_a_ordenar=COMARCA_PATH, cabecalho=False)
            print("Ficheiro de comarcas terminado")

        elif self.get_auto_estrada_pais(auto_estrada_tuplo) == vias.PORTUGAL:
            concelhos = set()

            with open(LOCAL_PORTUGAL_PATH, 'w', encoding=ENCODING) as f:
                for saida in saidas_ordenadas:
                    latitude = saidas[saida][0]
                    longitude = saidas[saida][1]

                    freguesia = self.get_divisao_administractiva(latitude, longitude, vias.ANTIGA_FREGUESIA)
                    time.sleep(1)
                    if not freguesia:  # Freguesia já existia antes de 2013
                        freguesia = self.get_divisao_administractiva(latitude, longitude, vias.FREGUESIA)
                        time.sleep(1)

                    concelho = self.get_divisao_administractiva(latitude, longitude, vias.CONCELHO)
                    time.sleep(1)

                    entidade_intermunicipal = self.get_divisao_administractiva(latitude, longitude, vias.ENTIDADE_INTERMUNICIPAL)
                    time.sleep(1)

                    distrito = self.get_divisao_administractiva(latitude, longitude, vias.DISTRITO_PT)
                    time.sleep(1)

                    f.write(f'{auto_estrada_numero} - Saída {saida},{freguesia},{concelho}\n')

                    concelhos.add(f'{concelho},{entidade_intermunicipal},{distrito},\n')  # OSM não fornece a região histórica

                    saidas_terminadas += 1
                    print(f'Saída {saida} terminada - {saidas_terminadas}/{len(saidas_ordenadas)} saídas processadas')

            with open(CONCELHO_PATH, 'w', encoding=ENCODING) as f:
                for concelho in concelhos:
                    f.write(concelho)

            ordenador.ordenar_ficheiros_csv(ficheiro_a_ordenar=LOCAL_PORTUGAL_PATH, cabecalho=False)
            print("Ficheiro de locais de Portugal terminado")
            ordenador.ordenar_ficheiros_csv(ficheiro_a_ordenar=CONCELHO_PATH, cabecalho=False)
            print("Ficheiro de concelhos terminado")

        else:
            pass

        print(f'Auto-estrada {auto_estrada_numero} processada')

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
            latitude = round(latitude / len(saidas_temp[saida]), COORDENADAS_CASAS_DECIMAIS)
            longitude = round(longitude / len(saidas_temp[saida]), COORDENADAS_CASAS_DECIMAIS)
            saidas[saida] = (latitude, longitude)
        return saidas

    def get_auto_estrada_numero(self, tuplo):
        return tuplo[0]  # Ex: A-5

    def get_auto_estrada_nome(self, tuplo):  # De acordo com o OpenStreetMap
        return tuplo[1]  # Ex: Autovía del Suroeste

    def get_auto_estrada_pais(self, tuplo):
        return tuplo[2]  # Ex: ES
