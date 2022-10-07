from car.vehicle import Vehicle
from car import vehicle


class Car(Vehicle):
    """
    Vehicle subclass representing a car
    """

    def get_redline(self) -> int:
        return 6500

    def get_max_rpm(self) -> int:
        return 8000

    def get_change_gear_suggestion(self) -> int:
        return 1000

    def get_max_speed(self) -> int:
        return 200

    def get_friction_deceleration_per_second(self) -> int:
        return 10

    def get_braking_per_second(self) -> int:
        return 40

    def get_forward_gear_count(self) -> int:
        return 5  # Max: 8

    def get_idle_to_redline_time_for_gear(self, gear: int) -> int:
        if gear == vehicle.REVERSE_GEAR:
            return 2
        elif gear == vehicle.NEUTRAL_GEAR:
            return 0
        elif gear == 1:
            return 2
        elif gear == 2:
            return 6
        elif gear == 3:
            return 12
        elif gear == 4:
            return 25
        elif gear == 5:
            return 40
        elif gear == 6:
            return 50
        elif gear == 7:
            return 70
        elif gear == 8:
            return 90
        else:  # Error - Not expected
            print("Requested idle to redline time for invalid gear")
            return 0

    def get_redline_speed_for_gear(self, gear: int) -> int:
        if gear == vehicle.REVERSE_GEAR:
            return self.get_max_speed() // 5
        elif gear == vehicle.NEUTRAL_GEAR:
            return 0
        elif gear == 1:
            return self.get_max_speed() // 5
        elif gear == 2:
            return 2 * (self.get_max_speed() // 5)
        elif gear == 3:
            return 3 * (self.get_max_speed() // 5)
        elif gear == 4:
            return 4 * (self.get_max_speed() // 5)
        elif gear == 5:
            return self.get_max_speed()
        elif gear == 6:
            return 6 * (self.get_max_speed() // 5)
        elif gear == 7:
            return 7 * (self.get_max_speed() // 5)
        elif gear == 8:
            return 8 * (self.get_max_speed() // 5)
        else:  # Not expected
            print("Requested redline speed for invalid gear")
            return 0
