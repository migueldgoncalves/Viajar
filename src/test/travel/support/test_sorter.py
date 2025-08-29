import unittest

from travel.support import sorter


class TestSorter(unittest.TestCase):

    def test_line_sorter(self):
        self.assertEqual(sorter.EQUAL_TO, sorter.line_sorting_function('"Álamo, Guerreiros do Rio"', '"Álamo, Guerreiros do Rio"'))
        self.assertEqual(sorter.MORE_THAN, sorter.line_sorting_function('"Álamo, Guerreiros do Rio"', 'Álamo, Guerreiros do Rio'))
        self.assertEqual(sorter.LESS_THAN, sorter.line_sorting_function('"Álamo, Guerreiros do Rio"', 'Guerreiros do Rio'))
        self.assertEqual(sorter.MORE_THAN, sorter.line_sorting_function('"Álamo, Guerreiros do Rio"', 'A-1 - Exit 1'))
        self.assertEqual(sorter.LESS_THAN, sorter.line_sorting_function('Guerreiros do Rio', 'Laranjeiras'))
        self.assertEqual(sorter.MORE_THAN, sorter.line_sorting_function('A-1 - Exit 10', 'A-1 - Exit 2'))
        self.assertEqual(sorter.MORE_THAN, sorter.line_sorting_function('A-1 - Exit 100', 'A-1 - Exit 9'))
        self.assertEqual(sorter.LESS_THAN, sorter.line_sorting_function('A-1 - Exit 100', 'A-2 - Exit 9'))
        self.assertEqual(sorter.MORE_THAN, sorter.line_sorting_function('A-10 - Exit 100', 'A-2 - Exit 9'))
        self.assertEqual(sorter.MORE_THAN, sorter.line_sorting_function('A-7 x AP-7 - VII', 'A2 x A22'))
        self.assertEqual(sorter.MORE_THAN, sorter.line_sorting_function('A-4 - Exit 250-252', 'A-4 - Exit 249'))
        self.assertEqual(sorter.LESS_THAN, sorter.line_sorting_function('A-4 - Exit 250-252', 'A-4 - Exit 253'))
        self.assertEqual(sorter.MORE_THAN, sorter.line_sorting_function('A-5 - Exit 250-252', 'A-5 - Aluche'))
        self.assertEqual(sorter.LESS_THAN, sorter.line_sorting_function('A-7 - Exit 132', 'A-7/AP-7 - Exit 155'))
        self.assertEqual(sorter.LESS_THAN, sorter.line_sorting_function('A-7 - Exit 156', 'A-7/AP-7 - Exit 155'))
        self.assertEqual(sorter.LESS_THAN, sorter.line_sorting_function('A-1 - Exit 10', 'A-1 - Exit 10A'))
        self.assertEqual(sorter.LESS_THAN, sorter.line_sorting_function('A-1 - Exit 10A', 'A-1 - Exit 10B'))
        self.assertEqual(sorter.MORE_THAN, sorter.line_sorting_function('A-1 - Exit 10A', 'A1 - Exit 10B'))
        self.assertEqual(sorter.LESS_THAN, sorter.line_sorting_function('Algarve International Circuit,37.231507,-8.628383,105,', '"Avenida de España, La Línea de la Concepción",36.164777,-5.360756,4,'))
        self.assertEqual(sorter.LESS_THAN, sorter.line_sorting_function('"Avenida de España, La Línea de la Concepción",36.164777,-5.360756,4,', 'Ayamonte,37.215788,-7.405922,20,'))
        self.assertEqual(sorter.LESS_THAN, sorter.line_sorting_function('A-7 - Exit 246,A-7 x MA-24 - West,Carro,1.0,A-7,NE,2,1', 'A-7 - Exit 292,A-7 - Exit 295,Car,3.3,A-7,E,2,1'))
        self.assertEqual(sorter.LESS_THAN, sorter.line_sorting_function('A-7 - Exit 292,A-7 - Exit 295,Car,3.3,A-7,E,2,1', 'A-7 - Exit 295,A-7 - Exit 305,Car,9.7,A-7,E,2,1'))
        self.assertEqual(sorter.LESS_THAN, sorter.line_sorting_function('"A-7 - Exit 292",A-7 - Exit 295,Car,3.3,A-7,E,2,1', 'A-7 - Exit 295,A-7 - Exit 305,Car,9.7,A-7,E,2,1'))
        self.assertEqual(sorter.LESS_THAN, sorter.line_sorting_function('A-7 - Exit 292,A-7 - Exit 295,Car,3.3,A-7,E,2,1', '"A-7 - Exit 295",A-7 - Exit 305,Car,9.7,A-7,E,2,1'))

    def test_split_by_commas(self):
        self.assertEqual(['Álamo', 'Alcoutim'], sorter.split_by_commas(['Álamo, Alcoutim']))
        self.assertEqual(['Álamo', 'Alcoutim', 'Alcoutim'], sorter.split_by_commas(['Álamo,Alcoutim,Alcoutim']))
        self.assertEqual(['"Álamo, Alcoutim"', 'Alcoutim', 'Alcoutim'], sorter.split_by_commas(['"Álamo, Alcoutim",Alcoutim,Alcoutim']))
        self.assertEqual(['A1 - Exit 18', '"Santa Maria da Feira, Travanca, Sanfins e Espargo"', 'Santa Maria da Feira'], sorter.split_by_commas(['A1 - Exit 18,"Santa Maria da Feira, Travanca, Sanfins e Espargo",Santa Maria da Feira']))

    def test_remove_quote_chars(self):
        self.assertEqual(['Álamo, Guerreiros do Rio'], sorter.remove_quote_chars(['"Álamo, Guerreiros do Rio"']))
        self.assertEqual(['Álamo, Guerreiros do Rio'], sorter.remove_quote_chars(['Álamo, Guerreiros do Rio']))

    def test_remove_diacritics(self):
        self.assertEqual(['Almunecar'], sorter.remove_diacritics(['Almuñécar']))
        self.assertEqual(['Alamo'], sorter.remove_diacritics(['Álamo']))
        self.assertEqual(['Conceicao'], sorter.remove_diacritics(['Conceição']))

    def test_convert_to_lower_case(self):
        self.assertEqual(['a-1 - exit 1'], sorter.convert_to_lower_case(['A-1 - Exit 1']))
        self.assertEqual(['a-1 - exit 1', 'a-1 - exit 2'], sorter.convert_to_lower_case(['A-1 - Exit 1', 'A-1 - Exit 2']))

    def test_separate_by_hyphen(self):
        self.assertEqual(['A-1', 'Exit 1'], sorter.separate_by_hyphen(['A-1 - Exit 1']))
        self.assertEqual(['A-1 Exit 1'], sorter.separate_by_hyphen(['A-1 Exit 1']))

    def test_separate_by_whitespace(self):
        self.assertEqual(['Vila', 'Real', 'de', 'Santo', 'António'], sorter.separate_by_whitespace(['Vila Real', 'de Santo António']))

    def test_split_by_number_sequences(self):
        self.assertEqual(['AP-', '36', '', 'x', 'R-', '4', ''], sorter.split_by_number_sequences(['AP-36', 'x', 'R-4']))
        self.assertEqual(['Exit', '32', 'B'], sorter.split_by_number_sequences(['Exit', '32B']))
        self.assertEqual(['Vélez-Málaga'], sorter.split_by_number_sequences(['Vélez-Málaga']))
        self.assertEqual(['A-', '5', ''], sorter.split_by_number_sequences(['A-5']))
        self.assertEqual(['A-', '5', 'R'], sorter.split_by_number_sequences(['A-5R']))
        self.assertEqual(['IC', '17', ''], sorter.split_by_number_sequences(['IC17']))
        self.assertEqual(['A', '26', '-', '1', ''], sorter.split_by_number_sequences(['A26-1']))
        self.assertEqual(['A-', '7', '/AP-', '7', '', 'Exit', '32', 'B'], sorter.split_by_number_sequences(['A-7/AP-7', 'Exit', '32B']))

    def test_comparator(self):
        self.assertEqual(sorter.LESS_THAN, sorter.comparator('a', 'b'))
        self.assertEqual(sorter.MORE_THAN, sorter.comparator('b', 'a'))
        self.assertEqual(sorter.EQUAL_TO, sorter.comparator('a', 'a'))
        self.assertEqual(sorter.LESS_THAN, sorter.comparator('az', 'b'))
        self.assertEqual(sorter.MORE_THAN, sorter.comparator('c', 'ba'))
        self.assertEqual(sorter.LESS_THAN, sorter.comparator('0', '1'))
        self.assertEqual(sorter.MORE_THAN, sorter.comparator('1', '0'))
        self.assertEqual(sorter.MORE_THAN, sorter.comparator('10', '2'))
        self.assertEqual(sorter.MORE_THAN, sorter.comparator('100', '99'))
        self.assertEqual(sorter.LESS_THAN, sorter.comparator('2', '10'))
        self.assertEqual(sorter.LESS_THAN, sorter.comparator('99', '100'))
        self.assertEqual(sorter.LESS_THAN, sorter.comparator('', '1'))
        self.assertEqual(sorter.LESS_THAN, sorter.comparator('', 'a'))
        self.assertEqual(sorter.MORE_THAN, sorter.comparator('1', ''))
        self.assertEqual(sorter.MORE_THAN, sorter.comparator('a', ''))
        self.assertEqual(sorter.LESS_THAN, sorter.comparator('Alcaria', 'Alcaria dos Javazes'))

    def test_convert_roman_to_arab_numbers(self):
        self.assertEqual(['1'], sorter.convert_roman_to_arab_numbers(['I']))
        self.assertEqual(['Port', 'of', 'Sines', 'Terminal', '21'], sorter.convert_roman_to_arab_numbers(['Port', 'of', 'Sines', 'Terminal', 'XXI']))

    def test_convert_roman_to_arab_number(self):
        self.assertEqual('', sorter.convert_roman_to_arab_number(''))
        self.assertEqual('   ', sorter.convert_roman_to_arab_number('   '))
        self.assertEqual('ewhfuiwhfiewhuifhwfohweyif', sorter.convert_roman_to_arab_number('ewhfuiwhfiewhuifhwfohweyif'))
        self.assertEqual('IC', sorter.convert_roman_to_arab_number('IC'))  # Portuguese Complementary Itinerary Road (Itinerário Complementar)
        self.assertEqual('M', sorter.convert_roman_to_arab_number('M'))  # Portuguese Municipal Road (Estrada Municipal)
        self.assertEqual('C', sorter.convert_roman_to_arab_number('C'))  # May appear inside a freeway/motorway exit number (ex: 108C)
        self.assertEqual('VC', sorter.convert_roman_to_arab_number('VC'))  # VC Fashion Outlet / Modivas Station in Porto Metro

        self.assertEqual(1, sorter.convert_roman_to_arab_number('I'))
        self.assertEqual(2, sorter.convert_roman_to_arab_number('II'))
        self.assertEqual(3, sorter.convert_roman_to_arab_number('III'))
        self.assertEqual(4, sorter.convert_roman_to_arab_number('IV'))
        self.assertEqual(5, sorter.convert_roman_to_arab_number('V'))
        self.assertEqual(6, sorter.convert_roman_to_arab_number('VI'))
        self.assertEqual(7, sorter.convert_roman_to_arab_number('VII'))
        self.assertEqual(8, sorter.convert_roman_to_arab_number('VIII'))
        self.assertEqual(9, sorter.convert_roman_to_arab_number('IX'))
        self.assertEqual(10, sorter.convert_roman_to_arab_number('X'))
        self.assertEqual(11, sorter.convert_roman_to_arab_number('XI'))
        self.assertEqual(19, sorter.convert_roman_to_arab_number('XIX'))
        self.assertEqual(20, sorter.convert_roman_to_arab_number('XX'))
        self.assertEqual(21, sorter.convert_roman_to_arab_number('XXI'))
        self.assertEqual(29, sorter.convert_roman_to_arab_number('XXIX'))
        self.assertEqual(30, sorter.convert_roman_to_arab_number('XXX'))
        self.assertEqual(31, sorter.convert_roman_to_arab_number('XXXI'))
        self.assertEqual(49, sorter.convert_roman_to_arab_number('XLIX'))
        self.assertEqual(50, sorter.convert_roman_to_arab_number('L'))
        self.assertEqual(51, sorter.convert_roman_to_arab_number('LI'))
        self.assertEqual(99, sorter.convert_roman_to_arab_number('XCIX'))
        self.assertEqual(101, sorter.convert_roman_to_arab_number('CI'))
        self.assertEqual(299, sorter.convert_roman_to_arab_number('CCXCIX'))
        self.assertEqual(300, sorter.convert_roman_to_arab_number('CCC'))
        self.assertEqual(301, sorter.convert_roman_to_arab_number('CCCI'))
        self.assertEqual(499, sorter.convert_roman_to_arab_number('CDXCIX'))
        self.assertEqual(500, sorter.convert_roman_to_arab_number('D'))
        self.assertEqual(501, sorter.convert_roman_to_arab_number('DI'))
        self.assertEqual(999, sorter.convert_roman_to_arab_number('CMXCIX'))
        self.assertEqual(1001, sorter.convert_roman_to_arab_number('MI'))
        self.assertEqual(2999, sorter.convert_roman_to_arab_number('MMCMXCIX'))
        self.assertEqual(3000, sorter.convert_roman_to_arab_number('MMM'))
        self.assertEqual(3001, sorter.convert_roman_to_arab_number('MMMI'))
        self.assertEqual(3999, sorter.convert_roman_to_arab_number('MMMCMXCIX'))

    def test_is_number(self):
        self.assertFalse(sorter.is_number('a'))
        self.assertFalse(sorter.is_number('B'))
        self.assertFalse(sorter.is_number('-'))
        self.assertFalse(sorter.is_number('.'))
        self.assertFalse(sorter.is_number(' '))
        self.assertFalse(sorter.is_number(''))
        self.assertFalse(sorter.is_number(','))
        self.assertFalse(sorter.is_number('"'))
        self.assertTrue(sorter.is_number('0'))
        self.assertTrue(sorter.is_number('1'))
        self.assertTrue(sorter.is_number('9'))
