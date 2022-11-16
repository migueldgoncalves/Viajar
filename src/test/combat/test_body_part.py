import unittest

from combat.fighter import BodyPart


class TestBodyPart(unittest.TestCase):

    def test_initialize_all_parameters_invalid(self):
        with self.assertRaises(AssertionError):
            BodyPart('', 0, 0, 0.0, 0)

    def test_initialize_invalid_name(self):
        with self.assertRaises(AssertionError):
            BodyPart('', 1, 100, 0.5, 500)

    def test_initialize_invalid_menu_key(self):
        with self.assertRaises(AssertionError):
            BodyPart('Fighter', 0, 100, 0.5, 500)
        with self.assertRaises(AssertionError):
            BodyPart('Fighter', -1, 100, 0.5, 500)

    def test_initialize_invalid_starting_health(self):
        with self.assertRaises(AssertionError):
            BodyPart('Fighter', 1, 0, 0.5, 500)
        with self.assertRaises(AssertionError):
            BodyPart('Fighter', 1, -1, 0.5, 500)

    def test_initialize_invalid_impact_in_general_health(self):
        with self.assertRaises(AssertionError):
            BodyPart('Fighter', 1, 100, -0.1, 500)
        with self.assertRaises(AssertionError):
            BodyPart('Fighter', 1, 100, 1.1, 500)

    def test_initialize_invalid_defense_bonus(self):
        with self.assertRaises(AssertionError):
            BodyPart('Fighter', 1, 100, 0.5, -1)

    def test_initialize_successful(self):
        body_part = BodyPart('Fighter', 1, 100, 0.5, 500)
        self.assertEqual('Fighter', body_part.name)
        self.assertEqual(1, body_part.menu_key)
        self.assertEqual(100, body_part.starting_health)
        self.assertEqual(100, body_part.health)
        self.assertEqual(0.5, body_part.impact_in_general_health)
        self.assertEqual(500, body_part.defense_bonus)
