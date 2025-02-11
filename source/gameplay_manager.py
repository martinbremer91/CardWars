from enum import Enum
import random
from typing import Callable, overload

class Player:
    def __init__(self, name: str, hp : int):
        self.name = name
        self.hp : int  = hp

class TurnPhase(Enum):
    P1_Main = 0
    P1_Battle = 1
    P2_Main = 2
    P2_Battle = 3

class Collection(Enum):
    Deck = 0
    Hand = 1
    In_Play = 2
    Discard = 3

class GameEntity:
    def __init__(self, name : str):
        self.name = name

    def on_play(self):
        pass

class Creature(GameEntity):
    def on_play(self):
        super().on_play()
        print("Type of GameEntity: Creature")

class Spell(GameEntity):
    def on_play(self):
        super().on_play()
        print("Type of GameEntity: Spell")

class Building(GameEntity):
    def on_play(self):
        super().on_play()
        print("Type of GameEntity: Building")

class Card:
    def __init__(self, owner : Player, game_entity : GameEntity, collection : list):
        self.owner = owner
        self.game_entity = game_entity
        self.collection = collection
        self.collection.append(self)

class Trigger:
    def __init__(self):
        self.subscribers : list[Callable] = list()

    def subscribe(self, subscriber : Callable):
        self.subscribers.append(subscriber)

    def invoke(self, arg = ...):
        for subscriber in self.subscribers:
            subscriber(arg)

active_player : Player

player_one : Player
player_two : Player

p1_deck : list[Card]
p2_deck : list[Card]

p1_hand : list[Card]
p2_hand : list[Card]

p1_cards_in_play : list[Card]
p2_cards_in_play : list[Card]

p1_discard : list[Card]
p2_discard : list[Card]

turn_phase : int

start_of_turn : Trigger
end_of_turn : Trigger

def init():
    global player_one
    global player_two
    global turn_phase
    global active_player

    init_collections()
    init_turn_phase_triggers()

    player_one = Player("Player 1", 25)
    player_two = Player("Player 2", 25)

    turn_phase = TurnPhase.P1_Main.value
    active_player = player_one

def init_collections():
    global p1_deck
    global p2_deck
    global p1_hand
    global p2_hand
    global p1_cards_in_play
    global p2_cards_in_play
    global p1_discard
    global p2_discard

    p1_deck = list()
    p2_deck = list()
    p1_hand = list()
    p2_hand = list()
    p1_cards_in_play = list()
    p2_cards_in_play = list()
    p1_discard = list()
    p2_discard = list()

def init_turn_phase_triggers():
    global start_of_turn
    global end_of_turn

    start_of_turn = Trigger()
    end_of_turn = Trigger()
    start_of_turn.subscribe(draw_cards)

def set_up_decks():
    # <placeholder>
    for i in range(40):
        Card(player_one, Creature(f"entity_{i}"), p1_deck)
        Card(player_two, Spell(f"entity_{i}"), p2_deck)

    shuffle(p1_deck)
    shuffle(p2_deck)
    # </placeholder>

def draw_first_hands():
    draw_cards(player_one, 5)
    draw_cards(player_two, 5)

def start_first_turn():
    start_of_turn.invoke(active_player)

def end_turn_phase():
    global turn_phase
    global active_player

    turn_phase += 1
    if turn_phase > TurnPhase.P2_Battle.value:
        turn_phase = TurnPhase.P1_Main.value
    print(TurnPhase(turn_phase).name)

    if turn_phase is TurnPhase.P1_Main.value:
        end_of_turn.invoke()
        active_player = player_one
        start_of_turn.invoke(active_player)
    elif turn_phase is TurnPhase.P2_Main.value:
        end_of_turn.invoke()
        active_player = player_two
        start_of_turn.invoke(active_player)

def shuffle(collection : list[Card]):
    random.shuffle(collection)

def get_collection(player : Player, collection : Collection) -> list[Card]:
    is_p1 = player is player_one
    
    match collection:
        case Collection.Deck:
            return p1_deck if is_p1 else p2_deck
        case Collection.Hand:
            return p1_hand if is_p1 else p2_hand
        case Collection.In_Play:
            return p1_cards_in_play if is_p1 else p2_cards_in_play
        case Collection.Discard:
            return p1_discard if is_p1 else p2_discard
        case _:
            raise Exception("No valid Collection given")

@overload
def move_between_collections(player : Player, from_enum : Collection, to_enum : Collection, amount : int): ...
@overload
def move_between_collections(player : Player, card : Card, to_enum : Collection): ...

def move_between_collections(player : Player, source : Card | Collection, to_enum : Collection, amount : int = ...):
    if isinstance(source, Card):
        to_coll: list[Card] = get_collection(player, to_enum)
        to_coll.append(source)
        source.collection.remove(source)
        source.collection = to_coll
    else:
        from_coll: list[Card] = get_collection(player, source)
        if not from_coll:
            return

        to_coll: list[Card] = get_collection(player, to_enum)

        for i in range(amount):
            card : Card = from_coll.pop(0)
            to_coll.append(card)
            card.collection = to_coll

def draw_cards(player : Player, amount : int = 1):
    move_between_collections(player, Collection.Deck, Collection.Hand, amount)

def play_card(player : Player, card : Card):
    move_between_collections(player, card, Collection.In_Play)

def mill_cards(player : Player, amount : int = 1):
    move_between_collections(player, Collection.Deck, Collection.Discard, amount)

def discard_cards(player : Player, amount : int = 1):
    hand : list[Card] = get_collection(player, Collection.Hand)
    discard : list[Card] = get_collection(player, Collection.Discard)

    for i in range(amount):
        if not hand:
            return

        # <placeholder> PLAYER CHOICE LOOP
        print("Choose a card to discard (by index):")
        for j in range(len(hand)):
            print(f"[{j}]:", hand[j].game_entity.name)
        chosen_index : int = int(input("> "))
        # </placeholder>
        
        discard.append(hand.pop(chosen_index))