import pathlib
import psycopg2
from psycopg2 import OperationalError

from viajar import viajar, local_portugal, local_espanha, local_gibraltar


class BDInterface:
    # Path da directoria relativa à base de dados
    path = str(pathlib.Path(__file__).parent.absolute()) + '\\viajar\\base_dados\\'
    path = path.replace('\\viajar\\viajar', '\\viajar')  # Necessário para a execução dos testes

    base_dados = 'viajar'
    utilizador = 'postgres'
    palavra_passe = 'postgres'
    host = 'localhost'
    porto = 5432

    def __init__(self):
        try:
            #  Efectua a ligação à base de dados
            self.ligacao = psycopg2.connect(
                database=self.base_dados,
                user=self.utilizador,
                password=self.palavra_passe,
                host=self.host,
                port=self.porto
            )
            self.ligacao.autocommit = True
            self.cursor = self.ligacao.cursor()

            #  Cria e preenche a base de dados
            path_script = self.path + 'base_dados.sql'
            with open(path_script, mode='r') as file:
                queries = file.read().split(';\n')
            for query in queries:
                self.cursor.execute(query + ';')
            self.preencher_base_dados()
        except OperationalError as e:
            print(f"Ocorreu o erro '{e}'")

    #  Retorna um local com todas as suas informações
    def obter_local(self, nome):
        #  Determinar o país
        query = "SELECT COUNT(nome) FROM local_portugal WHERE nome = '" + nome + "';"
        self.cursor.execute(query)
        resultado = self.cursor.fetchall()[0][0]
        if resultado == 1:  # Local de Portugal
            pais = 'Portugal'
        else:
            query = "SELECT COUNT(nome) FROM local_espanha WHERE nome = '" + nome + "';"
            self.cursor.execute(query)
            resultado = self.cursor.fetchall()[0][0]
            if resultado == 1:  # Local de Espanha
                pais = 'Espanha'
            else:
                query = "SELECT COUNT(nome) FROM local_gibraltar WHERE nome = '" + nome + "';"
                self.cursor.execute(query)
                resultado = self.cursor.fetchall()[0][0]
                if resultado == 1:  # Local de Gibraltar
                    pais = 'Gibraltar'
                else:
                    return None  # Local inválido

        #  Determinar os locais circundantes
        query = "SELECT * FROM ligacao WHERE local_a = '" + nome + "' OR local_b = '" + nome + "';"
        self.cursor.execute(query)
        resultado = self.cursor.fetchall()
        locais_circundantes = {}
        ordem = []
        sentidos_info_extra = {}
        for linha in resultado:
            if linha[0].strip() == nome:  # Local A
                ordem.append(linha[6])  # Ordem A
                local_circundante = linha[1].strip()
                ponto_cardeal = linha[5].strip()
            else:  # Local B
                ordem.append(linha[7])  # Ordem B
                local_circundante = linha[0].strip()
                ponto_cardeal = BDInterface.obter_ponto_cardeal_oposto(linha[5].strip())
            distancia = float(linha[3])
            meio_transporte = linha[2].strip()
            if linha[4] is not None:
                sentidos_info_extra[(local_circundante, meio_transporte)] = [linha[4].strip()]
            locais_circundantes[(local_circundante, meio_transporte)] = [ponto_cardeal, distancia, meio_transporte]
        locais_circundantes = BDInterface.ordenar_dicionario(locais_circundantes, ordem)

        #  Determinar os destinos por sentido
        query = "SELECT * FROM destino WHERE " \
                "(local_a = '" + nome + "' AND origem = 'true') OR (local_b = '" + nome + "' AND origem = 'false');"
        self.cursor.execute(query)
        resultado = self.cursor.fetchall()
        sentidos = {}
        for local_circundante in locais_circundantes:
            nome_local = local_circundante[0]
            meio_transporte = local_circundante[1]
            destinos = []
            for linha in resultado:
                if (nome_local in [linha[0], linha[1]]) & (meio_transporte == linha[2]):
                    destinos.append(linha[4].strip())
            if len(destinos) > 0:
                sentidos[(nome_local, meio_transporte)] = destinos

        #  Determinar os restantes parâmetros gerais
        query = "SELECT * FROM local WHERE nome = '" + nome + "';"
        self.cursor.execute(query)
        resultado = self.cursor.fetchall()
        latitude = float(resultado[0][1])
        longitude = float(resultado[0][2])
        altitude = int(resultado[0][3])
        info_extra = ''
        if resultado[0][4] is not None:
            info_extra = resultado[0][4].strip()

        #  Determinar os parâmetros específicos do país
        if pais == 'Portugal':
            query = "SELECT local_portugal.nome, freguesia, concelho.concelho, entidade_intermunicipal, distrito, " \
                    "regiao " \
                    "FROM local_portugal, concelho " \
                    "WHERE local_portugal.concelho = concelho.concelho AND local_portugal.nome = '" + nome + "';"
            self.cursor.execute(query)
            resultado = self.cursor.fetchall()
            freguesia = resultado[0][1].strip()
            concelho = resultado[0][2].strip()
            distrito = resultado[0][4].strip()
            entidade_intermunicipal = resultado[0][3].strip()
            regiao = resultado[0][5].strip()
        elif pais == 'Espanha':
            query = "SELECT nome, municipio, distrito, provincia.provincia, comunidade_autonoma " \
                    "FROM local_espanha, provincia " \
                    "WHERE local_espanha.provincia = provincia.provincia AND local_espanha.nome = '" + nome + "';"
            self.cursor.execute(query)
            resultado = self.cursor.fetchall()
            distrito = ''
            if resultado[0][2] is not None:
                distrito = resultado[0][2].strip()
            municipio = resultado[0][1].strip()
            provincia = resultado[0][3].strip()
            comunidade_autonoma = resultado[0][4].strip()
            query = "SELECT * FROM comarca WHERE municipio = '" + municipio + "' AND provincia = '" + provincia + "';"
            self.cursor.execute(query)
            resultado = self.cursor.fetchall()
            comarcas = []
            for linha in resultado:
                comarcas.append(linha[1].strip())
        elif pais == 'Gibraltar':
            query = "SELECT nome, major_residential_area FROM local_gibraltar WHERE nome = '" + nome + "';"
            self.cursor.execute(query)
            resultado = self.cursor.fetchall()
            major_residential_areas = []
            for linha in resultado:
                major_residential_areas.append(linha[1].strip())
        else:
            return None

        #  Criar o local
        if pais == 'Portugal':
            local = local_portugal.LocalPortugal(nome, locais_circundantes, latitude, longitude, altitude, freguesia,
                                                 concelho, distrito, entidade_intermunicipal, regiao)
        elif pais == 'Espanha':
            local = local_espanha.LocalEspanha(nome, locais_circundantes, latitude, longitude, altitude, municipio,
                                               comarcas, provincia, comunidade_autonoma)
            local.set_distrito(distrito)
        elif pais == 'Gibraltar':
            local = local_gibraltar.LocalGibraltar(nome, locais_circundantes, latitude, longitude, altitude,
                                                   major_residential_areas)
        else:
            return None
        local.set_sentidos(sentidos)
        local.set_sentidos_info_extra(sentidos_info_extra)
        local.set_info_extra(info_extra)

        return local

    #  Preenche a base de dados
    def preencher_base_dados(self):
        path_csv = self.path + 'local.csv'
        query = "COPY local(nome, latitude, longitude, altitude, info_extra) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = self.path + 'concelho.csv'
        query = "COPY concelho(concelho, entidade_intermunicipal, distrito, regiao) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = self.path + 'provincia.csv'
        query = "COPY provincia(provincia, comunidade_autonoma) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = self.path + 'municipio.csv'
        query = "COPY municipio(municipio, provincia) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = self.path + 'local_portugal.csv'
        query = "COPY local_portugal(nome, freguesia, concelho) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = self.path + 'local_espanha.csv'
        query = "COPY local_espanha(nome, municipio, provincia, distrito) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = self.path + 'local_gibraltar.csv'
        query = "COPY local_gibraltar(nome, major_residential_area) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = self.path + 'comarca.csv'
        query = "COPY comarca(municipio, comarca, provincia) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = self.path + 'ligacao.csv'
        query = "COPY ligacao(local_a, local_b, meio_transporte, distancia, info_extra, ponto_cardeal, ordem_a, " \
                "ordem_b) FROM '" + path_csv + "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

        path_csv = self.path + 'destino.csv'
        query = "COPY destino(local_a, local_b, meio_transporte, origem, destino) FROM '" + path_csv + \
                "' DELIMITER ',' CSV HEADER ENCODING 'utf8';"
        self.cursor.execute(query)

    #  Retorna o número de locais da base de dados
    def obter_numero_locais(self):
        query = "SELECT COUNT(nome) FROM local;"
        self.cursor.execute(query)
        return self.cursor.fetchall()[0][0]

    #  Retorna o ponto cardeal oposto
    @staticmethod
    def obter_ponto_cardeal_oposto(ponto_cardeal):
        if ponto_cardeal == viajar.NORTE:
            return viajar.SUL
        elif ponto_cardeal == viajar.NORDESTE:
            return viajar.SUDOESTE
        elif ponto_cardeal == viajar.ESTE:
            return viajar.OESTE
        elif ponto_cardeal == viajar.SUDESTE:
            return viajar.NOROESTE
        elif ponto_cardeal == viajar.SUL:
            return viajar.NORTE
        elif ponto_cardeal == viajar.SUDOESTE:
            return viajar.NORDESTE
        elif ponto_cardeal == viajar.OESTE:
            return viajar.ESTE
        elif ponto_cardeal == viajar.NOROESTE:
            return viajar.SUDESTE
        else:
            return ''

    #  Ordena os elementos de um dicionário de acordo com uma ordem fornecida
    @staticmethod
    def ordenar_dicionario(dicionario, ordem):
        novo_dic = {}
        for i in range(len(dicionario)):
            for j in range(len(dicionario)):
                if ordem[j] == len(novo_dic) + 1:
                    chave = list(dicionario)[j]
                    novo_dic[chave] = dicionario[chave]
        return novo_dic
