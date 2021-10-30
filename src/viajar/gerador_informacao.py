import os

import requests
try:
    import osmium
    import shapely.wkb as wkblib
    from shapely.geometry import Point
except:
    print("Bibliotecas osmium e/ou shapely não instaladas. Está a executar este ficheiro em Windows?")
    exit(1)

import viajar.vias as vias
import viajar.ordenador as ordenador
import viajar.haversine as haversine


class Path:

    def __init__(self, *args):
        path_list: list = []
        for arg in args:
            if type(arg) == Path:
                arg = arg.path
            path_list.append(arg)
        self.path: str = os.path.join(*path_list)

    def get_path(self) -> str:
        return self.path


class Coordenada:

    def __init__(self, latitude: float, longitude: float):
        self.latitude: float = latitude
        self.longitude: float = longitude

    def get_coordenadas(self) -> tuple:
        return self.get_latitude(), self.get_longitude()

    def get_latitude(self) -> float:
        return self.latitude

    def get_longitude(self) -> float:
        return self.longitude

    def set_latitude(self, latitude: float):
        self.latitude = latitude

    def set_longitude(self, longitude: float):
        self.longitude = longitude

    def __eq__(self, other):
        return self.get_latitude() == other.get_latitude() and self.get_longitude() == other.get_longitude()

    def __hash__(self):
        return hash(self.get_coordenadas())


COORDENADAS_CASAS_DECIMAIS: int = 6
ENCODING: str = 'utf-8'

PATH_BASE: Path = Path(os.path.dirname(os.path.realpath(__file__)))
CHAVE_API_PATH: Path = Path(PATH_BASE, '..', 'api_key.txt')
PASTA_TEMP: Path = Path(PATH_BASE, 'tmp')

# Contêm a informação de países vinda do OpenStreetMap
PASTA_OSM: Path = Path(PATH_BASE, 'osm')
OSM_GIBRALTAR: Path = Path(PASTA_OSM, 'gibraltar-latest.osm.pbf')
OSM_PORTUGAL: Path = Path(PASTA_OSM, 'portugal-latest.osm.pbf')
OSM_ESPANHA: Path = Path(PASTA_OSM, 'spain-latest.osm.pbf')

OPCAO_SAIR = 0
OPCAO_LOCAIS_DIV_ADMIN = 1
OPCAO_LIGACOES_DESTINOS = 2
OPCAO_CIMA_BAIXO = 1
OPCAO_BAIXO_CIMA = 2

# Parâmetros do OpenStreetMap

TIPO_NO: str = "n"  # Node
TIPO_VIA: str = "w"  # Way
TIPO_RELACAO: str = "r"  # Relation

MOTORWAY_JUNCTION: str = 'motorway_junction'
FREGUESIA_HISTORICA: str = 'historic_parish'

# A global factory that creates WKB from a osmium geometry
wkbfab = osmium.geom.WKBFactory()

"""
Gera ficheiros .csv com informação de saídas de auto-estradas
"""


