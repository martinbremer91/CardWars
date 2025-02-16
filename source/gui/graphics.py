import pygame
from pygame import Surface, Rect
from pygame.font import Font

from source import main
from source.system import configs

import pygame_gui

screen: Surface
font: Font

# gui_manager : pygame_gui.UIManager
# text_input_line : pygame_gui.elements.ui_text_entry_line.UITextEntryLine

def init():
    init_pygame()
    init_font()

def register_update():
    main.register_update(draw)

def init_pygame():
    global screen

    pygame.init()
    screen = pygame.display.set_mode(configs.window_dimensions)
    pygame.display.set_caption('CARD WARS')
    pygame.mouse.set_visible(True)

def init_font():
    global font
    font = pygame.font.SysFont(None, 24, bold=True)

def draw(delta_time):
    screen.fill(configs.bg_color)
    pygame.display.update()
