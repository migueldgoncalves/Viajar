## Create new means of transport

This tutorial describes how to add a new means of transport to this project.

### Requirements

Software development know-how is recommended.

### Steps

1. Access the file [travel.py](https://github.com/migueldgoncalves/Viajar/blob/master/src/travel/main/travel.py).
2. Near the top of the file, in the constants related to changing means of transport, add two new constants:
   * `SWITCH_TO_<new_means_of_transport>_STRING` (ex: `SWITCH_TO_CAR_STRING`)
   * `SWITCHED_TO_<new_means_of_transport>_STRING` (ex: `SWITCHED_TO_CAR_STRING`)
3. A few lines below, in the constants related to the means of transport, add a constant for the new means of transport.
4. Inside the method `change_means_transport`, add an `elif` for the new means of transport.
5. Inside the method `make journey`, inside the block of code related to changing means of transport, add an `elif` for the new means of transport.

The new means of transport can now be used in new connections in the DB.

Have a safe trip!