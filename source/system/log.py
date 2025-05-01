from datetime import datetime
from source.system.asset_manager import init_log, append_log, read_log

LOG_ERRORS = True
LOG_WARNINGS = True
LOG_GREEN_MSG = True
LOG_HL_MSG = True

global current_entry
global previous_entry

def init():
    global current_entry
    global previous_entry
    current_entry = list()
    previous_entry = list()
    init_log()
    add_message(f'CARD WARS - {datetime.now()}\n\nGAME START')
    push_log_entry()

def get_latest_log():
    return previous_entry

def add_message(message):
    current_entry.append(f"{message}\n")

def push_log_entry():
    global previous_entry
    for item in current_entry:
        append_log(item)
    append_log("=======================================\n")
    previous_entry = current_entry.copy()
    current_entry.clear()

def get_log_text():
    return read_log()
