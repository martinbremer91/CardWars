from source.gameplay.gameplay_enums import Landscape, EntityKind
from typing import Optional

class Entity:
    def __init__(self, name : str, landscape : Landscape, cost : int):
        self.kind : Optional[EntityKind] = None
        self.name : str = name
        self.base_land : Landscape = landscape
        self.land = landscape
        self.base_cost : int = cost
        self.cost : int = cost

    def on_play(self):
        pass

class Creature(Entity):
    def __init__(self, name : str, landscape : Landscape, cost : int):
        super().__init__(name, landscape, cost)
        self.kind = EntityKind.Creature

    def on_play(self):
        super().on_play()
        print("Played Creature")

class Spell(Entity):
    def __init__(self, name : str, landscape : Landscape, cost : int):
        super().__init__(name, landscape, cost)
        self.kind = EntityKind.Creature

    def on_play(self):
        super().on_play()
        print("Played Spell")

class Building(Entity):
    def __init__(self, name : str, landscape : Landscape, cost : int):
        super().__init__(name, landscape, cost)
        self.kind = EntityKind.Building

    def on_play(self):
        super().on_play()
        print("Played Building")