import psycopg2
from psycopg2 import OperationalError

from viajar import viajar, local_portugal, local_espanha


class BDInterface:
    # Path do script de SQL que cria e preenche a base de dados
    path = 'D:\\PycharmProjects\\Viajar\\src\\viajar\\base_dados\\base_dados.sql'

    base_dados = 'viajar'
    utilizador = 'postgres'
    palavra_passe = 'postgres'
    host = 'localhost'
    porto = 5432

    def __init__(self):
        '''
        with open('D:\\PycharmProjects\\Viajar\\src\\viajar\\base_dados\\destino.csv', encoding='utf-8') as file:
            csv_reader = csv.reader(file, delimiter=',')
            rows = []
            for row in csv_reader:
                origem = row[0]
                sentido = row[1]
                destino = row[2]
                local_a = row[3]
                local_b = row[4]
                meio_transporte = row[5]
                print([origem, sentido, destino, local_a, local_b, meio_transporte])
                origem = (origem == local_a)
                rows.append([local_a, local_b, meio_transporte, origem, destino])
            rows.sort()
            with open('D:\\PycharmProjects\\Viajar\\src\\viajar\\base_dados\\destino_2.csv', mode='w', encoding='utf-8') as new_file:
                writer = csv.writer(new_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(['Local A', 'Local B', 'Meio de transporte', 'Origem', 'Destino'])
                writer.writerows(rows)
                print(rows)
        '''

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

            #  Preenche a base de dados
            with open(self.path, mode='r') as file:
                queries = file.read().split(';\n')
            for query in queries:
                self.cursor.execute(query + ';')
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
                sentidos_info_extra[local_circundante] = [linha[4].strip()]
            locais_circundantes[local_circundante] = [ponto_cardeal, distancia, meio_transporte]
        locais_circundantes = BDInterface.ordenar_dicionario(locais_circundantes, ordem)

        #  Determinar os destinos por sentido
        query = "SELECT * FROM destino WHERE " \
                "(local_a = '" + nome + "' AND origem = 'true') OR (local_b = '" + nome + "' AND origem = 'false');"
        self.cursor.execute(query)
        resultado = self.cursor.fetchall()
        sentidos = {}
        for local_circundante in locais_circundantes:
            destinos = []
            for linha in resultado:
                if local_circundante in [linha[0], linha[1]]:
                    destinos.append(linha[4].strip())
            if len(destinos) > 0:
                sentidos[local_circundante] = destinos

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
                    "FROM local_portugal, local_concelho, concelho " \
                    "WHERE local_portugal.nome = local_concelho.nome AND local_concelho.concelho = concelho.concelho " \
                    "AND local_portugal.nome = '" + nome + "';"
            self.cursor.execute(query)
            resultado = self.cursor.fetchall()
            freguesia = resultado[0][1].strip()
            concelho = resultado[0][2].strip()
            distrito = resultado[0][4].strip()
            entidade_intermunicipal = resultado[0][3].strip()
            regiao = resultado[0][5].strip()
        elif pais == 'Espanha':
            query = "SELECT * FROM local_comarca WHERE nome = '" + nome + "';"
            self.cursor.execute(query)
            resultado = self.cursor.fetchall()
            comarca = resultado[0][1].strip()
            query = "SELECT local_espanha.nome, municipio, distrito, provincia.provincia, comunidade_autonoma " \
                    "FROM local_espanha, local_provincia, provincia " \
                    "WHERE local_espanha.nome = local_provincia.nome AND local_provincia.provincia = " \
                    "provincia.provincia AND local_espanha.nome = '" + nome + "';"
            self.cursor.execute(query)
            resultado = self.cursor.fetchall()
            distrito = ''
            if resultado[0][2] is not None:
                distrito = resultado[0][2].strip()
            municipio = resultado[0][1].strip()
            provincia = resultado[0][3].strip()
            comunidade_autonoma = resultado[0][4].strip()
        else:
            return None

        #  Criar o local
        if pais == 'Portugal':
            local = local_portugal.LocalPortugal(nome, locais_circundantes, latitude, longitude, altitude, freguesia,
                                                 concelho, distrito, entidade_intermunicipal, regiao)
        elif pais == 'Espanha':
            local = local_espanha.LocalEspanha(nome, locais_circundantes, latitude, longitude, altitude, municipio,
                                               comarca, provincia, comunidade_autonoma)
            local.set_distrito(distrito)
        else:
            return None
        local.set_sentidos(sentidos)
        local.set_sentidos_info_extra(sentidos_info_extra)
        local.set_info_extra(info_extra)

        return local

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
