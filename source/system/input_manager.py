from source.main import quit_app, toggle_paused
import pygame
from pygame.locals import *

listen_keys = [pygame.K_ESCAPE, pygame.K_SPACE]

def process_event(event):
    if event.type == pygame.QUIT or (event.type == KEYUP and event.key == pygame.K_ESCAPE):
        on_quit_request()
        return
    if event.type == KEYUP and event.key == pygame.K_SPACE:
        on_pause_request()

def on_quit_request():
    quit_app()

def on_pause_request():
    toggle_paused()
