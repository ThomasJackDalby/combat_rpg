from combat import *
from actions import *
from player import *
from robot import *

print("-= Welcome to Robot Factory v1.0 =-")

player = Player("Tom")
robot = Robot("MK2 IE123")

# battery
battery = ComponentType("Basic Battery")
battery.max_charge = 5
battery.max_health = 10

generator = ComponentType("Small Generator")
generator.max_charge = 0
generator.max_health = 4
generator.actions.append(Charge("Charge", 5))

# laser
laser = ComponentType("Laser")
laser.actions.append(Damage("Fire (Low Power)", 1, 1))
laser.actions.append(Damage("Fire (Med Power)", 2, 3))
laser.actions.append(Damage("Fire (High Power)", 4, 7))
laser.max_health = 5

player.components.append(Component(generator))
player.components.append(Component(laser))
player.components.append(Component(battery))
player.components.append(Component(battery))
player.components.append(Component(battery))

robot.components.append(Component(laser))
robot.components.append(Component(battery))
robot.components.append(Component(battery))
robot.components.append(Component(battery))

print(f"You've encountered a {robot.name}. It want's to fight!")
combat = Combat([player], [robot])
combat.process()