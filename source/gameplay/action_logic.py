from source.system.input_manager import Command, Options, Result, await_command
from source.ui.ui_manager import print_confirmation_dialog, print_log
from source.gameplay.action_data import ActionCode

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
            case Result.Cancel:
                return Command(Result.Refresh)
            case _:
                warning = f'Invalid command'
                continue

def await_confirmation(message):
    warning = None
    action_codes = [ 
        ActionCode.ESCAPE.to_repr(), 
        ActionCode.Y.to_repr(), 
        ActionCode.N.to_repr(), ]
    while True:
        print_confirmation_dialog(message, warning)
        command = await_command(Options(action_codes), False)
        match command.result:
            case Result.Nominal:
                return Command(Result.Nominal)
            case Result.Invalid:
                warning = f'Invalid command'
                continue
            case Result.Cancel:
                return Command(Result.Cancel)
            case _:
                raise Exception(f'Result not implemented: {command.result}')
