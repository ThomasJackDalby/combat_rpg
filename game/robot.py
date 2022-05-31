import math, random
from game.components import Component, COMPONENT_TYPES

class Robot:
    
    def __init__(self, name):
        self.name = name
        self.components = []
        self.inventory = {}
        self.speed = 1
        self.disabled = False

    def get_health(self):
        return sum((component.health for component in self.components))

    def get_max_health(self):
        return sum((component.max_health for component in self.components))

    def get_charge(self):
        return sum((component.charge for component in self.components if not component.disabled))

    def get_max_charge(self):
        return sum((component.max_charge for component in self.components if not component.disabled))
    
    def get_pressure(self):
        return sum((component.pressure for component in self.components if not component.disabled))

    def get_water(self):
        return sum((component.water for component in self.components if not component.disabled))

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

def build_robot():
    robot = Robot(f"MK {random.randint(0, 999):000}")
    number_of_components = random.randint(2, 5)
    for i in range(number_of_components):
        component = COMPONENT_TYPES[random.randint(0, len(COMPONENT_TYPES)-1)]
        robot.components.append(Component(component))
    return robot