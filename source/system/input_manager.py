import sys, termios, tty
from enum import IntEnum
from source.ui.ui_manager import UI_SETTING, UISetting

global quit_event
global open_log_event

class Constant:
    ESCAPE = '\\x1b'
    TAB = '\\t'
    Y = 'y'
    N = 'n'

class Result(IntEnum):
    Nominal = 0
    Cancel = 1
    Invalid = 2
    Refresh = 3
    OutOfRange = 4
    Index = 5

class Command:
    def __init__(self, result, raw_input = None):
        self.input = raw_input
        self.result = result
    @staticmethod
    def from_constant(constant):
        match constant:
            case Constant.ESCAPE:
                return Command(Result.Cancel, constant)
            case Constant.TAB:
                return Command(Result.Nominal, constant)
            case Constant.Y:
                return Command(Result.Nominal, constant)
            case Constant.N:
                return Command(Result.Cancel, constant)

class Options:
    def __init__(self, indices_max, constants):
        self.indices_max = indices_max
        self.commands = list()
        for i in range(0, len(constants)):
            self.commands.append(Command.from_constant(constants[i]))
    def validate(self, raw_input) -> Command:
        if raw_input.isdigit():
            if 0 <= int(raw_input) <= self.indices_max:
                return Command(Result.Index, raw_input)
            return Command(Result.OutOfRange, raw_input)
        valid_command = next((c for c in self.commands if c.input == raw_input), None)
        if valid_command:
            return valid_command
        return Command(Result.Invalid, raw_input)

def init(quit_handler, log_handler):
    global quit_event
    global open_log_event
    quit_event = quit_handler
    open_log_event = log_handler

def get_input():
    file_descriptor = sys.stdin.fileno()
    orig = termios.tcgetattr(file_descriptor)
    try:
        tty.setcbreak(file_descriptor)
        return repr(sys.stdin.read(1).lower()).strip('\'')
    except Exception as e:
        raise e
    finally:
        termios.tcsetattr(file_descriptor, termios.TCSAFLUSH, orig)

def await_command(options):
    require_confirm = False
    raw_input = repr(input()) if require_confirm else get_input()
    if UI_SETTING is UISetting.CONSOLE and raw_input == 'x':
        return quit_event()
    if raw_input == '?':
        return open_log_event()
    return options.validate(raw_input)

def await_confirmation():
    constants = [ Constant.ESCAPE, Constant.Y, Constant.N ]
    raw_input = get_input()
    return Options(-1, constants).validate(raw_input)
