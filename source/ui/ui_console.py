import os
from source.system.log import get_log_text, add_message, LOG_GREEN_MSG, LOG_HL_MSG, LOG_ERRORS, LOG_WARNINGS

class Color:
    DEFAULT = '\033[0m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_g(message):
    if LOG_GREEN_MSG:
        add_message(f'GREEN: {message}')
    print(Color.OKGREEN + message + Color.DEFAULT)
def print_w(message):
    if LOG_WARNINGS:
        add_message(f'WARNING: {message}')
    print(Color.WARNING + message + Color.DEFAULT)
def print_e(message):
    if LOG_ERRORS:
        add_message(f'ERROR: {message}')
    print(Color.ERROR + message + Color.DEFAULT)
def print_h(message):
    if LOG_HL_MSG:
        add_message(f'HIGHLIGHTED: {message}')
    print(Color.OKCYAN + message + Color.DEFAULT)

def clear():
    os.system('clear')

def print_divider():
    print("========================================\n")

def print_subdivider():
    print("----------------------------------------\n")

def print_warning_message(message):
    if not message:
        return
    print_e(message)
    print_subdivider()

def print_log(warning = None):
    clear()
    print_warning_message(warning)
    print(get_log_text())

def print_main_phase(player, turn_counter, action_labels, warning):
    clear()
    print_warning_message(warning)
    print(f"{player} MAIN PHASE - ROUND {int(turn_counter / 2 + (turn_counter % 2))}")
    print_divider()

    # print '%-12i%-12i' % (10 ** i, 20 ** i)

    for label in action_labels:
        print('%-5s -> %s' % (label.symbol, label.text))
        # print(f'{label.symbol} -> {label.text}')

def print_choice():
    clear()

def print_confirmation_dialog(message, warning = None):
    clear()
    print_warning_message(warning)
    print(f"{message} [Y/N]")
