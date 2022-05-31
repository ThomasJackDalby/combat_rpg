import game.currency as currency
from game.items import Item
from colorama import Fore

class Shop:

    def __init__(self):
        self.items = {}

    def buy(self, item, player):
        if item not in self.items:
            print("not for sale")
            return
        
        cost = self.items[item]
        if player.money < cost:
            print("not enough money") 
            return

        player.money -= cost
        player.items.append(item)
        del shop.items[item]

    def display(self):
        pass        

class Player:
    def __init__(self):
        self.money = 100
        self.items = []

if __name__ == "__main__":
    shop = Shop()
    shop.items[Item("Sword")] = currency.get_value((0, 15, 6))
    shop.items[Item("Electric Sword")] = currency.get_value((1, 2, 5))
    shop.items[Item("Coal")] = currency.get_value((0, 1, 0))
    shop.items[Item("Water")] = currency.get_value((0, 0, 2))

    player = Player()

    print("Welcome to the Shop :)")

    from tools import display_options

    is_valid = lambda item: None if player.money > shop.items[item] else ("Insufficient Funds", Fore.YELLOW)
    format_options = lambda item: [item.name, currency.format(shop.items[item])]
    display_options(shop.items, format_options, is_valid)
    exit()