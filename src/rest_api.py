from flask import Flask, render_template
import multiprocessing

from travel.main.db_interface import DBInterface

app = Flask(__name__)

print("Loading DB, please wait...")
db_interface = DBInterface()
db_interface.create_and_populate_travel_db()
print("REST API is ready to use")

lock: multiprocessing.Lock = multiprocessing.Lock()


@app.route("/")
def root():
    return render_template('index.html')


@app.route("/location/<name>")
def initial(name):
    name = name.replace("|", "/")  # Allows names with "/" to be processed
    with lock:
        location_info = db_interface.get_location_object(name)
    return {
        "name": location_info.get_name(),
        "latitude": location_info.get_latitude(),
        "longitude": location_info.get_longitude(),
        "info_brief": location_info.get_info_brief_to_print(),
        "connections": [x[0] for x in location_info.get_connections().keys()]
    }


@app.route("/all")
def hello_world():
    with lock:
        return db_interface.get_all_connections()

# Execution instructions
# Using a console, enter the root folder of this project
# Then, enter the src/ folder
# Then, run the following command: python -m flask --app rest_api run
# You can now access the page at the address localhost:5000
#    Using 127.0.0.1:5000 for some reason does not open Google Maps