import random
from colorama import Fore, Style

class Action:
    def __init__(self, name):
        self.name = name
        self.constraints = []
        self.effect = None
    
    def check_constraints(self, source, sources, targets):
        for constraint in self.constraints:
            constraint_result = constraint.invoke(source, sources, targets)
            if constraint_result is not None:
                return constraint_result
        return None


