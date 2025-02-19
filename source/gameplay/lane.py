from typing import Optional
from player import Player
from gameplay_enums import Landscape
from game_entities import Creature, Building

class Lane:
    def __init__(self, lane_id : Optional[int], player: Player, landscape : Optional[Landscape]):
        self.lane_id : Optional[int] = lane_id
        self.player : Player = player
        self.creature : Optional[Creature] = None
        self.building : Optional[Building] = None
        self.landscape : Optional[Landscape] = None
        self.flipped_land : bool = False
        self.can_play_creature : bool = True

        if landscape is not None:
            self.assign_landscape(landscape)

    def assign_landscape(self, landscape : Landscape):
        if self.landscape is not None:
            self.player.remove_landscape(landscape)

        self.landscape = landscape
        self.player.add_landscape(landscape)

    def set_flipped_land(self, flipped : bool):
        if self.flipped_land == flipped:
            return

        self.flipped_land = flipped
        if flipped:
            self.player.remove_landscape(self.landscape)
        else:
            self.player.add_landscape(self.landscape)

def select_lane(options : list[Lane]) -> Lane:
    index : int = -1
    while index < 0 or index >= len(options):
        user_prompt_options : str = ''
        for i in range(len(options)):
            user_prompt_options += f'[{i}]: {options[i].landscape.name}\n'

        print(f'Available Lanes:\n{user_prompt_options}')
        choice = input('Select lane:')
        if not choice.isdigit():
            continue
        choice = int(choice)
        if choice < 0 or choice >= len(options):
            print('invalid lane index')
            continue
        index = choice

    return options[index]