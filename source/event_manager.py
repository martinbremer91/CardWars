import pygame
from pygame.locals import *
from main import register_update
import graphics
import input_manager

def init():
    register_update(update)

def update():
    for event in pygame.event.get():
        graphics.gui_manager.process_events(event)
        if event.type == KEYUP:
            if event in input_manager.listen_key_up_events:
                input_manager.process_event(event)
