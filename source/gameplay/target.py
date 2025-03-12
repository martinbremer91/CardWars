import random
from source.gameplay.game_enums import TargetTag

counter = 0
# action_list = []
action_list = [0, 0, 0, 1,
               0, 0, 0, 1,
               0, 0,
               0, 2, 0, 3,
               0, 0, 0, 0,
               0, 2, 0, 3,
               0, 0, 0, 0]

class Target:
    def __init__(self, options = None, amount = 1):
        self.options = list() if not options else options
        self.amount = amount
        self.type_label = ""
        self.set_type_label()

    def set_type_label(self):
        if not self.options:
            self.type_label = ""
        elif isinstance(self.options, TargetTag):
            self.type_label = str(self.options)
        else:
            self.type_label = f"{type(self.options[0]).__name__}"
    def resolve(self, ctx):
        return self.options if not isinstance(self.options, TargetTag) \
            else get_targets_from_tag(self.options, ctx)

class Random(Target):
    def __init__(self, options = None, amount = 1):
        super().__init__(options, amount)
    def resolve(self, ctx):
        current_options = super().resolve(ctx)
        if isinstance(current_options, list) and len(current_options) >= self.amount:
            return random.choices(current_options, k=self.amount)
        return current_options

class Filter(Target):
    def __init__(self, condition, options = None, amount = 1):
        super().__init__(options, amount)
        self.condition = condition
    def resolve(self, ctx):
        current_options = super().resolve(ctx)
        filtered_options = None
        if isinstance(current_options, list):
            filtered_options = list()
            for option in current_options:
                if self.condition.resolve():
                    filtered_options.append(option)
        elif self.condition.resolve():
            filtered_options = current_options
        return filtered_options

class Choice(Target):
    def __init__(self, options = None, amount = 1):
        super().__init__(options, amount)
    def resolve(self, ctx):
        current_options = super().resolve(ctx)
        choices = list()
        global counter

        for c in range(min(len(current_options), self.amount)):
            while True:
                user_prompt_options = ''
                for i in range(len(current_options)):
                    user_prompt_options += f'[{i}]: {current_options[i].__str__()}\n'

                print(f'Available {self.type_label}s:\n{user_prompt_options}')
                index = str(action_list[counter]) if len(action_list) > counter else input(f'Select {self.type_label}:')
                counter += 1
                print('')

                # <placeholder>
                if index == 'c':
                    print('Application stopped by user')
                    exit()
                # </placeholder>

                if not index.isdigit():
                    # <placeholder>
                    test(index, self, ctx)
                    # </placeholder>
                    continue
                index = int(index)
                if index < 0 or index >= len(current_options):
                    print(f'invalid {self.type_label} index: digit out of range')
                    continue

                choices.append(current_options[index])
                break

        if len(choices) == 1:
            return choices[0]
        return choices

def get_creatures_from_lanes(lanes):
    creatures = None
    if isinstance(lanes, list):
        creatures = list()
        for lane in lanes:
            if lane.creature:
                creatures.append(lane.creature)
    elif lanes.creature:
        creatures = lanes.creature
    return creatures

def get_targets_from_tag(tag, entity):
    match tag:
        case TargetTag.Player:
            return entity.card.player
        case TargetTag.Opponent:
            return entity.card.player.opponent
        case TargetTag.All_Players:
            return [entity.card.player, entity.card.player.opponent]
        case TargetTag.Self:
            return entity
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
            return get_creatures_from_lanes(get_opposite_lane(entity.card.lane))
        case _:
            raise Exception(f'Could not get targets: invalid tag {tag}')

# <placeholder>
def test(index, choice, ctx):
    try:
        player = ctx.card.player
        entity = ctx
    except AttributeError:
        player = ctx
        entity = None

    match index:
        case 'ap':
            print(player.action_points)
        case _:
            print(f'invalid {choice.type_label} index: not a digit')
# </placeholder>