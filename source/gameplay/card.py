from random import shuffle
from source.gameplay.action_logic import get_action_indices_min_max, get_user_action_with_code, get_user_action_with_index, set_index_label_symbols
from source.gameplay.entities import get_entity_kind_from_string, get_entity_from_kind, Creature, Building
from source.gameplay.game_enums import CollectionType, Landscape, EntityType
from source.system.asset_manager import get_database, import_decklist
from source.gameplay.effect import SpendActionPoints
from source.gameplay.target import Choice
from source.system.input_manager import await_command, Result, Options
from source.ui.ui_manager import print_inspect_hand
from source.gameplay.action_data import ActionCode, UserAction, ActionLabel

class Collection:
    def __init__(self, player):
        self.cards = list()
        self.player = player

    def append(self, card):
        if not isinstance(card, Card):
            raise Exception("Cannot append collection with invalid type", type(card))
        self.cards.append(card)
    def remove(self, card):
        if not isinstance(card, Card):
            raise Exception("Cannot append collection with invalid type", type(card))
        self.cards.remove(card)
    def pop(self, index):
        return self.cards.pop(index)

class Card:
    def __init__(self, player , entity, collection):
        self.player  = player
        self.entity = entity
        self.collection = collection
        self.collection.append(self)
        self.lane = None
        self.entity.assign_card(self)

    def __str__(self):
        return self.entity.name

    def put_into_play(self, lane):
        move_between_collections(self.player, self, CollectionType.In_Play)
        self.lane = lane
        if isinstance(self.entity, Creature | Building):
            lane.add_entity(self.entity)
            self.entity.place_on_lane(lane)
        self.entity.on_play()
    def remove_from_play(self, to_enum):
        self.lane = None
        move_between_collections(self.player, self, to_enum)
    def replace(self, to_enum = CollectionType.Discard):
        self.remove_from_play(to_enum)
    def destroy(self):
        self.remove_from_play(CollectionType.Discard)

def get_card_from_id(player, card_data, deck : Collection) -> Card:
    entity_kind = get_entity_kind_from_string(card_data['type'])
    return Card(player, get_entity_from_kind(entity_kind, card_data), deck)

def get_deck_from_decklists(name, player) -> Collection:
    database = get_database()
    decklist = import_decklist(name)
    for item in decklist:
        for i in range(item[0]):
            get_card_from_id(player, database[str(item[1])], player.deck)
    return player.deck

def set_up_decks(player_one, player_two):
    player_one.deck = get_deck_from_decklists('Test', player_one)
    player_two.deck = get_deck_from_decklists('Test', player_two)

    shuffle_collection(player_one.deck)
    shuffle_collection(player_two.deck)

def shuffle_collection(collection):
    shuffle(collection.cards)

def inspect_hand(player):
    warning = None; override = False
    inspect_hand_actions = list()
    while True:
        if not override:
            inspect_hand_actions = get_default_inspect_hand_actions(player)
        labels = [a.label for a in inspect_hand_actions]
        action_codes = [c.action_code for c in inspect_hand_actions]
        print_inspect_hand(player, labels, warning)
        indices_min_max = get_action_indices_min_max(inspect_hand_actions)
        command = await_command(Options(action_codes, indices_min_max))
        match command.result:
            case Result.Nominal:
                warning = None
                if command.code_repr == ActionCode.ESCAPE.to_repr():
                    if override:
                        override = False; continue
                    override = False; break
                elif command.code_repr == ActionCode.RETURN.to_repr():
                    get_user_action_with_code(command.code_repr, inspect_hand_actions).subscriber()
                else:
                    raise Exception(f'Command result is Nominal but code_repr is not implemented')
            case Result.Index:
                warning = None; override = False
                get_user_action_with_index(command.code_repr, inspect_hand_actions).subscriber()
            case Result.OutOfRange:
                warning = f"Index out of range: \'{command.code_repr}\'"
            case Result.Invalid:
                warning = f"Invalid command: \'{command.code_repr}\'"
            case Result.Refresh:
                warning = None; override = False
            case Result.Filter:
                warning = None; override = True
                input = int(command.code_repr)
                inspect_hand_actions = update_inspect_hand_actions_for_ambiguous_indices(inspect_hand_actions, input)

