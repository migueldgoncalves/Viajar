import datetime

PRICE_LITER_FUEL = 2.0  # Euros
CONSUMPTION_LITERS_100_KM = 6  # liters / 100 km


class Journey:

    def __init__(self):
        self.elapsed_time: datetime.time = datetime.time(0, 0, 0)
        self.elapsed_days: int = 0
        self.traveled_distance: float = 0.0
        self.current_location: str = ""
        self.current_means_transport: str = ""

    def set_elapsed_time(self, time: datetime.time) -> None:
        self.elapsed_time = time

    def set_elapsed_days(self, days: int) -> None:
        self.elapsed_days = days

    def set_traveled_distance(self, distance: float) -> None:
        self.traveled_distance = distance

    def set_current_location(self, location: str) -> None:
        self.current_location = location

    def set_current_means_transport(self, means_transport: str) -> None:
        self.current_means_transport = means_transport

    def increment_elapsed_time(self, hours: int, minutes: int, seconds: int) -> None:
        """
        It is assumed that max time increment will not be longer than 23 hours, 59 minutes and 59 seconds
        """
        current_hours: int = self.elapsed_time.hour
        current_minutes: int = self.elapsed_time.minute
        current_seconds: int = self.elapsed_time.second

        current_seconds += seconds
        if current_seconds >= 60:
            current_minutes += 1
            current_seconds -= 60
        current_minutes += minutes
        if current_minutes >= 60:
            current_hours += 1
            current_minutes -= 60
        current_hours += hours
        if current_hours >= 24:
            self.elapsed_days += 1
            current_hours -= 24

        self.elapsed_time = datetime.time(current_hours, current_minutes, current_seconds)

    def reset_elapsed_time(self) -> None:
        self.elapsed_time = datetime.time(0, 0, 0)
        self.elapsed_days = 0

    def increment_traveled_distance(self, extra_distance: float) -> None:
        self.traveled_distance += extra_distance

    def reset_traveled_distance(self) -> None:
        self.traveled_distance = 0.0

    def get_elapsed_time(self) -> datetime.time:
        return self.elapsed_time

    def get_elapsed_days(self) -> int:
        return self.elapsed_days

    def get_traveled_distance(self) -> float:
        return self.traveled_distance

    def get_current_location(self) -> str:
        return self.current_location

    def get_current_means_transport(self) -> str:
        return self.current_means_transport

    def get_fuel_consumption(self) -> float:
        return CONSUMPTION_LITERS_100_KM * (self.get_traveled_distance() / 100)

    def get_consumed_fuel_price(self) -> float:
        return self.get_fuel_consumption() * PRICE_LITER_FUEL
