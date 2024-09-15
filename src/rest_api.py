from flask import Flask, render_template

from travel.main.db_interface import DBInterface

app = Flask(__name__)

print("Loading DB, please wait...")
db_interface = DBInterface()
db_interface.create_and_populate_travel_db()
print("REST API is ready to use")


@app.route("/")
def root():
    return render_template('index.html')


@app.route("/all")
def hello_world():
    return db_interface.get_all_connections()

# Execution instructions
# Using a console, enter the root folder of this project
# Then, enter the src/ folder
# Then, run the following command: python -m flask --app rest_api run
# You can now access the page at the address localhost:5000
#    Using 127.0.0.1:5000 for some reason does not open Google Maps