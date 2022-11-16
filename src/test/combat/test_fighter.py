import unittest

from combat import fighter


class TestFighter(unittest.TestCase):

    def setUp(self):
        self.character = fighter.Fighter("Fighter", 100, 100, 3, False, True)

    def test_initializer_successful_strength_speed_provided(self):
        character: fighter.Fighter = fighter.Fighter('Fighter', 100, 100, 1, True, False)
        self.assertEqual('Fighter', character.name)
        self.assertEqual(fighter.INITIAL_HEALTH, character.general_health)
        self.assertEqual(100, character.initial_strength)
        self.assertEqual(100, character.initial_speed)
        self.assertEqual(1, character.weapon_stats)
        self.assertEqual(True, character.shield)
        self.assertEqual(False, character.cpu)
        self.assertEqual(0, character.pain)
        self.assertEqual(0, character.bleeding)

        self.assertEqual(len(fighter.BODY_PART_KEYS), len(character.body_parts))
        for key in fighter.BODY_PART_KEYS:
            body_part_name: str = fighter.BODY_PART_KEYS[key]
            body_part: fighter.BodyPart = character.body_parts[body_part_name]
            self.assertEqual(body_part_name, body_part.name)
            self.assertEqual(key, body_part.menu_key)
            self.assertEqual(fighter.INITIAL_HEALTH, body_part.starting_health)
            self.assertEqual(fighter.INITIAL_HEALTH, body_part.health)
            self.assertEqual(fighter.IMPACT_BODY_PART_DAMAGE[body_part_name], body_part.impact_in_general_health)
            self.assertEqual(fighter.DEFENSE_BONUS[body_part_name], body_part.defense_bonus)

    def test_initializer_successful_strength_speed_not_provided(self):
        character: fighter.Fighter = fighter.Fighter('Fighter', 0, 0, 5, False, True)
        self.assertEqual('Fighter', character.name)
        self.assertEqual(fighter.INITIAL_HEALTH, character.general_health)
        self.assertTrue(fighter.MIN_STRENGTH <= character.initial_strength <= fighter.MAX_STRENGTH)
        self.assertTrue(fighter.MIN_SPEED <= character.initial_speed <= fighter.MAX_SPEED)
        self.assertEqual(5, character.weapon_stats)
        self.assertEqual(False, character.shield)
        self.assertEqual(True, character.cpu)
        self.assertEqual(0, character.pain)
        self.assertEqual(0, character.bleeding)

        self.assertEqual(len(fighter.BODY_PART_KEYS), len(character.body_parts))
        for key in fighter.BODY_PART_KEYS:
            body_part_name: str = fighter.BODY_PART_KEYS[key]
            body_part: fighter.BodyPart = character.body_parts[body_part_name]
            self.assertEqual(body_part_name, body_part.name)
            self.assertEqual(key, body_part.menu_key)
            self.assertEqual(fighter.INITIAL_HEALTH, body_part.starting_health)
            self.assertEqual(fighter.INITIAL_HEALTH, body_part.health)
            self.assertEqual(fighter.IMPACT_BODY_PART_DAMAGE[body_part_name], body_part.impact_in_general_health)
            self.assertEqual(fighter.DEFENSE_BONUS[body_part_name], body_part.defense_bonus)

    def test_initializer_invalid_arguments(self):
        with self.assertRaises(AssertionError):
            fighter.Fighter('', -1, -1, 0, False, False)

    def test_initializer_invalid_name(self):
        with self.assertRaises(AssertionError):
            fighter.Fighter('', 100, 100, 3, False, False)

    def test_initializer_invalid_strength(self):
        with self.assertRaises(AssertionError):
            fighter.Fighter('Fighter', -1, 100, 3, False, False)

    def test_initializer_invalid_speed(self):
        with self.assertRaises(AssertionError):
            fighter.Fighter('Fighter', 100, -1, 3, False, False)

    def test_initializer_invalid_weapon(self):
        with self.assertRaises(AssertionError):
            fighter.Fighter('Fighter', 100, 100, 0, False, False)
        with self.assertRaises(AssertionError):
            fighter.Fighter('Fighter', 100, 100, -1, False, False)

    def test_getter_setter_name(self):
        self.assertEqual('Fighter', self.character.get_name())
        with self.assertRaises(AssertionError):
            self.character.set_name('')
        self.character.set_name('Fighter2')
        self.assertEqual('Fighter2', self.character.get_name())

    def test_getter_setter_initial_strength(self):
        self.assertEqual(100, self.character.get_initial_strength())
        with self.assertRaises(AssertionError):
            self.character.set_initial_strength(0)
        with self.assertRaises(AssertionError):
            self.character.set_initial_strength(-1)
        self.character.set_initial_strength(99)
        self.assertEqual(99, self.character.get_initial_strength())

    def test_get_current_strength(self):
        self.assertEqual(100, self.character.get_current_strength())
        self.character.set_body_part_health(fighter.DOMINANT_ARM, 99)
        self.assertEqual(100, self.character.get_current_strength())
        self.character.set_body_part_health(fighter.DOMINANT_ARM, 98)
        self.assertEqual(100, self.character.get_current_strength())
        self.character.set_body_part_health(fighter.DOMINANT_ARM, 97)
        self.assertEqual(99, self.character.get_current_strength())
        self.character.set_body_part_health(fighter.DOMINANT_ARM, 96)
        self.assertEqual(99, self.character.get_current_strength())
        self.character.set_body_part_health(fighter.DOMINANT_ARM, 95)
        self.assertEqual(99, self.character.get_current_strength())
        self.character.set_body_part_health(fighter.DOMINANT_ARM, 94)
        self.assertEqual(98, self.character.get_current_strength())
        self.character.set_body_part_health(fighter.DOMINANT_ARM, 93)
        self.assertEqual(98, self.character.get_current_strength())
        self.character.set_body_part_health(fighter.DOMINANT_ARM, 92)
        self.assertEqual(98, self.character.get_current_strength())

        self.character.set_initial_strength(90)
        self.assertEqual(88, self.character.get_current_strength())

    def test_getter_setter_initial_speed(self):
        self.assertEqual(100, self.character.get_initial_speed())
        with self.assertRaises(AssertionError):
            self.character.set_initial_speed(0)
        with self.assertRaises(AssertionError):
            self.character.set_initial_speed(-1)
        self.character.set_initial_speed(99)
        self.assertEqual(99, self.character.get_initial_speed())

    def test_get_current_speed(self):
        self.assertEqual(100, self.character.get_current_speed())
        self.character.set_body_part_health(fighter.LEFT_LEG, 98)
        self.assertEqual(100, self.character.get_current_speed())
        self.character.set_body_part_health(fighter.LEFT_LEG, 96)
        self.assertEqual(100, self.character.get_current_speed())
        self.character.set_body_part_health(fighter.LEFT_LEG, 94)
        self.assertEqual(99, self.character.get_current_speed())
        self.character.set_body_part_health(fighter.LEFT_LEG, 92)
        self.assertEqual(99, self.character.get_current_speed())

        self.character.set_body_part_health(fighter.RIGHT_LEG, 98)
        self.assertEqual(99, self.character.get_current_speed())
        self.character.set_body_part_health(fighter.RIGHT_LEG, 96)
        self.assertEqual(98, self.character.get_current_speed())
        self.character.set_body_part_health(fighter.RIGHT_LEG, 94)
        self.assertEqual(98, self.character.get_current_speed())
        self.character.set_body_part_health(fighter.RIGHT_LEG, 92)
        self.assertEqual(98, self.character.get_current_speed())

        self.character.set_initial_speed(90)
        self.assertEqual(88, self.character.get_current_speed())

    def test_getter_setter_weapon_stats(self):
        self.assertEqual(3, self.character.get_weapon_stats())
        with self.assertRaises(AssertionError):
            self.character.set_weapon_stats(0)
        with self.assertRaises(AssertionError):
            self.character.set_weapon_stats(-1)
        self.character.set_weapon_stats(2)
        self.assertEqual(2, self.character.get_weapon_stats())

    def test_getter_setter_general_health(self):
        self.assertEqual(100, self.character.get_general_health())
        with self.assertRaises(AssertionError):
            self.character.set_general_health(-1)
        self.character.set_general_health(0)
        self.assertEqual(0, self.character.get_general_health())

    def test_getter_setter_body_part_health(self):
        for menu_key in fighter.BODY_PART_KEYS:
            self.assertEqual(100, self.character.get_body_part_health(menu_key))
            with self.assertRaises(AssertionError):
                self.character.set_body_part_health(menu_key, -1)
            self.character.set_body_part_health(menu_key, 0)
            self.assertEqual(0, self.character.get_body_part_health(menu_key))

    def test_getter_setter_shield_usage(self):
        self.assertFalse(self.character.get_shield_usage())
        self.character.set_shield_usage(True)
        self.assertTrue(self.character.get_shield_usage())

    def test_getter_setter_pain(self):
        self.assertEqual(0, self.character.get_pain())
        with self.assertRaises(AssertionError):
            self.character.set_pain(-1)
        self.character.set_pain(1)
        self.assertEqual(1, self.character.get_pain())

    def test_getter_setter_general_bleeding(self):
        self.assertEqual(0, self.character.get_bleeding())
        with self.assertRaises(AssertionError):
            self.character.set_bleeding(-1)
        self.character.set_bleeding(1)
        self.assertEqual(1, self.character.get_bleeding())

    def test_getter_setter_cpu(self):
        self.assertTrue(self.character.get_cpu())
        self.character.set_cpu(False)
        self.assertFalse(self.character.get_cpu())

    def test_get_attack_points(self):
        # Minimum without pain
        self.character.set_initial_strength(76)
        self.character.set_weapon_stats(1)
        for i in range(1000):
            self.assertTrue(152 <= self.character.get_attack_points() <= 912)

        # Maximum without pain
        self.character.set_initial_strength(124)
        self.character.set_weapon_stats(5)
        for i in range(1000):
            self.assertTrue(620 <= self.character.get_attack_points() <= 7440)

        # With strong pain
        self.character.set_pain(1000)
        for i in range(1000):
            self.assertEqual(0, self.character.get_attack_points())

    def test_get_defense_points(self):
        # Minimum without pain
        self.character.set_initial_speed(76)
        self.character.set_weapon_stats(1)
        self.character.set_shield_usage(False)
        for i in range(1000):
            self.assertTrue(152 <= self.character.get_defense_points() <= 912)

        # Maximum without pain
        self.character.set_initial_speed(124)
        self.character.set_weapon_stats(5)
        self.character.set_shield_usage(True)
        for i in range(1000):
            self.assertTrue(2620 <= self.character.get_defense_points() <= 9440)

        # With strong pain
        self.character.set_pain(1000)
        for i in range(1000):
            self.assertEqual(0, self.character.get_defense_points())

    def test_get_body_part_successful(self):
        for menu_key in fighter.BODY_PART_KEYS:
            body_part: fighter.BodyPart = self.character._get_body_part(identifier=menu_key)
            self.assertEqual(menu_key, body_part.menu_key)
            body_part_name: str = fighter.BODY_PART_KEYS[menu_key]
            body_part: fighter.BodyPart = self.character._get_body_part(identifier=body_part_name)
            self.assertEqual(body_part_name, body_part.name)

    def test_get_body_part_invalid_parameters(self):
        with self.assertRaises(AssertionError):
            self.character._get_body_part(0)
        with self.assertRaises(KeyError):
            self.character._get_body_part(-1)
        with self.assertRaises(KeyError):
            self.character._get_body_part('Invalid body part')

    def test_increase_pain(self):
        with self.assertRaises(AssertionError):
            self.character.increase_pain(-1)
        self.character.increase_pain(lost_health=0)
        self.assertEqual(0, self.character.get_pain())
        self.character.increase_pain(lost_health=1)
        self.assertEqual(0, self.character.get_pain())
        self.character.increase_pain(lost_health=2)
        self.assertEqual(0, self.character.get_pain())
        self.character.increase_pain(lost_health=3)
        self.assertEqual(1, self.character.get_pain())
        self.character.increase_pain(lost_health=4)
        self.assertEqual(2, self.character.get_pain())
        self.character.increase_pain(lost_health=5)
        self.assertEqual(3, self.character.get_pain())
        self.character.increase_pain(lost_health=6)
        self.assertEqual(4, self.character.get_pain())
        self.character.increase_pain(lost_health=7)
        self.assertEqual(5, self.character.get_pain())
        self.character.increase_pain(lost_health=8)
        self.assertEqual(7, self.character.get_pain())
        self.character.increase_pain(lost_health=9)
        self.assertEqual(9, self.character.get_pain())
        self.character.increase_pain(lost_health=10)
        self.assertEqual(11, self.character.get_pain())

    def test_increase_bleeding(self):
        with self.assertRaises(AssertionError):
            self.character.increase_pain(-1)
        for i in range(1000):
            self.character.increase_bleeding(lost_health=0)
        self.assertEqual(0, self.character.get_bleeding())
        for i in range(1000):
            self.character.increase_bleeding(lost_health=1)
        self.assertEqual(0, self.character.get_bleeding())
        for i in range(1000):
            self.character.increase_bleeding(lost_health=10)
        self.assertEqual(0, self.character.get_bleeding())
        while self.character.get_bleeding() == 0:
            self.character.increase_bleeding(lost_health=12)
        self.assertEqual(1, self.character.get_bleeding())
        while self.character.get_bleeding() == 1:
            self.character.increase_bleeding(lost_health=20)
        self.assertEqual(2, self.character.get_bleeding())
        while self.character.get_bleeding() == 2:
            self.character.increase_bleeding(lost_health=28)
        self.assertEqual(3, self.character.get_bleeding())
        while not self.character.get_bleeding() > 3:
            self.character.increase_bleeding(lost_health=30)
        self.assertEqual(5, self.character.get_bleeding())
        while not self.character.get_bleeding() > 5:
            self.character.increase_bleeding(lost_health=40)
        self.assertEqual(7, self.character.get_bleeding())

    def test_decrease_general_health(self):
        with self.assertRaises(AssertionError):
            self.character.decrease_general_health(-1)
        self.character.decrease_general_health(0)
        self.assertEqual(100, self.character.get_general_health())
        self.character.decrease_general_health(1)
        self.assertEqual(99, self.character.get_general_health())
        self.character.decrease_general_health(100)
        self.assertEqual(0, self.character.get_general_health())

    def test_decrease_general_health_from_bleeding(self):
        self.character.decrease_general_health_from_bleeding()
        self.assertEqual(100, self.character.get_general_health())
        self.character.set_bleeding(1)
        self.character.decrease_general_health_from_bleeding()
        self.assertEqual(99, self.character.get_general_health())
        self.character.set_bleeding(100)
        self.character.decrease_general_health_from_bleeding()
        self.assertEqual(0, self.character.get_general_health())

    def test_decrease_body_part_health_invalid_parameters(self):
        with self.assertRaises(AssertionError):
            self.character.decrease_body_part_health(-1, '')
        with self.assertRaises(AssertionError):
            self.character.decrease_body_part_health(-1, fighter.HEAD)
        with self.assertRaises(AssertionError):
            self.character.decrease_body_part_health(0, '')
        with self.assertRaises(KeyError):
            self.character.decrease_body_part_health(100, 'Invalid body part')
        self.assertEqual(100, self.character.get_general_health())  # Still full health - Nothing changed

    def test_decrease_body_part_health_successful(self):
        for body_part in self.character.body_parts.values():
            self.character.decrease_body_part_health(0, body_part.name)
            self.assertEqual(100, self.character.get_body_part_health(body_part.name))
            self.character.decrease_body_part_health(1, body_part.name)
            self.assertEqual(99, self.character.get_body_part_health(body_part.name))
            self.character.decrease_body_part_health(100, body_part.name)
            self.assertEqual(0, self.character.get_body_part_health(body_part.name))

        self.assertEqual(0, self.character.get_general_health())
        self.assertEqual(140, self.character.get_pain())
        self.assertEqual(35, self.character.get_bleeding())

    def test_decrease_body_part_health_from_attack_invalid_parameters(self):
        with self.assertRaises(AssertionError):
            self.character.decrease_body_part_health_from_attack(-1, -1, 0)
        with self.assertRaises(AssertionError):
            self.character.decrease_body_part_health_from_attack(-1, 0, 1)
        with self.assertRaises(AssertionError):
            self.character.decrease_body_part_health_from_attack(0, -1, 1)
        with self.assertRaises(AssertionError):
            self.character.decrease_body_part_health_from_attack(0, 0, 0)

    def test_decrease_body_part_health_from_attack_successful(self):
        max_points = (100 + 6 * 4) * 5 * 12  # 7.440

        for body_part_key in fighter.BODY_PART_KEYS:
            self.setUp()

            self.character.decrease_body_part_health_from_attack(0, 0, body_part_key)  # Attack == Defense
            self.assertEqual(100, self.character.get_body_part_health(body_part_key))
            self.assertEqual(100, self.character.get_general_health())
            self.assertEqual(0, self.character.get_bleeding())
            self.assertEqual(0, self.character.get_pain())

            self.character.decrease_body_part_health_from_attack(max_points, max_points, body_part_key)  # Attack == Defense
            self.assertEqual(100, self.character.get_body_part_health(body_part_key))
            self.assertEqual(100, self.character.get_general_health())
            self.assertEqual(0, self.character.get_bleeding())
            self.assertEqual(0, self.character.get_pain())

            self.character.decrease_body_part_health_from_attack(0, max_points, body_part_key)  # Attack << Defense
            self.assertEqual(100, self.character.get_body_part_health(body_part_key))
            self.assertEqual(100, self.character.get_general_health())
            self.assertEqual(0, self.character.get_bleeding())
            self.assertEqual(0, self.character.get_pain())

            self.character.decrease_body_part_health_from_attack(max_points, 0, body_part_key)  # Attack >> Defense
            self.assertEqual(26, self.character.get_body_part_health(body_part_key))
            self.assertTrue(26 <= self.character.get_general_health() <= 85)
            self.assertTrue(self.character.get_bleeding() > 0)
            self.assertEqual(15, self.character.get_pain())

    def test_generate_parameter_centered_at_100(self):
        for i in range(1000):
            if fighter.Fighter.generate_parameter_centered_at_100() < (100 - 24):
                self.fail("Value is too low")
            if fighter.Fighter.generate_parameter_centered_at_100() > (100 + 24):
                self.fail("Value is too high")

    def tearDown(self):
        self.character = None
