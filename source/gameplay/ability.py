class Ability:
    def __init__(self, trigger, effects, active_trigger = None, inactive_trigger = None):
        self.trigger = trigger
        self.effects = effects
        self.active_trigger = active_trigger
        self.inactive_trigger = inactive_trigger

        if not active_trigger:
            self.subscribe_effects_to_trigger()
        else:
            self.subscribe_active_trigger()

    def subscribe_active_trigger(self):
        self.active_trigger.subscribe(self.subscribe_effects_to_trigger)
    def subscribe_inactive_trigger(self):
        self.inactive_trigger.subscribe(self.unsubscribe_ability_effects)

    def subscribe_effects_to_trigger(self):
        if isinstance(self.effects, list):
            for effect in self.effects:
                self.trigger.subscribe(effect.resolve)
        else:
            self.trigger.subscribe(self.effects.resolve)

        if self.active_trigger:
            self.active_trigger.unsubscribe(self.subscribe_active_trigger)
        if self.inactive_trigger:
            self.inactive_trigger.subscribe(self.subscribe_inactive_trigger)

    def unsubscribe_ability_effects(self):
        if isinstance(self.effects, list):
            for effect in self.effects:
                self.trigger.unsubscribe(effect.resolve)
        else:
            self.trigger.unsubscribe(self.effects.resolve)

        if self.active_trigger:
            self.active_trigger.subscribe(self.subscribe_active_trigger)
        if self.inactive_trigger:
            self.inactive_trigger.unsubscribe(self.subscribe_inactive_trigger)