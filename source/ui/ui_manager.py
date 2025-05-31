from enum import IntEnum
import source.ui.ui_console as ui_console

class UISetting(IntEnum):
    CONSOLE = 0
    GUI = 1

UI_SETTING = UISetting.CONSOLE

def print_main_phase(player, turn_counter, action_labels, warning):
    match UI_SETTING:
        case UISetting.CONSOLE:
            ui_console.print_main_phase(player, turn_counter, action_labels, warning)
        case GUI:
            ...

def print_inspect_hand(player, action_labels, warning):
    match UI_SETTING:
        case UISetting.CONSOLE:
            ui_console.print_inspect_hand(player, action_labels, warning)
        case UISetting.GUI:
            ...

def print_inspect_card(card, player, action_labels, warning):
    match UI_SETTING:
        case UISetting.CONSOLE:
            ui_console.print_inspect_card(card, player, action_labels, warning)
        case UISetting.GUI:
            ...

def print_inspect_lanes(player, action_labels, warning):
    match UI_SETTING:
        case UISetting.CONSOLE:
            ui_console.print_inspect_lanes(player, action_labels, warning)
        case UISetting.GUI:
            ...

def print_inspect_discard_pile(player, action_labels, warning):
    match UI_SETTING:
        case UISetting.CONSOLE:
            ui_console.print_inspect_discard_pile(player, action_labels, warning)
        case UISetting.GUI:
            ...

def print_confirmation_dialog(message, warning = None):
    match UI_SETTING:
        case UISetting.CONSOLE:
            ui_console.print_confirmation_dialog(message, warning)
        case UISetting.GUI:
            ...

def print_log(warning = None):
    match UI_SETTING:
        case UISetting.CONSOLE:
            ui_console.print_log(warning)
        case UISetting.GUI:
            ...
