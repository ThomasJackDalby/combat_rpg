import math

class Coin:
    def __init__(self, name, metal, coins):
        self.name = name
        self.metal = metal
        self.coins = coins

COINS = [
    Coin("sovereign","gold",(1,0,0)),
    Coin("half sovereign","gold",(0,10,0)),
    Coin("crown","silver",(0,5,0)),
    Coin("half crown","silver",(0,2,6)),
    Coin("florin","silver",(0,2,0)),
    Coin("shilling","silver",(0,1,0)),
    Coin("sixpence","bronze",(0,0,6)),
    Coin("groat","bronze",(0,0,4)),
    Coin("threepence","bronze",(0,0,3)),
    Coin("penny","bronze",(0,0,1)),
]

def get_value(coins):
    return coins[0] * 240 + coins[1] * 12 + coins[2]

def get_coins(value):
    pounds = math.floor(value / 240)
    shillings = math.floor((value - pounds * 240) / 12)
    pence = value - pounds * 240 - shillings * 12
    return (pounds, shillings, pence) 

def format(value):
    if isinstance(value, tuple):
        coins = value
        amount = get_value(value)
    else:
        coins = get_coins(value)
        amount = value
    if amount < 240:
        if coins[2] == 0:
            return f"{coins[1]}/"
        return f"{coins[1]}/{coins[2]}"
    return f"£{coins[0]}-{coins[1]}s-{coins[2]}d"

if __name__ == "__main__":
    import random

    a = (random.randint(0, 5), random.randint(0, 20), random.randint(0, 20))
    b = (random.randint(0, 5), random.randint(0, 20), random.randint(0, 20))
    a = coins(abs(a))
    b = coins(abs(b))
    
    c = coins(abs(a)+abs(b))
    print(format(a),"+",format(b),"=",format(c))

