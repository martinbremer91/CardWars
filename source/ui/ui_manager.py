from enum import IntEnum
from source.gameplay.action_data import ActionType
import source.ui.ui_console as ui_console

class UISetting(IntEnum):
    CONSOLE = 0
    GUI = 1

UI_SETTING = UISetting.CONSOLE

def print_action(context, action_labels, warning):
    match context.type:
        case ActionType.MAIN_PHASE:
            print_main_phase(context.player, context.data, action_labels, warning)
        case ActionType.INSPECT_HAND:
            print_inspect_hand(context.player, action_labels, warning)
        case ActionType.INSPECT_CARD:
            print_inspect_card(context.player, context.data, action_labels, warning)

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

def print_inspect_card(player, card, action_labels, warning):
    match UI_SETTING:
        case UISetting.CONSOLE:
            ui_console.print_inspect_card(player, card, action_labels, warning)
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
