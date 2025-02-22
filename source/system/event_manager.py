import pygame
from pygame.locals import *
from source.main import register_update as main_register_update
from source.system import input_manager

def register_update():
    main_register_update(update)

def update(delta_time):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            input_manager.process_event(event)
        elif event.type == KEYUP:
            if event.key in input_manager.listen_keys:
                input_manager.process_event(event)