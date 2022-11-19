import unittest

from combat.combat import Combat
from combat import fighter


class TestCombat(unittest.TestCase):

    def setUp(self):
        self.combat: Combat = Combat()

    def test_initializer(self):
        self.assertEqual("Player1", self.combat.player.get_name())
        self.assertEqual("Enemy", self.combat.enemy.get_name())

        self.assertTrue(76 <= self.combat.player.get_current_strength() <= 124)
        self.assertTrue(76 <= self.combat.enemy.get_current_strength() <= 124)

        self.assertTrue(76 <= self.combat.player.get_current_speed() <= 124)
        self.assertTrue(76 <= self.combat.enemy.get_current_speed() <= 124)

        self.assertTrue(100, self.combat.player.get_general_health())
        self.assertTrue(100, self.combat.enemy.get_general_health())

        for key in fighter.BODY_PART_KEYS:
            self.assertTrue(100, self.combat.player.get_body_part_health(key))
            self.assertTrue(100, self.combat.enemy.get_body_part_health(key))

        self.assertEqual(3, self.combat.player.get_weapon_stats())
        self.assertEqual(3, self.combat.enemy.get_weapon_stats())

        self.assertEqual(0, self.combat.player.get_pain())
        self.assertEqual(0, self.combat.enemy.get_pain())

        self.assertEqual(0, self.combat.player.get_bleeding())
        self.assertEqual(0, self.combat.enemy.get_bleeding())

        self.assertTrue(self.combat.player.get_shield_usage())
        self.assertFalse(self.combat.enemy.get_shield_usage())

        self.assertFalse(self.combat.player.get_cpu())
        self.assertTrue(self.combat.enemy.get_cpu())

        self.assertEqual(0, self.combat.round)

    def test_print_statistics_invalid_parameters(self):
        with self.assertRaises(AssertionError):
            self.combat.print_statistics(None, visual=False)
        with self.assertRaises(AssertionError):
            self.combat.print_statistics(None, visual=True)

    def test_print_statistics_successful(self):
        # Ensure no exception is raised
        self.combat.print_statistics(self.combat.player, visual=False)
        self.combat.print_statistics(self.combat.enemy, visual=False)
        self.combat.print_statistics(self.combat.player, visual=True)
        self.combat.print_statistics(self.combat.enemy, visual=True)

    def test_attack_invalid_parameters(self):
        with self.assertRaises(AssertionError):
            self.combat.attack(None, None, 0)
        with self.assertRaises(AssertionError):
            self.combat.attack(None, self.combat.enemy, 1)
        with self.assertRaises(AssertionError):
            self.combat.attack(self.combat.player, None, 1)
        with self.assertRaises(AssertionError):
            self.combat.attack(self.combat.player, self.combat.enemy, 0)

    def test_attack_successful(self):
        self.combat.player.set_shield_usage(False)  # Ensures both fighters have the same chances of defeating each other

        body_part_key: int = fighter.HEAD  # Has no impact on strength or on speed, so fighters will conserve their fighting capacities after being hit
        for i in range(1000):  # 1000 full rounds
            self.combat.attack(attacker=self.combat.player, defender=self.combat.enemy, body_part_key=body_part_key)
            self.combat.attack(attacker=self.combat.enemy, defender=self.combat.player, body_part_key=body_part_key)

        self.assertEqual(0, self.combat.player.get_general_health())
        self.assertEqual(0, self.combat.enemy.get_general_health())

        self.assertEqual(0, self.combat.player.get_body_part_health(body_part_key))
        self.assertEqual(0, self.combat.enemy.get_body_part_health(body_part_key))

        self.assertTrue(self.combat.player.get_pain() > 0)
        self.assertTrue(self.combat.enemy.get_pain() > 0)

        # Bleeding can remain at 0 even after many rounds as it requires a strong successful attack, so will not be tested

    # Combat loop will not be tested as it involves providing user input, and it is not possible to know a priori
    # how many turns a combat will last. The right number of inputs must be provided, or an exception will be raised.

    def tearDown(self):
        self.combat = None
