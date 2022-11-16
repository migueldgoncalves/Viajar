import random


class Random:
    """
    This class provides random numbers inside specific ranges, such as simulating throwing two dice
    """

    @staticmethod
    def throw_dice(dice_number: int) -> int:
        if dice_number <= 0:
            return 0
        return random.Random().randint(dice_number, dice_number * 6)

    @staticmethod
    def get_random_percentage() -> float:
        return random.Random().randint(0, 100) * 0.01

    @staticmethod
    def get_random_int(max_int: int) -> int:
        if max_int <= 0:
            return 0
        return random.Random().randint(1, max_int)
