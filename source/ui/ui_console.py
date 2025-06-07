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

divider = "======================================================================="

def get_print_width():
    return len(divider)

def print_divider():
    print(divider)

def print_subdivider():
    print(divider.replace('=', '-'))

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

def print_inspect_card(player, card, action_labels, warning):
    clear_and_warning(warning)
    name = card.entity.name if card.player == player else card.entity.name + f" ({card.player})"
    print(f"{name} - {card.entity.land.value} {card.entity.entity_type.value}")
    print(f"Cost: {card.entity.cost.value} (current AP: {player.action_points.value})")
    print_subdivider()
    print_width = get_print_width()
    ability_str_lines = break_up_string_into_lines(card.entity.ability_text, print_width).splitlines()
    for line in ability_str_lines:
        print(line.center(print_width))
    if hasattr(card.entity, 'defense'):
        print_subdivider()
        atk_str = f"ATK {card.entity.attack.value}"
        def_str = f"DEF {card.entity.defense.value}"
        def_max_width = get_print_width() - 10
        print(f"{atk_str:<10}{def_str:>{def_max_width}}")
    print_divider()
    print_action_labels(action_labels, player)

def break_up_string_into_lines(text, line_length) -> str:
    if len(text) <= line_length:
        return text
    current_index = 0
    break_indices = list()
    finished = False
    while not finished:
        range_end = min(current_index + line_length - 1, len(text))
        current_range = range(current_index, range_end)
        for i in current_range:
            if i == len(text) - 1:
                finished = True
                break
            if text[i].isspace():
                current_index  = i
        if not break_indices or len(text[break_indices[-1]:]) >= line_length:
            break_indices.append(current_index)
    for index in break_indices:
        text = text[:index] + '\n' + text[index + 1:]
    return text

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
