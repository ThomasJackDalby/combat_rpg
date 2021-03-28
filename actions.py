import random

class Action:
    def get_required_charge(self):
        pass

    def get_description(self):
        pass

    def process(self, source, target):
        pass

class Damage(Action):
    def __init__(self, name, damage, required_charge):
        self.name = name
        self.damage = damage
        self.required_charge = required_charge

    def get_required_charge(self):
        return self.required_charge

    def process(self, source, target):
        target_component = None
        target_components = list(c for c in target.robot.components if not c.disabled)
        if len(target_components) > 0:
            target_component = random.choice(target_components)
        if target_component is None:
            print("Nothing to fire at..")
            return

        source.robot.modify_charge(-self.required_charge)
        start_health = target_component.health
        target_component.health -= self.damage
        if target_component.health < 0:
            target_component.health = 0
        health_amount = target_component.health - start_health
        print(f"{target.robot.name} took {-health_amount} DMG to its {target_component.name} ({target_component.health}/{target_component.max_health} HP)")


class Heal(Action):
    def __init__(self, amount):
        self.amount = amount

    def get_description(self):
        return f"Heal (+{self.amount} HP)"

    def process(self, source, target):
        start_health = source.robot.health
        source.robot.health += self.amount
        if source.robot.health > source.robot.max_health:
            source.robot.health = source.robot.max_health
        health_amount = source.robot.health - start_health
        print(f"{source.robot.name} healed {health_amount} to {source.robot.health} HP")

class Charge(Action):
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def get_required_charge(self):
        return 0

    def get_description(self):
        return f"Charge (+{self.amount} CRG)"

    def process(self, source, target):
        start_charge = source.robot.get_charge()
        source.robot.modify_charge(self.amount)
        charge_amount = source.robot.get_charge() - start_charge
        print(f"{source.robot.name} charged {charge_amount} to {source.robot.get_charge()} CRG")