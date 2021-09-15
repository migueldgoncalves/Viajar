#!/usr/bin/env python3

try:
    import osmium
    import shapely.wkb as wkblib
    from shapely.geometry import Point, MultiPolygon, LineString, Polygon
except:
    print("Bibliotecas osmium e/ou shapely não instaladas. Está a executar este ficheiro em Windows?")
    exit(1)

FILE_GIBRALTAR = 'osm/gibraltar-latest.osm.pbf'
FILE_PORTUGAL = 'osm/portugal-latest.osm.pbf'
FILE_SPAIN = 'osm/spain-latest.osm.pbf'

TIPO_NO = "n"  # Node
TIPO_VIA = "w"  # Way
TIPO_RELACAO = "r"  # Relation

MOTORWAY_JUNCTION = 'motorway_junction'
FREGUESIA_HISTORICA = 'historic_parish'

# A global factory that creates WKB from a osmium geometry
wkbfab = osmium.geom.WKBFactory()

#Como resolver isto:

#3 iterações do ficheiro

#1 - Descobrir nós associados a saídas da auto-estrada
#Percorrer 1º as relations e depois as ways em busca dos nós da autoestrada
#Guardar num set do faulthandler

#2 - Descobrir quais as saídas da auto-estrada e suas coordenadas
#Percorrer os nós
#Se ID for igual aos guardados, obter coordenadas e número de saída

#Intermédio - Para cada saída, fazer a média das coordenadas

#3 - Descobrir as divisões administractivas
#Percorrer as relations
#Se tiver um dos níveis administractivos desejados,
#    Percorrer as coordenadas de saídas e ver se relation contêm algum nó
#        Se contiver, guardar informação
#Nota: Antigas freguesias são guardadas de outra forma


class AreaHandler(osmium.SimpleHandler):
    def __init__(self):
        osmium.SimpleHandler.__init__(self)
        self.total = 0
        b = LineString([(0, 0), (2, 0)])
        c = Polygon([Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)])
        print(c.contains(Point(1.5, 0.1)))
        print(c)

    def area(self, a):
        try:
            wkb = wkbfab.create_multipolygon(a)
            area = wkblib.loads(wkb, hex=True)
            admin_levels = [1, 2, 3, 4, 5, 6, 7, 8]
            for admin_level in admin_levels:
                if a.tags.get('admin_level') and int(a.tags.get('admin_level')) == admin_level:
                    if area.contains(Point(-9.3707, 38.7226)):
                        print(a.tags.get('name'), a.tags.get('admin_level'))
        except:
            pass
        self.total += 1

    def way(self, w):
        try:
            wkb = wkbfab.create_linestring(w)
            line = wkblib.loads(wkb, hex=True)
            # Length is computed in WGS84 projection, which is practically meaningless.
            # Lets pretend we didn't notice, it is an example after all.
            self.total += 1
        except:
            pass


class WayLenHandler(osmium.SimpleHandler):
    def __init__(self):
        osmium.SimpleHandler.__init__(self)
        self.total = 0

    def way(self, w):
        print(w)
        try:
            wkb = wkbfab.create_linestring(w)
            line = wkblib.loads(wkb, hex=True)
            # Length is computed in WGS84 projection, which is practically meaningless.
            # Lets pretend we didn't notice, it is an example after all.
            self.total += line.length
        except:
            pass


class CounterHandler(osmium.SimpleHandler):
    def __init__(self):
        osmium.SimpleHandler.__init__(self)
        self.num_nodes = 0

    def node(self, n):
        self.num_nodes += 1


class HotelHandler(osmium.SimpleHandler):
    def __init__(self):
        super(HotelHandler, self).__init__()
        self.hotels = []

    def node(self, o):
        if o.tags.get('tourism') == 'hotel' and 'name' in o.tags:
            self.hotels.append(o.tags['name'])


class AutoEstradaSaidasNosHandler(osmium.SimpleHandler):
    """
    Dado um nome de auto-estrada (Ex: "Autoestrada do Norte, Autovía de Málaga), retorna os IDs de nós dessa auto-estrada
    """
    def __init__(self, auto_estrada_nome):
        super(AutoEstradaSaidasNosHandler, self).__init__()
        self.auto_estrada_nome = auto_estrada_nome
        self.auto_estrada_nos_ids = set()

    def relation(self, r):
        if r.tags.get('name') == self.auto_estrada_nome:
            for membro in r.members:
                if membro.type == TIPO_NO:
                    self.auto_estrada_nos_ids.add(membro.ref)  # ref contêm o ID do elemento

    def way(self, w):
        if w.tags.get('name') == self.auto_estrada_nome:
            for node in w.nodes:
                self.auto_estrada_nos_ids.add(node.ref)


class AutoEstradaSaidasHandler(osmium.SimpleHandler):
    """
    Dado um conjunto de IDs de nós correspondentes a saídas de uma auto-estrada, retorna o número da saída e as coordenadas
    desses nós
    """
    def __init__(self, nos_id_set):
        super(AutoEstradaSaidasHandler, self).__init__()
        self.nos_id_set = nos_id_set
        self.nos_dict = {}

    def node(self, n):
        if n.id in self.nos_id_set:
            if n.tags.get('highway') and n.tags.get('highway') == MOTORWAY_JUNCTION and n.tags.get('ref'):
                saida_numero = n.tags.get('ref')
                if not self.nos_dict.get(saida_numero, []):
                    self.nos_dict[saida_numero] = []
                try:
                    self.nos_dict[saida_numero].append((n.location.lat, n.location.lon))
                except:  # Nó não tem latitude, longitude, ou os dois
                    pass


