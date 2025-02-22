from source.gameplay.player import Player
from source.gameplay.card import set_up_decks, try_play_card
from source.gameplay.choice import Choice
from source.gameplay.effect import DrawCards, GainActionPoints, SpendActionPoints
from source.gameplay.gameplay_enums import TurnPhase
from source.gameplay.lane import init_lanes
from source.gameplay.combat import get_active_combat_lanes, resolve_attack

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

    player_one = Player("Player 1", 25)
    player_two = Player("Player 2", 25)
    player_one.assign_opponent(player_two)
    player_two.assign_opponent(player_one)

    subscribe_players_global_abilities()

    init_lanes((player_one, player_two))

def subscribe_players_global_abilities():
    player_one.start_of_turn.subscribe(DrawCards(None, player_one, 1).resolve)
    player_two.start_of_turn.subscribe(DrawCards(None, player_two, 1).resolve)
    player_one.start_of_turn.subscribe(GainActionPoints(None, player_one, 2).resolve)
    player_two.start_of_turn.subscribe(GainActionPoints(None, player_two, 2).resolve)
    player_one.end_of_turn.subscribe(SpendActionPoints(None, player_one, -1).resolve)
    player_two.end_of_turn.subscribe(SpendActionPoints(None, player_two, -1).resolve)

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
        active_player.start_of_turn.invoke()
    elif turn_phase is TurnPhase.P2_Main:
        active_player = player_two
        active_player.start_of_turn.invoke()

    resolve_main_phase()

def resolve_main_phase():
    print('##############################')
    print(active_player.name, 'main phase')
    while True:
        card = Choice(active_player.hand.cards).resolve()
        if card is None:
            break
        try_play_card(active_player, card)
        if active_player.action_points == 0:
            break
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
    print('##############################')
    print(active_player.name, 'COMBAT PHASE')
    lanes = get_active_combat_lanes(active_player)
    while len(lanes) > 0:
        lane = Choice(lanes).resolve()
        resolve_attack(lane)
        lanes.remove(lane)