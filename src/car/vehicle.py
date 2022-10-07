from abc import abstractmethod

REVERSE_GEAR = -1
NEUTRAL_GEAR = 0


class Vehicle:
    """
    Superclass that represents a general vehicle. Should be subclassed by classes representing specific vehicles or vehicle types
    """
    @abstractmethod
    def get_redline(self) -> int:
        """
        In RPM
        """
        pass

    @abstractmethod
    def get_max_rpm(self) -> int:
        """
        Max RPM to allow in simulation for that vehicle. Can be higher than redline
        """
        pass

    @abstractmethod
    def get_change_gear_suggestion(self) -> int:
        """
        How many RPM below the redline will suggestion to change gear be shown
        """
        pass

    @abstractmethod
    def get_max_speed(self) -> int:
        """
        In km/h - Should be speed when entering redline in top gear
        """
        pass

    @abstractmethod
    def get_friction_deceleration_per_second(self) -> int:
        """
        Returns km/h decelerated per second due to friction, when not accelerating nor braking
        """
        pass

    @abstractmethod
    def get_braking_per_second(self) -> int:
        """
        Returns km/h braked per second, when applying the brakes
        """
        pass

    @abstractmethod
    def get_forward_gear_count(self) -> int:
        """
        Returns number of forward gears i.e. excluding reverse and neutral gears
        """
        pass

    @abstractmethod
    def get_idle_to_redline_time_for_gear(self, gear: int) -> int:
        """
        Returns time to go from idle to redline when accelerating in provided gear, in seconds
        """
        pass

    @abstractmethod
    def get_redline_speed_for_gear(self, gear: int) -> int:
        """
        Returns speed when entering redline for provided gear, in km/h
        """
        pass
