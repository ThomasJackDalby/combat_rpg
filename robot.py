import math

class Robot:
    
    def __init__(self, name):
        self.name = name
        self.components = []
        self.speed = 1

    def get_health(self):
        return sum((component.health for component in self.components))

    def get_max_health(self):
        return sum((component.max_health for component in self.components))

    def get_charge(self):
        return sum((component.charge for component in self.components if not component.disabled))

    def get_max_charge(self):
        return sum((component.max_charge for component in self.components if not component.disabled))

    def modify_charge(self, amount):
        delta = int(math.copysign(1, amount))
        while amount != 0:
            if delta > 0:
                component = next(iter(sorted((c for c in self.components if c.charge < c.max_charge), key=lambda c: c.charge)), None)
            else:  
                component = next(iter(sorted((c for c in self.components if c.charge > 0), key=lambda c: c.charge, reverse=True)), None)
            if component is None:
                return
            component.charge += delta
            amount -= delta

    def get_actions(self):
        return [action for component in self.components for action in component.actions]

class ComponentType:
    def __init__(self, name):
        self.name = name
        self.max_health = 0
        self.max_charge = 0
        self.actions = []

class Component:
    def __init__(self, component_type):
        if not isinstance(component_type, ComponentType):
            raise Exception()

        self.component_type = component_type

        self.name = component_type.name
        self.max_health = component_type.max_health
        self.max_charge = component_type.max_charge
        self.actions = list(component_type.actions)

        self.health = self.max_health
        self.charge = self.max_charge
        self.disabled = False if self.health > 0 else True

if __name__ == "__main__":
    robot = Robot("Test")
    robot.components.append(Component("A"))
    robot.components.append(Component("B"))
    robot.components.append(Component("C"))

    print("   "," ".join((f"{c.charge:2}/{c.max_charge:2}" for c in robot.components)))

    changes = [-6, 4, -1, -7, -4]
    for change in changes:
        robot.modify_charge(change)
        print(f"{change:3}", " ".join((f"{c.charge:2}/{c.max_charge:2}" for c in robot.components)), robot.get_charge())