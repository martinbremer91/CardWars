from source.gameplay.game_manager import init as game_init
from source.gameplay.game_manager import start_play
from source.system.log import init as log_init
from source.system.input_manager import init as input_init
from source.system.input_manager import Result, await_confirmation
from source.ui.ui_manager import print_confirmation_dialog

def handle_quit_command():
    message = None
    while True:
        print_confirmation_dialog('Are you sure you want to quit?', message)
        command = await_confirmation()
        match command.result:
            case Result.Nominal:
                quit()
            case Result.Invalid:
                message = f'Invalid command: {command.input}'
                continue
            case Result.Cancel:
                return Result.Refresh
            case _:
                raise Exception(f'Result not implemented: {command.result}')

def quit():
    print('User quit the application')
    exit()

log_init()
input_init(handle_quit_command)
game_init()

start_play()