def get_default_inspect_hand_actions(player) -> list:
    inspect_hand_actions = list()
    for card in player.hand.cards:
        card_action = UserAction(ActionLabel(card.entity.name), ActionCode.INDEX, inspect_card)
        inspect_hand_actions.append(card_action)
        inspect_hand_actions.append(UserAction(ActionLabel('test'), ActionCode.INDEX, inspect_card))
    inspect_hand_actions.append(UserAction(ActionLabel('Back', ActionCode.ESCAPE.to_symbol()), ActionCode.ESCAPE))
    set_index_label_symbols(inspect_hand_actions)
    return inspect_hand_actions

def update_inspect_hand_actions_for_ambiguous_indices(inspect_hand_actions, input) -> list:
    override_actions = list()
    for action in inspect_hand_actions:
        if action.action_code != ActionCode.INDEX:
            continue
        if input == int(action.label.symbol):
            override_actions.append(UserAction(ActionLabel(action.label.text, ActionCode.RETURN.to_symbol()), ActionCode.RETURN, inspect_card))
        action_first_digit = int(str(action.label.symbol)[0])
        if input == action_first_digit:
            override_actions.append(UserAction(ActionLabel(action.label.text), ActionCode.INDEX, inspect_card))
    override_actions.append(UserAction(ActionLabel('Cancel', ActionCode.ESCAPE.to_symbol()), ActionCode.ESCAPE))
    set_index_label_symbols(override_actions, offset = 0)
    return override_actions

def inspect_card():
    #card = Choice(active_player.hand.cards).resolve(active_player)
    #if card is None:
    #    break
    #try_play_card(active_player, card)
    #if active_player.action_points == 0:
    #    break
    print('test')
    exit()

def inspect_lanes(player):
    print("inspect lanes")
    exit()

def inspect_discard_pile(player):
    print("inspect discard pile")
    exit()

def move_between_collections(player, src, to_enum, amount = None):
    if isinstance(src, Card):
        to_coll = player.get_collection(to_enum)
        to_coll.append(src)
        src.collection.remove(src)
        src.collection = to_coll
    else:
        from_coll = player.get_collection(src)
        if not from_coll:
            return

        to_coll = player.get_collection(to_enum)

        for i in range(amount):
            card = from_coll.pop(0)
            to_coll.append(card)
            card.collection = to_coll

def check_card_landscape_requirement(player, card) -> bool:
    cost = card.entity.cost.value
    land = card.entity.land.value

    if land is Landscape.Rainbow:
        return player.landscape_count() >= cost
    else:
        return player.landscape_count(land) >= cost

def check_card_action_cost_requirement(player, cost) -> bool:
    return int(player.action_points.value) >= cost

def check_card_lane_availability(player, entity, lanes) -> bool:
    match entity.entity_type.value:
        case EntityType.Creature:
            for lane in player.lanes:
                if lane.can_play_creature:
                    lanes.append(lane)
        case EntityType.Spell:
            return True
        case EntityType.Building:
            for lane in player.lanes:
                lanes.append(lane)
        case _:
            raise Exception("invalid entity kind")

    return len(lanes) != 0

def check_card_specific_requirements() -> bool:
    return True

def try_play_card(player, card):
    cost = card.entity.cost

    if not check_card_landscape_requirement(player, card):
        print(f"{player.name} failed land requirement")
        return
    if not check_card_action_cost_requirement(player, cost.value):
        print(f"{player.name} failed action cost requirement")
        return

    available_lanes = list()
    if not check_card_lane_availability(player, card.entity, available_lanes):
        print(f"{player.name} failed lane availability requirement")
        return
    if not check_card_specific_requirements():
        return

    selected_lane = None

    if card.entity.entity_type is not EntityType.Spell:
        selected_lane = Choice(available_lanes).resolve(player)
        if selected_lane.creature is not None:
            selected_lane.creature.destroy()
        elif selected_lane.building is not None:
            selected_lane.building.destroy()
    card.put_into_play(selected_lane)
    SpendActionPoints(card.entity, player, cost.value).resolve()

def mill_cards(player, amount = 1):
    move_between_collections(player, CollectionType.Deck, CollectionType.Discard, amount)

def discard_cards(player, amount = 1):
    hand = player.get_collection(CollectionType.Hand)

    for i in range(amount):
        if not hand:
            return

        card = Choice(hand.cards).resolve(player)
        move_between_collections(player, card, CollectionType.Discard)
