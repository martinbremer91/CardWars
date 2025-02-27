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
    print(Color.OKGREEN + message + Color.DEFAULT)
def print_w(message):
    print(Color.WARNING + message + Color.DEFAULT)
def print_e(message):
    print(Color.ERROR + message + Color.DEFAULT)
def print_h(message):
    print(Color.OKCYAN + message + Color.DEFAULT)