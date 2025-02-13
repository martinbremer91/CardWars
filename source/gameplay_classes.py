from enum import Enum
from typing import Callable

class TurnPhase(Enum):
    P1_Main = 0
    P1_Battle = 1
    P2_Main = 2
    P2_Battle = 3

class Collection(Enum):
    Deck = 0
    Hand = 1
    In_Play = 2
    Discard = 3

class EntityKind(Enum):
    NULL = 0
    Creature = 1
    Spell = 2
    Building = 3

class Landscape(Enum):
    Rainbow = 0
    BluePlains = 1
    NiceLands = 2
    Cornfield = 3
    IcyLands = 4
    SandyLands = 5
    UselessSwamp = 6
    LavaFlats = 7

class Player:
    def __init__(self, name: str, hp : int):
        self.name : str = name
        self.hp : int  = hp
        self.action_points : int = 0
        self.landscapes : dict[Landscape, int] = dict()

    def take_damage(self, amount : int):
        self.hp = max(self.hp - amount, 0)
    def heal_damage(self, amount : int):
        self.hp = min(self.hp + amount, 25)
    def gain_action_points(self, amount : int):
        self.action_points += amount
    def spend_action_points(self, amount: int):
        if self.action_points - amount < 0:
            raise Exception(f"{self.name}: player cannot have negative number of action points")
        else:
            self.action_points -= amount
    def add_landscape(self, landscape : Landscape):
        if landscape in self.landscapes.keys():
            self.landscapes[landscape] += 1
        else:
            self.landscapes[landscape] = 1
    def remove_landscape(self, landscape : Landscape):
        if landscape not in self.landscapes.keys():
            raise Exception(f"{self.name}: attempted to remove landscape type ({landscape.name}) "
                            f"but player has none")
        else:
            self.landscapes[landscape] -= 1
            if self.landscapes[landscape] == 0:
                self.landscapes.pop(landscape)

class GameEntity:
    def __init__(self, name : str, landscape : Landscape, cost : int):
        self.kind : EntityKind = EntityKind.NULL
        self.name : str = name
        self.base_land : Landscape = landscape
        self.land = landscape
        self.base_cost : int = cost
        self.cost : int = cost

    def on_play(self):
        pass

class Creature(GameEntity):
    def __init__(self, name : str, landscape : Landscape, cost : int):
        super().__init__(name, landscape, cost)
        self.kind = EntityKind.Creature

    def on_play(self):
        super().on_play()
        print("Type of GameEntity: Creature")

class Spell(GameEntity):
    def __init__(self, name : str, landscape : Landscape, cost : int):
        super().__init__(name, landscape, cost)
        self.kind = EntityKind.Creature

    def on_play(self):
        super().on_play()
        print("Type of GameEntity: Spell")

class Building(GameEntity):
    def __init__(self, name : str, landscape : Landscape, cost : int):
        super().__init__(name, landscape, cost)
        self.kind = EntityKind.Building

    def on_play(self):
        super().on_play()
        print("Type of GameEntity: Building")

class Card:
    def __init__(self, owner : Player, game_entity : GameEntity, collection : list):
        self.owner : Player = owner
        self.game_entity : GameEntity = game_entity
        self.collection : list[Card] = collection
        self.collection.append(self)

class Trigger:
    def __init__(self):
        self.subscribers : list[Callable] = list()

    def subscribe(self, subscriber : Callable):
        self.subscribers.append(subscriber)

    def invoke(self, arg = ...):
        for subscriber in self.subscribers:
            subscriber(arg)

class Lane:
    creature: Creature

    def __init__(self, lane_id : int, landscape : Landscape):
        self.lane_id : int = lane_id
        self.landscape : Landscape = landscape
        self.building : list[Building] = list()
        self.flipped_land : bool = False