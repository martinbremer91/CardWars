from source.gameplay.gameplay_enums import TargetTag

class Trigger:
    def __init__(self):
        self.subscribers = list()

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def invoke(self, arg):
        for subscriber in self.subscribers:
            subscriber(arg)

class Choice[T]:
    def __init__(self, options = None):
        self.options = list() if not options else options
        self.type_label = ""
        self.set_type_label()

    def set_type_label(self):
        if not self.options:
            self.type_label = ""
        elif isinstance(self.options, TargetTag):
            self.type_label = self.options.name
        else:
            self.type_label = f"{type(self.options[0]).__name__}"
    def resolve(self, entity = None) -> T:
        if self.options and isinstance(self.options, TargetTag):
            if not entity:
                raise Exception('Failed to resolve choice: tag given but entity is None')
            self.options = get_targets_from_tag(self.options, entity)
        if not self.options:
            print('No suitable options to choose\n')
            return None

        while True:
            user_prompt_options = ''
            for i in range(len(self.options)):
                user_prompt_options += f'[{i}]: {self.options[i]}\n'

            print(f'Available {self.type_label}s:\n{user_prompt_options}')
            index = input(f'Select {self.type_label}:')
            print('')

            if not index.isdigit():
                print(f'invalid {self.type_label} index: not a digit')
                continue
            index = int(index)
            if index < 0 or index >= len(self.options):
                print(f'invalid {self.type_label} index: digit out of range')
                continue

            return self.options[index]

class Effect:
    def __init__(self, entity):
        self.entity = entity
    def resolve(self, arg):
        pass

class DealDamage(Effect):
    def __init__(self, entity, target, value):
        super().__init__(entity)
        self.target = target
        self.value = value
    def resolve(self, arg):
        if isinstance(self.target, Choice):
            self.target = self.target.resolve(self.entity)
        if self.target is not None:
            self.target.take_damage(self.value)
            print(f'{self.entity} deals {self.value} damage to {self.target}. HP: {self.target.defense}')
        else:
            print(f"{self.entity.name}'s ability fizzled")

class Ability:
    def __init__(self, trigger, effects):
        self.trigger = trigger
        self.effects = effects
        # TODO: this shouldn't always happen here (depends on trigger: e.g. SEP yes, EOT no)
        self.subscribe_effects_to_trigger()

    def subscribe_effects_to_trigger(self):
        for effect in self.effects:
            self.trigger.subscribe(effect.resolve)

def get_creatures_from_lanes(lanes):
    creatures = list()
    for lane in lanes:
        if lane.creature:
            creatures.append(lane.creature)
    return creatures

def get_targets_from_tag(tag, entity):
    match tag:
        case TargetTag.Player:
            return [entity.card.player]
        case TargetTag.Opponent:
            return [entity.card.player.opponent]
        case TargetTag.All_Players:
            return [entity.card.player, entity.card.player.opponent]
        case TargetTag.Self:
            return [entity]
        case TargetTag.All_Creatures:
            return [get_creatures_from_lanes(entity.card.player.lanes),
                    get_creatures_from_lanes(entity.card.player.opponent.lanes)]
        case TargetTag.Own_Creatures:
            return get_creatures_from_lanes(entity.card.player.lanes)
        case TargetTag.Foe_Creatures:
            return get_creatures_from_lanes(entity.card.player.opponent.lanes)
        case TargetTag.Adjacent_Creatures:
            from source.gameplay.lane import get_adjacent_lanes
            return get_creatures_from_lanes(get_adjacent_lanes(entity.card.lane))
        case TargetTag.Opposite_Creature:
            from source.gameplay.lane import get_opposite_lane
            return get_creatures_from_lanes([get_opposite_lane(entity.card.lane)])
        case _:
            raise Exception(f'Could not get targets: invalid tag {tag.name}')