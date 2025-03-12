class Stat:
    def __init__(self, value):
        self._value = value
        self.modifier = None
    def __str__(self):
        return self.value.__str__()
    def __int__(self):
        return int(self.value)
    def __eq__(self, other):
        return int(self.value) == int(other)
    def __lt__(self, other):
        return int(self.value) < int(other)
    def __le__(self, other):
        return int(self.value) <= int(other)
    def __gt__(self, other):
        return int(self.value) > int(other)
    def __ge__(self, other):
        return int(self.value) >= int(other)
    def __add__(self, other):
        return int(self.value) + int(other)
    def __sub__(self, other):
        return int(self.value) - int(other)
    @property
    def value(self):
        return self._value if not self.modifier else self.modifier.value
    def add_modifier(self, value, deactivation_trigger):
        if self.modifier:
            self.modifier.remove_self_from_stat()
        if self._value != value:
            self.modifier = Modifier(value, deactivation_trigger)
            self.modifier.register_deactivation_trigger(self)

class IntStat(Stat):
    def __init__(self, value):
        super().__init__(value)
        self.modifiers = list()
    @property
    def value(self):
        sum_of_values = self._value
        for m in self.modifiers:
            sum_of_values += m.value
        return sum_of_values
    def add_modifier(self, value, deactivation_trigger):
        modifier = Modifier(value, deactivation_trigger)
        self.modifiers.append(modifier)
        modifier.register_deactivation_trigger(self)

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

        if isinstance(self.stat, IntStat):
            self.stat.modifiers.remove(self)
        else:
            self.stat.modifier = None