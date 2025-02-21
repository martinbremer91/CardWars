from source.gameplay.gameplay_enums import Landscape
from source.gameplay.entities import Creature, Building

class Lane:
    def __init__(self, lane_id, player, landscape):
        self.lane_id = lane_id
        self.player = player
        self.creature = None
        self.building = None
        self.landscape = None
        self.flipped_land : bool = False
        self.can_play_creature : bool = True

        if landscape is not None:
            self.assign_landscape(landscape)

        self.player.lanes.append(self)

    def __str__(self):
        return str(self.lane_id)

    def assign_landscape(self, landscape):
        if self.landscape is not None:
            self.player.remove_landscape(landscape)

        self.landscape = landscape
        self.player.add_landscape(landscape)

    def set_flipped_land(self, flipped):
        if self.flipped_land == flipped:
            return

        self.flipped_land = flipped
        if flipped:
            self.player.remove_landscape(self.landscape)
        else:
            self.player.add_landscape(self.landscape)

    def add_entity(self, entity):
        if isinstance(entity, Creature):
            # TODO: entity replacement code
            self.creature = entity
        elif isinstance(entity, Building):
            self.creature = entity
            # TODO: entity replacement code

lanes : list[Lane]

def init_lanes(players):
    global lanes
    lanes = list()

    for l in range(4):
        lanes.append(Lane(l, players[0], Landscape.BluePlains))
        lanes.append(Lane(l + 10, players[1], Landscape.Cornfield))

def get_opposite_lane(lane) -> Lane:
    opposite_index : int = lane.lane_id + 10 if lane.lane_id < 5 else lane.lane_id - 10
    for l in lanes:
        if l.lane_id == opposite_index:
            return l
    raise Exception('Failed to get opposite lane')

def get_adjacent_lanes(lane) -> list:
    output = list()
    for l in lane.player.output:
        if l.lane_id == lane.lane_id - 1 or l.lane_id == lane.lane_id + 1:
            output.append(l)

    return output