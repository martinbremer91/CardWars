from enum import IntEnum

class UserAction:
    def __init__(self, label, action_code, subscriber = None):
        self.label = label
        self.action_code = action_code
        self.subscriber = subscriber

class ActionLabel:
    def __init__(self, text, symbol = None):
        self.text = text
        self.symbol = symbol

class ActionCode(IntEnum):
    INDEX = 0
    ESCAPE = 1
    SPACE = 2
    RETURN = 3
    TAB = 4
    Y = 5
    N = 6
    def to_repr(self):
        match self:
            case ActionCode.INDEX:
                return None
            case ActionCode.ESCAPE:
                return '\\x1b'
            case ActionCode.SPACE:
                return ' '
            case ActionCode.RETURN:
                return '\\n'
            case ActionCode.TAB:
                return '\\t'
            case ActionCode.Y:
                return 'y'
            case ActionCode.N:
                return 'n'
            case _:
                raise Exception(f'Action code not implemented {self}')
    def to_symbol(self):
        match self:
            case ActionCode.INDEX:
                raise Exception('cannot get symbol of indexed actions')
            case ActionCode.ESCAPE:
                return '[esc]'
            case ActionCode.SPACE:
                return '[spc]'
            case ActionCode.RETURN:
                return '[ret]'
            case ActionCode.TAB:
                return '[tab]'
            case ActionCode.Y:
                return 'Y'
            case ActionCode.N:
                return 'N'
            case _:
                raise Exception(f'Action code not implemented {self}')
