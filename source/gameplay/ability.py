class Ability:
    def __init__(self, trigger, effects):
        self.trigger = trigger
        self.effects = effects
        # TODO: this shouldn't always happen here (depends on trigger: e.g. SEP yes, EOT no)
        self.subscribe_effects_to_trigger()

    def subscribe_effects_to_trigger(self):
        if isinstance(self.effects, list):
            for effect in self.effects:
                self.trigger.subscribe(effect.resolve)
        else:
            self.trigger.subscribe(self.effects.resolve)