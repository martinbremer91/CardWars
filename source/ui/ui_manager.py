from enum import IntEnum
import source.ui.ui_console as ui_console

class UISetting(IntEnum):
    CONSOLE = 0
    GUI = 1

UI_SETTING = UISetting.CONSOLE

def print_main_phase(player, action_labels, warning):
    match UI_SETTING:
        case UISetting.CONSOLE:
            ui_console.print_main_phase(player, action_labels, warning)
        case GUI:
            # TODO implement ui_gui
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
