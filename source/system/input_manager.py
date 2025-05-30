﻿import sys, termios, tty
from enum import IntEnum
from source.ui.ui_manager import UI_SETTING, UISetting

global quit_event
global open_log_event

class Result(IntEnum):
    Nominal = 0
    Cancel = 1
    Invalid = 2
    Refresh = 3
    OutOfRange = 4
    Index = 5
    Filter = 6

class Options:
    def __init__(self, action_codes, indices_min_max = (0, 0)):
        self.action_codes = list()
        for i in range(0, len(action_codes)):
            self.action_codes.append(action_codes[i])
        self.indices_min = indices_min_max[0]
        self.indices_max = indices_min_max[1]
    def validate(self, raw_input):
        if raw_input.isdigit():
            if self.indices_min <= int(raw_input) <= self.indices_max:
                if self.indices_max > 9 and not self.check_unambiguous(raw_input):
                    return Command(Result.Filter, raw_input)
                return Command(Result.Index, raw_input)
            return Command(Result.OutOfRange, raw_input)
        valid_code = next((c for c in self.action_codes if c.to_repr() == raw_input), None)
        if valid_code:
            return Command(Result.Nominal, valid_code.to_repr())
        return Command(Result.Invalid, raw_input)
    def check_unambiguous(self, input) -> bool:
        indices_max_first_digit = int(str(self.indices_max)[0])
        return int(input) > indices_max_first_digit

class Command:
    def __init__(self, result, code_repr = None):
        self.result = result
        self.code_repr = code_repr

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

def await_command(options, incl_global_cmds = True):
    require_confirm = False
    raw_input = repr(input()) if require_confirm else get_input()
    if incl_global_cmds:
        if UI_SETTING is UISetting.CONSOLE and raw_input == 'x':
            return quit_event()
        if raw_input == '?':
            return open_log_event()
    return options.validate(raw_input)
