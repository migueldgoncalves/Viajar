import random
import datetime
from typing import Callable, Optional

from travel.main import journey, db_interface, location, menu
from car import car_simulator

# Strings related to changing means of transport
SWITCH_TO_CAR_STRING = "Return to the road"
SWITCH_TO_BOAT_STRING = "Board a boat"
SWITCH_TO_SHIP_STRING = "Board a ship"
SWITCH_TO_PLANE_STRING = "Board a plane"
SWITCH_TO_TRAIN_STRING = "Board a train"  # Use when only "low-speed" train is available
SWITCH_TO_STANDARD_TRAIN_STRING = "Board a standard train"  # Use when both "low-speed" and high-speed train are available
SWITCH_TO_HIGH_SPEED_TRAIN_STRING = "Board a high-speed train"
SWITCH_TO_SUBWAY_STRING = "Board a subway train"
SWITCH_TO_TRANSFER_STRING = "Transfer between means of transport"
SWITCH_TO_HIKING_STRING = "Start hiking"
SWITCHED_TO_CAR_STRING = "You are back on the road"
SWITCHED_TO_BOAT_STRING = "You are aboard a boat"
SWITCHED_TO_SHIP_STRING = "You are aboard a ship"
SWITCHED_TO_PLANE_STRING = "You are aboard a plane"
SWITCHED_TO_TRAIN_STRING = "You are aboard a train"  # Use when only "low-speed" train is available
SWITCHED_TO_STANDARD_TRAIN_STRING = "You are aboard a standard train"  # Use when both "low-speed" and high-speed train are available
SWITCHED_TO_HIGH_SPEED_TRAIN_STRING = "You are aboard a high-speed train"
SWITCHED_TO_SUBWAY_STRING = "You are aboard a subway train"
SWITCHED_TO_TRANSFER_STRING = "You are transferring between means of transport"
SWITCHED_TO_HIKING_STRING = "You are now hiking"

# Permanent options in the journey menu
OPTION_SHOW_LOCATION_INFO = "Show location information"
OPTION_SHOW_JOURNEY_STATISTICS = "Show journey statistics"

# Example menu option: 1 -> Alcoutim (N, 1 km) » Guadiana River: Direction Mértola/Pomarão
# Other string separators are defined elsewhere
SEPARATOR_WAY_INFO = "»"
SEPARATOR_DIRECTION = ":"

# Speed (km/h)
MIN_SPEED = 50
MAX_SPEED = 120

# Means of transport - Must match means of transport present in Connection table of DB
CAR = 'Car'
BOAT = 'Boat'
SHIP = "Ship"
PLANE = 'Plane'
TRAIN = 'Train'  # "Low-speed" train
HIGH_SPEED_TRAIN = 'High-Speed Train'
SUBWAY = 'Subway'
TRANSFER = 'Transfer'
HIKING = 'Hiking'
DEFAULT_MEANS_TRANSPORT = CAR


