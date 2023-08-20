import unittest
import unittest.mock
import io

from travel.main import menu
from test.utils import redirect_output


def _exit_menu_routine() -> None:
    print("Exiting")  # Prevents exit() being called on exiting menu


class MenuTest(unittest.TestCase):

    #  #  #  #  #  #  #  #  #  #
    # Menu integration testing #
    #  #  #  #  #  #  #  #  #  #

    # No parameters

    def test_numeric_menu_no_parameters(self):
        stdout_redirect: io.StringIO = redirect_output()

        menu.present_numeric_menu(option_labels=[], menu_introduction=[], exit_routine=None)
        self.assertTrue(menu.ERROR_NO_OPTION_LABELS in stdout_redirect.getvalue())
        self.assertFalse(menu.ERROR_NO_MENU_INTRODUCTION in stdout_redirect.getvalue())

        stdout_redirect: io.StringIO = redirect_output()  # Clears redirect object from previous prints

        menu.present_numeric_menu(option_labels=['Option A'], menu_introduction=[], exit_routine=None)
        self.assertFalse(menu.ERROR_NO_OPTION_LABELS in stdout_redirect.getvalue())
        self.assertTrue(menu.ERROR_NO_MENU_INTRODUCTION in stdout_redirect.getvalue())

    def test_boolean_menu_no_parameters(self):
        stdout_redirect: io.StringIO = redirect_output()

        menu.present_boolean_menu(menu_introduction=[])
        self.assertTrue(menu.ERROR_NO_MENU_INTRODUCTION in stdout_redirect.getvalue())

    # Invalid input

    def test_invalid_numeric_menu_input_one_option(self):
        stdout_redirect: io.StringIO = redirect_output()

        with unittest.mock.patch('builtins.input', side_effect=["", "a", "-1", "2", "0"]):  # All inputs should be strings
            menu.present_numeric_menu(option_labels=['Option A'], menu_introduction=['A menu'], exit_routine=_exit_menu_routine)
        self.assertEqual(1, stdout_redirect.getvalue().count(menu.ERROR_EMPTY_INPUT))
        self.assertEqual(1, stdout_redirect.getvalue().count(menu.ERROR_INPUT_NOT_INT))
        self.assertEqual(2, stdout_redirect.getvalue().count(menu.ERROR_INVALID_OPTION_NUMBER))
        self.assertEqual(1, stdout_redirect.getvalue().count("Exiting"))

    def test_invalid_numeric_menu_input_multiple_options(self):
        stdout_redirect: io.StringIO = redirect_output()

        with unittest.mock.patch('builtins.input', side_effect=["", "a", "-1", "4", "0"]):  # All inputs should be strings
            menu.present_numeric_menu(option_labels=['Option A, Option B, Option C'], menu_introduction=['A menu'],
                                      exit_routine=_exit_menu_routine)
        self.assertEqual(1, stdout_redirect.getvalue().count(menu.ERROR_EMPTY_INPUT))
        self.assertEqual(1, stdout_redirect.getvalue().count(menu.ERROR_INPUT_NOT_INT))
        self.assertEqual(2, stdout_redirect.getvalue().count(menu.ERROR_INVALID_OPTION_NUMBER))
        self.assertEqual(1, stdout_redirect.getvalue().count("Exiting"))

    def test_invalid_boolean_menu_input(self):
        stdout_redirect: io.StringIO = redirect_output()

        with unittest.mock.patch('builtins.input', side_effect=["", "a", "-1", "4", "y"]):  # All inputs should be strings
            menu.present_boolean_menu(menu_introduction=['A menu'])
        self.assertEqual(1, stdout_redirect.getvalue().count(menu.ERROR_EMPTY_INPUT))
        self.assertEqual(3, stdout_redirect.getvalue().count(menu.ERROR_INPUT_NOT_BOOLEAN))

    # Valid menu parameters

    def test_valid_numeric_menu_exit(self):
        stdout_redirect: io.StringIO = redirect_output()

        with unittest.mock.patch('builtins.input', side_effect=["0"]):  # All inputs should be strings
            menu.present_numeric_menu(option_labels=['Option A'], menu_introduction=['A menu'],
                                      exit_routine=_exit_menu_routine)
        self.assertEqual(1, stdout_redirect.getvalue().count("Exiting"))

    def test_valid_numeric_menu_introduction_single_line(self):
        stdout_redirect: io.StringIO = redirect_output()

        with unittest.mock.patch('builtins.input', side_effect=["0"]):  # All inputs should be strings
            menu.present_numeric_menu(option_labels=['Option A'], menu_introduction=['A menu'],
                                      exit_routine=_exit_menu_routine)
        self.assertTrue("A menu" in stdout_redirect.getvalue())

    def test_valid_boolean_menu_introduction_single_line(self):
        stdout_redirect: io.StringIO = redirect_output()

        with unittest.mock.patch('builtins.input', side_effect=["y"]):  # All inputs should be strings
            menu.present_boolean_menu(menu_introduction=['A menu'])
        self.assertTrue("A menu" in stdout_redirect.getvalue())

    def test_valid_numeric_menu_introduction_multiple_lines(self):
        stdout_redirect: io.StringIO = redirect_output()

        with unittest.mock.patch('builtins.input', side_effect=["0"]):  # All inputs should be strings
            menu.present_numeric_menu(option_labels=['Option A'], menu_introduction=['A menu', 'Another line', 'And another'],
                                      exit_routine=_exit_menu_routine)
        self.assertTrue("A menu" in stdout_redirect.getvalue())
        self.assertTrue("\nAnother line" in stdout_redirect.getvalue())
        self.assertTrue("\nAnd another" in stdout_redirect.getvalue())

    def test_valid_boolean_menu_introduction_multiple_lines(self):
        stdout_redirect: io.StringIO = redirect_output()

        with unittest.mock.patch('builtins.input', side_effect=["y"]):  # All inputs should be strings
            menu.present_boolean_menu(menu_introduction=['A menu', 'Another line', 'And another'])
        self.assertTrue("A menu" in stdout_redirect.getvalue())
        self.assertTrue("\nAnother line" in stdout_redirect.getvalue())
        self.assertTrue("\nAnd another" in stdout_redirect.getvalue())

    def test_valid_numeric_menu_one_option(self):
        stdout_redirect: io.StringIO = redirect_output()

        with unittest.mock.patch('builtins.input', side_effect=["1"]):  # All inputs should be strings
            returned_option = menu.present_numeric_menu(option_labels=['Option A'], menu_introduction=['A menu'],
                                                        exit_routine=_exit_menu_routine)

        self.assertEqual(1, returned_option)
        self.assertTrue('A menu' in stdout_redirect.getvalue())
        self.assertTrue('0 -> Exit program' in stdout_redirect.getvalue())
        self.assertTrue('1 -> Option A' in stdout_redirect.getvalue())

        error_messages = menu.ALL_ERRORS
        for error in error_messages:
            self.assertFalse(error in stdout_redirect.getvalue())

    def test_valid_numeric_menu_multiple_options(self):
        stdout_redirect: io.StringIO = redirect_output()

        with unittest.mock.patch('builtins.input', side_effect=["3"]):  # All inputs should be strings
            returned_option = menu.present_numeric_menu(option_labels=['Option A', 'Option B', 'Option C'],
                                                        menu_introduction=['A menu'], exit_routine=_exit_menu_routine)

        self.assertEqual(3, returned_option)
        self.assertTrue('A menu' in stdout_redirect.getvalue())
        self.assertTrue('0 -> Exit program' in stdout_redirect.getvalue())
        self.assertTrue('1 -> Option A' in stdout_redirect.getvalue())
        self.assertTrue('2 -> Option B' in stdout_redirect.getvalue())
        self.assertTrue('3 -> Option C' in stdout_redirect.getvalue())

        error_messages = menu.ALL_ERRORS
        for error in error_messages:
            self.assertFalse(error in stdout_redirect.getvalue())

    def test_valid_boolean_menu(self):
        stdout_redirect: io.StringIO = redirect_output()

        for option in ["y", "Y", "n", "N"]:
            with unittest.mock.patch('builtins.input', side_effect=[option]):  # All inputs should be strings
                returned_option = menu.present_boolean_menu(menu_introduction=['A menu'])

            self.assertEqual(returned_option, True if option.lower() == 'y' else False)
            self.assertTrue('A menu' in stdout_redirect.getvalue())

            error_messages = menu.ALL_ERRORS
            for error in error_messages:
                self.assertFalse(error in stdout_redirect.getvalue())

    #  #  #  #  #  #  #  #  #  #
    # Auxiliary method testing #
    #  #  #  #  #  #  #  #  #  #

    # Menu type and options type validation

    def test_validate_menu_options_type_invalid(self):
        stdout_redirect: io.StringIO = redirect_output()

        for menu_options_type in ['', '   ', 'a', 1, True, '   a     ']:
            self.assertFalse(menu.validate_menu_options_type(menu_options_type))
        self.assertEqual(6, stdout_redirect.getvalue().count(menu.ERROR_INVALID_MENU_OPTIONS_TYPE))

    def test_validate_menu_options_type_valid(self):
        stdout_redirect: io.StringIO = redirect_output()

        for menu_options_type in menu.ALL_MENU_OPTIONS_TYPES:
            self.assertTrue(menu.validate_menu_options_type(menu_options_type))

        for error_message in menu.ALL_ERRORS:
            self.assertFalse(error_message in stdout_redirect.getvalue())

    # Menu parameters validation

    def test_validate_option_labels(self):
        stdout_redirect: io.StringIO = redirect_output()

        self.assertFalse(menu.validate_option_labels([]))
        self.assertTrue(menu.validate_option_labels(['Option A']))
        self.assertTrue(menu.validate_option_labels(['Option A', 'Option B', 'Option C']))

        self.assertEqual(1, stdout_redirect.getvalue().count(menu.ERROR_NO_OPTION_LABELS))

    def test_validate_menu_introduction(self):
        stdout_redirect: io.StringIO = redirect_output()

        self.assertFalse(menu.validate_menu_introduction([]))
        self.assertTrue(menu.validate_menu_introduction(['A menu']))
        self.assertTrue(menu.validate_menu_introduction(['A menu', 'Another line', 'And another']))

        self.assertEqual(1, stdout_redirect.getvalue().count(menu.ERROR_NO_MENU_INTRODUCTION))

    # Menu presentation

    def test_present_menu_introduction_single_line(self):
        stdout_redirect: io.StringIO = redirect_output()
        menu.present_menu_introduction(['A menu'])
        self.assertTrue('A menu' in stdout_redirect.getvalue())

    def test_present_menu_introduction_multiple_lines(self):
        stdout_redirect: io.StringIO = redirect_output()
        menu.present_menu_introduction(['A menu', 'Another line', 'And another'])
        self.assertTrue('A menu' in stdout_redirect.getvalue())
        self.assertTrue('\nAnother line' in stdout_redirect.getvalue())
        self.assertTrue('\nAnd another' in stdout_redirect.getvalue())

    def test_present_menu_options_one_option(self):
        stdout_redirect: io.StringIO = redirect_output()
        menu.present_menu_options(['Option A'])
        self.assertTrue('0 -> Exit program' in stdout_redirect.getvalue())
        self.assertTrue('\n1 -> Option A' in stdout_redirect.getvalue())

    def test_present_menu_options_multiple_options(self):
        stdout_redirect: io.StringIO = redirect_output()
        menu.present_menu_options(['Option A', 'Option B', 'Option C'])
        self.assertTrue('0 -> Exit program' in stdout_redirect.getvalue())
        self.assertTrue('\n1 -> Option A' in stdout_redirect.getvalue())
        self.assertTrue('\n2 -> Option B' in stdout_redirect.getvalue())
        self.assertTrue('\n3 -> Option C' in stdout_redirect.getvalue())

    # Request input from user

    def test_request_input_from_user(self):
        with unittest.mock.patch('builtins.input', side_effect=["1"]):  # All inputs should be strings
            raw_input = menu.request_input_from_user()
        self.assertEqual("1", raw_input)

        with unittest.mock.patch('builtins.input', side_effect=["a"]):  # All inputs should be strings
            raw_input = menu.request_input_from_user()
        self.assertEqual("a", raw_input)

        with unittest.mock.patch('builtins.input', side_effect=["A set of words"]):  # All inputs should be strings
            raw_input = menu.request_input_from_user()
        self.assertEqual("A set of words", raw_input)

    def test_request_boolean_input_from_user(self):
        with unittest.mock.patch('builtins.input', side_effect=["1"]):  # All inputs should be strings
            raw_input = menu.request_boolean_input_from_user()
        self.assertEqual("1", raw_input)

        with unittest.mock.patch('builtins.input', side_effect=["a"]):  # All inputs should be strings
            raw_input = menu.request_boolean_input_from_user()
        self.assertEqual("a", raw_input)

        with unittest.mock.patch('builtins.input', side_effect=["A set of words"]):  # All inputs should be strings
            raw_input = menu.request_boolean_input_from_user()
        self.assertEqual("A set of words", raw_input)

    # User input validation

    def test_validate_input_is_not_empty_invalid(self):
        stdout_redirect: io.StringIO = redirect_output()
        self.assertFalse(menu.validate_input_is_not_empty(''))
        self.assertFalse(menu.validate_input_is_not_empty('            '))
        self.assertEqual(2, stdout_redirect.getvalue().count(menu.ERROR_EMPTY_INPUT))

    def test_validate_input_is_not_empty_valid(self):
        stdout_redirect: io.StringIO = redirect_output()
        self.assertTrue(menu.validate_input_is_not_empty('1'))
        self.assertTrue(menu.validate_input_is_not_empty('a'))
        self.assertTrue(menu.validate_input_is_not_empty('A set of words'))
        self.assertTrue(menu.validate_input_is_not_empty('    a     '))
        self.assertEqual(0, stdout_redirect.getvalue().count(menu.ERROR_EMPTY_INPUT))

    def test_validate_input_is_int_invalid(self):
        stdout_redirect: io.StringIO = redirect_output()
        self.assertFalse(menu.validate_input_is_int(''))
        self.assertFalse(menu.validate_input_is_int('            '))
        self.assertFalse(menu.validate_input_is_int('a'))
        self.assertFalse(menu.validate_input_is_int('A set of words'))
        self.assertFalse(menu.validate_input_is_int('      a       '))
        self.assertEqual(5, stdout_redirect.getvalue().count(menu.ERROR_INPUT_NOT_INT))

    def test_validate_input_is_int_valid(self):
        stdout_redirect: io.StringIO = redirect_output()
        self.assertTrue(menu.validate_input_is_int('0'))
        self.assertTrue(menu.validate_input_is_int('-1'))
        self.assertTrue(menu.validate_input_is_int('1'))
        self.assertTrue(menu.validate_input_is_int('-12345465789'))
        self.assertTrue(menu.validate_input_is_int('12345465789'))
        self.assertEqual(0, stdout_redirect.getvalue().count(menu.ERROR_INPUT_NOT_INT))

    def test_validate_option_inside_range_invalid(self):
        stdout_redirect: io.StringIO = redirect_output()

        # Single option
        self.assertFalse(menu.validate_option_inside_range(-123456789, ['Option A']))
        self.assertFalse(menu.validate_option_inside_range(-1, ['Option A']))
        self.assertFalse(menu.validate_option_inside_range(1, ['Option A']))
        self.assertFalse(menu.validate_option_inside_range(123456789, ['Option A']))

        # Multiple options
        self.assertFalse(menu.validate_option_inside_range(-123456789, ['Option A', 'Option B', 'Option C']))
        self.assertFalse(menu.validate_option_inside_range(-1, ['Option A', 'Option B', 'Option C']))
        self.assertFalse(menu.validate_option_inside_range(3, ['Option A', 'Option B', 'Option C']))
        self.assertFalse(menu.validate_option_inside_range(123456789, ['Option A', 'Option B', 'Option C']))

        self.assertEqual(8, stdout_redirect.getvalue().count(menu.ERROR_INVALID_OPTION_NUMBER))

    def test_validate_option_inside_range_valid(self):
        stdout_redirect: io.StringIO = redirect_output()

        # Single option
        self.assertTrue(menu.validate_option_inside_range(0, ['Option A']))

        # Multiple options
        self.assertTrue(menu.validate_option_inside_range(0, ['Option A', 'Option B', 'Option C']))
        self.assertTrue(menu.validate_option_inside_range(1, ['Option A', 'Option B', 'Option C']))
        self.assertTrue(menu.validate_option_inside_range(2, ['Option A', 'Option B', 'Option C']))

        self.assertEqual(0, stdout_redirect.getvalue().count(menu.ERROR_INVALID_OPTION_NUMBER))

    def test_validate_input_is_boolean_invalid(self):
        stdout_redirect: io.StringIO = redirect_output()
        self.assertFalse(menu.validate_input_is_boolean(''))
        self.assertFalse(menu.validate_input_is_boolean('            '))
        self.assertFalse(menu.validate_input_is_boolean('a'))
        self.assertFalse(menu.validate_input_is_boolean('A set of words'))
        self.assertFalse(menu.validate_input_is_boolean('      a       '))
        self.assertEqual(5, stdout_redirect.getvalue().count(menu.ERROR_INPUT_NOT_BOOLEAN))

    def test_validate_input_is_boolean_valid(self):
        stdout_redirect: io.StringIO = redirect_output()
        self.assertTrue(menu.validate_input_is_boolean('y'))
        self.assertTrue(menu.validate_input_is_boolean('Y'))
        self.assertTrue(menu.validate_input_is_boolean('n'))
        self.assertTrue(menu.validate_input_is_boolean('N'))
        self.assertEqual(0, stdout_redirect.getvalue().count(menu.ERROR_INPUT_NOT_BOOLEAN))

    # Valid option processing

    def test_valid_numeric_option_processing(self):
        stdout_redirect: io.StringIO = redirect_output()

        self.assertEqual(-2, menu.valid_numeric_option_processing(-2, exit_routine=None))
        self.assertEqual(-1, menu.valid_numeric_option_processing(-1, exit_routine=None))
        self.assertEqual(0, menu.valid_numeric_option_processing(0, exit_routine=_exit_menu_routine))  # If exit routine was None, exit() would be called and test would fail
        self.assertEqual(1, menu.valid_numeric_option_processing(1, exit_routine=None))
        self.assertEqual(2, menu.valid_numeric_option_processing(2, exit_routine=None))

        self.assertEqual(1, stdout_redirect.getvalue().count('Exiting'))

    def test_valid_boolean_option_processing(self):
        self.assertTrue(menu.valid_boolean_option_processing('y'))
        self.assertTrue(menu.valid_boolean_option_processing('Y'))
        self.assertFalse(menu.valid_boolean_option_processing('n'))
        self.assertFalse(menu.valid_boolean_option_processing('N'))
