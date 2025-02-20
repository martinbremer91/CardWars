from source.gameplay.gameplay_enums import Landscape, EntityType
from typing import Optional

class Entity:
    def __init__(self, name : str, landscape : Landscape, cost : int):
        self.kind : Optional[EntityType] = None
        self.name : str = name
        self.base_land : Landscape = landscape
        self.land : Landscape = landscape
        self.base_cost : int = cost
        self.cost : int = cost

    def on_play(self):
        pass
    def place_on_lane(self, lane):
        pass

class Creature(Entity):
    def __init__(self, name : str, landscape : Landscape, cost : int, attack : int, defense : int):
        super().__init__(name, landscape, cost)
        self.kind : EntityType = EntityType.Creature
        self.base_attack : int = attack
        self.base_defense : int = defense
        self.attack : int = self.base_attack
        self.defense : int = self.base_defense
        self.exhausted : bool = False
        self.flooped : bool = False

    def on_play(self):
        super().on_play()
        print(f"Played {self.land.name} Creature")
    def place_on_lane(self, lane):
        lane.creature = self

class Spell(Entity):
    def __init__(self, name : str, landscape : Landscape, cost : int):
        super().__init__(name, landscape, cost)
        self.kind : EntityType = EntityType.Creature

    def on_play(self):
        super().on_play()
        print(f"Played {self.land.name} Spell")

class Building(Entity):
    def __init__(self, name : str, landscape : Landscape, cost : int):
        super().__init__(name, landscape, cost)
        self.kind : EntityType = EntityType.Building

    def on_play(self):
        super().on_play()
        print(f"Played {self.land.name} Building")
    def place_on_lane(self, lane):
        lane.building = self

def create_creature_from_card_data(card_data : dict[str,]) -> Creature:
    name : str = card_data['name']
    landscape : Landscape = Landscape.get_landscape_from_str(card_data['landscape'])
    cost : int = int(card_data['cost'])
    attack : int = int(card_data['attack'])
    defense : int = int(card_data['defense'])
    return Creature(name, landscape, cost, attack, defense)

def create_spell_from_card_data(card_data : dict[str,]) -> Spell:
    name : str = card_data['name']
    landscape : Landscape = Landscape.get_landscape_from_str(card_data['landscape'])
    cost : int = int(card_data['cost'])
    return Spell(name, landscape, cost)

def create_building_from_card_data(card_data : dict[str,]) -> Building:
    name : str = card_data['name']
    landscape : Landscape = Landscape.get_landscape_from_str(card_data['landscape'])
    cost : int = int(card_data['cost'])
    return Building(name, landscape, cost)

def get_entity_kind_from_string(kind_str : str) -> EntityType:
    match kind_str.lower():
        case "creature":
            return EntityType.Creature
        case "spell":
            return EntityType.Spell
        case "building":
            return EntityType.Building
        case _:
            raise Exception("Could not return ")

def get_entity_from_kind(kind : EntityType, card_data : dict[str,]) -> Entity:
    match kind:
        case EntityType.Creature:
            return create_creature_from_card_data(card_data)
        case EntityType.Spell:
            return create_spell_from_card_data(card_data)
        case EntityType.Building:
            return create_building_from_card_data(card_data)
        case _:
            raise Exception("Invalid EntityKind")