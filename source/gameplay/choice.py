from source.gameplay.game_enums import TargetTag

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
            self.type_label = self.options.name
        else:
            self.type_label = f"{type(self.options[0]).__name__}"
    def resolve(self, entity = None):
        if self.options and isinstance(self.options, TargetTag):
            if not entity:
                raise Exception('Failed to resolve choice: tag given but entity is None')
            self.options = get_targets_from_tag(self.options, entity)
        if not self.options:
            print('No suitable options to choose\n')
            return None

        choices = list()

        for c in range(min(len(self.options), self.amount)):
            while True:
                user_prompt_options = ''
                for i in range(len(self.options)):
                    user_prompt_options += f'[{i}]: {self.options[i].__str__()}\n'

                print(f'Available {self.type_label}s:\n{user_prompt_options}')
                index = input(f'Select {self.type_label}:')
                print('')

                # <placeholder>
                if index == 'c':
                    print('Application stopped by user')
                    exit()
                # </placeholder>

                if not index.isdigit():
                    print(f'invalid {self.type_label} index: not a digit')
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
            raise Exception(f'Could not get targets: invalid tag {tag.name}')