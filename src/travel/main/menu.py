from typing import Callable, Optional
"""
Module that prints a menu to the user and processes the respective input
"""

EXIT_OPTION = 0
EXIT_OPTION_LABEL = "Exit program"

INPUT_LINE_TEXT = 'Write your option here'
INPUT_BOOLEAN_LINE_TEXT = 'Write your option here [Y/N]'

ERROR_NO_OPTION_LABELS = 'No option labels provided - Menu cannot be presented'
ERROR_NO_MENU_INTRODUCTION = 'No menu introduction provided - Menu cannot be presented'
ERROR_INPUT_NOT_INT = 'Input should be a number'
ERROR_INVALID_OPTION_NUMBER = 'Invalid option number'
ERROR_EMPTY_INPUT = 'Please provide an option'
ERROR_INVALID_MENU_OPTIONS_TYPE = 'Invalid menu options type provided - Menu cannot be presented'
ERROR_INPUT_NOT_BOOLEAN = 'Input should be Y or N'
ALL_ERRORS = [ERROR_NO_MENU_INTRODUCTION, ERROR_NO_OPTION_LABELS, ERROR_INVALID_OPTION_NUMBER, ERROR_EMPTY_INPUT,
              ERROR_INPUT_NOT_INT, ERROR_INVALID_MENU_OPTIONS_TYPE, ERROR_INPUT_NOT_BOOLEAN]  # Used in unit tests

SEPARATOR = "->"  # Ex: 0 -> Exit program

MENU_OPTIONS_NUMERIC = 'numeric'
MENU_OPTIONS_BOOLEAN = 'boolean'
ALL_MENU_OPTIONS_TYPES = [MENU_OPTIONS_NUMERIC, MENU_OPTIONS_BOOLEAN]


#  #  #  #  #  #
# Main methods #
#  #  #  #  #  #

def present_boolean_menu(menu_introduction: list[str] = None) -> Optional[bool]:
    """
    Presents menu where only Y, y, N, and n, are accepted as options, then returns either True or False accordingly
    """
    return _present_menu(menu_options_type=MENU_OPTIONS_BOOLEAN, menu_introduction=menu_introduction)


def present_numeric_menu(option_labels: list[str] = None, menu_introduction: list[str] = None,
                         exit_routine: Callable = None) -> Optional[int]:
    """
    Presents menu where only numbers equal or larger than 0 are accepted as options. Option 0 is treated as option to exit.
        For the other options, the option number is returned to the routine caller.
    """
    return _present_menu(menu_options_type=MENU_OPTIONS_NUMERIC, option_labels=option_labels,
                         menu_introduction=menu_introduction, exit_routine=exit_routine)


def _present_menu(menu_options_type: str, option_labels: list[str] = None, menu_introduction: list[str] = None,
                  exit_routine: Callable = None) -> Optional[int]:
    """
    Presents a menu to the user and processes the respective input. If the user types an invalid input, a new input is
    requested from the user. The input is returned once the user types a valid input.
    An exit option is made available by typing 0 for menus with numeric options.

    :param menu_options_type: Determines the type of options expected. Supported: numbers only, Y/N
    :param option_labels: List of labels to be printed for the different options. Determines the number of options of the menu.
        Label for the exit option does not need to be provided.
    :param menu_introduction: Text to be printed before presenting the menu. Each list element is printed in a different line.
    :param exit_routine: Routine to call if user chooses to exit program. Defaults to exiting immediately.
    :return: Input introduced by user, once determined to be valid.
    """
    # Menu type and options type validation
    success = validate_menu_options_type(menu_options_type)
    if not success:
        return

    # Menu parameters validation
    if menu_options_type == MENU_OPTIONS_NUMERIC:
        success = validate_option_labels(option_labels) and validate_menu_introduction(menu_introduction)
        if not success:
            return
    elif menu_options_type == MENU_OPTIONS_BOOLEAN:  # Boolean menus do not have option labels
        success = validate_menu_introduction(menu_introduction)
        if not success:
            return

    # Menu presentation
    if menu_options_type == MENU_OPTIONS_NUMERIC:
        present_menu_introduction(menu_introduction)
        present_menu_options(option_labels)
    elif menu_options_type == MENU_OPTIONS_BOOLEAN:  # Boolean menus do not have option labels
        present_menu_introduction(menu_introduction)

    while True:
        # Request input from user
        raw_input: str = ''
        if menu_options_type == MENU_OPTIONS_NUMERIC:
            raw_input = request_input_from_user()
        elif menu_options_type == MENU_OPTIONS_BOOLEAN:
            raw_input = request_boolean_input_from_user()

        # Invalid option processing
        success = validate_input_is_not_empty(raw_input)
        if not success:
            continue
        option: int = -1
        if menu_options_type == MENU_OPTIONS_NUMERIC:
            success = validate_input_is_int(raw_input)
            if not success:
                continue
            option = int(raw_input)
            success = validate_option_inside_range(option, option_labels)
            if not success:
                continue
        elif menu_options_type == MENU_OPTIONS_BOOLEAN:
            success = validate_input_is_boolean(raw_input)
            if not success:
                continue

        # Valid option processing and return
        if menu_options_type == MENU_OPTIONS_NUMERIC:
            return valid_numeric_option_processing(option, exit_routine)
        elif menu_options_type == MENU_OPTIONS_BOOLEAN:
            return valid_boolean_option_processing(raw_input)  # Boolean menus do not provide exit options


