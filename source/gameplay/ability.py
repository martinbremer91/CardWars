class Ability:
    def __init__(self, trigger, effects, activation_trigger = None, deactivation_trigger = None):
        self.trigger = trigger
        self.effects = effects
        self.activation_trigger = activation_trigger
        self.deactivation_trigger = deactivation_trigger

        if not activation_trigger:
            self.subscribe_ability_effects()
        else:
            self.subscribe_activation_trigger()
        if deactivation_trigger:
            self.subscribe_deactivation_trigger()

    def subscribe_activation_trigger(self):
        self.activation_trigger.subscribe(self.subscribe_ability_effects)
    def subscribe_deactivation_trigger(self):
        self.deactivation_trigger.subscribe(self.unsubscribe_ability_effects)

    def subscribe_ability_effects(self):
        if isinstance(self.effects, list):
            for effect in self.effects:
                self.trigger.subscribe(effect.resolve)
        else:
            self.trigger.subscribe(self.effects.resolve)
    def unsubscribe_ability_effects(self):
        if isinstance(self.effects, list):
            for effect in self.effects:
                self.trigger.unsubscribe(effect.resolve)
        else:
            self.trigger.unsubscribe(self.effects.resolve)