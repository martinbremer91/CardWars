import os
from source.system.log import get_log_text

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
def clear():
    os.system('clear')

def print_divider():
    print("========================================\n")

def print_subdivider():
    print("----------------------------------------\n")

def print_log():
    clear()
    print(get_log_text())

def print_main_phase(player):
    clear()
    print(f"{player} MAIN PHASE")
    print_divider()
    
def print_choice():
    clear()

def print_confirmation_dialog(message, warning = None):
    clear()
    if warning:
        print_e(warning)
        print_subdivider()
    print(f"{message} [Y/N]")
