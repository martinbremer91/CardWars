from source.gameplay.game_manager import init as game_init
from source.gameplay.game_manager import start_play
from source.system.log import init as log_init, push_log_entry
from source.system.input_manager import init as input_init
from source.system.input_manager import Constant, Command, Options, Result, await_command, await_confirmation
from source.ui.ui_manager import print_confirmation_dialog, print_log

def handle_quit_command():
    warning = None
    while True:
        print_confirmation_dialog('Are you sure you want to quit?', warning)
        command = await_confirmation()
        match command.result:
            case Result.Nominal:
                quit()
            case Result.Invalid:
                warning = f'Invalid command: {command.input}'
                continue
            case Result.Cancel:
                return Command(Result.Refresh)
            case _:
                raise Exception(f'Result not implemented: {command.result}')

def handle_log_command():
    warning = None
    while True:
        print_log(warning)
        command = await_command(Options(-1, [ Constant.ESCAPE ]))
        match command.result:
            case Result.Cancel:
                return Command(Result.Refresh)
            case _:
                warning = f'Invalid command: {command.input}'
                continue

def quit():
    print('User quit the application')
    push_log_entry()
    exit()

log_init()
input_init(handle_quit_command, handle_log_command)
game_init()

start_play()
