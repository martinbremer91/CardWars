class Condition:
    def __init__(self, param_a, condition_type, param_b):
        self.param_a = param_a
        self.param_b = param_b
        self.condition_type = condition_type

    def resolve(self, entity):
        ...

class Property:
    ...