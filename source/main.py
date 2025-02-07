import asyncio
from typing import Callable
import configs
import event_manager
import graphics
import client

async def main():
    configs.init()
    graphics.init()
    event_manager.init()
    client.init()

    while configs.running:
        for update in configs.update_methods:
            update()
        await asyncio.sleep(configs.timestep)

def register_update(update: Callable):
    configs.update_methods.append(update)

def quit_app():
    configs.running = False

def toggle_paused():
    configs.paused = not configs.paused

if __name__ == '__main__':
    asyncio.run(main())
