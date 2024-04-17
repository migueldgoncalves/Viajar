from travel.support import ways, information_generator, sorter, sqlite_interface, region_bounds_finder
from travel.main import menu, travel
from car import car_simulator

"""
Main - Execute to access all available scripts
"""


# INSERT HERE location where to start journey
INITIAL_LOCATION = 'Cruzamento Sul da A-2 com a AP-7'

# INSERT HERE road or railway to be analysed by the automatic generator of information
WAY_TO_PROCESS = ways.PT_PORTO_METRO_LINE_E

OPTION_TRAVEL = 1
OPTION_CAR = 2

OPTION_GENERATOR = 3
OPTION_SORTER = 4
OPTION_SQLITE = 5
OPTION_REGION_BOUNDS_FINDER = 6

print("======================================")
print("Welcome to the project Viajar (Travel)")
print("======================================")

option_labels: list[str] = [
    'Main - Travel',
    'Main - Car',
    'Support - Automatic generator of information',
    'Support - Sorter of .csv files',
    'Support - Creator of SQLite database',
    'Support - Region extreme points finder',
]
menu_introduction: list[str] = ["Which script do you want to execute?"]

# Guaranteed to be valid non-exit option
user_option = menu.present_numeric_menu(option_labels, menu_introduction)

# Process user options

if user_option == OPTION_TRAVEL:
    travel.Travel(INITIAL_LOCATION).make_journey()

elif user_option == OPTION_CAR:
    '''
    README FOR CAR PACKAGE
    
    To use the command Run of the IDE PyCharm to execute the car script:
        In Run > Edit Configurations > Enable option "Emulate terminal in output console"
        This is due to the usage of the msvcrt library in the car package to detect and read pressed keys
    '''
    car_simulator.CarSimulator().travel(distance_to_travel=0, destination="")

elif user_option == OPTION_GENERATOR:
    information_generator.InformationGenerator(WAY_TO_PROCESS, get_altitude_info=True).present_main_menu()

elif user_option == OPTION_SORTER:
    sorter.ordenar_ficheiros_csv()

elif user_option == OPTION_SQLITE:
    sqlite_interface.SQLiteBDInterface()

elif user_option == OPTION_REGION_BOUNDS_FINDER:
    region_bounds_finder.obter_pontos_extremos()
