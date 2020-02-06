import random


class Aleatorio:

    @staticmethod
    def um_dado():
        return random.Random().randint(1, 6)

    @staticmethod
    def dois_dados():
        return random.Random().randint(1, 12)

    @staticmethod
    def percentagem_aleatoria():
        return random.Random().randint(0, 100)
