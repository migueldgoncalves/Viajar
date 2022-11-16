from typing import Union
from combat import random

INITIAL_HEALTH = 100

HEAD = "Head"
CHEST = "Chest"
BELLY = "Belly"
DOMINANT_ARM = "Dominant Arm"
NON_DOMINANT_ARM = "Non-Dominant Arm"
LEFT_LEG = "Left Leg"
RIGHT_LEG = "Right Leg"

IMPACT_BODY_PART_DAMAGE = {  # Ex: Losing 1 arm health point causes the loss of 0.2 general health points
    HEAD: 1,
    CHEST: 1,
    BELLY: 0.8,
    DOMINANT_ARM: 0.2,
    NON_DOMINANT_ARM: 0.2,
    LEFT_LEG: 0.2,
    RIGHT_LEG: 0.2
}

DEFENSE_BONUS = {  # Points to add to fighter defense when attacked in a certain body part
    HEAD: 1000,
    CHEST: 1000,
    BELLY: 500,
    DOMINANT_ARM: 1500,
    NON_DOMINANT_ARM: 0,
    LEFT_LEG: 0,
    RIGHT_LEG: 0
}

BODY_PART_KEYS = {  # Map menu options to body parts
    1: HEAD,
    2: CHEST,
    3: BELLY,
    4: DOMINANT_ARM,
    5: NON_DOMINANT_ARM,
    6: LEFT_LEG,
    7: RIGHT_LEG
}

PAIN_GAIN_PER_HEALTH_LOSS = 0.2  # Gained pain points per lost health points in the attacked body part
STRENGTH_LOSS_PER_HEALTH_LOSS = 0.25  # Lost strength points per lost health points in the dominant arm, if attacked
SPEED_LOSS_PER_HEALTH_LOSS = 0.25  # Lost speed points per lost health points in the legs, if attacked
BLEEDING_CHANCE_PER_HEALTH_LOSS = 0.02  # When attacked, chances of bleeding are this value multiplied by the lost health in the body part
BLEEDING_GAIN_PER_HEALTH_LOSS = 0.05  # If an attack causes bleeding, gain of bleeding points is this value multiplied by the health loss in the body part
HEALTH_LOSS_PER_BLEEDING = 1  # Each round, bleeding fighters lose this value multiplied by the bleeding points worth of general health points
DEFENSE_ATTACK_LOSS_PER_PAIN = 20  # Attack and defense points lost with each pain point
HEALTH_LOSS_PER_ATTACK_POWER = 0.01  # Health points lost for every attack point above the defense points in a round
SHIELD_DEFENSE = 2000  # Defense points

MIN_STRENGTH = 100 - 4 * 6  # Where 6 = Max value of die throw
MAX_STRENGTH = 100 + 4 * 6
MIN_SPEED = 100 - 4 * 6
MAX_SPEED = 100 + 4 * 6


class BodyPart:
    """
    This class is a data access object representing a generic body part
    """
    def __init__(self, name: str, menu_key: int, starting_health: int, impact_in_general_health: float, defense_bonus: int):
        """
        Init routine
        :param name: Name of the body part
        :param menu_key: Key pointing at the body part in the combat menu
        :param starting_health: Health at the start of the combat
        :param impact_in_general_health: How damaging to the body is being attacked in this body part. Should be between 0 and 1, where
            0 means an attack in this body part does not affect general health, and 1 means that the general body health will decrease
            as much as the health of this body part in an attack
        :param defense_bonus: Points to add to the fighter defense when attacked in this body part
        """
        # Parameter checking
        assert name
        assert menu_key > 0
        assert starting_health > 0
        assert 0 <= impact_in_general_health <= 1
        assert defense_bonus >= 0

        self.name: str = name
        self.menu_key: int = menu_key

        self.starting_health: int = starting_health
        self.health: int = self.starting_health
        self.impact_in_general_health: float = impact_in_general_health

        self.defense_bonus: int = defense_bonus


