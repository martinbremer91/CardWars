from enum import IntEnum

class UserAction:
    def __init__(self, label, action_code):
        self.label = label
        self.action_code = action_code

class ActionLabel:
    def __init__(self, text, symbol = None):
        self.text = text
        self.symbol = symbol

class ActionCode(IntEnum):
    INDEX = 0
    ESCAPE = 1
    SPACE = 2
    TAB = 3
    Y = 4
    N = 5
    def to_repr(self):
        match self:
            case ActionCode.INDEX:
                raise Exception('cannot get code_str of indexed actions')
            case ActionCode.ESCAPE:
                return '\\x1b'
            case ActionCode.SPACE:
                return ' '
            case ActionCode.TAB:
                return '\\t'
            case ActionCode.Y:
                return 'y'
            case ActionCode.N:
                return 'n'
            case _:
                raise Exception(f'Action code not implemented {self}')
    def to_icon(self):
        match self:
            case ActionCode.INDEX:
                raise Exception('cannot get symbol of indexed actions')
            case ActionCode.ESCAPE:
                return '[esc]'
            case ActionCode.SPACE:
                return '[spc]'
            case ActionCode.TAB:
                return '[tab]'
            case ActionCode.Y:
                return 'Y'
            case ActionCode.N:
                return 'N'
            case _:
                raise Exception(f'Action code not implemented {self}')
