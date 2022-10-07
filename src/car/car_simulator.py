import msvcrt
import time

from car.vehicle import Vehicle
from car import vehicle
from car.car import Car

SECONDS_PER_HOUR = 3600

WAIT_FOR_INPUT = 0.2  # Seconds - Wait time for command to be introduced

# Inputs
ACCELERATE_KEY = b'w'  # W key
ACCELERATE_KEY_ALT = b'H'  # Up arrow
BRAKE_KEY = b's'  # S key
BRAKE_KEY_ALT = b'P'  # Down arrow
GEAR_UP_KEY = b'd'  # D key
GEAR_UP_KEY_ALT = b'M'  # Right arrow
GEAR_DOWN_KEY = b'a'  # A key
GEAR_DOWN_KEY_ALT = b'K'  # Left arrow
EXIT_KEY = b'q'  # Q key

# Instructions
ACCELERATE_KEYS_STRING = f"{ACCELERATE_KEY.decode().upper()} key or Up arrow"
BRAKE_KEYS_STRING = f"{BRAKE_KEY.decode().upper()} key or Down arrow"
GEAR_UP_KEYS_STRING = f"{GEAR_UP_KEY.decode().upper()} key or Right arrow"
GEAR_DOWN_KEYS_STRING = f"{GEAR_DOWN_KEY.decode().upper()} key or Left arrow"
EXIT_KEY_STRING = f"{EXIT_KEY.decode().upper()} key"

# Car modes
MODE_IDLE = 0
MODE_BRAKING = -1
MODE_ACCELERATING = 1


