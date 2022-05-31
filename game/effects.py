from colorama import Fore, Style
import inspect, sys

class Effect:
    def __init__(self):
        pass

class ElectricAttack(Effect):
    key = "electric_attack"
    num_args = 2
    
    def __init__(self, args):
        self.attack = int(args[0])
        self.required_charge = int(args[1])

    def invoke(self, source, sources, targets):
        target, target_component = select_target_component(source, targets)
        if target is None or target_component is None:
            return
        
        if source.robot.get_charge() < self.required_charge:
            return
        
        print(f"{source.robot.name} attacked {target.robot.name}'s {target_component.name}")
        source.robot.modify_charge(-self.required_charge)
        direct_attack(target, target_component, self.attack)
    
    def format(self):
        return f"{self.name} {key}" 

class SteamAttack(Effect):
    key = "steam_attack"
    num_args = 2

    def __init__(self, args):
        self.attack = int(args[0])
        self.required_pressure = int(args[1])

    def invoke(self, source, sources, targets):
        target, target_component = select_target_component(source, targets)
        if target is None or target_component is None:
            return
        
        if source.robot.get_pressure() < self.required_pressure:
            return
        
        print(f"{source.robot.name} attacked {target.robot.name}'s {target_component.name}")
        direct_attack(target, target_component, self.attack)

class Attack(Effect):
    key = "attack"
    num_args = 1

    def __init__(self, args):
        self.attack = int(args[0])

    def invoke(self, source, sources, targets):
        target, target_component = select_target_component(source, targets)
        if target is None or target_component is None:
            return

        print(f"{source.robot.name} attacked {target.robot.name}'s {target_component.name}")
        direct_attack(target, target_component, self.attack)

class ModifyCharge(Effect):
    key = "modify_charge"
    num_args = 1

    def __init__(self, args):
        self.amount = int(args[0]) 

    def invoke(self, source, sources, targets):
        start_charge = source.robot.get_charge()
        source.robot.modify_charge(self.amount)
        charge_amount = source.robot.get_charge() - start_charge
        print(f"{source.robot.name} gained {charge_amount} CHG ({source.robot.get_charge()}/{source.robot.get_max_charge()} CRG)")

class ModifyPressure(Effect):
    key = "modify_pressure"
    num_args = 1

    def __init__(self, args):
        self.amount = int(args[0]) 

    def invoke(self, source, sources, targets):
        start_charge = source.robot.get_charge()
        source.robot.modify_charge(self.amount)
        charge_amount = source.robot.get_charge() - start_charge
        print(f"{source.robot.name} gained {charge_amount} CHG ({source.robot.get_charge()}/{source.robot.get_max_charge()} CRG)")

# helper functions
def select_target_component(source, targets):
    target = source.get_combatant(targets)
    if target is None:
        print("No target selected.")
        return None, None
        
    target_component = source.get_component(target)
    if target_component is None:
        print("No component selected.")
        return target, None
        
    return target, target_component

def direct_attack(target, target_component, attack):
    start_health = target_component.health
    damage = attack - target_component.defence
    if damage < 0:
        print("No damage was dealt.")
        return        
    target_component.health -= damage
    if target_component.health < 0:
        target_component.health = 0
    health_amount = target_component.health - start_health
    print(f"{Fore.RED}{target.robot.name} took {-health_amount} DMG to its {target_component.name} ({target_component.health}/{target_component.max_health} HP){Style.RESET_ALL}")

EFFECTS = {object_type.__dict__["key"] : object_type for object_type_name, object_type in inspect.getmembers(sys.modules[__name__], inspect.isclass) if object_type_name != "Effect" and issubclass(object_type, Effect) }

if __name__ == "__main__":
    print("Effects:")
    for effect in EFFECTS:
        print(f"- {effect}")