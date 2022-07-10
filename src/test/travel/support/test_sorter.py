import unittest

from travel.support import sorter


class TestOrdenador(unittest.TestCase):

    def test_ordenador(self):
        self.assertEqual(sorter.IGUAL, sorter.ordenador('"Álamo, Guerreiros do Rio"', '"Álamo, Guerreiros do Rio"'))
        self.assertEqual(sorter.MAIOR, sorter.ordenador('"Álamo, Guerreiros do Rio"', 'Álamo, Guerreiros do Rio'))
        self.assertEqual(sorter.MENOR, sorter.ordenador('"Álamo, Guerreiros do Rio"', 'Guerreiros do Rio'))
        self.assertEqual(sorter.MAIOR, sorter.ordenador('"Álamo, Guerreiros do Rio"', 'A-1 - Saída 1'))
        self.assertEqual(sorter.MENOR, sorter.ordenador('Guerreiros do Rio', 'Laranjeiras'))
        self.assertEqual(sorter.MAIOR, sorter.ordenador('A-1 - Saída 10', 'A-1 - Saída 2'))
        self.assertEqual(sorter.MAIOR, sorter.ordenador('A-1 - Saída 100', 'A-1 - Saída 9'))
        self.assertEqual(sorter.MENOR, sorter.ordenador('A-1 - Saída 100', 'A-2 - Saída 9'))
        self.assertEqual(sorter.MAIOR, sorter.ordenador('A-10 - Saída 100', 'A-2 - Saída 9'))
        self.assertEqual(sorter.MENOR, sorter.ordenador('Cruzamento VII da A-7 com a AP-7', 'Cruzamento da A2 com a A22'))
        self.assertEqual(sorter.MAIOR, sorter.ordenador('A-4 - Saída 250-252', 'A-4 - Saída 249'))
        self.assertEqual(sorter.MENOR, sorter.ordenador('A-4 - Saída 250-252', 'A-4 - Saída 253'))
        self.assertEqual(sorter.MAIOR, sorter.ordenador('A-5 - Saída 250-252', 'A-5 - Aluche'))
        self.assertEqual(sorter.MENOR, sorter.ordenador('A-7 - Saída 132', 'A-7/AP-7 - Saída 155'))
        self.assertEqual(sorter.MENOR, sorter.ordenador('A-7 - Saída 156', 'A-7/AP-7 - Saída 155'))
        self.assertEqual(sorter.MENOR, sorter.ordenador('A-1 - Saída 10', 'A-1 - Saída 10A'))
        self.assertEqual(sorter.MENOR, sorter.ordenador('A-1 - Saída 10A', 'A-1 - Saída 10B'))
        self.assertEqual(sorter.MAIOR, sorter.ordenador('A-1 - Saída 10A', 'A1 - Saída 10B'))
        self.assertEqual(sorter.MENOR, sorter.ordenador('Autódromo Internacional do Algarve,37.231507,-8.628383,105,', '"Avenida de España, La Línea de la Concepción",36.164777,-5.360756,4,'))
        self.assertEqual(sorter.MENOR, sorter.ordenador('"Avenida de España, La Línea de la Concepción",36.164777,-5.360756,4,', 'Ayamonte,37.215788,-7.405922,20,'))
        self.assertEqual(sorter.MENOR, sorter.ordenador('A-7 - Saída 246,Cruzamento Oeste da A-7 com a MA-24,Carro,1.0,A-7,NE,2,1', 'A-7 - Saída 292,A-7 - Saída 295,Carro,3.3,A-7,E,2,1'))
        self.assertEqual(sorter.MENOR, sorter.ordenador('A-7 - Saída 292,A-7 - Saída 295,Carro,3.3,A-7,E,2,1', 'A-7 - Saída 295,A-7 - Saída 305,Carro,9.7,A-7,E,2,1'))
        self.assertEqual(sorter.MENOR, sorter.ordenador('"A-7 - Saída 292",A-7 - Saída 295,Carro,3.3,A-7,E,2,1', 'A-7 - Saída 295,A-7 - Saída 305,Carro,9.7,A-7,E,2,1'))
        self.assertEqual(sorter.MENOR, sorter.ordenador('A-7 - Saída 292,A-7 - Saída 295,Carro,3.3,A-7,E,2,1', '"A-7 - Saída 295",A-7 - Saída 305,Carro,9.7,A-7,E,2,1'))

    def test_separar_por_virgulas(self):
        self.assertEqual(['Álamo', 'Alcoutim'], sorter.separar_por_virgulas(['Álamo, Alcoutim']))
        self.assertEqual(['Álamo', 'Alcoutim', 'Alcoutim'], sorter.separar_por_virgulas(['Álamo,Alcoutim,Alcoutim']))
        self.assertEqual(['"Álamo, Alcoutim"', 'Alcoutim', 'Alcoutim'], sorter.separar_por_virgulas(['"Álamo, Alcoutim",Alcoutim,Alcoutim']))

    def test_retirar_aspas(self):
        self.assertEqual(['Álamo, Guerreiros do Rio'], sorter.retirar_aspas(['"Álamo, Guerreiros do Rio"']))
        self.assertEqual(['Álamo, Guerreiros do Rio'], sorter.retirar_aspas(['Álamo, Guerreiros do Rio']))

    def test_retirar_acentuacao(self):
        self.assertEqual(['A-1 - Saida 1'], sorter.retirar_acentuacao(['A-1 - Saída 1']))
        self.assertEqual(['Almunecar'], sorter.retirar_acentuacao(['Almuñécar']))
        self.assertEqual(['Alamo'], sorter.retirar_acentuacao(['Álamo']))
        self.assertEqual(['Conceicao'], sorter.retirar_acentuacao(['Conceição']))

    def test_converter_para_minusculas(self):
        self.assertEqual(['a-1 - saída 1'], sorter.converter_para_minusculas(['A-1 - Saída 1']))
        self.assertEqual(['a-1 - saída 1', 'a-1 - saída 2'], sorter.converter_para_minusculas(['A-1 - Saída 1', 'A-1 - Saída 2']))

    def test_separar_por_hifen(self):
        self.assertEqual(['A-1', 'Saída 1'], sorter.separar_por_hifen(['A-1 - Saída 1']))
        self.assertEqual(['A-1 Saída 1'], sorter.separar_por_hifen(['A-1 Saída 1']))

    def test_separar_por_espacos(self):
        self.assertEqual(['Cruzamento', 'da', 'AP-32', 'com', 'a', 'A-1'], sorter.separar_por_espacos(['Cruzamento da AP-32', 'com a A-1']))

    def test_separar_numeros_nao_numeros(self):
        self.assertEqual(['Cruzamento', 'da', 'AP-', '36', '', 'com', 'a', 'R-', '4', ''], sorter.separar_numeros_nao_numeros(['Cruzamento', 'da', 'AP-36', 'com', 'a', 'R-4']))
        self.assertEqual(['Saída', '32', 'B'], sorter.separar_numeros_nao_numeros(['Saída', '32B']))
        self.assertEqual(['Vélez-Málaga'], sorter.separar_numeros_nao_numeros(['Vélez-Málaga']))
        self.assertEqual(['A-', '5', ''], sorter.separar_numeros_nao_numeros(['A-5']))
        self.assertEqual(['A-', '5', 'R'], sorter.separar_numeros_nao_numeros(['A-5R']))
        self.assertEqual(['IC', '17', ''], sorter.separar_numeros_nao_numeros(['IC17']))
        self.assertEqual(['A', '26', '-', '1', ''], sorter.separar_numeros_nao_numeros(['A26-1']))
        self.assertEqual(['A-', '7', '/AP-', '7', '', 'Saída', '32', 'B'], sorter.separar_numeros_nao_numeros(['A-7/AP-7', 'Saída', '32B']))

    def test_comparador(self):
        self.assertEqual(sorter.MENOR, sorter.comparador('a', 'b'))
        self.assertEqual(sorter.MAIOR, sorter.comparador('b', 'a'))
        self.assertEqual(sorter.IGUAL, sorter.comparador('a', 'a'))
        self.assertEqual(sorter.MENOR, sorter.comparador('azzzzzzzzzzzzzzzzzzzzzzzz', 'b'))
        self.assertEqual(sorter.MAIOR, sorter.comparador('c', 'baaaaaaaaaaaaaaaaa'))
        self.assertEqual(sorter.MENOR, sorter.comparador('0', '1'))
        self.assertEqual(sorter.MAIOR, sorter.comparador('1', '0'))
        self.assertEqual(sorter.MAIOR, sorter.comparador('10', '2'))
        self.assertEqual(sorter.MAIOR, sorter.comparador('100', '99'))
        self.assertEqual(sorter.MENOR, sorter.comparador('2', '10'))
        self.assertEqual(sorter.MENOR, sorter.comparador('99', '100'))
        self.assertEqual(sorter.MENOR, sorter.comparador('', '1'))
        self.assertEqual(sorter.MENOR, sorter.comparador('', 'a'))
        self.assertEqual(sorter.MAIOR, sorter.comparador('1', ''))
        self.assertEqual(sorter.MAIOR, sorter.comparador('a', ''))
        self.assertEqual(sorter.MENOR, sorter.comparador('Alcaria', 'Alcaria dos Javazes'))

    def test_conversor_lista_numeros_romanos_arabes(self):
        self.assertEqual(['1'], sorter.conversor_lista_numeros_romanos_arabes(['I']))
        self.assertEqual(['Porto', 'de', 'Sines', 'Terminal', '21'], sorter.conversor_lista_numeros_romanos_arabes(['Porto', 'de', 'Sines', 'Terminal', 'XXI']))

    def test_conversor_numeros_romanos_arabes(self):
        self.assertEqual('', sorter.conversor_numeros_romanos_arabes(''))
        self.assertEqual('   ', sorter.conversor_numeros_romanos_arabes('   '))
        self.assertEqual('ewhfuiwhfiewhuifhwfohweyif', sorter.conversor_numeros_romanos_arabes('ewhfuiwhfiewhuifhwfohweyif'))
        self.assertEqual('IC', sorter.conversor_numeros_romanos_arabes('IC'))  # Itinerário Complementar
        self.assertEqual('M', sorter.conversor_numeros_romanos_arabes('M'))  # Estrada Municipal
        self.assertEqual('C', sorter.conversor_numeros_romanos_arabes('C'))  # Pode aparecer num número de saída. Ex: A-7 - Saída 108C

        self.assertEqual(1, sorter.conversor_numeros_romanos_arabes('I'))
        self.assertEqual(2, sorter.conversor_numeros_romanos_arabes('II'))
        self.assertEqual(3, sorter.conversor_numeros_romanos_arabes('III'))
        self.assertEqual(4, sorter.conversor_numeros_romanos_arabes('IV'))
        self.assertEqual(5, sorter.conversor_numeros_romanos_arabes('V'))
        self.assertEqual(6, sorter.conversor_numeros_romanos_arabes('VI'))
        self.assertEqual(7, sorter.conversor_numeros_romanos_arabes('VII'))
        self.assertEqual(8, sorter.conversor_numeros_romanos_arabes('VIII'))
        self.assertEqual(9, sorter.conversor_numeros_romanos_arabes('IX'))
        self.assertEqual(10, sorter.conversor_numeros_romanos_arabes('X'))
        self.assertEqual(11, sorter.conversor_numeros_romanos_arabes('XI'))
        self.assertEqual(19, sorter.conversor_numeros_romanos_arabes('XIX'))
        self.assertEqual(20, sorter.conversor_numeros_romanos_arabes('XX'))
        self.assertEqual(21, sorter.conversor_numeros_romanos_arabes('XXI'))
        self.assertEqual(29, sorter.conversor_numeros_romanos_arabes('XXIX'))
        self.assertEqual(30, sorter.conversor_numeros_romanos_arabes('XXX'))
        self.assertEqual(31, sorter.conversor_numeros_romanos_arabes('XXXI'))
        self.assertEqual(49, sorter.conversor_numeros_romanos_arabes('XLIX'))
        self.assertEqual(50, sorter.conversor_numeros_romanos_arabes('L'))
        self.assertEqual(51, sorter.conversor_numeros_romanos_arabes('LI'))
        self.assertEqual(99, sorter.conversor_numeros_romanos_arabes('XCIX'))
        self.assertEqual(101, sorter.conversor_numeros_romanos_arabes('CI'))
        self.assertEqual(299, sorter.conversor_numeros_romanos_arabes('CCXCIX'))
        self.assertEqual(300, sorter.conversor_numeros_romanos_arabes('CCC'))
        self.assertEqual(301, sorter.conversor_numeros_romanos_arabes('CCCI'))
        self.assertEqual(499, sorter.conversor_numeros_romanos_arabes('CDXCIX'))
        self.assertEqual(500, sorter.conversor_numeros_romanos_arabes('D'))
        self.assertEqual(501, sorter.conversor_numeros_romanos_arabes('DI'))
        self.assertEqual(999, sorter.conversor_numeros_romanos_arabes('CMXCIX'))
        self.assertEqual(1001, sorter.conversor_numeros_romanos_arabes('MI'))
        self.assertEqual(2999, sorter.conversor_numeros_romanos_arabes('MMCMXCIX'))
        self.assertEqual(3000, sorter.conversor_numeros_romanos_arabes('MMM'))
        self.assertEqual(3001, sorter.conversor_numeros_romanos_arabes('MMMI'))
        self.assertEqual(3999, sorter.conversor_numeros_romanos_arabes('MMMCMXCIX'))

    def test_is_numerico(self):
        self.assertFalse(sorter.is_numerico('a'))
        self.assertFalse(sorter.is_numerico('B'))
        self.assertFalse(sorter.is_numerico('-'))
        self.assertFalse(sorter.is_numerico('.'))
        self.assertFalse(sorter.is_numerico(' '))
        self.assertFalse(sorter.is_numerico(''))
        self.assertFalse(sorter.is_numerico(','))
        self.assertFalse(sorter.is_numerico('"'))
        self.assertTrue(sorter.is_numerico('0'))
        self.assertTrue(sorter.is_numerico('1'))
        self.assertTrue(sorter.is_numerico('9'))
