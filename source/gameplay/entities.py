from source.gameplay.gameplay_enums import Landscape, EntityType

class Entity:
    def __init__(self, name, landscape, cost):
        self.entity_type = None
        self.name = name
        self.base_land = landscape
        self.land = landscape
        self.base_cost = cost
        self.cost = cost

    def on_play(self):
        pass
    def place_on_lane(self, lane):
        pass

class Creature(Entity):
    def __init__(self, name, landscape, cost, attack, defense):
        super().__init__(name, landscape, cost)
        self.entity_type = EntityType.Creature
        self.base_attack = attack
        self.base_defense = defense
        self.attack = self.base_attack
        self.defense = self.base_defense
        self.exhausted = False
        self.flooped = False

    def on_play(self):

        print(f"Played {self.land.name} Creature")
    def place_on_lane(self, lane):
        lane.creature = self
    def take_damage(self, damage):
        self.defense = max(self.defense - damage, 0)
        if self.defense == 0:
            self.destroy()
    def destroy(self):
        # TODO: discard card
        # TODO: remove from lane
        # TODO: invoke on_leave_play
        print(self.name, 'destroyed')

class Spell(Entity):
    def __init__(self, name, landscape, cost):
        super().__init__(name, landscape, cost)
        self.entity_type = EntityType.Creature

    def on_play(self):
        print(f"Played {self.land.name} Spell")

class Building(Entity):
    def __init__(self, name, landscape, cost):
        super().__init__(name, landscape, cost)
        self.entity_type = EntityType.Building

    def on_play(self):
        print(f"Played {self.land.name} Building")
    def place_on_lane(self, lane):
        lane.building = self
    def destroy(self):
        # TODO: discard card
        # TODO: remove from lane
        # TODO: invoke on_leave_play
        print(self.name, 'destroyed')

def create_creature_from_card_data(card_data) -> Creature:
    name = card_data['name']
    landscape = Landscape.get_landscape_from_str(card_data['landscape'])
    cost = int(card_data['cost'])
    attack = int(card_data['attack'])
    defense = int(card_data['defense'])
    return Creature(name, landscape, cost, attack, defense)

def create_spell_from_card_data(card_data) -> Spell:
    name = card_data['name']
    landscape = Landscape.get_landscape_from_str(card_data['landscape'])
    cost = int(card_data['cost'])
    return Spell(name, landscape, cost)

def create_building_from_card_data(card_data) -> Building:
    name = card_data['name']
    landscape = Landscape.get_landscape_from_str(card_data['landscape'])
    cost = int(card_data['cost'])
    return Building(name, landscape, cost)

def get_entity_kind_from_string(kind_str) -> EntityType:
    match kind_str.lower():
        case "creature":
            return EntityType.Creature
        case "spell":
            return EntityType.Spell
        case "building":
            return EntityType.Building
        case _:
            raise Exception("Could not return ")

def get_entity_from_kind(kind, card_data) -> Entity:
    match kind:
        case EntityType.Creature:
            return create_creature_from_card_data(card_data)
        case EntityType.Spell:
            return create_spell_from_card_data(card_data)
        case EntityType.Building:
            return create_building_from_card_data(card_data)
        case _:
            raise Exception("Invalid EntityKind")