class GeradorInformacao:

    def __init__(self, auto_estrada_para_analisar: tuple, obter_altitudes=True):
        self.auto_estrada_numero: str = auto_estrada_para_analisar[0]  # Ex: A-5
        self.auto_estrada_nome: str = auto_estrada_para_analisar[1]  # Ex: Autovia del Suroeste
        self.pais: str = auto_estrada_para_analisar[2]  # Ex: ES
        self.obter_altitudes: bool = obter_altitudes

        self.local_path: Path = Path(PASTA_TEMP, f'{self.auto_estrada_numero}_local.csv')
        self.local_espanha_path: Path = Path(PASTA_TEMP, f'{self.auto_estrada_numero}_local_espanha.csv')
        self.local_portugal_path: Path = Path(PASTA_TEMP, f'{self.auto_estrada_numero}_local_portugal.csv')
        self.municipio_path: Path = Path(PASTA_TEMP, f'{self.auto_estrada_numero}_municipio.csv')
        self.comarca_path: Path = Path(PASTA_TEMP, f'{self.auto_estrada_numero}_comarca.csv')
        self.concelho_path: Path = Path(PASTA_TEMP, f'{self.auto_estrada_numero}_concelho.csv')
        self.ligacao_path: Path = Path(PASTA_TEMP, f'{self.auto_estrada_numero}_ligacao.csv')
        self.destino_path: Path = Path(PASTA_TEMP, f'{self.auto_estrada_numero}_destino.csv')

        print("Bem-vindo/a ao gerador automático de informação.")
        print("Escreva a opção desejada e pressione ENTER.")
        print(f"{OPCAO_SAIR} - Sair do programa")
        print(f"{OPCAO_LOCAIS_DIV_ADMIN} - Gerar locais e divisões administrativas da {self.auto_estrada_numero}")
        print(f"{OPCAO_LIGACOES_DESTINOS} - Gerar ligações e destinos da {self.auto_estrada_numero}")
        while True:
            opcao = input("Escreva a opção desejada e pressione ENTER: ")
            if opcao == str(OPCAO_SAIR):
                print("Escolheu sair.")
                print("Boa viagem!")
                exit(0)
            elif opcao == str(OPCAO_LOCAIS_DIV_ADMIN):
                print(f"Escolheu gerar os locais e divisões administrativas da {self.auto_estrada_numero}.")
                self.opcao_obter_locais_divs_admins()
                break
            elif opcao == str(OPCAO_LIGACOES_DESTINOS):
                print(f"Escolheu gerar as ligações e destinos da {self.auto_estrada_numero}.")
                self.opcao_obter_ligacoes_destinos()
                break
        exit(0)

    def opcao_obter_ligacoes_destinos(self):
        """
        A partir de um ficheiro de locais de uma auto-estrada, cria os ficheiros de ligações e de destinos correspondentes
        """
        if not os.path.exists(self.local_path.path):
            print(f'O ficheiro de locais da {self.auto_estrada_numero} não existe.')
            print(f'Execute este programa novamente e seleccione a opção {OPCAO_LOCAIS_DIV_ADMIN}.')
            exit(0)
        aviso: str = f'A auto-estrada {self.auto_estrada_numero} parece já ter um ficheiro de ligações.'
        self._detector_ficheiro_repetido(self.ligacao_path.path, aviso)
        aviso: str = f'A auto-estrada {self.auto_estrada_numero} parece já ter um ficheiro de destinos.'
        self._detector_ficheiro_repetido(self.destino_path.path, aviso)

        print(f'Como deseja que a auto-estrada {self.auto_estrada_numero} seja ordenada?')
        print("Escreva a opção desejada e pressione ENTER")
        print(f"{OPCAO_SAIR} - Sair do programa")
        print(f"{OPCAO_CIMA_BAIXO} - De cima para baixo")
        print(f"{OPCAO_BAIXO_CIMA} - De baixo para cima")
        while True:
            opcao = input("Escreva a opção desejada e pressione ENTER: ")
            if opcao == str(OPCAO_SAIR):
                print("Escolheu sair.")
                print("Boa viagem!")
                exit(0)
            elif opcao == str(OPCAO_LOCAIS_DIV_ADMIN):
                print("A auto-estrada será ordenada de cima para baixo")
                invertido: bool = False
                break
            elif opcao == str(OPCAO_LIGACOES_DESTINOS):
                print(f"A auto-estrada será ordenada de baixo para cima")
                invertido: bool = True
                break

        self.create_ficheiros_ligacoes_destinos(invertido=invertido)
        print(f'Auto-estrada {self.auto_estrada_numero} processada')
        print("Boa viagem!")

    def opcao_obter_locais_divs_admins(self):
        """
        Recolhe informação sobre as saídas de uma auto-estrada usando o OSM e cria os respectivos ficheiros de locais e
        de divisões administrativas
        """
        aviso: str = f'A auto-estrada {self.auto_estrada_numero} parece já ter sido processada antes.'
        self._detector_ficheiro_repetido(self.local_path.path, aviso)

        if self.pais == vias.PORTUGAL:
            self.ficheiro_osm: str = OSM_PORTUGAL.path
        elif self.pais == vias.ESPANHA:
            self.ficheiro_osm: str = OSM_ESPANHA.path
        elif self.pais == vias.GIBRALTAR:
            self.ficheiro_osm: str = OSM_ESPANHA.path
        # elif self.pais == vias.ANDORRA:
        #     self.ficheiro_osm: str = OSM_ANDORRA.path
        else:
            print(f'País inválido - Processamento da {self.auto_estrada_numero} cancelado')
            exit(1)

        # Chave da API da Google - Usada para obter altitudes
        with open(CHAVE_API_PATH.path, 'r', encoding=ENCODING) as f:
            self.api_key: str = f.readlines()[0]

        self.create_ficheiros_locais_divisoes_admin()
        print(f'Auto-estrada {self.auto_estrada_numero} processada')
        print("Boa viagem!")

    def create_ficheiros_locais_divisoes_admin(self):
        print("################")
        print(f'A iniciar processamento da auto-estrada {self.auto_estrada_numero}...')
        print(f'Isto vai demorar uns minutos')
        print("################\n")

        saidas_coordenadas: dict = self.get_auto_estradas_saidas()
        saidas_ordenadas: list = list(saidas_coordenadas.keys())
        saidas_ordenadas.sort()

        print(f'{len(saidas_ordenadas)} saídas encontradas')
        if len(saidas_ordenadas) == 0:
            print(f'Processamento da {self.auto_estrada_numero} cancelado')
            exit(1)

        if not os.path.exists(PASTA_TEMP.path):
            os.makedirs(PASTA_TEMP.path)

        with open(os.path.join(self.local_path.path), 'w', encoding=ENCODING) as f:
            for saida in saidas_ordenadas:
                latitude: float = saidas_coordenadas[saida].get_latitude()
                longitude: float = saidas_coordenadas[saida].get_longitude()
                altitude: int = 0
                if self.obter_altitudes:
                    print(f'A obter a altitude da saída {saida}...')
                    altitude: int = self.get_altitude(latitude, longitude)
                f.write(f'{self.auto_estrada_numero} - Saída {saida},{latitude},{longitude},{altitude},\n')
        ordenador.ordenar_ficheiros_csv(ficheiro_a_ordenar=self.local_path.path, cabecalho=False)
        print(f'Ficheiro de locais criado')

        saidas_terminadas: int = 0

        if self.pais == vias.ESPANHA:
            municipios: set = set()
            comarcas: set = set()

            divisoes_pretendidas: list = [vias.PROVINCIA, vias.COMARCA, vias.MUNICIPIO, vias.DISTRITO_ES]
            divisoes_saidas: dict = self.get_divisoes_administrativas(  # {(37.1, -7.5): {6: 'Alcoutim', 7: 'Alcoutim', 8: 'Faro'}}
                list(saidas_coordenadas.values()), divisoes_pretendidas)

            with open(self.local_espanha_path.path, 'w', encoding=ENCODING) as f:
                for saida in saidas_ordenadas:
                    ponto: Coordenada = saidas_coordenadas[saida]

                    municipio: str = divisoes_saidas.get(ponto, {}).get(vias.MUNICIPIO, "")
                    provincia: str = divisoes_saidas.get(ponto, {}).get(vias.PROVINCIA, "")
                    comarca: str = divisoes_saidas.get(ponto, {}).get(vias.COMARCA, '')  # Nem sempre está disponível
                    distrito_es: str = divisoes_saidas.get(ponto, {}).get(vias.DISTRITO_ES, '')  # Só disponível nas grandes cidades

                    f.write(f'{self.auto_estrada_numero} - Saída {saida},{municipio},{provincia},{distrito_es}\n')

                    municipios.add(f'{municipio},{provincia}\n')
                    if comarca:
                        comarcas.add(f'{municipio},{comarca},{provincia}\n')

                    saidas_terminadas += 1
                    print(f'Saída {saida} terminada - {saidas_terminadas}/{len(saidas_ordenadas)} saídas processadas')

            with open(self.municipio_path.path, 'w', encoding=ENCODING) as f:
                for municipio in municipios:
                    f.write(municipio)

            with open(self.comarca_path.path, 'w', encoding=ENCODING) as f:
                for comarca in comarcas:
                    f.write(comarca)

            ordenador.ordenar_ficheiros_csv(ficheiro_a_ordenar=self.local_espanha_path.path, cabecalho=False)
            print("Ficheiro de locais de Espanha terminado")
            ordenador.ordenar_ficheiros_csv(ficheiro_a_ordenar=self.municipio_path.path, cabecalho=False)
            print("Ficheiro de municípios terminado")
            ordenador.ordenar_ficheiros_csv(ficheiro_a_ordenar=self.comarca_path.path, cabecalho=False)
            print("Ficheiro de comarcas terminado")

        elif self.pais == vias.PORTUGAL:
            concelhos: set = set()

            divisoes_pretendidas: list = [vias.DISTRITO_PT, vias.CONCELHO, vias.FREGUESIA]
            divisoes_saidas: dict = self.get_divisoes_administrativas(  # {(37.1, -7.5): {6: 'Alcoutim', 7: 'Alcoutim', 8: 'Faro'}}
                list(saidas_coordenadas.values()), divisoes_pretendidas)

            with open(self.local_portugal_path.path, 'w', encoding=ENCODING) as f:
                for saida in saidas_ordenadas:
                    ponto: Coordenada = saidas_coordenadas[saida]

                    freguesia: str = divisoes_saidas.get(ponto, {}).get(vias.FREGUESIA, "")  # Antiga freguesia, se existir
                    concelho: str = divisoes_saidas.get(ponto, {}).get(vias.CONCELHO, "")
                    distrito: str = divisoes_saidas.get(ponto, {}).get(vias.DISTRITO_PT, "")

                    f.write(f'{self.auto_estrada_numero} - Saída {saida},{freguesia},{concelho}\n')

                    concelhos.add(f'{concelho},,{distrito},\n')  # Inserir manualmente entidade intermunicipal e região histórica

                    saidas_terminadas += 1
                    print(f'Saída {saida} terminada - {saidas_terminadas}/{len(saidas_ordenadas)} saídas processadas')

            with open(self.concelho_path.path, 'w', encoding=ENCODING) as f:
                for concelho in concelhos:
                    f.write(concelho)

            ordenador.ordenar_ficheiros_csv(ficheiro_a_ordenar=self.local_portugal_path.path, cabecalho=False)
            print("Ficheiro de locais de Portugal terminado")
            ordenador.ordenar_ficheiros_csv(ficheiro_a_ordenar=self.concelho_path.path, cabecalho=False)
            print("Ficheiro de concelhos terminado")

        else:
            pass

    def create_ficheiros_ligacoes_destinos(self, invertido: bool):
        with open(self.local_path.path, 'r', encoding=ENCODING) as f:
            conteudo: list = f.readlines()

        if len(conteudo) == 0:
            print(f'O ficheiro de locais da auto-estrada {self.auto_estrada_numero} está vazio.')
            print("A sair.")
            exit(0)
        elif len(conteudo) == 1:
            print(f'O ficheiro de locais da auto-estrada {self.auto_estrada_numero} só tem 1 local.')
            print("Não é possível criar ligações nem destinos.")
            print("A sair.")
            exit(0)

        if invertido:
            conteudo = list(reversed(conteudo))

        ligacoes: list = []
        destinos: list = []
        for idx, local in enumerate(conteudo):
            if idx <= len(conteudo) - 2:  # Índice não é o do último elemento
                local_a: str = conteudo[idx].split(",")[0]
                local_b: str = conteudo[idx + 1].split(",")[0]
                meio_transporte: str = 'Carro'
                info_extra: str = self.auto_estrada_numero
                latitude_a, longitude_a = conteudo[idx].split(',')[1], conteudo[idx].split(',')[2]
                latitude_b, longitude_b = conteudo[idx + 1].split(',')[1], conteudo[idx + 1].split(',')[2]
                ponto_cardeal: str = haversine.obter_ponto_cardeal(origem=(latitude_a, longitude_a), destino=(latitude_b, longitude_b))

                ligacao: str = f'{local_a},{local_b},{meio_transporte},,{info_extra},{ponto_cardeal},2,1\n'  # Distância fica em branco
                destino_false: str = f'{local_a},{local_b},{meio_transporte},False,\n'
                destino_true: str = f'{local_a},{local_b},{meio_transporte},True,\n'

                ligacoes.append(ligacao)
                destinos.append(destino_false)
                destinos.append(destino_true)

        with open(self.ligacao_path.path, 'w', encoding=ENCODING) as f:
            f.writelines(ligacoes)
        with open(self.destino_path.path, 'w', encoding=ENCODING) as f:
            f.writelines(destinos)

    def get_altitude(self, latitude: float, longitude: float) -> int:
        try:
            url: str = f'https://maps.googleapis.com/maps/api/elevation/json?locations={latitude},{longitude}&key={self.api_key}'
            return int(requests.get(url=url).json()['results'][0]['elevation'])
        except Exception as e:
            print(str(e))
            return 0

    def get_divisoes_administrativas(self, locais: list, divisoes_pretendidas: list) -> dict:
        """
        Dado uma lista de coordenadas, retorna dicionário com, para cada local, os nomes das divisões administrativas pretendidas
        """
        print("A obter divisões administrativas...")

        h: CoordenadasParaDivisoesAdministrativas = CoordenadasParaDivisoesAdministrativas(locais, divisoes_pretendidas, self.pais)
        h.apply_file(self.ficheiro_osm, locations=True)

        print("Divisões administrativas obtidas\n")

        return h.coordenadas_divisoes_admin

    def get_auto_estradas_saidas(self) -> dict:
        print("A obter nós correspondentes a saídas...")

        h: AutoEstradaSaidasNosHandler = AutoEstradaSaidasNosHandler(self.auto_estrada_nome)
        h.apply_file(self.ficheiro_osm, locations=True)
        nos_id_set: set = h.auto_estrada_nos_ids
        vias_a_processar: set = h.vias_a_processar
        h: AutoEstradaSaidasNosHandler = AutoEstradaSaidasNosHandler(self.auto_estrada_nome, vias_a_processar=vias_a_processar, auto_estrada_nos_ids=nos_id_set)
        h.apply_file(self.ficheiro_osm, locations=True)  # Segunda passagem, necessário em certas auto-estradas
        nos_id_set: set = h.auto_estrada_nos_ids

        if len(nos_id_set) == 0:
            print(f'Não foi encontrado nenhum nó associado às saídas da {self.auto_estrada_numero}. A auto-estrada está em {self.pais}?')
            print(f'Pode também ser uma auto-estrada sem números de saída no OpenStreetMap')
            exit(0)

        print("Nós correspondentes a saídas obtidos\n")
        print("A obter números de saídas e coordenadas de nós...")

        h: AutoEstradaSaidasHandler = AutoEstradaSaidasHandler(nos_id_set)
        h.apply_file(self.ficheiro_osm, locations=True)
        saidas_temp: dict = h.saidas_dict

        print("Coordenadas de nós e números de saídas obtidos\n")
        print("A obter coordenadas de saídas...")

        saidas: dict = {}
        for saida in saidas_temp:
            latitude = 0.0
            longitude = 0.0
            for ponto in saidas_temp[saida]:
                latitude += ponto.get_latitude()
                longitude += ponto.get_longitude()
            latitude = round(latitude / len(saidas_temp[saida]), COORDENADAS_CASAS_DECIMAIS)
            longitude = round(longitude / len(saidas_temp[saida]), COORDENADAS_CASAS_DECIMAIS)
            saidas[saida] = Coordenada(latitude, longitude)

        print("Coordenadas de saídas obtidas\n")

        return saidas

    def _detector_ficheiro_repetido(self, path: str, aviso: str):
        """
        Detecta se o ficheiro fornecido existe. Se existe, apresenta o aviso ao utilizador e dá opção de escolha.
        Se a opção for de cancelar, sai do programa, caso contrário continua
        :param path: Path do ficheiro
        :param aviso: String de aviso que indique qual o ficheiro já existente
        :return:
        """
        if os.path.exists(path):
            print(aviso)
            print(f'Se continuar, irá reescrever o ficheiro criado. Deseja prosseguir?')
            while True:
                opcao = repr(input(f'Escreva S para prosseguir ou N para cancelar a operação, depois pressione ENTER:'))
                if 's' in opcao.lower():
                    print()
                    break
                elif 'n' in opcao.lower():
                    print(f'Processamento da {self.auto_estrada_numero} cancelado.')
                    exit(0)


