import csv
import pathlib
from functools import cmp_to_key
import os

from travel.main.cardinal_points import obter_ponto_cardeal_oposto

"""
Ordenador do conteúdo de ficheiros .csv
"""

MENOR = -1
IGUAL = 0
MAIOR = 1

DELIMITER = ','
QUOTECHAR = '"'
QUOTING = csv.QUOTE_NONE
ENCODING = 'utf-8'
ESCAPECHAR = ''

CSV_COMARCA = 'comarca.csv'
CSV_CONCELHO = 'concelho.csv'
CSV_DESTINO = 'destination.csv'
CSV_LIGACAO = 'connection.csv'
CSV_LOCAL = 'location.csv'
CSV_LOCAL_ESPANHA = 'location_spain.csv'
CSV_LOCAL_GIBRALTAR = 'location_gibraltar.csv'
CSV_LOCAL_PORTUGAL = 'location_portugal.csv'
CSV_MUNICIPIO = 'municipio.csv'
CSV_PROVINCIA = 'province.csv'

# Path da directoria relativa à base de dados
path = os.path.join(str(pathlib.Path(__file__).parent.absolute()), '..', 'database')

# Posições dos campos dos ficheiros .csv
LOCAL_A = 0
LOCAL_B = 1
PONTO_CARDEAL = 5
ORDEM_A = 6
ORDEM_B = 7
ORIGEM = 3


def ordenar_ficheiros_csv(ficheiro_a_ordenar=None, cabecalho=True):
    """
    Ordena os ficheiros .csv da base de dados
    :param ficheiro_a_ordenar: Path absoluto para ficheiro .csv a ordenar. Se for None, são ordenados todos os .csv da base de dados
    :param cabecalho: Se True, considera que a 1ª linha do ficheiro .csv é o cabeçalho
    :return:
    """
    print('A começar ordenação...')

    if ficheiro_a_ordenar is None:
        ordenar_ligacoes_destinos()
        print('Locais das tabelas de ligação e destino ordenados')

    chave = cmp_to_key(ordenador)

    if ficheiro_a_ordenar is not None:
        ficheiros_a_ordenar = [ficheiro_a_ordenar]
    else:
        ficheiros_a_ordenar = [CSV_COMARCA, CSV_CONCELHO, CSV_DESTINO, CSV_LIGACAO, CSV_LOCAL, CSV_LOCAL_ESPANHA,
                               CSV_LOCAL_GIBRALTAR, CSV_LOCAL_PORTUGAL, CSV_MUNICIPIO, CSV_PROVINCIA]

    for ficheiro in ficheiros_a_ordenar:
        if ficheiro_a_ordenar is None:
            path_csv = os.path.join(path, ficheiro)
        else:
            path_csv = ficheiro

        linhas = csv_para_list(path_csv)
        if cabecalho:
            cabecalho = linhas.pop(0)
        print(f'A ordenar ficheiro {ficheiro}. {len(linhas)} entradas no ficheiro')
        linhas.sort(key=chave)
        if cabecalho:
            linhas.insert(0, cabecalho)
        list_para_csv(path_csv, linhas)

    print('Ordenação concluída')


def ordenar_ligacoes_destinos():
    """
    Para cada linha das tabelas de ligação e destino, troca entre si os locais se estiverem desordenados.
    Se isso acontecer, inverte também os parâmetros que dependem da ordem dos locais na linha:
        -Tabela ligação: inverter ponto cardeal (E -> O), trocar ordem A com ordem B
        -Tabela destino: inverter origem (False -> True)
    :return:
    """
    path_ligacao = os.path.join(path, CSV_LIGACAO)
    path_destino = os.path.join(path, CSV_DESTINO)

    for path_csv in [path_ligacao, path_destino]:
        linhas = csv_para_list(path_csv)
        cabecalho = linhas.pop(0)

        linhas_ordenadas = []
        for linha in linhas:
            campos = separar_por_virgulas([linha])
            local_a = campos[LOCAL_A]
            local_b = campos[LOCAL_B]

            chave = cmp_to_key(ordenador)
            temp = [local_a, local_b]
            temp.sort(key=chave)

            if temp != [local_a, local_b]:  # Locais estão pela ordem errada
                campos[LOCAL_A] = local_b
                campos[LOCAL_B] = local_a

                if path_csv == path_ligacao:
                    ordem_a = campos[ORDEM_A]
                    ordem_b = campos[ORDEM_B]

                    campos[PONTO_CARDEAL] = obter_ponto_cardeal_oposto(campos[PONTO_CARDEAL])
                    campos[ORDEM_A] = ordem_b
                    campos[ORDEM_B] = ordem_a

                elif path_csv == path_destino:
                    campos[ORIGEM] = True if campos[ORIGEM] == 'False' else False

            for i in range(len(campos)):
                campos[i] = str(campos[i])
            linhas_ordenadas.append(",".join(campos))

        linhas_ordenadas.insert(0, cabecalho)
        list_para_csv(path_csv, linhas_ordenadas)


