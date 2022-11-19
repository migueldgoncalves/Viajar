from combat import fighter, random
from travel.main import menu


class Combat:
    """
    Upper-level class of the Combat package, representing a successive set of rounds where in each round
        each fighter alternates between attacking and defending
    """
    def __init__(self):
        self.player: fighter.Fighter = fighter.Fighter(name="Player1", strength=0, speed=0, weapon_stats=3, shield=True, cpu=False)
        self.enemy: fighter.Fighter = fighter.Fighter(name="Enemy", strength=0, speed=0, weapon_stats=3, shield=False, cpu=True)

        self.round: int = 0

    #  #  #  #  #  #
    #  Exit routine  #
    #  #  #  #  #  #

    @staticmethod
    def exit():
        print("")
        print("You have chosen to leave the combat")
        print("See you next time")
        exit(0)

    #  #  #  #  #  #  #  #
    #  Auxiliary methods  #
    #  #  #  #  #  #  #  #

    @staticmethod
    def print_statistics(character: fighter.Fighter, visual: bool = False) -> None:
        """
        Prints fighter statistics
        :param character: The fighter whose statistics are to be printed
        :param visual: If True, a more visual summary is printed. If False, a more textual and compact summary is printed
        """
        assert character

        if not character.get_cpu():
            print("Your stats:")
        else:
            print("Your enemy stats:")

        if visual:  # Replace numbers with bars - Fills more lines in the console
            print(f'General health: {"*" * character.get_general_health()}')
            for body_part in fighter.BODY_PART_KEYS.values():
                print(f'{body_part} health: {"*" * character.get_body_part_health(body_part)}')
            print(f'Strength: {"*" * character.get_current_strength()}')
            print(f'Speed: {"*" * character.get_current_speed()}')
            print(f'Pain: {"*" * character.get_pain()}')
            print(f'Bleeding: {"*" * character.get_bleeding()}')
        else:  # Use numbers instead of bars - Fills fewer lines in the console
            print(f"General health: {character.get_general_health()}; "
                  f"{fighter.HEAD}: {character.get_body_part_health(fighter.HEAD)}; "
                  f"{fighter.CHEST}: {character.get_body_part_health(fighter.CHEST)}; "
                  f"{fighter.BELLY}: {character.get_body_part_health(fighter.BELLY)}; "
                  f"{fighter.DOMINANT_ARM}: {character.get_body_part_health(fighter.DOMINANT_ARM)}; "
                  f"{fighter.NON_DOMINANT_ARM}: {character.get_body_part_health(fighter.NON_DOMINANT_ARM)}; "
                  f"{fighter.LEFT_LEG}: {character.get_body_part_health(fighter.LEFT_LEG)}; "
                  f"{fighter.RIGHT_LEG}: {character.get_body_part_health(fighter.RIGHT_LEG)}; "
                  f"Strength: {character.get_current_strength()}; "
                  f"Speed: {character.get_current_speed()}; "
                  f"Pain: {character.get_pain()}; "
                  f"Bleeding: {character.get_bleeding()}")
        print("")

    @staticmethod
    def attack(attacker: fighter.Fighter, defender: fighter.Fighter, body_part_key: int) -> None:
        """
        Routine representing an attack within a round
        :param attacker: Fighter attacking
        :param defender: Fighter defending
        :param body_part_key: Menu key pointing at the body part to attack
        """
        assert attacker
        assert defender
        assert attacker.get_name() != defender.get_name()  # A fighter is not supposed to attack themselves!
        assert body_part_key

        if not attacker.get_cpu():  # User is attacking
            print("")
            print("Your attack:")
        else:  # CPU is attacking
            print("The attack of your enemy:")
        attack_points: int = attacker.get_attack_points()

        if not defender.get_cpu():  # User is defending
            print("Your defense:")
        else:  # CPU is defending
            print("The defense of your enemy:")
        defense_points: int = defender.get_defense_points()

        if attack_points > defense_points:
            defender.decrease_body_part_health_from_attack(attack_points, defense_points, body_part_key)
            print("")
            if not attacker.get_cpu():  # User attacked the CPU with success
                print("You have attacked your enemy")
            else:  # CPU attacked the user with success
                print("Your enemy has attacked you")
            print("")
        else:
            if not defender.get_cpu():  # User defended the CPU attack
                print("You have defended the attack of your enemy")
            else:  # CPU defended the user attack
                print("Your enemy has defended your attack")
            print("")

    #  #  #  #  #  #
    #  Main routine  #
    #  #  #  #  #  #

    def combat_loop(self) -> None:
        """
        Main routine - Will loop round after round until either one of the fighters wins or the user exits
        """
        # Introduction
        print("")
        print("Welcome to the combat")
        print(f"Your character has {self.player.get_current_strength()} strength points and {self.player.get_current_speed()} speed points")
        print(f"Your enemy has {self.enemy.get_current_strength()} strength points and {self.enemy.get_current_speed()} speed points")

        # Main loop
        while True:
            self.round += 1
            print("")
            print(f"ROUND {self.round}")
            print("")

            self.print_statistics(self.player)
            self.print_statistics(self.enemy)

            # Menu presentation - Returns user input, always a valid option
            option: int = menu.present_numeric_menu(
                option_labels=list(fighter.BODY_PART_KEYS.values()),
                menu_introduction=['Select the enemy body part to attack'],
                exit_routine=Combat.exit
            )

            # Attacks
            self.attack(attacker=self.player, defender=self.enemy, body_part_key=option)  # User attacks - Is always first
            if self.enemy.get_general_health() <= 0:
                print("You have killed your enemy - You won")
                exit(0)
            self.attack(attacker=self.enemy, defender=self.player, body_part_key=random.Random.get_random_int(7))  # Enemy attacks - Is always last
            if self.player.get_general_health() <= 0:
                print("You died")
                exit(0)

            # Health loss due to bleeding
            self.player.decrease_general_health_from_bleeding()
            if self.player.get_general_health() <= 0:
                print("You bled to death")
                exit(0)
            self.enemy.decrease_general_health_from_bleeding()
            if self.enemy.get_general_health() <= 0:
                print("Your enemy bled to death - You won")
                exit(0)
