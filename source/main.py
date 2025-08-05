from source.gameplay.game_manager import init as game_init
from source.gameplay.game_manager import start_play
from source.system.log import init as log_init, push_log_entry
from source.system.input_manager import init as init_input
from source.gameplay.action_logic import handle_log_action, handle_quit_action
from source.gameplay.action_logic import init as init_action_logic
from source.ui.ui_manager import init_gui

def quit():
    print('User quit the application')
    push_log_entry()
    exit()

log_init()
game_init()

init_action_logic(quit)
init_input(handle_quit_action, handle_log_action)

init_gui(quit)

start_play()
