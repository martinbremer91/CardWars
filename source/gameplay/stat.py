class Stat:
    def __init__(self, value):
        self.value = value
        self.modifier = None
    def __str__(self):
        return self.get().__str__()
    def get(self):
        return self.value if not self.modifier else self.modifier.value
    def add_modifier(self, modifier):
        if self.modifier:
            self.modifier.remove_self_from_stat()
        self.modifier = modifier
        modifier.register_deactivation_trigger(self)
    def remove_modifier(self, modifier = None):
        self.modifier = None

class IntStat(Stat):
    def __init__(self, value):
        super().__init__(value)
        self.modifiers = list()
    def get(self):
        sum_of_values = self.value
        for m in self.modifiers:
            sum_of_values += m.value
        return sum_of_values
    def add_modifier(self, modifier):
        self.modifiers.append(modifier)
        modifier.register_deactivation_trigger(self)
    def remove_modifier(self, modifier = None):
        self.modifiers.remove(modifier)

class Modifier:
    def __init__(self, value, deactivation_trigger):
        self.value = value
        self.deactivation_trigger = deactivation_trigger
        self.stat = None

    def register_deactivation_trigger(self, stat):
        self.stat = stat
        self.deactivation_trigger.subscribe(self.remove_self_from_stat)
    def remove_self_from_stat(self):
        self.deactivation_trigger.unsubscribe(self.remove_self_from_stat)
        self.stat.remove_modifier(self)