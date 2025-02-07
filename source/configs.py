from typing import Callable

# app configs
update_methods: list[Callable]
paused: bool

# graphics configs
window_dimensions: (int, int) = (1200, 600)
margins: (int, int, int, int) = (20, 20, 20, 20)
bg_color: (int, int, int) = (127, 127, 127)

def init():
    global update_methods
    global paused

    update_methods = list()
    paused = False
