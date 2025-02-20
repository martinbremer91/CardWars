from typing import Optional
from random import shuffle
from source.gameplay.player import Player
from source.gameplay.entities import Entity, get_entity_kind_from_string, get_entity_from_kind
from source.gameplay.gameplay_enums import EntityType, CollectionType, Landscape
from source.gameplay.lane import Lane
from source.system.asset_manager import get_database, import_decklist
from source.gameplay.game_logic import Choice

class Collection:
    def __init__(self, player : Player):
        self.cards : list[Card] = list()
        self.player : Player = player

    def append(self, card):
        if not isinstance(card, Card):
            raise Exception("Cannot append collection with invalid type", type(card))
        self.cards.append(card)
    def remove(self, card):
        if not isinstance(card, Card):
            raise Exception("Cannot append collection with invalid type", type(card))
        self.cards.remove(card)
    def pop(self, index : int):
        return self.cards.pop(index)

class Card:
    def __init__(self, owner : Player, game_entity : Entity, collection : Collection):
        self.owner : Player = owner
        self.game_entity : Entity = game_entity
        self.collection : Collection = collection
        self.collection.append(self)

p1_deck : Collection
p2_deck : Collection
p1_hand : Collection
p2_hand : Collection
p1_cards_in_play : Collection
p2_cards_in_play : Collection
p1_discard : Collection
p2_discard : Collection

def init_collections(player_one : Player, player_two : Player):
    global p1_deck
    global p2_deck
    global p1_hand
    global p2_hand
    global p1_cards_in_play
    global p2_cards_in_play
    global p1_discard
    global p2_discard

    p1_deck = Collection(player_one)
    p2_deck = Collection(player_two)
    p1_hand = Collection(player_one)
    p2_hand = Collection(player_two)
    p1_cards_in_play = Collection(player_one)
    p2_cards_in_play = Collection(player_two)
    p1_discard = Collection(player_one)
    p2_discard = Collection(player_two)

def get_card_from_id(player : Player, card_data : dict[str, ], deck : Collection) -> Card:
    entity_kind : EntityType = get_entity_kind_from_string(card_data['type'])
    return Card(player, get_entity_from_kind(entity_kind, card_data), deck)

def get_deck_from_decklists(name : str, player : Player) -> Collection:
    database : dict[str, dict[str, ]] = get_database()

    decklist : list[(int, int)] = import_decklist(name)
    deck : Collection = Collection(player)

    for item in decklist:
        for i in range(item[0]):
            get_card_from_id(player, database[str(item[1])], deck)

    return deck

def set_up_decks(player_one : Player, player_two : Player):
    global p1_deck
    global p2_deck
    p1_deck = get_deck_from_decklists('Finn', player_one)
    p2_deck = get_deck_from_decklists('Jake', player_two)

    shuffle_collection(p1_deck)
    shuffle_collection(p2_deck)

def shuffle_collection(collection : Collection):
    shuffle(collection.cards)

def get_collection(player: Player, collection: CollectionType) -> Collection:
    match collection:
        case CollectionType.Deck:
            return p1_deck if player is p1_deck.player else p2_deck
        case CollectionType.Hand:
            return p1_hand if player is p1_hand.player else p2_hand
        case CollectionType.In_Play:
            return p1_cards_in_play if player is p1_cards_in_play else p2_cards_in_play
        case CollectionType.Discard:
            return p1_discard if player is p1_discard else p2_discard
        case _:
            raise Exception("No valid Collection given")

def move_between_collections(player: Player, source: Card | CollectionType, to_enum: CollectionType,
                             amount: Optional[int] = None):
    if isinstance(source, Card):
        to_coll: Collection = get_collection(player, to_enum)
        to_coll.append(source)
        source.collection.remove(source)
        source.collection = to_coll
    else:
        from_coll: Collection = get_collection(player, source)
        if not from_coll:
            return

        to_coll: Collection = get_collection(player, to_enum)

        for i in range(amount):
            card: Card = from_coll.pop(0)
            to_coll.append(card)
            card.collection = to_coll

def draw_cards(player : Player, amount : int = 1):
    move_between_collections(player, CollectionType.Deck, CollectionType.Hand, amount)

def check_card_landscape_requirement(player : Player, card : Card) -> bool:
    cost : int = card.game_entity.cost
    land : Landscape = card.game_entity.land

    if land is Landscape.Rainbow:
        return sum(player.landscapes.values()) >= cost
    else:
        return land in player.landscapes.keys() and player.landscapes[land] >= cost

def check_card_action_cost_requirement(player : Player, cost : int) -> bool:
    return player.action_points >= cost

def check_card_lane_availability(player : Player, entity : Entity, lanes : list[Lane]) -> bool:
    match entity.kind:
        case EntityType.Creature:
            for lane in player.lanes:
                if lane.can_play_creature:
                    lanes.append(lane)
        case EntityType.Spell:
            return True
        case EntityType.Building:
            for lane in player.lanes:
                if lane.building is None:
                    lanes.append(lane)
        case _:
            raise Exception("invalid entity kind")

    return len(lanes) != 0

def check_card_specific_requirements() -> bool:
    return True

def try_play_card(player : Player, card : Card):
    cost : int = card.game_entity.cost

    if not check_card_landscape_requirement(player, card):
        print(f"{player.name} failed land requirement")
        return
    if not check_card_action_cost_requirement(player, cost):
        print(f"{player.name} failed action cost requirement")
        return

    available_lanes : list[Lane] = list()
    if not check_card_lane_availability(player, card.game_entity, available_lanes):
        print(f"{player.name} failed lane availability requirement")
        return
    if not check_card_specific_requirements():
        return

    selected_lane : Optional[Lane, None] = None
    if card.game_entity.kind is not EntityType.Spell:
        selected_lane = Choice[Lane](available_lanes).resolve()
    put_card_in_play(player, card, selected_lane)
    player.spend_action_points(cost)

def put_card_in_play(player: Player, card: Card, lane : Optional[Lane]):
    move_between_collections(player, card, CollectionType.In_Play)
    card.game_entity.on_play()
    if card.game_entity.kind is not EntityType.Spell:
        card.game_entity.place_on_lane(lane)

def mill_cards(player: Player, amount: int = 1):
    move_between_collections(player, CollectionType.Deck, CollectionType.Discard, amount)

def discard_cards(player: Player, amount: int = 1):
    hand: Collection = get_collection(player, CollectionType.Hand)
    discard: Collection = get_collection(player, CollectionType.Discard)

    for i in range(amount):
        if not hand:
            return

        # <placeholder> PLAYER CHOICE LOOP
        print("Choose a card to discard (by index):")
        for j in range(len(hand.cards)):
            print(f"[{j}]:", hand.cards[j].game_entity.name)
        chosen_index: int = int(input("> "))
        # </placeholder>

        discard.append(hand.pop(chosen_index))