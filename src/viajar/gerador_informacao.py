import os

import requests
import overpy

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
GIBRALTAR = 4

# Portugal
ENTIDADE_INTERMUNICIPAL = 5  # Nos Açores e na Madeira identificam ilhas
DISTRITO_PT = 6
CONCELHO = 7
FREGUESIA = 8
ANTIGA_FREGUESIA = 9  # Existe dentro de uniões de antigas freguesias

# Auto-estradas

ES_A5 = ("A-5", "Autovía del Suroeste")
ES_M40 = ("M-40", "Autopista de Circunvalación M-40")
PT_A5 = ("A5", "Autoestrada da Costa do Estoril")

# Linhas ferroviárias

LINHA_DO_NORTE = "Linha do Norte"

"""
Gera ficheiros .csv com informação de saídas de auto-estradas
"""


class GeradorInformacao:

    def __init__(self):
        self.api = overpy.Overpass()
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../api_key.txt'), 'r') as f:
            self.api_key = f.readlines()[0]

    def create_locais_ficheiro(self, auto_estrada_tuplo):
        auto_estrada_numero = self.get_auto_estrada_numero(auto_estrada_tuplo)
        saidas = self.get_auto_estradas_saidas(auto_estrada_tuplo)
        saidas_ordenadas = list(saidas.keys())
        saidas_ordenadas.sort()

        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'local.csv'), 'w') as f:
            for saida in saidas_ordenadas:
                latitude = saidas[saida][0]
                longitude = saidas[saida][1]
                altitude = self.get_altitude(latitude, longitude)
                f.write(f'{auto_estrada_numero} - Saída {saida},{latitude},{longitude},{altitude},\n')
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'local_divisoes.csv'), 'w') as f:
            for saida in saidas_ordenadas:
                latitude = saidas[saida][0]
                longitude = saidas[saida][1]
                freguesia = self.get_divisao_administractiva(latitude, longitude, FREGUESIA)
                concelho = self.get_divisao_administractiva(latitude, longitude, CONCELHO)
                f.write(f'{auto_estrada_numero} - Saída {saida},{freguesia},{concelho}\n')
                print(f'Terminada saída {saida}')
                # TODO - Caso espanhol

    def get_altitude(self, latitude, longitude):
        url = f'https://maps.googleapis.com/maps/api/elevation/json?locations={latitude},{longitude}&key={self.api_key}'
        return int(requests.get(url=url).json()['results'][0]['elevation'])

    def get_divisao_administractiva(self, latitude, longitude, divisao):
        result = self.api.query(f'is_in({latitude},{longitude});relation(pivot)[admin_level = {divisao}];(._;>;);out;')
        return result.relations[0].tags['name']

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
            latitude = round(latitude / len(saidas_temp[saida]), 7)
            longitude = round(longitude / len(saidas_temp[saida]), 7)
            saidas[saida] = (latitude, longitude)
        return saidas

    def get_auto_estrada_numero(self, tuplo):
        return tuplo[0]  # Ex: A-5

    def get_auto_estrada_nome(self, tuplo):
        return tuplo[1]  # Ex: Autovía del Suroeste


GeradorInformacao().create_locais_ficheiro(PT_A5)
