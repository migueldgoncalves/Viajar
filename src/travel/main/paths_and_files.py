import os
"""
File containing constants with file paths and file names
"""

# IMPORTANT: Project should be outside of drive C: - There may permission issues otherwise
BASE_PROJECT_PATH = os.path.join('D:\\', 'PycharmProjects', 'Viajar')
SRC_RELATIVE_PATH = 'src'
TRAVEL_PACKAGE_RELATIVE_PATH = os.path.join(BASE_PROJECT_PATH, SRC_RELATIVE_PATH, 'travel')
BASE_PATH = os.path.join(BASE_PROJECT_PATH, TRAVEL_PACKAGE_RELATIVE_PATH)

# Google API key file
GOOGLE_API_KEY_FILE = 'api_key.txt'
GOOGLE_API_KEY_FILEPATH = os.path.join(BASE_PROJECT_PATH, SRC_RELATIVE_PATH, GOOGLE_API_KEY_FILE)

# Folders
DB_FILES_FOLDER_NAME = 'database'
DB_FILES_FOLDER_PATH = os.path.join(BASE_PATH, DB_FILES_FOLDER_NAME)
CSV_FOLDER_NAME = 'csv'
CSV_FOLDER_PATH = os.path.join(BASE_PATH, CSV_FOLDER_NAME)
TMP_FOLDER_NAME = 'tmp'
TMP_FOLDER_PATH = os.path.join(BASE_PATH, TMP_FOLDER_NAME)

# Database base files folder - Contains schema in SQL, E-R model and relational model
DB_SCRIPT_FILE = 'database.sql'
DB_SCRIPT_PATH = os.path.join(DB_FILES_FOLDER_PATH, DB_SCRIPT_FILE)

# CSV files folder - Contains the information to populate the DB
CSV_COMARCA = 'comarca.csv'
CSV_COMARCA_PATH = os.path.join(CSV_FOLDER_PATH, CSV_COMARCA)
CSV_CONCELHO = 'concelho.csv'
CSV_CONCELHO_PATH = os.path.join(CSV_FOLDER_PATH, CSV_CONCELHO)
CSV_DESTINATION = 'destination.csv'
CSV_DESTINATION_PATH = os.path.join(CSV_FOLDER_PATH, CSV_DESTINATION)
CSV_CONNECTION = 'connection.csv'
CSV_CONNECTION_PATH = os.path.join(CSV_FOLDER_PATH, CSV_CONNECTION)
CSV_LOCATION = 'location.csv'
CSV_LOCATION_PATH = os.path.join(CSV_FOLDER_PATH, CSV_LOCATION)
CSV_LOCATION_SPAIN = 'location_spain.csv'
CSV_LOCATION_SPAIN_PATH = os.path.join(CSV_FOLDER_PATH, CSV_LOCATION_SPAIN)
CSV_LOCATION_GIBRALTAR = 'location_gibraltar.csv'
CSV_LOCATION_GIBRALTAR_PATH = os.path.join(CSV_FOLDER_PATH, CSV_LOCATION_GIBRALTAR)
CSV_LOCATION_PORTUGAL = 'location_portugal.csv'
CSV_LOCATION_PORTUGAL_PATH = os.path.join(CSV_FOLDER_PATH, CSV_LOCATION_PORTUGAL)
CSV_MUNICIPIO = 'municipio.csv'
CSV_MUNICIPIO_PATH = os.path.join(CSV_FOLDER_PATH, CSV_MUNICIPIO)
CSV_PROVINCE = 'province.csv'
CSV_PROVINCE_PATH = os.path.join(CSV_FOLDER_PATH, CSV_PROVINCE)

# Temporary CSV files folder - Used by the automatic information generator to store processed way files
TMP_CSV_WAY_NAME_PLACEHOLDER = '%$%$'  # Final filepaths should include the way name to process - A placeholder is now used, which should be replaced
TMP_CSV_COMARCA_PATH = os.path.join(TMP_FOLDER_PATH, f'{TMP_CSV_WAY_NAME_PLACEHOLDER}_{CSV_COMARCA}')
TMP_CSV_CONCELHO_PATH = os.path.join(TMP_FOLDER_PATH, f'{TMP_CSV_WAY_NAME_PLACEHOLDER}_{CSV_CONCELHO}')
TMP_CSV_DESTINATION_PATH = os.path.join(TMP_FOLDER_PATH, f'{TMP_CSV_WAY_NAME_PLACEHOLDER}_{CSV_DESTINATION}')
TMP_CSV_CONNECTION_PATH = os.path.join(TMP_FOLDER_PATH, f'{TMP_CSV_WAY_NAME_PLACEHOLDER}_{CSV_CONNECTION}')
TMP_CSV_LOCATION_PATH = os.path.join(TMP_FOLDER_PATH, f'{TMP_CSV_WAY_NAME_PLACEHOLDER}_{CSV_LOCATION}')
TMP_CSV_LOCATION_SPAIN_PATH = os.path.join(TMP_FOLDER_PATH, f'{TMP_CSV_WAY_NAME_PLACEHOLDER}_{CSV_LOCATION_SPAIN}')
TMP_CSV_LOCATION_GIBRALTAR_PATH = os.path.join(TMP_FOLDER_PATH, f'{TMP_CSV_WAY_NAME_PLACEHOLDER}_{CSV_LOCATION_GIBRALTAR}')
TMP_CSV_LOCATION_PORTUGAL_PATH = os.path.join(TMP_FOLDER_PATH, f'{TMP_CSV_WAY_NAME_PLACEHOLDER}_{CSV_LOCATION_PORTUGAL}')
TMP_CSV_MUNICIPIO_PATH = os.path.join(TMP_FOLDER_PATH, f'{TMP_CSV_WAY_NAME_PLACEHOLDER}_{CSV_MUNICIPIO}')
TMP_CSV_PROVINCE_PATH = os.path.join(TMP_FOLDER_PATH, f'{TMP_CSV_WAY_NAME_PLACEHOLDER}_{CSV_PROVINCE}')

# Android and SQLite - Related to creation of Android SQLite DB
BASE_ANDROID_PROJECT_PATH = os.path.join('D:\\', 'AndroidStudioProjects', 'Viajar')
ANDROID_DB_FOLDER_RELATIVE_PATH = os.path.join('app', 'src', 'main', 'assets')  # Android DB will be placed in this folder
ANDROID_DB_FOLDER_PATH = os.path.join(BASE_ANDROID_PROJECT_PATH, ANDROID_DB_FOLDER_RELATIVE_PATH)
ANDROID_DB_FILENAME = 'Travel'  # Do not include extension
ANDROID_DB_FILE_PATH = os.path.join(ANDROID_DB_FOLDER_PATH, ANDROID_DB_FILENAME)  # Full path of the Android DB file