class Fighter:
    """
    This class is a data access object representing a fighter
    """

    def __init__(self, name: str, strength: int, speed: int, weapon_stats: int, shield: bool, cpu: bool):
        """
        Initializer routine
        :param name: Fighter name.
        :param strength: If present, will be the fighter starting strength. If 0, strength will be randomly calculated. Should be value between 76 and 124
        :param speed: If present, will be the fighter starting speed. If 0, speed will be randomly calculated. Should be value between 76 and 124
        :param weapon_stats: Attack and defense capabilities of the fighter weapon. Should be value between 1 and 5
        :param shield: If True, fighter carries a shield. If False, fighter has no shield
        :param cpu: If True, fighter will be CPU-controlled. If False, fighter will be user-controlled
        """
        assert name
        assert strength >= 0
        assert speed >= 0
        assert weapon_stats > 0

        self.name: str = name
        self.general_health: int = INITIAL_HEALTH
        self.weapon_stats: int = weapon_stats
        self.shield: bool = shield
        self.pain: int = 0
        self.bleeding: int = 0
        self.cpu: bool = cpu  # False - User-controlled, True - CPU-controlled

        self.body_parts: dict[str, BodyPart] = {}
        for key in BODY_PART_KEYS.keys():
            body_part_name: str = BODY_PART_KEYS[key]
            body_part: BodyPart = BodyPart(name=body_part_name, menu_key=key, starting_health=INITIAL_HEALTH,
                                           impact_in_general_health=IMPACT_BODY_PART_DAMAGE[body_part_name],
                                           defense_bonus=DEFENSE_BONUS[body_part_name])
            self.body_parts[body_part_name] = body_part

        if strength == 0:  # Not provided - Should be calculated randomly
            self.initial_strength: int = random.Random.generate_parameter_centered_at_100()
        else:
            self.initial_strength: int = strength

        if speed == 0:  # Not provided - Should be calculated randomly
            self.initial_speed: int = random.Random.generate_parameter_centered_at_100()
        else:
            self.initial_speed: int = speed

    def get_name(self) -> str:
        return self.name

    def get_initial_strength(self) -> int:
        return self.initial_strength

    def get_current_strength(self) -> int:
        return round(self.initial_strength - round(
            (INITIAL_HEALTH - self.get_body_part_health(DOMINANT_ARM)) * STRENGTH_LOSS_PER_HEALTH_LOSS))

    def get_initial_speed(self) -> int:
        return self.initial_speed

    def get_current_speed(self):
        return round(self.initial_speed - round(
            (INITIAL_HEALTH - ((self.get_body_part_health(LEFT_LEG) + self.get_body_part_health(RIGHT_LEG)) / 2)) * SPEED_LOSS_PER_HEALTH_LOSS))

    def get_weapon_stats(self) -> int:
        return self.weapon_stats

    def get_general_health(self) -> int:
        return self.general_health

    def get_body_part_health(self, identifier: Union[str, int]) -> int:
        body_part: BodyPart = self._get_body_part(identifier)
        return body_part.health

    def get_shield_usage(self) -> bool:
        return self.shield

    def get_pain(self) -> int:
        return self.pain

    def get_bleeding(self) -> int:
        return self.bleeding

    def get_cpu(self) -> bool:
        return self.cpu

    def get_attack_points(self) -> int:
        """
        Generates a value of attack points for the fighter, considering their physical condition and adding randomness
        """
        base_points: int = self.get_current_strength() * self.get_weapon_stats() * random.Random.throw_dice(2)  # 152 <= value <= 7.440
        points_lost_from_pain: int = self.get_pain() * DEFENSE_ATTACK_LOSS_PER_PAIN

        attack_points: int = base_points - points_lost_from_pain

        if attack_points < 0:  # Attack points should be >= 0
            attack_points = 0

        print(f"Base attack points: {base_points}")
        print(f"Attack points lost due to pain: {points_lost_from_pain}")
        print(f"TOTAL: {attack_points}")
        print("")

        return attack_points

    def get_defense_points(self):
        """
        Generates a value of defense points for the fighter, considering their physical condition, presence of a shield, and adding randomness
        """
        base_points: int = self.get_current_speed() * self.get_weapon_stats() * random.Random.throw_dice(2)  # 152 <= value <= 7.740
        points_lost_from_pain: int = self.get_pain() * DEFENSE_ATTACK_LOSS_PER_PAIN

        if self.shield:
            defense_points: int = base_points - points_lost_from_pain + SHIELD_DEFENSE
        else:
            defense_points: int = base_points - points_lost_from_pain

        if defense_points < 0:  # Defense points should be >= 0
            defense_points = 0

        print(f"Base defense points: {base_points}")
        print(f"Defense points lost due to pain: {points_lost_from_pain}")
        if self.get_shield_usage():
            print(f"Defense points gained from the shield: {SHIELD_DEFENSE}")
        print(f"TOTAL: {defense_points}")
        print("")

        return defense_points

    def _get_body_part(self, identifier: Union[str, int]) -> BodyPart:
        """
        Returns a body part object matching the provided menu key or body part name. Raises Exception if no match is found
        """
        assert identifier
        assert type(identifier) in [str, int]
        if type(identifier) == int:
            menu_key: int = identifier
            body_part_name = BODY_PART_KEYS[menu_key]  # Intended to raise Exception if no match found
        else:  # type == str
            body_part_name: str = identifier
        body_part: BodyPart = self.body_parts[body_part_name]  # Intended to raise Exception if no match found
        return body_part

    def set_name(self, name: str) -> None:
        assert name
        self.name = name

    def set_initial_strength(self, strength: int) -> None:
        assert strength > 0
        self.initial_strength = strength

    def set_initial_speed(self, speed: int) -> None:
        assert speed > 0
        self.initial_speed = speed

    def set_weapon_stats(self, weapon_stats: int) -> None:
        assert weapon_stats > 0
        self.weapon_stats = weapon_stats

    def set_general_health(self, general_health: int) -> None:
        assert general_health >= 0  # Can be set to 0 when the fighter dies
        self.general_health = general_health

    def set_body_part_health(self, identifier: Union[str, int], health: int) -> None:
        assert health >= 0
        body_part: BodyPart = self._get_body_part(identifier)
        body_part.health = health

    def set_shield_usage(self, shield: bool) -> None:
        self.shield = shield

    def set_pain(self, pain: int) -> None:
        assert pain >= 0
        self.pain = pain

    def set_bleeding(self, bleeding: int) -> None:
        assert bleeding >= 0
        self.bleeding = bleeding

    def set_cpu(self, cpu: bool) -> None:
        self.cpu = cpu

    def increase_pain(self, lost_health: int) -> None:
        """
        Increases pain based on lost health in the attacked body part
        :param lost_health: In the attacked body part
        """
        assert lost_health >= 0

        pain_increase: int = round(lost_health * PAIN_GAIN_PER_HEALTH_LOSS)
        if pain_increase == 0:  # Nothing to do
            return

        self.set_pain(self.get_pain() + pain_increase)
        if pain_increase == 1:
            print("Pain increased 1 point")
        else:
            print(f"Pain increased {pain_increase} points")

    def increase_bleeding(self, lost_health: int) -> None:
        """
        Increases bleeding based on lost health in the attacked body part
        :param lost_health: In the attacked body part
        """
        assert lost_health >= 0

        bleeding_chance: float = BLEEDING_CHANCE_PER_HEALTH_LOSS * lost_health
        if bleeding_chance > random.Random.get_random_percentage():  # Attack caused bleeding
            bleeding_increase: int = round(lost_health * BLEEDING_GAIN_PER_HEALTH_LOSS)
            if not bleeding_increase:  # Nothing to do
                return

            self.set_bleeding(self.get_bleeding() + bleeding_increase)
            if bleeding_increase == 1:
                print("Bleeding increased 1 point")
            else:
                print(f"Bleeding increased {bleeding_increase} points")

    def decrease_general_health(self, lost_health: float) -> None:
        assert lost_health >= 0

        lost_health = round(lost_health)
        if not lost_health or not self.general_health:  # Nothing to do
            return
        elif lost_health > self.general_health:  # Prevents health from decreasing under 0
            lost_health = self.general_health

        self.set_general_health(self.get_general_health() - lost_health)
        if lost_health == 1:
            print("General health lost 1 point")
        else:
            print(f"General health lost {lost_health} points")

    def decrease_general_health_from_bleeding(self):
        self.decrease_general_health(round(self.bleeding * HEALTH_LOSS_PER_BLEEDING))

    def decrease_body_part_health(self, lost_health: int, identifier: Union[str, int]) -> None:
        """
        Main routine to call to calculate effects of successful attack on a fighter
        """
        assert lost_health >= 0
        assert identifier

        body_part: BodyPart = self._get_body_part(identifier)
        if not lost_health or not self.get_body_part_health(identifier):  # Nothing to do
            return
        elif lost_health > body_part.health:  # Prevents health from decreasing under 0
            lost_health = body_part.health

        body_part.health -= lost_health
        self.decrease_general_health(lost_health * body_part.impact_in_general_health)
        self.increase_pain(lost_health)
        self.increase_bleeding(lost_health)
        if lost_health == 1:
            print(f"{body_part.name} lost 1 health point")
        else:
            print(f"{body_part.name} lost {lost_health} health points")

    def decrease_body_part_health_from_attack(self, enemy_attack_points: int, own_defense_points: int, body_part_id: Union[str, int]) -> None:
        assert enemy_attack_points >= 0
        assert own_defense_points >= 0
        assert body_part_id

        if enemy_attack_points <= own_defense_points:  # Defense successful - Nothing to do
            return

        lost_health: int = round((enemy_attack_points - own_defense_points) * HEALTH_LOSS_PER_ATTACK_POWER)
        self.decrease_body_part_health(lost_health, body_part_id)
