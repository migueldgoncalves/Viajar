from typing import Union
import csv
from functools import cmp_to_key

from travel.main.cardinal_points import get_opposite_cardinal_point
from travel.main import paths_and_files

"""
This module sorts the content of .csv files
"""

LESS_THAN = -1
EQUAL_TO = 0
MORE_THAN = 1

DELIMITER = ','
QUOTECHAR = '"'
QUOTING = csv.QUOTE_NONE
ENCODING = 'utf-8'

# Positions of fields inside the database .csv files
LOCATION_A = 0
LOCATION_B = 1
CARDINAL_POINT = 5
ORDER_A = 6
ORDER_B = 7
SOURCE = 3


def sort_csv_files(file_to_sort=None, is_header_present=True) -> None:
    """
    Main routine to sort .csv files
    :param file_to_sort: Absolute path to a .csv file to be sorted. If None, all .csv files of the DB are instead sorted
    :param is_header_present: If True, first line in file is considered to be the header. If False, no header is assumed to be present
    :return:
    """
    print('Starting .csv file(s) sorting...')

    if file_to_sort is None:
        sort_locations_in_connections_and_destinations()
        print("Sorted locations inside Connection and Destination tables")

    sorting_key = cmp_to_key(line_sorting_function)

    if file_to_sort is not None:
        all_files_to_sort = [file_to_sort]
    else:
        all_files_to_sort = [
            paths_and_files.CSV_CONCELHO_PATH, paths_and_files.CSV_CONNECTION_PATH,
            paths_and_files.CSV_DESTINATION_PATH, paths_and_files.CSV_LOCATION_PATH, paths_and_files.CSV_LOCATION_ANDORRA_PATH,
            paths_and_files.CSV_LOCATION_BEYOND_IBERIAN_PENINSULA_PATH, paths_and_files.CSV_LOCATION_GIBRALTAR_PATH,
            paths_and_files.CSV_LOCATION_PORTUGAL_PATH, paths_and_files.CSV_LOCATION_SPAIN_PATH,
            paths_and_files.CSV_MUNICIPIO_PATH, paths_and_files.CSV_PROVINCE_PATH,
        ]

    for path_csv in all_files_to_sort:

        file_lines: list[str] = csv_to_list(path_csv)
        if is_header_present:
            header: str = file_lines.pop(0)
        else:
            header: str = ''
        print(f'Sorting file {path_csv}. {len(file_lines)} entries in the file')
        file_lines.sort(key=sorting_key)
        if header:
            file_lines.insert(0, header)
        list_to_csv(path_csv, file_lines)

    print('Finished sorting')


def sort_locations_in_connections_and_destinations() -> None:
    """
    For each line of the Connection and Destination tables, switches the 2 location names if they are not sorted
    If this occurs, also inverts the parameters that rely on the order of the location names in that line:
        -Connection table - Invert cardinal point (ex: E -> W), switch order A with order B
        -Destination table - Invert source (ex: False -> True)
    :return:
    """
    connections_filepath: str = paths_and_files.CSV_CONNECTION_PATH
    destinations_filepath: str = paths_and_files.CSV_DESTINATION_PATH

    for path_csv in [connections_filepath, destinations_filepath]:
        lines: list[str] = csv_to_list(path_csv)
        header: str = lines.pop(0)

        sorted_lines: list[str] = []
        for line in lines:
            fields: list[str] = split_by_commas([line])
            location_a: str = fields[LOCATION_A]
            location_b: str = fields[LOCATION_B]

            sorting_key = cmp_to_key(line_sorting_function)
            sorted_location_names: list[str] = [location_a, location_b]
            sorted_location_names.sort(key=sorting_key)

            if sorted_location_names != [location_a, location_b]:  # Location names are not sorted
                fields[LOCATION_A] = location_b
                fields[LOCATION_B] = location_a

                if path_csv == connections_filepath:
                    order_a: str = fields[ORDER_A]
                    order_b: str = fields[ORDER_B]

                    fields[CARDINAL_POINT] = get_opposite_cardinal_point(fields[CARDINAL_POINT])
                    fields[ORDER_A] = order_b
                    fields[ORDER_B] = order_a

                elif path_csv == destinations_filepath:
                    fields[SOURCE] = 'True' if fields[SOURCE] == 'False' else 'False'

            for i in range(len(fields)):
                fields[i] = str(fields[i])
            sorted_lines.append(",".join(fields))

        sorted_lines.insert(0, header)
        list_to_csv(path_csv, sorted_lines)


