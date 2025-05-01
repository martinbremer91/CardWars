from source.gameplay.player import Player
from source.gameplay.card import set_up_decks, try_play_card
from source.gameplay.target import Choice
from source.gameplay.effect import DrawCards, GainActionPoints, SpendActionPoints
from source.gameplay.game_enums import TurnPhase
from source.gameplay.lane import init_lanes
from source.gameplay.combat import get_active_combat_lanes, resolve_attack  
from source.system.input_manager import await_command, Result
from source.ui.ui_manager import print_main_phase

active_player : Player
player_one : Player
player_two : Player
turn_phase : TurnPhase
turn_counter : int

def init():
    global player_one
    global player_two
    global turn_phase
    global active_player
    global turn_counter

    turn_counter = 0

    player_one = Player("Player 1")
    player_two = Player("Player 2")
    player_one.assign_opponent(player_two)
    player_two.assign_opponent(player_one)

    subscribe_players_global_abilities()

    init_lanes((player_one, player_two))

def subscribe_players_global_abilities():
    player_one.start_of_turn.subscribe(DrawCards(None, player_one, 1).resolve)
    player_two.start_of_turn.subscribe(DrawCards(None, player_two, 1).resolve)
    player_one.start_of_turn.subscribe(GainActionPoints(None, player_one, 2).resolve)
    player_two.start_of_turn.subscribe(GainActionPoints(None, player_two, 2).resolve)

def start_play():
    global turn_phase
    turn_phase = TurnPhase.P1_Main
    set_up_decks(player_one, player_two)
    draw_first_hands()
    start_turn()

def draw_first_hands():
    DrawCards(None, player_one, 5).resolve()
    DrawCards(None, player_two, 5).resolve()

def start_turn():
    global active_player
    global turn_counter

    turn_counter += 1

    if turn_phase is TurnPhase.P1_Main:
        active_player = player_one
    elif turn_phase is TurnPhase.P2_Main:
        active_player = player_two
    active_player.start_of_turn.invoke()

    resolve_main_phase()

def resolve_main_phase():
    while True:
        print_main_phase(active_player)
        match await_command().result:
            case Result.Nominal:
                ...
            case Result.Cancel:
                raise Exception('Cannot cancel MainPhase')
            case Result.Invalid:
                continue
        #card = Choice(active_player.hand.cards).resolve(active_player)
        #if card is None:
        #    break
        #try_play_card(active_player, card)
        #if active_player.action_points == 0:
        #    break
    advance_turn_phase()

def advance_turn_phase():
    global turn_phase

    phase_value = turn_phase.value + 1
    if phase_value > TurnPhase.P2_Battle.value:
        phase_value = TurnPhase.P1_Main.value
    turn_phase = TurnPhase(phase_value)

    if turn_phase is TurnPhase.P1_Main or turn_phase is TurnPhase.P2_Main:
        active_player.end_of_turn.invoke()
        start_turn()
        advance_turn_phase()
    elif turn_phase is TurnPhase.P1_Battle or TurnPhase.P2_Battle:
        if turn_counter > 1:
            resolve_combat()
        advance_turn_phase()

def resolve_combat():
    lanes = get_active_combat_lanes(active_player)
    while len(lanes) > 0:
        lane = Choice(lanes).resolve(active_player)
        resolve_attack(lane)
        lanes.remove(lane)
