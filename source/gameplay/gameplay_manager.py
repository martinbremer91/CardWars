from source.gameplay.player import Player
from source.gameplay.card import init_collections, draw_cards, set_up_decks
from source.gameplay.game_logic import Trigger, Choice
from gameplay_enums import TurnPhase
from source.gameplay.lane import Lane, init_lanes
from source.gameplay.combat import get_active_combat_lanes, resolve_attack

active_player : Player
player_one : Player
player_two : Player
turn_phase : TurnPhase
start_of_turn : Trigger
end_of_turn : Trigger

def init():
    global player_one
    global player_two
    global turn_phase
    global active_player

    player_one = Player("Player 1", 25)
    player_two = Player("Player 2", 25)

    init_collections(player_one, player_two)
    init_turn_phase_triggers()
    init_lanes((player_one, player_two))

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
    set_up_decks(player_one, player_two)
    draw_first_hands()
    start_turn()

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

    if turn_phase is TurnPhase.P1_Main or turn_phase is TurnPhase.P2_Main:
        end_of_turn.invoke(active_player)
        # <placeholder> todo: only call start_turn once (async) end_of_turn.invoke resolves
        start_turn()
        # </placeholder>
    elif turn_phase is TurnPhase.P1_Battle or TurnPhase.P2_Battle:
        resolve_combat()

def resolve_combat():
    lanes : list[Lane] = get_active_combat_lanes(active_player)
    while len(lanes) > 0:
        lane = Choice[Lane](lanes).resolve()
        resolve_attack(lane)
        lanes.remove(lane)
    advance_turn_phase()

def gain_turn_start_action_points(player : Player):
    player.gain_action_points(2)

def lose_unused_action_points(player : Player):
    player.action_points = 0