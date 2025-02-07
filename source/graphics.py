import pygame
from pygame import Surface, Rect
from pygame.font import Font

import main
import configs
import client

import pygame_gui

screen: Surface
font: Font

gui_manager : pygame_gui.UIManager
text_input_line : pygame_gui.elements.ui_text_entry_line.UITextEntryLine

def init():
    global gui_manager

    init_pygame()
    gui_manager = pygame_gui.UIManager(configs.window_dimensions)
    init_font()
    init_network_ui()

def init_network_ui():
    global text_input_line

    pygame_gui.elements.UITextBox(client.external_ip, relative_rect=pygame.Rect((350, 200), (200, 50)),
                                        manager = gui_manager, object_id="test_ip_text")

    text_input_line = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 275), (200, 50)),
                                        manager=gui_manager, object_id="test_input_field")


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
    global gui_manager
    global text_input_line

    gui_manager.update(delta_time)

    screen.fill(configs.bg_color)

    #draw calls
    gui_manager.draw_ui(screen)

    pygame.display.update()