def csv_para_list(path_csv):
    """
    Retorna csv como lista de linhas
    :param path_csv:
    :return:
    """

    with open(path_csv, mode='r', encoding=ENCODING) as ficheiro:
        reader = csv.reader(ficheiro, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=QUOTING, escapechar=ESCAPECHAR)
        linhas = []
        for linha in reader:
            linhas.append(",".join(linha))

        return linhas


def list_para_csv(path_csv, linhas):
    """
    Escreve lista de linhas para ficheiro csv
    :param path_csv:
    :param linhas:
    :return:
    """

    with open(path_csv, mode='w', encoding=ENCODING) as ficheiro:
        for linha in linhas:
            ficheiro.write(linha)
            ficheiro.write("\n")


def ordenador(a, b):
    """
    Função de ordenação das linhas de um ficheiro .csv
    :param a:
    :param b:
    :return: -1 se parâmetro a for menor que b, 0 se for igual, 1 se for maior
    """
    a = [a]
    b = [b]

    # Pré-processamento

    a = separar_por_virgulas(a)
    b = separar_por_virgulas(b)

    a = retirar_aspas(a)
    b = retirar_aspas(b)

    a = retirar_acentuacao(a)
    b = retirar_acentuacao(b)

    a = separar_por_hifen(a)
    b = separar_por_hifen(b)

    a = separar_por_espacos(a)
    b = separar_por_espacos(b)

    a = separar_numeros_nao_numeros(a)
    b = separar_numeros_nao_numeros(b)

    a = conversor_lista_numeros_romanos_arabes(a)
    b = conversor_lista_numeros_romanos_arabes(b)

    a = converter_para_minusculas(a)
    b = converter_para_minusculas(b)

    # Comparação

    for i in range(len(a)):
        if i >= len(b):
            return MAIOR  # A-1 - Saída 1A > A-1 - Saída 1

        comparacao = comparador(a[i], b[i])
        if comparacao != IGUAL:
            return comparacao

    return IGUAL


def separar_por_virgulas(lista):
    lista_temp = []
    for palavra in lista:
        lista_temp.extend(palavra.split(','))

    lista_retornar = []
    continuar = False
    for i in range(len(lista_temp)):
        if continuar:
            continuar = False
            continue

        palavra = lista_temp[i]
        if QUOTECHAR in palavra and i < len(lista_temp) - 1:
            lista_retornar.append(palavra + "," + lista_temp[i+1])  # '"Álamo', 'Alcoutim"' -> '"Álamo, Alcoutim"'
            continuar = True
        else:
            lista_retornar.append(palavra.strip())

    return lista_retornar


def retirar_aspas(lista):
    lista_retornar = []
    for palavra in lista:
        palavra = palavra.replace('"', '')
        lista_retornar.append(palavra)
    return lista_retornar


def retirar_acentuacao(lista):
    lista_retornar = []
    for palavra in lista:
        palavra = palavra.replace('á', 'a')
        palavra = palavra.replace('Á', 'A')

        palavra = palavra.replace('à', 'a')
        palavra = palavra.replace('À', 'A')

        palavra = palavra.replace('ã', 'a')
        palavra = palavra.replace('Ã', 'A')

        palavra = palavra.replace('â', 'a')
        palavra = palavra.replace('Â', 'A')

        palavra = palavra.replace('ç', 'c')
        palavra = palavra.replace('Ç', 'C')

        palavra = palavra.replace('é', 'e')
        palavra = palavra.replace('É', 'E')

        palavra = palavra.replace('è', 'e')
        palavra = palavra.replace('È', 'E')

        palavra = palavra.replace('ê', 'e')
        palavra = palavra.replace('Ê', 'E')

        palavra = palavra.replace('í', 'i')
        palavra = palavra.replace('Í', 'I')

        palavra = palavra.replace('ì', 'i')
        palavra = palavra.replace('Ì', 'I')

        palavra = palavra.replace('î', 'i')
        palavra = palavra.replace('Î', 'I')

        palavra = palavra.replace('ñ', 'n')
        palavra = palavra.replace('Ñ', 'N')

        palavra = palavra.replace('ó', 'o')
        palavra = palavra.replace('Ó', 'O')

        palavra = palavra.replace('ò', 'o')
        palavra = palavra.replace('Ò', 'O')

        palavra = palavra.replace('õ', 'o')
        palavra = palavra.replace('Õ', 'O')

        palavra = palavra.replace('ô', 'o')
        palavra = palavra.replace('Ô', 'O')

        palavra = palavra.replace('ú', 'u')
        palavra = palavra.replace('Ú', 'U')

        palavra = palavra.replace('ù', 'u')
        palavra = palavra.replace('Ù', 'U')

        palavra = palavra.replace('û', 'u')
        palavra = palavra.replace('Û', 'U')

        lista_retornar.append(palavra)

    return lista_retornar


