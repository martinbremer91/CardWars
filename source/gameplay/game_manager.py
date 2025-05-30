from source.constants import DISCARD_PILE_LABEL_TEXT, HAND_LABEL_TEXT
from source.gameplay.action_logic import get_action_indices_min_max, set_index_label_symbols
from source.gameplay.player import Player
from source.gameplay.card import set_up_decks, inspect_hand, inspect_lanes, inspect_discard_pile
from source.gameplay.target import Choice
from source.gameplay.effect import DrawCards, GainActionPoints
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
    main_phase_actions = list()
    main_phase_actions.append(UserAction(ActionLabel(HAND_LABEL_TEXT), ActionCode.INDEX, inspect_hand))
    main_phase_actions.append(UserAction(ActionLabel('Lanes'), ActionCode.INDEX, inspect_lanes))
    main_phase_actions.append(UserAction(ActionLabel(DISCARD_PILE_LABEL_TEXT), ActionCode.INDEX, inspect_discard_pile))
    main_phase_actions.append(UserAction(ActionLabel('Pass Turn', pass_turn_action_code.to_symbol()), pass_turn_action_code))
    set_index_label_symbols(main_phase_actions)

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
    action_codes = [a.action_code for a in main_phase_actions]
    action_indices_min_max = get_action_indices_min_max(main_phase_actions)
    while True:
        print_main_phase(active_player, turn_counter, labels, warning)
        command = await_command(Options(action_codes, action_indices_min_max))
        match command.result:
            case Result.Nominal:
                # TODO: add confirmation dialogue before pass turn if player still has Action Points
                if command.code_repr == pass_turn_action_code.to_repr():
                    break
                raise Exception(f'Nominal result but code repr not implemented: {command.code_repr}')
            case Result.Index:
                if command.code_repr is None or not command.code_repr.isdigit():
                    raise Exception("Command code is None or is not a digit")
                main_phase_actions[int(command.code_repr) - 1].subscriber(active_player)
                warning = None
            case Result.OutOfRange:
                warning = f"Index out of range: \'{command.code_repr}\'"
            case Result.Invalid:
                warning = f"Invalid command: \'{command.code_repr}\'"
            case Result.Refresh:
                warning = None
            case _:
                raise Exception(f'Result not implemented: {command.result}')
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
