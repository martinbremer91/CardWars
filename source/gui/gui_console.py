import os
from source.system.log import get_log_text

def clear():
    os.system('clear')

def print_log():
    clear()
    print(get_log_text())
