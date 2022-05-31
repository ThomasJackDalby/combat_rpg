from tabulate import tabulate

class ComponentType:
    def __init__(self, component_type, name=""):
        self.component_type = component_type
        self.name = name
        self.defence = 0
        self.mass = 0
        self.max_health = 0
        self.max_charge = 0
        self.pressure = 0
        self.speed = 0
        self.active_actions = []
        self.passive_actions = []

class Component:
    def __init__(self, component_type):
        if not isinstance(component_type, ComponentType):
            raise Exception()

        self.component_type = component_type

        self.name = component_type.name
        self.pressure = component_type.pressure
        self.defence = component_type.defence
        self.speed = component_type.speed
        self.max_health = component_type.max_health
        self.max_charge = component_type.max_charge
        self.active_actions = list(component_type.active_actions)
        self.passive_actions = list(component_type.passive_actions)

        self.health = self.max_health
        self.charge = self.max_charge
        self.disabled = False
        self.destroyed = False

LOAD_TYPE = 0
LOAD_NAME = 1
LOAD_ATTRIBUTES = 2
LOAD_ACTIONS = 3

def load_component_types(file_path):
    from game.actions import Action
    from game.effects import EFFECTS
    from game.constraints import CONSTRAINTS

    with open(file_path, "r") as file:
        lines = [line.strip() for line in file.readlines()]

    component_type_name = None
    component_type = None
    component_types = []
    state = LOAD_TYPE
    for line in lines:
        if state == LOAD_TYPE:
            component_type_name = line.strip().upper()
            state = LOAD_NAME
        elif state == LOAD_NAME:
            component_type = ComponentType(component_type_name, line.title())
            state = LOAD_ATTRIBUTES
        elif state == LOAD_ATTRIBUTES:
            values = [int(bit.strip()) for bit in line.split(" ")]
            component_type.max_health = values[0]
            component_type.defence = values[1]
            component_type.max_charge = values[2]
            component_type.pressure = values[3]
            state = LOAD_ACTIONS
        elif state == LOAD_ACTIONS:
            if not line:
                component_types.append(component_type)
                component_type = None
                component_type_name = None
                state = LOAD_TYPE
            else:
                data = line.split(" ")
                action_type = data[0]
                action_name = data[1]
                action = Action(action_name)
                
                data = data[2:]

                effect_type_name = data[0]
                effect_type = EFFECTS[effect_type_name]
                effect = effect_type(data[1:1+effect_type.num_args])
                action.effect = effect

                data = data[1+effect_type.num_args:]
                while len(data) > 0:
                    constraint_type_name = data[0]
                    constraint_type = CONSTRAINTS[constraint_type_name]
                    constraint = constraint_type(data[1:1+constraint_type.num_args])
                    action.constraints.append(constraint)
                    data = data[1+constraint_type.num_args:]

                if action_type == "A":
                    component_type.active_actions.append(action)
                elif action_type == "P":
                    component_type.passive_actions.append(action)

    return component_types

def save_component_types(file_path, component_types):
    lines = []

    for ct in component_types:
        lines.append(f"{ct.role}")
        lines.append(f"{ct.name}")
        lines.append(f"{ct.max_health} {ct.defence} {ct.max_charge} {ct.pressure}")
        for action in ct.active_actions:
            lines.append(f"A {action.format()}")
        for action in ct.passive_actions:
            lines.append(f"P {action.format()}")

def parse(target_type, text_input):
    if target_type is int:
        return int(text_input)
    raise Exception()

COMPONENT_TYPES = load_component_types("data/component_types.txt")


