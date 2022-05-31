import random
from colorama import Fore, Style
from game.player import Player
from game.robot import Robot

class Combat:

    def __init__(self, team_a, team_b):
        
        def get_combat_wrapper(robot):
            if isinstance(robot, Player):
                return PlayerCombatWrapper(robot)
            return RobotCombatWrapper(robot)
            raise Exception(f"Unknown type [{robot}]")
        
        self.team_a = [get_combat_wrapper(robot) for robot in team_a]
        self.team_b = [get_combat_wrapper(robot) for robot in team_b]
        self.combatants = self.team_a + self.team_b

        print("-- Allies --")
        for combatant in self.team_a:
            print(f"{combatant.robot.name}")
            for component in combatant.robot.components:
                print(f"> {component.name}")
        print("-- Enemies --")
        for combatant in self.team_b:
            print(f"{combatant.robot.name}")
            for component in combatant.robot.components:
                print(f"> {component.name}")

    def process(self):
        print(f"{', '.join((c.robot.name for c in self.team_a))} vs {(', '.join((c.robot.name for c in self.team_b)))}")
        time = -1
        while True:
            time += 1

            players_left = True
            while players_left:
                current = next((c for c in self.combatants if c.next_time == time), None)
                if current is None:
                    players_left = False
                    break
            
                print()
                print(f" --- {current.robot.name} ---")
                display_stats(current.robot)

                current.next_time += current.cooldown
                current_team = self.team_a if current in self.team_a else self.team_b
                other_team = self.team_a if current_team is self.team_b else self.team_b

                # active action
                active_action = current.get_active_action(current_team, other_team)
                if active_action is None:
                    print(f"{current.robot.name} did nothing.")
                else:
                    constraint_reason = active_action.check_constraints(current, current_team, other_team)
                    if constraint_reason is not None:
                        print(f"{Fore.YELLOW}{active_action.name} failed due to [{constraint_reason}]{Style.RESET_ALL}")
                    else:
                        active_action.effect.invoke(current, current_team, other_team)
                        self.process_action_effects()
                        if self.check_combat_over():
                            return
                for passive_action in (action for component in current.robot.components for action in component.passive_actions): # order these?
                    passive_constraint = passive_action.check_constraints(current, current_team, other_team)
                    if passive_constraint is not None:
                        print(f"{Fore.YELLOW}{passive_action.name} failed due to [{passive_constraint}]{Style.RESET_ALL}")
                    else:
                        passive_action.effect.invoke(current, current_team, other_team)
                        self.process_action_effects()
                        if self.check_combat_over():
                            return

    def process_action_effects(self):
        for combatant in self.combatants:
                for component in combatant.robot.components:
                    if not component.disabled and component.health <= 0:
                        print(f"{Fore.RED}{combatant.robot.name}'s {component.name} was disabled.{Style.RESET_ALL}")
                        component.disabled = True
                if all(c.disabled for c in combatant.robot.components):
                    combatant.disabled = True
                    print(f"{Fore.RED}{combatant.robot.name} has been disabled.{Style.RESET_ALL}")

    def check_combat_over(self):
        return all(c.disabled for c in self.team_a) or all(c.disabled for c in self.team_b)

def display_stats(robot):
    hp = f"HP:{robot.get_health()}/{robot.get_max_health()}"
    charge = f"CHG:{robot.get_charge()}/{robot.get_max_charge()}"
    pressure = f"PRS:{robot.get_pressure()}"
    print(" ".join([hp, charge, pressure]))

class CombatWrapper:
    def __init__(self, robot):  
        self.robot = robot
        self.disabled = False
        self.next_time = 0

class PlayerCombatWrapper(CombatWrapper):
    def __init__(self, player):
        CombatWrapper.__init__(self, player)
        self.cooldown = 5

    def get_active_action(self, sources, targets):
        actions = [(component, action) for component in self.robot.components for action in component.active_actions]
        valid_actions = []
        i = 0
        print("Select action:")
        for component, action in actions:
            if component.disabled:
                print(f"{Fore.RED}[-] {component.name}: {action.name} [Destroyed]{Style.RESET_ALL}")
            else:
                constraint_reason = action.check_constraints(self, sources, targets)
                if constraint_reason is not None:
                    print(f"{Fore.YELLOW}[-] {component.name}: {action.name} [{constraint_reason}]{Style.RESET_ALL}")
                else:
                    print(f"[{i}] {component.name}: {action.name}")
                    i += 1
                    valid_actions.append(action)

        if len(valid_actions) == 0:
            input("No actions available...")
            return None

        i = -1
        while i < 0 or i >= len(valid_actions):
            i = int(input("> "))
        return valid_actions[i]

    def get_combatant(self, combatants):
        i = 0
        valid_combatants = []
        print("Select robot:")
        for combatant in combatants:
            if combatant.robot.disabled:
                print(f"{Fore.RED}[-] {combatant.robot.name} [Destroyed]{Style.RESET_ALL}")
            else:
                print(f"[{i}] {combatant.robot.name}")
                i += 1
                valid_combatants.append(combatant)
        
        if len(valid_combatants) == 1:
            return valid_combatants[0]

        if len(valid_combatants) == 0:
            print("No robots available...")
            return None

        i = -1
        while i < 0 or i >= len(valid_combatants):
            i = int(input("> "))
        return valid_combatants[i]

    def get_component(self, target):
        i = 0
        valid_components = []
        print("Select component:")
        for component in target.robot.components:
            if component.disabled:
                print(f"{Fore.RED}[-] {component.name} [Destroyed]{Style.RESET_ALL}")
            else:
                print(f"[{i}] {component.name}")
                i += 1
                valid_components.append(component)
        
        if len(valid_components) == 1:
            return valid_components[0]

        if len(valid_components) == 0:
            print("No components available...")
            return None

        i = -1
        while i < 0 or i >= len(valid_components):
            i = int(input("> "))
        return valid_components[i]

class RobotCombatWrapper(CombatWrapper):
    def __init__(self, robot):
        CombatWrapper.__init__(self, robot)
        self.cooldown = 7

    def get_active_action(self, sources, targets):
        actions = [action for component in self.robot.components for action in component.active_actions]
        if len(actions) > 0:
            return random.choice(actions)
        return None

    def get_combatant(self, combatants):
        if len(combatants) > 0:
            return random.choice(combatants)
        return None

    def get_component(self, target):
        target_components = [component for component in target.robot.components if not component.disabled]
        if len(target_components) > 0:
            return random.choice(target_components)
        return None