import psycopg2
from psycopg2 import OperationalError


class BDInterface:

    # Path do script de SQL que cria e preenche a base de dados
    path = 'D:\\PycharmProjects\\Viajar\\src\\viajar\\base_dados\\base_dados.sql'

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

            #  Preenche a base de dados
            with open(self.path, mode='r') as file:
                queries = file.read().split(';\n')
            for query in queries:
                self.cursor.execute(query + ';')
        except OperationalError as e:
            print(f"Ocorreu o erro '{e}'")

    #  Retorna um local com todas as suas informações
    def obter_local(self, nome):
        query = "SELECT * FROM local WHERE nome = '" + nome + "';"
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
        return nome

    #  Retorna o número de locais da base de dados
    def obter_numero_locais(self):
        query = "SELECT COUNT(nome) FROM local;"
        self.cursor.execute(query)
        return self.cursor.fetchall()[0][0]
