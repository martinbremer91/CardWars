from source.gameplay.game_enums import TargetTag

counter = 0
# action_list = []
action_list = [0, 0, 0, 1,
               0, 0, 0, 0, 1, 0, 0, 0,
               0, 0, 0, 0, 2, 0, 0, 0, 0]

class Choice:
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
        if self.options and isinstance(self.options, TargetTag):
            if not ctx:
                raise Exception('Failed to resolve choice: tag given but no entity passed in as "ctx" param')
            self.options = get_targets_from_tag(self.options, ctx)
        if not self.options:
            print('No suitable options to choose\n')
            return None

        choices = list()
        global counter

        for c in range(min(len(self.options), self.amount)):
            while True:
                user_prompt_options = ''
                for i in range(len(self.options)):
                    user_prompt_options += f'[{i}]: {self.options[i].__str__()}\n'

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
                if index < 0 or index >= len(self.options):
                    print(f'invalid {self.type_label} index: digit out of range')
                    continue

                choices.append(self.options[index])
                break

        if len(choices) == 1:
            return choices[0]
        return choices

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