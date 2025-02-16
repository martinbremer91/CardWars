from player import Player
from game_entities import Entity, Creature, Spell, Building
from card import Card
from game_logic import Trigger
from gameplay_enums import TurnPhase, Landscape, Collection, EntityKind
from lane import Lane
import random
from typing import Optional

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
turn_phase : TurnPhase
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

    init_lanes()

def init_lanes():
    # <placeholder>
    for l in range(4):
        player_one.lanes.append(Lane(l, player_one, Landscape.NiceLands))
        player_two.lanes.append(Lane(l + 10, player_two, Landscape.NiceLands))
    # </placeholder>

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
    start_of_turn.subscribe(gain_turn_start_action_points)
    start_of_turn.subscribe(draw_cards)
    end_of_turn = Trigger()
    end_of_turn.subscribe(lose_unused_action_points)

def start_play():
    global turn_phase
    turn_phase = TurnPhase.P1_Main
    set_up_decks()
    draw_first_hands()
    start_turn()

def set_up_decks():
    # <placeholder>
    for i in range(40):
        Card(player_one, Building(f"entity_{i}", Landscape.NiceLands, 1), p1_deck)
        Card(player_two, Spell(f"entity_{i}", Landscape.NiceLands, 2), p2_deck)

    shuffle(p1_deck)
    shuffle(p2_deck)
    # </placeholder>

def draw_first_hands():
    draw_cards(player_one, 5)
    draw_cards(player_two, 5)

def start_turn():
    global active_player

    if turn_phase is TurnPhase.P1_Main:
        active_player = player_one
        start_of_turn.invoke(active_player)
    elif turn_phase is TurnPhase.P2_Main:
        active_player = player_two
        start_of_turn.invoke(active_player)

def advance_turn_phase():
    global turn_phase

    turn_phase = TurnPhase(turn_phase.value + 1)
    if turn_phase.value > TurnPhase.P2_Battle.value:
        turn_phase = TurnPhase.P1_Main

    if turn_phase is TurnPhase.P1_Main or TurnPhase.P2_Main:
        end_of_turn.invoke(active_player)
        # <placeholder> todo: only call start_turn once (async) end_of_turn.invoke resolves
        start_turn()
        # </placeholder>

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

def move_between_collections(player : Player, source : Card | Collection, to_enum : Collection,
                             amount : Optional[int] = None):
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

def gain_turn_start_action_points(player : Player):
    player.gain_action_points(2)

def lose_unused_action_points(player : Player):
    player.action_points = 0

def draw_cards(player : Player, amount : int = 1):
    move_between_collections(player, Collection.Deck, Collection.Hand, amount)

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
        case EntityKind.Creature:
            for lane in player.lanes:
                if lane.can_play_creature:
                    lanes.append(lane)
        case EntityKind.Spell:
            lanes.append(player.stack)
            return True
        case EntityKind.Building:
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

    # todo: lane selection / assignment of card to selected lane
    player.spend_action_points(cost)
    put_card_in_play(player, card)

def put_card_in_play(player : Player, card : Card):
    move_between_collections(player, card, Collection.In_Play)
    card.game_entity.on_play()

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


# test code
def print_state():
    print("p1 actions", player_one.action_points)
    print("p1 hand", len(p1_hand))
    print("p1 deck", len(p1_deck))
    print("p1 play", len(p1_cards_in_play))
    print("p1 discard", len(p1_discard))
    print("")
    print("p2 actions", player_two.action_points)
    print("p2 hand", len(p2_hand))
    print("p2 deck", len(p2_deck))
    print("p2 play", len(p2_cards_in_play))
    print("p2 discard", len(p2_discard))
    print("---")

def print_landscapes():
    for l1 in player_one.lanes:
        print(f"P1 lane", l1.landscape)
    for l2 in player_two.lanes:
        print(f"P2 lane", l2.landscape)
    print("P1 lands", player_one.landscapes)
    print("P2 lands", player_two.landscapes)
    print("")

init()
start_play()

print_landscapes()

print_state()
print_state()
advance_turn_phase()
advance_turn_phase()
print_state()