class CoordenadasParaDivisoesAdministrativas(osmium.SimpleHandler):
    """
    Dado um conjunto de coordenadas, retorna um dicionário onde a chave é um tuplo de coordenadas (lat, lon) e o valor é
    outro dicionário onde a chave é o nível administrativo (Ex: Em Portugal, distrito = 6) e o valor o nome da divisão
    """
    def __init__(self, lista_coordenadas):
        super(CoordenadasParaDivisoesAdministrativas, self).__init__()
        self.lista_coordenadas = lista_coordenadas
        self.coordenadas_divisoes_admin = {}
        self.antiga_freguesia = {}  # {'A2 - Saída 1': True} - Local "A2 - Saída 1" está numa antiga freguesia

    def area(self, a):
        try:
            wkb = wkbfab.create_multipolygon(a)
            area = wkblib.loads(wkb, hex=True)

            if a.tags.get('border_type') == FREGUESIA_HISTORICA:
                for saida in self.lista_coordenadas:
                    coordenadas = self.lista_coordenadas[saida]
                    if not self.coordenadas_divisoes_admin.get(coordenadas):
                        self.coordenadas_divisoes_admin[coordenadas] = {}
                    if area.contains(Point(coordenadas[1], coordenadas[0])):  # (longitude, latitude)
                        self.coordenadas_divisoes_admin[coordenadas][8] = a.tags.get('name')
                        self.antiga_freguesia[coordenadas] = True
            for nivel_admin in [6, 7, 8]:
                if a.tags.get('admin_level') and int(a.tags.get('admin_level')) == nivel_admin:
                    for saida in self.lista_coordenadas:
                        coordenadas = self.lista_coordenadas[saida]
                        if not self.coordenadas_divisoes_admin.get(coordenadas):
                            self.coordenadas_divisoes_admin[coordenadas] = {}
                        if area.contains(Point(coordenadas[1], coordenadas[0])):  # (longitude, latitude)
                            if nivel_admin != 8 or not self.antiga_freguesia.get(coordenadas, False):  # Local não está já associado a antiga freguesia
                                self.coordenadas_divisoes_admin[coordenadas][nivel_admin] = a.tags.get('name')
        except:  # Pode não ter sido possível converter relação em área
            pass


if __name__ == '__main__':

    #h = CounterHandler()

    #h.apply_file(FILE_GIBRALTAR)
    #print(f'Gibraltar number of nodes: {h.num_nodes}')

    #h.apply_file(FILE_PORTUGAL)
    #print(f'Portugal number of nodes: {h.num_nodes}')

    #h.apply_file(FILE_SPAIN)
    #print(f'Spain number of nodes: {h.num_nodes}')


    #h = HotelHandler()
    #h.apply_file(FILE_GIBRALTAR)

    #print("Hotels are:")
    #print(sorted(h.hotels))

    #h.apply_file(FILE_PORTUGAL)
    #print(sorted(h.hotels))

    #h = WayLenHandler()
    #h.apply_file(FILE_PORTUGAL, locations=True)
    #print("Total length: %f" % h.total)

    #h = AreaHandler()
    #h.apply_file(FILE_PORTUGAL, locations=True)
    #print(f'Total areas: {h.total}')

    #h = AreaHandler()
    #h.apply_file(FILE_PORTUGAL, locations=True)
    #print(f'Total relations: {h.total}')

    ficheiro_pbf = FILE_PORTUGAL

    # a = AreaHandler()
    # a.apply_file(ficheiro_pbf, locations=True)
    # exit(0)

    print(f'A iniciar processamento da auto-estrada {"A-2"}... Isto vai demorar uns minutos\n')
    print("A obter nós correspondentes a saídas...")

    h = AutoEstradaSaidasNosHandler("Autoestrada do Sul")
    h.apply_file(ficheiro_pbf, locations=True)
    nos_id_set = h.auto_estrada_nos_ids

    if len(nos_id_set) == 0:
        print(f'Não foi encontrado nenhum nó associado às saídas da auto-estrada {"A-2"}. A auto-estrada está em {"Portugal"}?')
        print(f'Pode também ser uma auto-estrada sem números de saída no OpenStreetMap')

    print("Nós correspondentes a saídas obtidos\n")
    print("A obter números de saídas e coordenadas de nós...")

    h = AutoEstradaSaidasHandler(nos_id_set)
    h.apply_file(ficheiro_pbf, locations=True)
    saidas_temp = h.nos_dict

    print("Coordenadas de nós e números de saídas obtidos\n")
    print("A obter coordenadas de saídas...")

    COORDENADAS_CASAS_DECIMAIS = 6

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

    print("Coordenadas de saídas obtidas\n")
    print("A obter divisões administrativas...")

    h = CoordenadasParaDivisoesAdministrativas(saidas)
    h.apply_file(ficheiro_pbf, locations=True)

    print(h.coordenadas_divisoes_admin)

    print("Divisões administrativas obtidas\n")
    print(f'Processamento da auto-estrada {"A-2"} terminado')
