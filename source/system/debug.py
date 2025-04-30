import os

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

clear = lambda: os.system('clear')
clear()

cols, rows = (10, 50)
arr = [['']*cols]*rows

position = (5, 5)

def getch():
    import sys, termios, tty

    file_descriptor = sys.stdin.fileno()
    orig = termios.tcgetattr(file_descriptor)

    try:
        tty.setcbreak(file_descriptor)
        return sys.stdin.read(1)
    except Exception as e:
        raise e
    finally:
        termios.tcsetattr(file_descriptor, termios.TCSAFLUSH, orig)

def draw():
    for y in range(cols):
        row = ""
        for x in range(rows):
            if x == position[0] and y == position[1]:
                arr[x][y] = 'X'
            elif x == 0 or y == 0 or x == rows - 1 or y == cols - 1:
                arr[x][y] = '#'
            else:
                arr[x][y] = '-'
            row += arr[x][y]
        print(row)

while True:
    draw()
    cmd = getch()
    if cmd is None:
        continue
    match cmd.lower():
        case 'w':
            pos_y = max(position[1] - 1, 1)
            position = (position[0], pos_y)
        case 'a':
            pos_x = max(position[0] - 1, 1)
            position = (pos_x, position[1])
        case 's':
            pos_y = min(position[1] + 1, cols - 2)
            position = (position[0], pos_y)
        case 'd':
            pos_x = min(position[0] + 1, rows - 2)
            position = (pos_x, position[1])
        case ' ':
            break
        case _:
            pass
    clear()