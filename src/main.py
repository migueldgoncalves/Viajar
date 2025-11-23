from travel.support import ways, information_generator, sorter, sqlite_interface, region_bounds_finder
from travel.main import menu, travel, paths_and_files, db_distance_calculator
from car import car_simulator

"""
Main - Execute to access all available scripts
"""

# Set initial location for journey
DEFAULT_INITIAL_LOCATION = 'Guerreiros do Rio'
try:
    with open(paths_and_files.INITIAL_LOCATION_FILEPATH, 'r') as f:
        file_content: list[str] = f.readlines()
    if file_content and file_content[0]:
        INITIAL_LOCATION = file_content[0]
    else:
        with open(paths_and_files.INITIAL_LOCATION_FILEPATH, 'w') as f:
            INITIAL_LOCATION = DEFAULT_INITIAL_LOCATION
            f.write(DEFAULT_INITIAL_LOCATION)
except FileNotFoundError:
    with open(paths_and_files.INITIAL_LOCATION_FILEPATH, 'w') as f:
        INITIAL_LOCATION = DEFAULT_INITIAL_LOCATION
        f.write(DEFAULT_INITIAL_LOCATION)

# INSERT HERE road or railway to be analysed by the automatic generator of information
WAY_TO_PROCESS = ways.ES_A66

OPTION_TRAVEL = 1
OPTION_CAR = 2
OPTION_DISTANCE_CALCULATOR = 3

OPTION_GENERATOR = 4
OPTION_SORTER = 5
OPTION_SQLITE = 6
OPTION_REGION_BOUNDS_FINDER = 7

print("======================================")
print("Welcome to the project Viajar (Travel)")
print("======================================")

option_labels: list[str] = [
    'Main - Travel',
    'Main - Car',
    'Main - Internal distance calculator',
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

elif user_option == OPTION_DISTANCE_CALCULATOR:
    db_distance_calculator.main()

elif user_option == OPTION_GENERATOR:
    information_generator.InformationGenerator(WAY_TO_PROCESS, get_altitude_info=True).present_main_menu()

elif user_option == OPTION_SORTER:
    sorter.sort_csv_files()

elif user_option == OPTION_SQLITE:
    sqlite_interface.SQLiteDBInterface()

elif user_option == OPTION_REGION_BOUNDS_FINDER:
    region_bounds_finder.get_extreme_points()