def default_exit_routine():
    print("You have chosen to exit")
    print("See you soon")
    exit(0)

#  #  #  #  #  #  #  #
# Auxiliary methods #
#  #  #  #  #  #  #  #


# Menu type and options type validation
# True is returned if parameter(s) is/are valid, False otherwise

def validate_menu_options_type(menu_options_type: str) -> bool:
    if menu_options_type in ALL_MENU_OPTIONS_TYPES:
        return True
    else:
        print(ERROR_INVALID_MENU_OPTIONS_TYPE)
        return False


# Menu parameters validation
# True is returned if parameter(s) is/are valid, False otherwise

def validate_option_labels(option_labels: list[str]) -> bool:
    if option_labels:
        return True
    else:
        print(ERROR_NO_OPTION_LABELS)
        return False


def validate_menu_introduction(menu_introduction: list[str]) -> bool:
    if menu_introduction:
        return True
    else:
        print(ERROR_NO_MENU_INTRODUCTION)
        return False


# Menu presentation

def present_menu_introduction(menu_introduction: list[str]) -> None:
    for line in menu_introduction:
        print(line)


def present_menu_options(option_labels: list[str]) -> None:
    option_labels.insert(0, EXIT_OPTION_LABEL)  # Exit option is always first menu option

    for index, label in enumerate(option_labels):  # Exit option is assigned option 0
        full_option_text: str = f'{index} {SEPARATOR} {label}'  # Ex: 0 -> Exit program
        print(full_option_text)


# Request input from user

def request_input_from_user() -> str:
    raw_option: str = input(f'{INPUT_LINE_TEXT}: ')
    return raw_option


def request_boolean_input_from_user() -> str:
    raw_option: str = input(f'{INPUT_BOOLEAN_LINE_TEXT}: ')
    return raw_option


# User input validation
# True is returned if parameter(s) is/are valid, else otherwise

def validate_input_is_not_empty(raw_input: str) -> bool:
    if raw_input.strip():
        return True
    else:
        print(ERROR_EMPTY_INPUT)
        return False


def validate_input_is_int(raw_input: str) -> bool:
    try:
        int(raw_input)
    except ValueError:  # Not an int
        print(ERROR_INPUT_NOT_INT)
        return False
    else:
        return True


def validate_option_inside_range(option: int, option_labels: list[str]) -> bool:
    total_options: int = len(option_labels) - 1  # Not including exit option
    if 0 <= option <= total_options:
        return True
    else:
        print(ERROR_INVALID_OPTION_NUMBER)
        return False


def validate_input_is_boolean(raw_input: str) -> bool:
    boolean_options = ['y', 'n']
    if raw_input.lower() in boolean_options:
        return True
    else:
        print(ERROR_INPUT_NOT_BOOLEAN)
        return False


# Valid option processing

def valid_numeric_option_processing(option: int, exit_routine: Optional[Callable]) -> Optional[int]:
    """
    If user option is to exit, exit routine is called or, if not provided, program is exited.
    If user provides another valid option, it is returned to the routine that called this menu module
    """
    if option == EXIT_OPTION:
        if exit_routine:
            exit_routine()  # It is assumed that no arguments are required
            return EXIT_OPTION
        else:  # Default
            default_exit_routine()
    else:  # Valid non-zero option
        return option


def valid_boolean_option_processing(option: str) -> bool:
    return option.lower() == 'y'  # Assumes option is 'y', 'Y', 'n' or 'N'
