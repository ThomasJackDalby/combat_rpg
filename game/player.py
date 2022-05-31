from game.robot import Robot
import game.currency as currency

class Player(Robot):
    def __init__(self, name):
        Robot.__init__(self, name)
        self.money = currency.get_value((5, 0, 0))