class AutoEstradaSaidasNosHandler(osmium.SimpleHandler):
    """
    Dado um nome de auto-estrada (Ex: "Autoestrada do Norte", "Autovía de Málaga"), em 2 chamadas obtêm os IDs dos nós dessa auto-estrada
    1ª chamada - Obtêm IDs de nós pertencentes a relações e vias com o nome da auto-estrada desejada, assim como IDs de
        vias com outros nomes / sem nome pertencentes a relações com o nome da auto-estrada
    2ª chamada - Dadas as vias encontradas e os IDs dos nós já encontrados, obtêm os IDs dos nós dessas vias
        Fornecer os IDs dos nós já encontrados destina-se apenas aos prints da classe
    """
    def __init__(self, auto_estrada_nome: str, vias_a_processar: set = None, auto_estrada_nos_ids: set = None):
        super(AutoEstradaSaidasNosHandler, self).__init__()
        self.auto_estrada_nome: str = auto_estrada_nome
        self.auto_estrada_nos_ids: set = set()
        self.vias_a_processar: set = set()
        if auto_estrada_nos_ids:  # Segunda passagem pelo ficheiro
            self.auto_estrada_nos_ids = auto_estrada_nos_ids
        if vias_a_processar:  # Segunda passagem pelo ficheiro
            self.vias_a_processar = vias_a_processar

    def relation(self, r):
        if r.tags.get('name') == self.auto_estrada_nome:
            for membro in r.members:
                if membro.type == TIPO_NO:
                    self.auto_estrada_nos_ids.add(membro.ref)  # ref contêm o ID do elemento
                    if len(self.auto_estrada_nos_ids) == 1:
                        print("1 nó encontrado")
                    else:
                        print(f'{len(self.auto_estrada_nos_ids)} nós encontrados')
                elif membro.type == TIPO_VIA:
                    self.vias_a_processar.add(membro.ref)  # Guarda ID da via para segunda passagem pelo ficheiro

    def way(self, w):
        if w.tags.get('name') == self.auto_estrada_nome or w.id in self.vias_a_processar:
            for node in w.nodes:
                self.auto_estrada_nos_ids.add(node.ref)
                if len(self.auto_estrada_nos_ids) == 1:
                    print("1 nó encontrado")
                else:
                    print(f'{len(self.auto_estrada_nos_ids)} nós encontrados')