def csv_to_list(path_csv: str) -> list[str]:
    """
    Returns the content of a .csv file as a list of strings
    :param path_csv: The absolute path to the file
    :return: Content of the file
    """

    with open(path_csv, mode='r', encoding=ENCODING) as f:
        reader = csv.reader(f, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=QUOTING)
        lines: list[str] = []
        for line in reader:
            lines.append(",".join(line))

        return lines


def list_to_csv(path_csv: str, content_lines: list[str]) -> None:
    """
    Writes list of lines into a .csv file. File will be overwritten
    :param path_csv: Absolute path to the .csv file to write
    :param content_lines: The lines to write
    :return:
    """

    with open(path_csv, mode='w', encoding=ENCODING) as f:
        for line in content_lines:
            f.write(line)
            f.write("\n")


def line_sorting_function(line_a: str, line_b: str) -> int:
    """
    Base sorting function for the lines of a .csv file
    :param line_a: A line of content
    :param line_b: Another line of content
    :return: -1 if line A comes first, 0 if lines A and B are the same, 1 if line B comes first
    """
    a: list[str] = [line_a]
    b: list[str] = [line_b]

    # Pre-processing

    a = split_by_commas(a)
    b = split_by_commas(b)

    a = remove_quote_chars(a)
    b = remove_quote_chars(b)

    a = remove_diacritics(a)
    b = remove_diacritics(b)

    a = separate_by_hyphen(a)
    b = separate_by_hyphen(b)

    a = separate_by_whitespace(a)
    b = separate_by_whitespace(b)

    a = split_by_number_sequences(a)
    b = split_by_number_sequences(b)

    a = convert_roman_to_arab_numbers(a)
    b = convert_roman_to_arab_numbers(b)

    a = convert_to_lower_case(a)
    b = convert_to_lower_case(b)

    # Comparing

    for i in range(len(a)):
        if i >= len(b):
            return MORE_THAN  # A-1 - Exit 1A > A-1 - Exit 1 (i.e. "A-1 - Exit 1" will appear first)

        comparing_result: int = comparator(a[i], b[i])
        if comparing_result != EQUAL_TO:
            return comparing_result

    return EQUAL_TO  # Same string?


def split_by_commas(string_list: list[str]) -> list[str]:
    temp_list: list[str] = []
    for word in string_list:
        temp_list.extend(word.split(','))

    list_to_return: list[str] = []
    continue_processing: int = 0
    for i in range(len(temp_list)):
        if continue_processing:
            continue_processing -= 1
            continue

        word: str = temp_list[i]
        if QUOTECHAR in word and i < len(temp_list) - 1:  # Word must be concatenated with one or more words in front of it. Ex: '"Álamo', 'Alcoutim"' -> '"Álamo, Alcoutim"'
            string_with_commas: str = ''
            for j in range(i, len(temp_list)):
                string_with_commas = ','.join([string_with_commas, temp_list[j]])
                if QUOTECHAR in temp_list[j] and i != j:
                    break
                continue_processing += 1
            string_with_commas = string_with_commas[1:]  # At this point this string has a leading "," that must be removed
            list_to_return.append(string_with_commas)
        else:
            list_to_return.append(word.strip())

    return list_to_return


def remove_quote_chars(string_list: list[str]) -> list[str]:
    list_to_return: list[str] = []
    for word in string_list:
        word = word.replace('"', '')
        list_to_return.append(word)
    return list_to_return


def remove_diacritics(string_list: list[str]) -> list[str]:
    list_to_return: list[str] = []
    for word in string_list:
        word = word.replace('á', 'a')
        word = word.replace('Á', 'A')

        word = word.replace('à', 'a')
        word = word.replace('À', 'A')

        word = word.replace('ã', 'a')
        word = word.replace('Ã', 'A')

        word = word.replace('â', 'a')
        word = word.replace('Â', 'A')

        word = word.replace('ç', 'c')
        word = word.replace('Ç', 'C')

        word = word.replace('é', 'e')
        word = word.replace('É', 'E')

        word = word.replace('è', 'e')
        word = word.replace('È', 'E')

        word = word.replace('ê', 'e')
        word = word.replace('Ê', 'E')

        word = word.replace('í', 'i')
        word = word.replace('Í', 'I')

        word = word.replace('ì', 'i')
        word = word.replace('Ì', 'I')

        word = word.replace('î', 'i')
        word = word.replace('Î', 'I')

        word = word.replace('ñ', 'n')
        word = word.replace('Ñ', 'N')

        word = word.replace('ó', 'o')
        word = word.replace('Ó', 'O')

        word = word.replace('ò', 'o')
        word = word.replace('Ò', 'O')

        word = word.replace('õ', 'o')
        word = word.replace('Õ', 'O')

        word = word.replace('ô', 'o')
        word = word.replace('Ô', 'O')

        word = word.replace('ú', 'u')
        word = word.replace('Ú', 'U')

        word = word.replace('ù', 'u')
        word = word.replace('Ù', 'U')

        word = word.replace('û', 'u')
        word = word.replace('Û', 'U')

        list_to_return.append(word)

    return list_to_return


