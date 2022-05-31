import inspect, sys

class Constraint:
    def __init__(self):
        pass

class MinimumCharge(Constraint):
    key = "minimum_charge"
    num_args = 1

    def __init__(self, args):
        Constraint.__init__(self)
        self.amount = int(args[0]) 

    def invoke(self, source, sources, targets):
        return None if source.robot.get_charge() > self.amount else f"Low Charge (<{self.amount} CHG)"


CONSTRAINTS = {object_type.__dict__["key"] : object_type for object_type_name, object_type in inspect.getmembers(sys.modules[__name__], inspect.isclass) if object_type_name != "Constraint" and issubclass(object_type, Constraint) }

if __name__ == "__main__":
    print("Contraints:")
    for constraint in CONSTRAINTS:
        print(f"- {constraint}")