class AutoEstradaSaidasHandler(osmium.SimpleHandler):
    """
    Dado um conjunto de IDs de nós correspondentes a saídas de uma auto-estrada, retorna o número da saída e as coordenadas
    desses nós
    """
    def __init__(self, nos_id_set: set):
        super(AutoEstradaSaidasHandler, self).__init__()
        self.nos_id_set: set = nos_id_set
        self.saidas_dict: dict = {}
        self.nos_processados: int = 0

    def node(self, n):
        if n.id in self.nos_id_set:
            if n.tags.get('highway') and n.tags.get('highway') == MOTORWAY_JUNCTION and n.tags.get('ref'):
                saida_numero: str = n.tags.get('ref')
                if not self.saidas_dict.get(saida_numero, []):
                    self.saidas_dict[saida_numero]: list = []
                try:
                    ponto: Coordenada = Coordenada(n.location.lat, n.location.lon)
                    self.saidas_dict[saida_numero].append(ponto)
                    self.nos_processados += 1
                    print(f'{self.nos_processados} nós com informação de saída encontrados de entre {len(self.nos_id_set)} disponíveis')
                except:  # Nó não tem latitude, longitude, ou os dois
                    pass


class CoordenadasParaDivisoesAdministrativas(osmium.SimpleHandler):
    """
    Dado um conjunto de coordenadas, retorna um dicionário onde a chave é um tuplo de coordenadas (lat, lon) e o valor é
    outro dicionário onde a chave é o nível administrativo (Ex: Em Portugal, distrito = 6) e o valor o nome da divisão
    """
    def __init__(self, lista_coordenadas: list, divisoes_pretendidas: list, pais: str):
        super(CoordenadasParaDivisoesAdministrativas, self).__init__()
        self.lista_coordenadas: list = lista_coordenadas
        self.divisoes_pretendidas: list = divisoes_pretendidas  # Quais as divisões administrativas pretendidas
        self.pais: str = pais
        self.coordenadas_divisoes_admin: dict = {}
        self.antiga_freguesia: dict = {}  # {(36.5, -8.5): True} - As coordenadas estão numa antiga freguesia
        self.saidas_concluidas: int = 0

    def area(self, a):
        try:
            if a.tags.get('border_type') == FREGUESIA_HISTORICA and self.pais == vias.PORTUGAL:
                wkb = wkbfab.create_multipolygon(a)
                area = wkblib.loads(wkb, hex=True)

                for ponto in self.lista_coordenadas:
                    if not self.coordenadas_divisoes_admin.get(ponto):
                        self.coordenadas_divisoes_admin[ponto] = {}
                    if area.contains(Point(ponto.get_longitude(), ponto.get_latitude())):  # (longitude, latitude)
                        self.coordenadas_divisoes_admin[ponto][vias.FREGUESIA] = a.tags.get('name')
                        self.antiga_freguesia[ponto] = True
                        if len(self.coordenadas_divisoes_admin[ponto]) == len(self.divisoes_pretendidas):
                            self.saidas_concluidas += 1
                            print(f'Divisões administrativas obtidas para {self.saidas_concluidas}/{len(self.lista_coordenadas)} locais')
            for nivel_admin in self.divisoes_pretendidas:
                if a.tags.get('admin_level') and int(a.tags.get('admin_level')) == nivel_admin:
                    wkb = wkbfab.create_multipolygon(a)
                    area = wkblib.loads(wkb, hex=True)

                    for ponto in self.lista_coordenadas:
                        if not self.coordenadas_divisoes_admin.get(ponto):
                            self.coordenadas_divisoes_admin[ponto] = {}
                        if area.contains(Point(ponto.get_longitude(), ponto.get_latitude())) and \
                                not self.antiga_freguesia.get(ponto, False):  # Local não está já associado a antiga freguesia
                            self.coordenadas_divisoes_admin[ponto][nivel_admin] = a.tags.get('name')
                            if len(self.coordenadas_divisoes_admin[ponto]) == len(self.divisoes_pretendidas):
                                self.saidas_concluidas += 1
                                print(f'Divisões administrativas obtidas para {self.saidas_concluidas}/{len(self.lista_coordenadas)} locais')
        except:  # Pode não ter sido possível converter relação em área
            pass
