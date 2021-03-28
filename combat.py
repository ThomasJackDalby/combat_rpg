from actions import *
from player import *
from robot import *
from colorama import Fore
from colorama import Style

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
            
                print(f" --- {current.robot.name} ---")
                print(f"HP:{current.robot.get_health()}/{current.robot.get_max_health()} CRG:{current.robot.get_charge()}/{current.robot.get_max_charge()}")

                current.next_time += current.cooldown

                action = current.get_action()
                if action is None:
                    print(f"{current.robot.name} did nothing.")
                    continue
                print(f"{current.robot.name} chose [{action.name}]")
                
                other = next((c for c in self.combatants if c is not current), None)
                action.process(current, other)

                for combatant in self.combatants:
                    for component in combatant.robot.components:
                        if not component.disabled and component.health <= 0:
                            print(f"{Fore.RED}{component.name} was disabled.{Style.RESET_ALL}")
                            component.disabled = True
                    if all(c.disabled for c in combatant.robot.components):
                        combatant.disabled = True
                        print(f"{combatant.robot.name} has been disabled.")
                
                if all(c.disabled for c in self.team_a) or all(c.disabled for c in self.team_b):
                    return

class CombatWrapper:
    def __init__(self, robot):  
        self.robot = robot
        self.disabled = False
        self.next_time = 0

class PlayerCombatWrapper(CombatWrapper):
    def __init__(self, player):
        CombatWrapper.__init__(self, player)
        self.cooldown = 5

    def get_action(self):
        actions = [(component, action) for component in self.robot.components for action in component.actions]
        valid_actions = []
        i = 0
        for component, action in actions:
            if component.disabled:
                print(f"{Fore.RED}[-] {component.name}: {action.name} [Destroyed]{Style.RESET_ALL}")
            elif self.robot.get_charge() < action.get_required_charge():
                print(f"{Fore.YELLOW}[-] {component.name}: {action.name} [Low Charge]{Style.RESET_ALL}")
            else:
                print(f"[{i}] {component.name}: {action.name}")
                i += 1
                valid_actions.append(action)

        if len(valid_actions) == 0:
            print("No actions currently available...")
            return Charge("Passive Charge", 1)

        a = -1
        while a < 0 or a >= len(valid_actions):
            a = int(input("Select action: "))
        return valid_actions[a]

class RobotCombatWrapper(CombatWrapper):
    def __init__(self, robot):
        CombatWrapper.__init__(self, robot)
        self.cooldown = 7

    def get_action(self):
        actions = self.robot.get_actions()
        if len(actions) > 0:
            return random.choice(actions)
        return Charge("Passive Charge", 1)