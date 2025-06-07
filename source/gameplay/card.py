from random import shuffle
from typing import assert_type
from source.gameplay.action_logic import ActionRegistry, get_action_indices_min_max, resolve_user_action, set_index_label_symbols
from source.gameplay.entities import get_entity_kind_from_string, get_entity_from_kind, Creature, Building
from source.gameplay.game_enums import CollectionType, Landscape, EntityType
from source.system.asset_manager import get_database, import_decklist
from source.gameplay.effect import SpendActionPoints
from source.gameplay.target import Choice
from source.system.input_manager import await_command, Options
from source.ui.ui_manager import print_inspect_card
from source.gameplay.action_data import ActionCode, ActionContext, ActionType, UserAction, ActionLabel

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
        return self.entity.name.value

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

def init(player_one, player_two):
    set_up_decks(player_one, player_two)
    ActionRegistry.get().inspect_hand_action = inspect_hand
    ActionRegistry.get().inspect_card_action = inspect_card
    ActionRegistry.get().inspect_lanes_action = inspect_lanes
    ActionRegistry.get().inspect_discard_pile_action = inspect_discard_pile

def set_up_decks(player_one, player_two):
    player_one.deck = get_deck_from_decklists('Test', player_one)
    player_two.deck = get_deck_from_decklists('Test', player_two)
    shuffle_collection(player_one.deck)
    shuffle_collection(player_two.deck)

def shuffle_collection(collection):
    shuffle(collection.cards)

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
        to_coll = player.get_collection(to_enum); assert amount
        for _ in range(amount):
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
    for _ in range(amount):
        if not hand:
            return
        card = Choice(hand.cards).resolve(player)
        move_between_collections(player, card, CollectionType.Discard)

def inspect_hand(context):
    context = ActionContext(ActionType.INSPECT_HAND, context.player)
    resolve_user_action(context, get_inspect_hand_actions)

def get_inspect_hand_actions(context) -> list:
    inspect_hand_actions = list()
    for card in context.player.hand.cards:
        hand_action = UserAction(ActionLabel(card.entity.name.value), ActionCode.INDEX, ActionType.INSPECT_CARD)
        inspect_hand_actions.append(hand_action)
    inspect_hand_actions.append(UserAction(ActionLabel('Back', ActionCode.ESCAPE.to_symbol()), ActionCode.ESCAPE))
    set_index_label_symbols(inspect_hand_actions)
    return inspect_hand_actions

def inspect_card(context):
    selected_card_action = context.data
    card = next((c for c in context.player.hand.cards if c.entity.name.value == selected_card_action.label.text), None)
    assert card
    context = ActionContext(ActionType.INSPECT_CARD, context.player, card)
    resolve_user_action(context, get_inspect_card_actions)

def get_inspect_card_actions(context) -> list:
    inspect_card_actions = list()
    inspect_card_actions.append(UserAction(ActionLabel('Back', ActionCode.ESCAPE.to_symbol()), ActionCode.ESCAPE))
    return inspect_card_actions

def inspect_lanes(context):
    print("inspect lanes")
    exit()

def inspect_discard_pile(context):
    print("inspect discard pile")
    exit()