def convert_to_lower_case(string_list: list[str]) -> list[str]:
    list_to_return: list[str] = []
    for word in string_list:
        list_to_return.append(word.lower())
    return list_to_return


def separate_by_hyphen(string_list: list[str]) -> list[str]:
    list_to_return: list[str] = []
    for word in string_list:
        list_to_return.extend(word.split(' - '))
    return list_to_return


def separate_by_whitespace(string_list: list[str]) -> list[str]:
    list_to_return: list[str] = []
    for word in string_list:
        list_to_return.extend(word.split(' '))
    return list_to_return


def split_by_number_sequences(string_list: list[str]) -> list[str]:
    """
    Splits words with alphanumeric chars into blocks with either numbers only or no numbers at all
    A number-only block will be followed by an empty block if the original word has no letters afterward
    -A-5 -> ['A-', '5', '']
    -A-5R -> ['A-', '5', 'R']
    :param string_list:
    :return:
    """
    list_to_return: list[str] = []
    for word in string_list:

        blocks: list[str] = []
        block: str = ''
        numeric: bool = False

        for i in range(len(word)):
            letter: str = word[i]
            if numeric == is_number(letter):
                block += letter
            else:
                numeric = is_number(letter)
                if block:
                    blocks.append(block)
                block = ''
                block += letter

            if i == len(word) - 1:
                blocks.append(block)
                if is_number(letter):
                    blocks.append('')

        list_to_return.extend(blocks)

    return list_to_return


def comparator(a: Union[str, int], b: Union[str, int]) -> int:
    """
    Base sorting function. Compares two blocks of letters or numbers
    :param a:
    :param b:
    :return: -1 if block A comes first, 0 if both blocks are the same, 1 if block B comes first
    """
    if len(a.strip()) == 0 and len(b.strip()) > 0:
        return LESS_THAN
    elif len(a.strip()) > 0 and len(b.strip()) == 0:
        return MORE_THAN

    if is_number(a) and not is_number(b):
        return LESS_THAN  # Numbers will appear before letters
    elif not is_number(a) and is_number(b):
        return MORE_THAN

    if is_number(a):
        a = int(a)
    if is_number(b):
        b = int(b)

    if a < b:
        return LESS_THAN
    elif a == b:
        return EQUAL_TO
    else:
        return MORE_THAN


def convert_roman_to_arab_numbers(string_list: list[str]) -> list[str]:
    list_to_return: list[str] = []
    for word in string_list:
        list_to_return.append(str(convert_roman_to_arab_number(word)))
    return list_to_return


def convert_roman_to_arab_number(potential_number: str) -> Union[str, int]:
    """
    :param potential_number: String that may be a Roman numeral
    :return: Corresponding Arab number, or the same string if not a Roman numeral
    """
    roman_numerals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

    # IC - Portuguese Complementary Itinerary Road (Itinerário Complementar)
    # M - Portuguese Municipal Road (Estrada Municipal)
    # C - May appear inside a freeway/motorway exit number (ex: 108C)
    if potential_number in ['IC', 'M', 'C']:  # Do not handle as a Roman numeral
        return potential_number

    if len(potential_number.strip()) == 0:
        return potential_number

    value: int = 0
    continue_processing: bool = False
    for i in range(len(potential_number)):
        if continue_processing:
            continue_processing = False
            continue

        if potential_number[i] not in roman_numerals.keys():
            return potential_number  # Not a Roman numeral
        elif i < len(potential_number) - 1 and potential_number[i + 1] not in roman_numerals.keys():
            return potential_number

        if i == len(potential_number) - 1:
            value += roman_numerals[potential_number[i]]
        elif potential_number[i] == potential_number[i + 1] or roman_numerals[potential_number[i + 1]] < roman_numerals[potential_number[i]]:  # XX, XI
            value += roman_numerals[potential_number[i]]
        elif roman_numerals[potential_number[i + 1]] > roman_numerals[potential_number[i]]:  # Ex: IX
            value = value + roman_numerals[potential_number[i + 1]] - roman_numerals[potential_number[i]]
            continue_processing = True

    return value


def is_number(char: str) -> bool:
    return char.isdigit()