def converter_para_minusculas(lista):
    lista_retornar = []
    for palavra in lista:
        lista_retornar.append(palavra.lower())
    return lista_retornar


def separar_por_hifen(lista):
    lista_retornar = []
    for palavra in lista:
        lista_retornar.extend(palavra.split(' - '))
    return lista_retornar


def separar_por_espacos(lista):
    lista_retornar = []
    for palavra in lista:
        lista_retornar.extend(palavra.split(' '))
    return lista_retornar


def separar_numeros_nao_numeros(lista):
    """
    Separa palavras com caracteres alfa-numéricos em blocos só com letras ou só com números
    A um bloco numérico irá seguir-se um bloco vazio se não houver letras a seguir
    -A-5 -> ['A-', '5', '']
    -A-5R -> ['A-', '5', 'R']
    :param lista:
    :return:
    """
    lista_retorno = []
    for palavra in lista:

        blocos = []
        bloco = ''
        numerico = False

        for i in range(len(palavra)):
            letra = palavra[i]
            if numerico == is_numerico(letra):
                bloco += letra
            else:
                numerico = is_numerico(letra)
                if bloco:
                    blocos.append(bloco)
                bloco = ''
                bloco += letra

            if i == len(palavra) - 1:
                blocos.append(bloco)
                if is_numerico(letra):
                    blocos.append('')

        lista_retorno.extend(blocos)

    return lista_retorno


def comparador(a, b):
    """
    Função de ordenação, compara blocos de letras ou de números
    :param a:
    :param b:
    :return: -1 se elemento a é menor que elemento b, 0 se for igual, 1 se for maior
    """
    if len(a.strip()) == 0 and len(b.strip()) > 0:
        return MENOR
    elif len(a.strip()) > 0 and len(b.strip()) == 0:
        return MAIOR

    if is_numerico(a) and not is_numerico(b):
        return MENOR  # Números virão antes de palavras
    elif not is_numerico(a) and is_numerico(b):
        return MAIOR

    if is_numerico(a):
        a = int(a)
    if is_numerico(b):
        b = int(b)

    if a < b:
        return MENOR
    elif a == b:
        return IGUAL
    else:
        return MAIOR


def conversor_lista_numeros_romanos_arabes(lista):
    lista_retornar = []
    for palavra in lista:
        lista_retornar.append(str(conversor_numeros_romanos_arabes(palavra)))
    return lista_retornar


def conversor_numeros_romanos_arabes(numero_potencial):
    """
    :param numero_potencial: String que poderá ser número romano
    :return: Conversão para número árabe, ou string intacta se não for número romano
    """
    algarismos_romanos = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

    # IC - Itinerário Complementar, M - Estrada Municipal, C - Pode aparecer num número de saída (ex: 108C)
    if numero_potencial in ['IC', 'M', 'C']:  # Não considerar como número romano
        return numero_potencial

    if len(numero_potencial.strip()) == 0:
        return numero_potencial

    valor = 0
    continuar = False
    for i in range(len(numero_potencial)):
        if continuar:
            continuar = False
            continue

        if numero_potencial[i] not in algarismos_romanos.keys():
            return numero_potencial  # Não é número romano
        elif i < len(numero_potencial) - 1 and numero_potencial[i+1] not in algarismos_romanos.keys():
            return numero_potencial

        if i == len(numero_potencial) - 1:
            valor += algarismos_romanos[numero_potencial[i]]
        elif numero_potencial[i] == numero_potencial[i+1] or \
                algarismos_romanos[numero_potencial[i+1]] < algarismos_romanos[numero_potencial[i]]:  # XX, XI
            valor += algarismos_romanos[numero_potencial[i]]
        elif algarismos_romanos[numero_potencial[i+1]] > algarismos_romanos[numero_potencial[i]]:  # Ex: IX
            valor = valor + algarismos_romanos[numero_potencial[i+1]] - algarismos_romanos[numero_potencial[i]]
            continuar = True

    return valor


def is_numerico(caracter):
    return caracter.isdigit()
