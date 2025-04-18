import asyncio
import sys
from typing import Callable

import pygame

import source.system.configs as configs
import source.system.event_manager as event_manager
import gui.graphics as graphics

async def main():
    configs.init()
    graphics.init()

    event_manager.register_update()
    graphics.register_update()

    clock = pygame.time.Clock()

    while True:
        pg_delta_time = clock.tick(60)/1000

        for update in configs.update_methods:
            update(pg_delta_time)

def register_update(update: Callable):
    configs.update_methods.append(update)

def quit_app():
    pygame.quit()
    sys.exit()

def toggle_paused():
    configs.paused = not configs.paused

if __name__ == '__main__':
    asyncio.run(main())
