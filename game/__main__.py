from tabulate import tabulate
from game.player import Player
from game.robot import build_robot
from game.combat import Combat
from game.components import COMPONENT_TYPES, Component
from game.items import Item
from game.shop import Shop
from game.tools import display_options
import game.currency as currency

print("-= Welcome to Robot Factory v1.0 =-")
print("")
print("What is your name?")
name = input("> ")
player = Player(name)

print(f"Welcome {name} to the Robot Factory.")

# shop = Shop()
# shop.items[Item("Sword")] = currency.get_value((0, 15, 6))
# shop.items[Item("Electric Sword")] = currency.get_value((1, 2, 5))
# shop.items[Item("Coal")] = currency.get_value((0, 1, 0))
# shop.items[Item("Water")] = currency.get_value((0, 0, 2))

# while True:
#     print("Select action:")
#     option = display_options(["combat", "items", "shop", "save"], lambda x: [x])
#     print(f"You chose {option}")

#     if option == "combat":
#         print(f"You've encountered a mob of robots! They want to fight!")
#         combat = Combat([player], [build_robot(), build_robot()])
#         combat.process()
#     elif option == "shop":
#         is_valid = lambda item: None if player.money > shop.items[item] else ("Insufficient Funds", Fore.YELLOW)
#         format_options = lambda item: [item.name, currency.format(shop.items[item])]
#         shop_choice = display_options(shop.items, format_options, is_valid)
#         if shop_choice == None:
#             continue
#         else:
#             print(f"You bought this thing! {shop_choice}")

print("Select your components:")
print(tabulate([[i, c.component_type, c.name, c.mass, c.speed, c.defence, c.max_charge, c.pressure] for (i, c) in enumerate(COMPONENT_TYPES)], headers=["ID", "Type", "Name", "MSS", "SPD", "DEF", "CRG", "PRS"]))
while True:
    index = input("> ")
    if index is None or index == "":
        break
    component_type = COMPONENT_TYPES[int(index)]
    print(f"Equipping {component_type.name} to robot.")
    player.components.append(Component(component_type))
print("Done.")

combat = Combat([player], [build_robot(), build_robot()])
combat.process()