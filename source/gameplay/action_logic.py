from typing import Callable
from source.system.input_manager import Command, Options, Result, await_command
from source.ui.ui_manager import print_action, print_confirmation_dialog, print_log
from source.gameplay.action_data import ActionCode, ActionContext, ActionLabel, ActionType, UserAction

global quit_action

def init(quit):
    global quit_action
    quit_action = quit

class ActionRegistry:
    main_phase_action : Callable
    inspect_hand_action : Callable
    inspect_card_action : Callable
    inspect_lanes_action : Callable
    inspect_discard_pile_action : Callable
    @staticmethod
    def get():
        return action_registry

action_registry = ActionRegistry()

def resolve_user_action(context, refresh_actions, actions = None, refresh = True):
    warning = None
    while True:
        if refresh_actions is not None:
            actions = refresh_actions(context)
        if actions is None:
            raise Exception('User actions cannot be None')
        labels = [a.label for a in actions]
        action_codes = [c.action_code for c in actions]
        print_action(context, labels, warning)
        warning = None
        indices_min_max = get_action_indices_min_max(actions)
        command = await_command(Options(action_codes, indices_min_max))
        match command.result:
            case Result.Nominal:
                if command.code_repr == ActionCode.ESCAPE.to_repr() or ActionCode.SPACE.to_repr():
                    break
                elif command.code_repr == ActionCode.RETURN.to_repr():
                    selected_user_action = get_user_action_with_code(command.code_repr, actions)
                    if selected_user_action.subscriber_action_type is not None:
                        selected_action_ctx = ActionContext(selected_user_action.subscriber_action_type, context.player, selected_user_action)
                        process_selected_action(selected_user_action, selected_action_ctx)
                        if not refresh:
                            break
                else:
                    raise Exception(f'Command result is Nominal but code_repr is not implemented')
            case Result.Index:
                selected_user_action = get_user_action_with_index(command.code_repr, actions)
                if selected_user_action.subscriber_action_type is not None:
                    selected_action_ctx = ActionContext(selected_user_action.subscriber_action_type, context.player, selected_user_action)
                    process_selected_action(selected_user_action, selected_action_ctx)
                    if not refresh:
                        break
            case Result.OutOfRange:
                warning = f'Index out of range: \'{command.code_repr}\''
            case Result.Invalid:
                warning = f'Invalid command: \'{command.code_repr}\''
            case Result.Refresh:
                if not refresh:
                    break
            case Result.Filter:
                filtered_actions = get_filtered_actions(actions, command.code_repr)
                resolve_user_action(context, None, filtered_actions, False)

def process_selected_action(action, context):
    match action.subscriber_action_type:
        case ActionType.MAIN_PHASE:
            action_registry.main_phase_action()
        case ActionType.INSPECT_HAND:
            action_registry.inspect_hand_action(context)
        case ActionType.INSPECT_CARD:
            action_registry.inspect_card_action(context)

def get_filtered_actions(actions, input) -> list:
    input_int = int(input)
    filtered_actions = list()
    for action in actions:
        if action.action_code != ActionCode.INDEX:
            continue
        action_first_digit = int(str(action.label.symbol)[0])
        filtered_action = None
        if input_int == int(action.label.symbol):
            filtered_action = UserAction(ActionLabel(action.label.text, ActionCode.RETURN.to_symbol()), ActionCode.RETURN, action.subscriber_action_type)
        elif input_int == action_first_digit:
            filtered_action = UserAction(ActionLabel(action.label.text), ActionCode.INDEX, action.subscriber_action_type)
        if filtered_action:
            filtered_actions.append(filtered_action)
    back_action = UserAction(ActionLabel('Cancel', ActionCode.ESCAPE.to_symbol()), ActionCode.ESCAPE)
    filtered_actions.append(back_action)
    set_index_label_symbols(filtered_actions, offset = 0)
    return filtered_actions

def handle_quit_action():
    while True:
        command = await_confirmation('Are you sure you want to quit?')
        match command.result:
            case Result.Nominal:
                quit_action()
            case Result.Cancel:
                return Command(Result.Refresh)
            case _:
                raise Exception(f'Result not implemented: {command.result}')

def handle_log_action():
    warning = None
    while True:
        print_log(warning)
        command = await_command(Options([ActionCode.ESCAPE]), False)
        match command.result:
            case Result.Nominal:
                return Command(Result.Refresh)
            case Result.Invalid:
                warning = f'Invalid command : {command.code_repr}'
                continue

def await_confirmation(message):
    warning = None
    action_codes = [ 
        ActionCode.ESCAPE, 
        ActionCode.Y, 
        ActionCode.N, ]
    while True:
        print_confirmation_dialog(message, warning)
        command = await_command(Options(action_codes), False)
        match command.result:
            case Result.Nominal:
                if command.code_repr == ActionCode.Y.to_repr():
                    return Command(Result.Nominal)
                return Command(Result.Cancel)
            case Result.Invalid:
                warning = f'Invalid command : {command.code_repr}'
                continue
            case _:
                raise Exception(f'Result not implemented: {command.result}')

def set_index_label_symbols(actions, offset = 1):
    counter = offset
    for action in actions:
        if action.action_code is ActionCode.INDEX:
            action.label.symbol = str(counter)
            counter += 1

def get_action_indices_min_max(actions) -> tuple[int, int]:
    min = 9999
    max = 0
    for action in actions:
        if action.action_code is not ActionCode.INDEX:
            continue
        index = int(action.label.symbol)
        min = index if index < min else min
        max = index if index > max else max
    return (min, max)

def get_user_action_with_index(index, actions) -> UserAction:
    for action in actions:
        if action.label.symbol == index:
            return action
    raise Exception(f'Could not find action with index \'{index}\'')

def get_user_action_with_code(code, actions) -> UserAction:
    for action in actions:
        if action.action_code.to_repr() == code:
            return action
    raise Exception(f'Could not find action with code \'{code}\'')
