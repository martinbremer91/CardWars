from source.system.input_manager import Command, Options, Result, await_command
from source.ui.ui_manager import print_confirmation_dialog, print_log
from source.gameplay.action_data import ActionCode, UserAction

global quit_action

def init(quit):
    global quit_action
    quit_action = quit

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
        command = await_command(Options([ActionCode.ESCAPE.to_repr()]), False)
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
