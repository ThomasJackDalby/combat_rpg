
DEFENCES = [(None, 0, 0), ("lightly armoured", 2, 1), ("heavily armoured", 5, 2)]

def generate_batterys():
    # size, max_charge, size_mass
    battery_sizes = [("small", 4, 1), ("medium", 7, 2), ("large", 15, 3)]
    batterys = []
    for size, max_charge, size_mass in battery_sizes:
        for defence_type, defence, defence_mass in DEFENCES:
            battery = ComponentType("Battery", get_name([size, defence_type, "battery"]))
            battery.max_charge = max_charge
            battery.defence = defence
            battery.mass = size_mass + defence_mass
            batterys.append(battery)
    return batterys

def generate_generators():
    generator_types = ["coal", "electric", "alchemic", "thermal"]
    generator_sizes = [("small", 4, 20, 1), ("medium", 7, 30, 2), ("large", 15, 45, 3)]
    generators = []
    for generator_type in generator_types:
        for size, passive_charge, active_charge, mass in generator_sizes:
            for defence_type, defence, defence_mass in DEFENCES:
                generator = ComponentType("Generator", get_name([size, defence_type, generator_type, "generator"]))               
                generator.defence = defence
                generator.mass = size_mass + defence_mass
                generator.active_actions.append(Action(  ))
                generators.append(generator)
    return generator
    
def generate_boilers():
    boiler_types = ["coal", "electric", "alchemic", "thermal"]
    boiler_sizes = [("small", 4, 1), ("medium", 7, 2), ("large", 15, 3)]
    boilers = []
    for boiler_type in boiler_types:
        for size, pressure, mass in boiler_sizes:
            for defence_type, defence, defence_mass in DEFENCES:
                boiler = ComponentType("Boiler", get_name([size, defence_type, boiler_type, "boiler"]))
                boiler.pressure = pressure
                boiler.defence = defence
                boiler.mass = size_mass + defence_mass
                boilers.append(boiler)
    return boilers

def get_name(sections):
    name = " ".join((section for section in sections if section is not None))
    return name.title()

if __name__ == "__main__":
    component_types = generate_component_types()
    print(tabulate([[c.component_type, c.name, c.mass, c.speed, c.defence, c.max_charge, c.pressure] for c in component_types], headers=["Type", "Name", "MSS", "SPD", "DEF", "CRG", "PRS"]))