class Travel:
    """
    Main class related to the journey. Creates and populates the DB, presents the user interface, and receives and
        processes the user input
    """

    def __init__(self, initial_location: str, return_and_not_exit: bool = False):
        """
        If return_and_not_exit is True, exit routine will exit journey menu but not exit program. Can be set to True during
            automatic tests to simulate a journey and analise the output and state after providing each option
        """
        self.initial_location: str = initial_location
        self.return_and_not_exit: bool = return_and_not_exit

        self.db_interface: db_interface.DBInterface = db_interface.DBInterface()  # Contains all available locations
        self.db_initialized: bool = self.db_interface.create_and_populate_travel_db()
        if not self.db_initialized:  # Error while initializing the DB
            # Error message is printed when trying to start journey - Not adding it here prevents printing same message twice
            return

        # Initialize journey
        self.current_journey: journey.Journey = journey.Journey()
        self.car_simulation: car_simulator.CarSimulator = car_simulator.CarSimulator()
        self.current_journey.set_current_location(self.initial_location)
        self.current_journey.set_current_means_transport(DEFAULT_MEANS_TRANSPORT)
        print("Welcome to the journey")
        print("You have", self.db_interface.get_total_location_number(), "available locations to visit")
        print("Your starting location will be", self.initial_location)
        print("")

        # User selects if they wish to simulate car journey between locations, or if moving between locations should be instant
        self.is_car_requested: bool = self.request_car_simulation_usage()

    #  #  #  #  #  #
    # Menu options #
    #  #  #  #  #  #

    def exit_journey(self) -> None:
        if self.return_and_not_exit:
            return  # Return instead of exit

        print("")
        print("You have chosen to exit the journey.")
        print("See you soon.")
        self.db_interface.exit()
        exit(0)

    def print_location_info(self) -> None:
        print("")
        self.get_current_location_object().print_info_complete()

    def print_journey_statistics(self) -> None:
        print("")
        print(f"You have traveled {self.current_journey.get_traveled_distance()} km")
        if self.current_journey.get_elapsed_days() == 0:  # Ex: You have been travelling for 00:43:25
            print(f"You have been travelling for {self.current_journey.get_elapsed_time()}")
        elif self.current_journey.get_elapsed_days() == 1:  # Ex: You have been travelling for 1 day and 00:43:25
            print(f"You have been travelling for 1 day and {self.current_journey.get_elapsed_time()}")
        else:  # Ex: You have been travelling for 3 days and 00:43:25
            print(f"You have been travelling for {self.current_journey.get_elapsed_days()} days and {self.current_journey.get_elapsed_time()}")
        print(f"You have consumed {self.current_journey.get_fuel_consumption()} liters of fuel")
        print(f"You have spent {self.current_journey.get_consumed_fuel_price()} euros in fuel")

    def change_means_transport(self, new_means_transport: str) -> None:
        self.current_journey.set_current_means_transport(new_means_transport)

        print("")
        if self.current_journey.get_current_means_transport() == CAR:
            print(SWITCHED_TO_CAR_STRING)
        elif self.current_journey.get_current_means_transport() == BOAT:
            print(SWITCHED_TO_BOAT_STRING)
        elif self.current_journey.get_current_means_transport() == SHIP:
            print(SWITCHED_TO_SHIP_STRING)
        elif self.current_journey.get_current_means_transport() == PLANE:
            print(SWITCHED_TO_PLANE_STRING)
        elif self.current_journey.get_current_means_transport() == TRAIN:
            high_speed_train_present: bool = False
            for x in self.get_current_location_object().get_connections():
                if x[1] == HIGH_SPEED_TRAIN:
                    high_speed_train_present = True
            if high_speed_train_present:
                print(SWITCHED_TO_STANDARD_TRAIN_STRING)  # Allows distinguishing from the high-speed train
            else:
                print(SWITCHED_TO_TRAIN_STRING)
        elif self.current_journey.get_current_means_transport() == SUBWAY:
            print(SWITCHED_TO_SUBWAY_STRING)
        elif self.current_journey.get_current_means_transport() == HIGH_SPEED_TRAIN:
            print(SWITCHED_TO_HIGH_SPEED_TRAIN_STRING)
        elif self.current_journey.get_current_means_transport() == TRANSFER:
            print(SWITCHED_TO_TRANSFER_STRING)
        elif self.current_journey.get_current_means_transport() == HIKING:
            print(SWITCHED_TO_HIKING_STRING)
        print("You have new available destinations")

    #  #  #  #  #  #  #  #
    # Auxiliary methods #
    #  #  #  #  #  #  #  #

    def get_current_location_object(self) -> location.Location:
        location_name: str = self.current_journey.get_current_location()
        return self.db_interface.get_location_object(location_name)

    @staticmethod
    def seconds_to_datetime(seconds: int) -> datetime.time:
        """
        Expects a value between 0 and 86399 (23 hours, 59 minutes and 59 seconds)
        """
        hours: int = seconds // 3600
        seconds = seconds - (hours * 3600)
        minutes: int = seconds // 60
        seconds = seconds - (minutes * 60)
        return datetime.time(int(hours), int(minutes), int(seconds))

    def increment_traveled_time(self, elapsed_seconds: int) -> None:
        """
        Expects a value between 0 and 86399 (23 hours, 59 minutes and 59 seconds)
        """
        elapsed_time: datetime.time = self.seconds_to_datetime(elapsed_seconds)
        self.current_journey.increment_elapsed_time(elapsed_time.hour, elapsed_time.minute, elapsed_time.second)

    def update_journey(self, desired_surrounding_location: str) -> None:
        """
        Given desired surrounding location to travel to, updates the journey and runs the car simulation if requested
        """
        print(f"You have chosen to go to {desired_surrounding_location}")

        leg_distance: float = self.get_current_location_object().get_distance(
            desired_surrounding_location, self.current_journey.get_current_means_transport())

        if not self.is_car_requested:  # If car simulation is not being used
            average_speed: int = int(random.uniform(MIN_SPEED, MAX_SPEED))  # For now, average speed will be random
            elapsed_seconds: int = int(leg_distance / average_speed * 3600)
            self.increment_traveled_time(elapsed_seconds)

        self.current_journey.increment_traveled_distance(leg_distance)
        self.current_journey.set_current_location(desired_surrounding_location)

        # Run car simulation if requested and if current means of transport is car
        if self.is_car_requested and self.current_journey.get_current_means_transport() == CAR:
            elapsed_time: int = int(self.car_simulation.travel(leg_distance, desired_surrounding_location))  # Actual time spent in simulation
            self.increment_traveled_time(elapsed_time)

    @staticmethod
    def request_car_simulation_usage():
        menu_introduction: list[str] = [
            "Do you wish to simulate a car journey when travelling between locations?",
            "If not, travel between locations will be instant"
        ]
        user_requested_car: bool = menu.present_boolean_menu(menu_introduction)
        return user_requested_car

    #  #  #  #  #  #
    # Main method #
    #  #  #  #  #  #

    def make_journey(self):
        if not self.db_initialized:  # Failed to initialize DB - Cancel journey
            print("Error while initializing DB - Cannot start journey")
            return

        while True:
            # [location_name, means_transport] -> [cardinal_point, distance, means_transport]
            connections: dict[tuple[str, str], tuple[str, float, str]] = self.get_current_location_object().get_connections()

            option_labels: list[str] = []
            option_to_action: dict[int, Callable] = {}  # Maps option numbers to the respective routines
            option_to_action_argument: dict[int, Optional[str]] = {}  # Maps option numbers to the respective routine arguments

            # Location options

            index: int = 1
            surrounding_locations_current_transport: list[str] = []
            for means_of_transport in connections:

                # Get parameters
                surrounding_location_name: str = means_of_transport[0]
                means_transport: str = means_of_transport[1]
                cardinal_point: str = self.get_current_location_object().get_cardinal_point(
                    surrounding_location_name, means_transport)
                distance: float = self.get_current_location_object().get_distance(surrounding_location_name, means_transport)

                # For locations accessible with the current means of transport, get option labels and actions
                if means_transport == self.current_journey.get_current_means_transport():
                    surrounding_locations_current_transport.append(surrounding_location_name)
                    if means_transport == TRANSFER:  # Ex: 1 - Guerreiros do Rio
                        label: str = f'{surrounding_location_name}'
                    else:  # Ex: 1 - Guerreiros do Rio (N, 1 km)
                        label: str = f'{surrounding_location_name} ({cardinal_point}, {distance} km)'

                    way = self.get_current_location_object().get_way(surrounding_location_name, means_transport)
                    destinations = self.get_current_location_object().get_destinations_as_string(
                        surrounding_location_name, means_transport)  # Major destinations available by going to that location
                    if way and destinations:  # Way is only printed if there are associated destinations
                        label = f'{label} {SEPARATOR_WAY_INFO} {way}{SEPARATOR_DIRECTION} Direction {destinations}'

                    # Full label example
                    # Alcoutim (N, 9.5 km) » Rio Guadiana: Direction Alcoutim / Mértola / Sanlúcar de Guadiana

                    option_labels.append(label)
                    option_to_action[index] = self.update_journey
                    option_to_action_argument[index] = surrounding_location_name

                    index += 1

            # Options to change means of transport, if any

            available_means_transport: list[str] = []  # Other means of transport apart from current one
            for means_of_transport_and_location_name in connections:
                means_transport: str = means_of_transport_and_location_name[1]
                if means_transport != self.current_journey.get_current_means_transport() and \
                        means_transport not in available_means_transport:
                    available_means_transport.append(means_transport)

            if len(available_means_transport) > 0:  # Means of transport can be changed
                for means_of_transport in available_means_transport:
                    label: str = ''
                    if means_of_transport == CAR:
                        label = SWITCH_TO_CAR_STRING
                    elif means_of_transport == BOAT:
                        label = SWITCH_TO_BOAT_STRING
                    elif means_of_transport == SHIP:
                        label = SWITCH_TO_SHIP_STRING
                    elif means_of_transport == PLANE:
                        label = SWITCH_TO_PLANE_STRING
                    elif means_of_transport == TRAIN:
                        high_speed_train_present = False
                        # Both "standard" and high-speed train are present
                        for x in self.get_current_location_object().get_connections():
                            if x[1] == HIGH_SPEED_TRAIN:
                                high_speed_train_present = True
                        label = SWITCH_TO_STANDARD_TRAIN_STRING if high_speed_train_present else SWITCH_TO_TRAIN_STRING
                    elif means_of_transport == SUBWAY:
                        label = SWITCH_TO_SUBWAY_STRING
                    elif means_of_transport == HIGH_SPEED_TRAIN:
                        label = SWITCH_TO_HIGH_SPEED_TRAIN_STRING
                    elif means_of_transport == TRANSFER:
                        label = SWITCH_TO_TRANSFER_STRING
                    elif means_of_transport == HIKING:
                        label = SWITCH_TO_HIKING_STRING

                    option_labels.append(label)
                    option_to_action[index] = self.change_means_transport
                    option_to_action_argument[index] = means_of_transport

                    index += 1

            # Option to print full location info

            label = OPTION_SHOW_LOCATION_INFO
            option_labels.append(label)
            option_to_action[index] = self.print_location_info
            option_to_action_argument[index] = None
            index += 1

            # Option to print journey statistics - Bottom menu option

            label = OPTION_SHOW_JOURNEY_STATISTICS
            option_labels.append(label)
            option_to_action[index] = self.print_journey_statistics
            option_to_action_argument[index] = None
            index += 1

            location_menu_introduction: list[str] = [
                "",  # Empty line between each printing of the location menu
                self.get_current_location_object().get_info_brief_to_print(),
                "Select one of the following options"
            ]

            # Guaranteed to be valid int
            user_option: int = menu.present_numeric_menu(option_labels=option_labels,
                                                         menu_introduction=location_menu_introduction,
                                                         exit_routine=self.exit_journey)

            if user_option == menu.EXIT_OPTION and self.return_and_not_exit:  # Menu does not return
                break  # Exits menu loop without exiting program and preserves journey state for analysis

            callback: Callable = option_to_action[user_option]
            argument: Optional[str] = option_to_action_argument[user_option]
            if argument:
                callback(argument)
            else:
                callback()
