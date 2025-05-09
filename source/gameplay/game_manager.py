from source.gameplay.player import Player
from source.gameplay.card import set_up_decks, try_play_card
from source.gameplay.target import Choice
from source.gameplay.effect import DrawCards, GainActionPoints, SpendActionPoints
from source.gameplay.game_enums import TurnPhase
from source.gameplay.lane import init_lanes
from source.gameplay.combat import get_active_combat_lanes, resolve_attack  
from source.system.input_manager import await_command, Result, Options
from source.ui.ui_manager import print_main_phase
from source.gameplay.action_data import UserAction, ActionLabel, ActionCode

active_player : Player
player_one : Player
player_two : Player
turn_phase : TurnPhase
turn_counter : int
main_phase_actions : list
combat_phase_actions : list
pass_turn_action_code = ActionCode.SPACE

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
    create_main_phase_user_actions()
    create_combat_phase_user_actions()
    init_lanes((player_one, player_two))

def subscribe_players_global_abilities():
    player_one.start_of_turn.subscribe(DrawCards(None, player_one, 1).resolve)
    player_two.start_of_turn.subscribe(DrawCards(None, player_two, 1).resolve)
    player_one.start_of_turn.subscribe(GainActionPoints(None, player_one, 2).resolve)
    player_two.start_of_turn.subscribe(GainActionPoints(None, player_two, 2).resolve)

def create_main_phase_user_actions():
    global main_phase_actions
    pass_code = pass_turn_action_code
    main_phase_actions = list()
    main_phase_actions.append(UserAction(ActionLabel('Hand'), ActionCode.INDEX))
    main_phase_actions.append(UserAction(ActionLabel('Lanes'), ActionCode.INDEX))
    main_phase_actions.append(UserAction(ActionLabel('Graveyard'), ActionCode.INDEX))
    main_phase_actions.append(UserAction(ActionLabel('Pass Turn', pass_code.to_icon()), pass_code))
    for i in range(1, len(main_phase_actions)):
        if main_phase_actions[i-1].action_code is ActionCode.INDEX:
            main_phase_actions[i-1].label.symbol = str(i)

def create_combat_phase_user_actions():
    global combat_phase_actions
    combat_phase_actions = list()

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
    warning = None
    labels = [a.label for a in main_phase_actions]
    action_codes = [c.action_code for c in main_phase_actions]
    while True:
        print_main_phase(active_player, labels, warning)
        command = await_command(Options(action_codes))
        match command.result:
            case Result.Nominal:
                ...
            case Result.OutOfRange:
                warning = 'Index out of range'
                continue
            case Result.Cancel:
                raise Exception('Cannot cancel MainPhase')
            case Result.Invalid:
                warning = 'Invalid command'
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
