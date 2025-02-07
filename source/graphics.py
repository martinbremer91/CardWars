import pygame
from pygame import Surface, Rect
from pygame.font import Font

import main
import configs
import client

from pygame.rect import Rect
import pygame_gui

screen: Surface
font: Font

gui_manager : pygame_gui.UIManager

def init():
    global gui_manager

    init_pygame()
    gui_manager = pygame_gui.UIManager(configs.window_dimensions)
    init_font()
    main.register_update(draw)

def init_pygame():
    global screen

    pygame.init()
    screen = pygame.display.set_mode(configs.window_dimensions)
    pygame.display.set_caption('CARD WARS')
    pygame.mouse.set_visible(1)

def init_font():
    global font
    font = pygame.font.SysFont(None, 24, bold=True)

def draw():
    global gui_manager
    gui_manager.update(configs.timestep)

    screen.fill(configs.bg_color)

    #draw calls
    gui_manager.draw_ui(screen)

    pygame.display.flip()
