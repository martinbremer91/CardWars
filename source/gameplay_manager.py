from enum import Enum
import random

class Player:
    def __init__(self, hp : int):
        self.hp : int  = hp

class TurnPhase(Enum):
    P1_Main = 0
    P1_Battle = 1
    P2_Main = 2
    P2_Battle = 3

class Collection(Enum):
    Deck = 0
    Hand = 1
    Discard = 2

class Card:
    def __init__(self, id : int):
        self.id = id

player_one : Player
player_two : Player

p1_deck : list[Card]
p2_deck : list[Card]

p1_hand : list[Card]
p2_hand : list[Card]

p1_discard : list[Card]
p2_discard : list[Card]

turn_phase : int

def init():
    global player_one
    global player_two
    global turn_phase

    global p1_deck
    global p2_deck

    global p1_hand
    global p2_hand

    global p1_discard
    global p2_discard

    player_one = Player(25)
    player_two = Player(25)
    turn_phase = TurnPhase.P1_Main.value

    p1_deck = list()
    p2_deck = list()

    p1_hand = list()
    p2_hand = list()

    p1_discard = list()
    p2_discard = list()

def end_turn_phase():
    global turn_phase

    turn_phase += 1
    if (turn_phase > TurnPhase.P2_Battle.value):
        turn_phase = TurnPhase.P1_Main.value
    print(TurnPhase(turn_phase).name)

def shuffle(collection : list[Card]):
    random.shuffle(collection)

def get_collection(player : Player, collection : str) -> list[Card]:
    global p1_deck
    global p2_deck
    global p1_hand
    global p2_hand
    global p1_discard
    global p2_discard    

    is_p1 = player is player_one    
    
    match collection:
        case Collection.Deck:
            return p1_deck if is_p1 else p2_deck
        case Collection.Hand:
            return p1_hand if is_p1 else p2_hand
        case Collection.Discard:
            return p1_discard if is_p1 else p2_discard
        case _:
            raise Exception("No valid CardCollection given")

def move_between_collections(player : Player, from_enum : str, to_enum : str, amount : int):
    from_coll : list[Card] = get_collection(player, from_enum)

    if not from_coll:
        return

    to_coll : list[Card] = get_collection(player, to_enum)

    for i in range(amount):
        to_coll.append(from_coll.pop(0))

def draw_cards(player : Player, amount : int = 1):
    move_between_collections(player, Collection.Deck, Collection.Hand, amount)

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
            print(f"[{j}]:", hand[j].id)
        chosen_index : int = int(input("> "))
        # </placeholder>
        
        discard.append(hand.pop(chosen_index))
    


# test code
init()

for i in range(40):
    p1_deck.append(Card(i))
    p2_deck.append(Card(i))

shuffle(p1_deck)
shuffle(p2_deck)

draw_cards(player_one, 4)
print("player one draws four cards")

discard_cards(player_one, 2)
print("hand:", len(p1_hand))
print("dicard:", len(p1_discard))