class CarSimulator:
    """
    CAR SIMULATOR

    This car simulation will either accelerate as fast as possible, brake as fast as possible, or slowly come to a halt due to friction.
    It will also accelerate at a constant rate within a gear
    """

    def __init__(self):
        self.car: Vehicle = Car()  # For now, vehicle type is always the same

        self.speed: float = 0.0  # km/h
        self.rpm: float = 0.0
        self.gear: int = vehicle.NEUTRAL_GEAR
        self.travelled_distance: float = 0.0  # km
        self.mode: int = MODE_IDLE  # Either idle, accelerating or braking
        self.last_read_input: float = 0.0

    #  #  #  #  #  #  #
    #  Instructions  #
    #  #  #  #  #  #  #

    @staticmethod
    def print_instructions() -> None:
        """
        Prints the car simulation instructions
        """
        print("You have the following available commands:")
        print("")
        print(f'Exit simulation - {EXIT_KEY_STRING}')
        print(f'Accelerate - {ACCELERATE_KEYS_STRING}')
        print(f'Brake - {BRAKE_KEYS_STRING}')
        print(f'Gear up - {GEAR_UP_KEYS_STRING}')
        print(f'Gear down - {GEAR_DOWN_KEYS_STRING}')
        print("")
        print("Have a safe trip!")
        print("")

    #  #  #  #  #  #
    #  Car actions  #
    #  #  #  #  #  #

    def change_gear(self, gear: int) -> None:
        """
        Sets the current gear and updated RPM
        :param gear: New current gear
        """
        if (gear != vehicle.REVERSE_GEAR) and (gear != vehicle.NEUTRAL_GEAR) and gear not in range(self.car.get_forward_gear_count() + 1):
            print("Invalid gear provided")
            return

        self.gear = gear
        self.update_rpm()

    def accelerate_car(self) -> None:
        """
        Processes a user input to accelerate car. Key can be held down.
        """
        if self.mode != MODE_ACCELERATING:  # User just touched key - Wait for next key reading before processing
            self.mode = MODE_ACCELERATING
            self.last_read_input = time.time()
            return

        current_time: float = time.time()
        time_since_last_input: float = current_time - self.last_read_input
        self.last_read_input = current_time

        if self.rpm < self.car.get_max_rpm():
            redline_speed: int = self.car.get_redline_speed_for_gear(self.gear)
            idle_to_redline_time: float = self.car.get_idle_to_redline_time_for_gear(self.gear)
            if self.gear == vehicle.REVERSE_GEAR:
                self.speed -= (redline_speed / idle_to_redline_time * time_since_last_input)  # In reverse gear, speed is negative
            elif self.gear == vehicle.NEUTRAL_GEAR:
                pass  # Nothing to do
            elif vehicle.NEUTRAL_GEAR < self.gear <= self.car.get_forward_gear_count():
                self.speed += (redline_speed / idle_to_redline_time * time_since_last_input)

        self.update_rpm()

    def decelerate_car(self, mode: int) -> None:
        """
        Processes either a user input to brake, or a deceleration by friction when the user is not braking nor accelerating
        :param mode: Either IDLE or BRAKING - Indicated whether this is a user input to brake, or a deceleration by friction
            when the user is not braking nor accelerating
        """
        speed_loss: float = 0

        if mode == MODE_BRAKING:  # User is braking
            if self.mode != MODE_BRAKING:  # User just touched key - Wait for next key reading before processing
                self.mode = MODE_BRAKING
                self.last_read_input = time.time()
                return

            current_time: float = time.time()
            time_since_last_input: float = current_time - self.last_read_input
            self.last_read_input = current_time
            speed_loss = self.car.get_braking_per_second() * time_since_last_input

        elif mode == MODE_IDLE:  # Car is slowing down on its own
            if self.mode != MODE_IDLE:
                self.mode = MODE_IDLE
                self.last_read_input = 0.0  # Reset
            speed_loss = self.car.get_friction_deceleration_per_second() * WAIT_FOR_INPUT  # During WAIT_FOR_INPUT time, user has pressed no key

        if self.speed > 0:
            if self.speed >= speed_loss:
                self.speed -= speed_loss
            else:
                self.speed = 0
        elif self.speed < 0:
            if abs(self.speed) >= speed_loss:
                self.speed += speed_loss
            else:
                self.speed = 0

        self.update_rpm()

    #  #  #  #  #  #  #  #
    #  Auxiliary methods  #
    #  #  #  #  #  #  #  #

    def print_gear(self) -> None:
        """
        Prints the current gear
        """
        if self.gear > 3:
            print(f'{self.gear}th gear')
        elif self.gear == 3:
            print("3rd gear")
        elif self.gear == 2:
            print("2nd gear")
        elif self.gear == 1:
            print("1st gear")
        elif self.gear == vehicle.NEUTRAL_GEAR:
            print("Neutral")
        elif self.gear == vehicle.REVERSE_GEAR:
            print("Reverse")

    def print_rpm(self) -> None:
        """
        Prints the current RPM, along with if gear should be changed or if car has reached the redline
        """
        if (0 < self.gear < self.car.get_forward_gear_count()) & (self.rpm < (self.car.get_redline() - self.car.get_change_gear_suggestion())):
            print(f'{int(self.rpm)} RPM')
        elif (not(vehicle.NEUTRAL_GEAR < self.gear < self.car.get_forward_gear_count())) & (abs(self.rpm) < self.car.get_redline()):  # Top gear or neutral or reverse
            print(f'{int(self.rpm)} RPM')
        elif (0 < self.gear < self.car.get_forward_gear_count()) & (
                (self.car.get_redline() - self.car.get_change_gear_suggestion()) <= self.rpm < self.car.get_redline()):
            print(f'{int(self.rpm)} RPM - Change gear')
        else:
            print(f'{int(self.rpm)} RPM - Redline!')

    def print_distance(self, leg_distance: float = 0.0, destination: str = None) -> None:
        """
        Prints travelled distance, along with remaining distance to reach destination if integrating with the journey
        :param leg_distance: Should be provided if integrating with the journey. It is the full distance between starting point
            and destination
        :param destination: Destination to be reached, if integrating with the journey
        """
        rounded_travelled_distance: float = round(self.travelled_distance, 3)
        print(f"You have travelled {rounded_travelled_distance} km")
        if leg_distance > 0 and destination:  # Integrating with journey
            remaining_distance: float = round((leg_distance - self.travelled_distance), 3)
            print(f"{remaining_distance} km left to reach {destination}")

    def print_car_state(self, leg_distance: float = 0.0, destination: str = None) -> None:
        """
        Prints the car state
        :param leg_distance: Should be provided if integrating with the journey. It is the full distance between starting point
            and destination
        :param destination: Destination to be reached, if integrating with the journey
        """
        print("")
        print(f"Current speed: {int(self.speed)} km/h")
        self.print_gear()
        self.print_rpm()
        self.print_distance(leg_distance, destination)

    def update_rpm(self) -> None:
        """
        Updates the current RPM based on the current speed and gear
        """
        redline_speed: int = self.car.get_redline_speed_for_gear(self.gear)
        if self.gear == vehicle.REVERSE_GEAR:
            self.rpm = abs(self.speed * self.car.get_redline() / redline_speed)
        elif self.gear == vehicle.NEUTRAL_GEAR:
            self.rpm = 0
        elif vehicle.NEUTRAL_GEAR < self.gear <= self.car.get_forward_gear_count():
            self.rpm = self.speed * self.car.get_redline() / redline_speed

    def increment_distance_by_elapsed_time(self, elapsed_time: float) -> None:
        """
        Increments traveled distance given elapsed time
        :param elapsed_time: In seconds
        """
        if elapsed_time < 0:
            print("Provided negative time when incrementing distance")
            return
        self.travelled_distance += elapsed_time * self.speed / SECONDS_PER_HOUR

    def reset_car_simulation(self) -> None:
        """
        Resets the car simulation
        """
        self.speed = 0
        self.rpm = 0
        self.gear = 0
        self.travelled_distance = 0

    def exit_simulation(self) -> None:
        """
        Exits the simulation
        """
        print("")
        print("You have chosen to exit")
        print("See you next time")
        exit(0)

    #  #  #  #  #  #
    #  Main method  #
    #  #  #  #  #  #

    def travel(self, distance_to_travel, destination) -> float:
        """
        Main method to run the car simulation
        :param distance_to_travel: If integrating with the journey, should be distance to travel before exiting simulation
        :param destination: If integrating with the journey, should be the name of the destination, to be displayed
        :return: If integrating with the journey, will be time spent inside simulation
        """
        print("")
        print("Welcome to the car simulation")
        print("")

        self.print_instructions()
        elapsed_time: float = 0

        # Distance being 0 == Infinite journey with no destination
        while (distance_to_travel == 0) | (self.travelled_distance < distance_to_travel):  # Processes car movement
            timer: float = time.perf_counter()  # Set and reset time count

            while (distance_to_travel == 0) | (self.travelled_distance < distance_to_travel):  # Processes moments when user is not pressing keys
                if msvcrt.kbhit():  # A key is being pressed
                    break
                elif time.perf_counter() >= (timer + WAIT_FOR_INPUT):  # No key has been pressed after some time
                    self.decelerate_car(MODE_IDLE)  # Car is decelerating through friction
                    self.print_car_state(distance_to_travel, destination)
                    self.increment_distance_by_elapsed_time(time.perf_counter() - timer)
                    timer = time.perf_counter()  # Reset timer

            key: bytes = msvcrt.getch()  # Reads key being pressed

            # Processes pressed key
            if key == EXIT_KEY:
                self.exit_simulation()
            elif (key == ACCELERATE_KEY) | (key == ACCELERATE_KEY_ALT):
                self.accelerate_car()
                self.print_car_state(distance_to_travel, destination)
            elif (key == BRAKE_KEY) | (key == BRAKE_KEY_ALT):
                self.decelerate_car(MODE_BRAKING)
                self.print_car_state(distance_to_travel, destination)
            elif (key == GEAR_UP_KEY) | (key == GEAR_UP_KEY_ALT):
                if self.gear < self.car.get_forward_gear_count():  # If gear is not top gear, shifts up
                    self.change_gear(self.gear + 1)
                    self.print_car_state(distance_to_travel, destination)
            elif (key == GEAR_DOWN_KEY) | (key == GEAR_DOWN_KEY_ALT):
                if self.gear > vehicle.REVERSE_GEAR:  # If gear is not reverse, shifts down
                    self.change_gear(self.gear - 1)
                    self.print_car_state(distance_to_travel, destination)

            self.increment_distance_by_elapsed_time(time.perf_counter() - timer)
            elapsed_time += time.perf_counter() - timer

        # At this point, there is integration with journey and car has reached destination
        print("")
        print("You have reached your destination")
        self.reset_car_simulation()
        return elapsed_time  # Time spent in simulation, for this journey leg
