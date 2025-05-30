import os
from source.constants import DISCARD_PILE_LABEL_TEXT, HAND_LABEL_TEXT
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

def print_warning(message):
    if not message:
        return
    print_e(message)
    print_subdivider()

def clear_and_warning(warning):
    clear()
    print_warning(warning)

def print_log(warning = None):
    clear_and_warning(warning)
    print(get_log_text())

def print_main_phase(player, turn_counter, action_labels, warning):
    clear_and_warning(warning)
    print(f"{player} MAIN PHASE - ROUND {int(turn_counter / 2 + (turn_counter % 2))}")
    print_divider()
    print_action_labels(action_labels, player, get_card_count_for_collection_label)

def print_inspect_hand(player, action_labels, warning):
    clear_and_warning(warning)
    print(f"{player} HAND ({len(player.hand.cards)})")
    print_divider()
    print_action_labels(action_labels, player)
    exit()

def print_inspect_lanes(player, action_labels, warning):
    clear_and_warning(warning)

def print_inspect_discard_pile(player, action_labels, warning):
    clear_and_warning(warning)

def print_action_labels(labels, player, label_text_override = None):
    for label in labels:
        text = label_text_override(player, label) if label_text_override is not None else label.text
        print('%-5s -> %s' % (label.symbol, text))

def get_card_count_for_collection_label(player, label):
    if label.text == HAND_LABEL_TEXT:
        return label.text + f' ({len(player.hand.cards)})'
    elif label.text == DISCARD_PILE_LABEL_TEXT:
        return label.text + f' ({len(player.discard.cards)})'
    return label.text

def print_confirmation_dialog(message, warning = None):
    clear_and_warning(warning)
    print(f"{message} [Y/N]")
