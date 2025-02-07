from typing import Callable

# app configs
update_methods: list[Callable]
timestep: float
running: bool
paused: bool

# graphics configs
window_dimensions: (int, int) = (1200, 600)
margins: (int, int, int, int) = (20, 20, 20, 20)
bg_color: (int, int, int) = (127, 127, 127)

def init():
    global update_methods
    global timestep
    global running
    global paused

    update_methods = list()
    timestep = 0.02
    running = True
    paused = False
