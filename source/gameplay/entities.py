from source.gameplay.game_enums import Landscape, EntityType, TriggerType
from source.gameplay.trigger import Trigger
from source.gameplay.cw_lang import parse

class Entity:
    def __init__(self, name, landscape, cost, ability_text, cw_lang):
        self.entity_type = None
        self.card = None
        self.name = name
        self.base_land = landscape
        self.land = landscape
        self.base_cost = cost
        self.cost = cost
        self.ability_text = ability_text
        self.cw_lang = cw_lang
        self.self_enters_play = Trigger(TriggerType.Self_Enters_Play)
        self.self_exits_play = Trigger(TriggerType.Self_Exits_Play)
        self.abilities = list()
        self.abilities.append(parse(cw_lang, self))

    def __str__(self):
        return self.name

    def assign_card(self, card):
        self.card = card
    def on_play(self):
        self.self_enters_play.invoke()
    def on_exit_play(self):
        self.self_exits_play.invoke()
    def place_on_lane(self, lane):
        pass

class Creature(Entity):
    def __init__(self, name, landscape, cost, ability_text, cw_lang, attack, defense):
        super().__init__(name, landscape, cost, ability_text, cw_lang)
        self.entity_type = EntityType.Creature
        self.base_attack = attack
        self.attack = self.base_attack
        self.base_defense = defense
        self.defense = self.base_defense
        self.damage = 0
        self.exhausted = False
        self.flooped = False

    def on_play(self):
        print(f"{self.card.player.name} played {self.name} ({self.land.name} Creature)\n")
        super().on_play()
    def place_on_lane(self, lane):
        lane.creature = self
    def take_damage(self, damage):
        self.damage += damage
        if self.damage >= self.defense:
            self.destroy()
    def heal_damage(self, value):
        self.damage = max(0, self.damage - value)
    def destroy(self):
        print(self.name, 'destroyed')
        self.card.lane.creature = None
        self.self_exits_play.invoke()
        self.card.destroy()

class Spell(Entity):
    def __init__(self, name, landscape, cost, ability_text, cw_lang):
        super().__init__(name, landscape, cost, ability_text, cw_lang)
        self.entity_type = EntityType.Spell

    def on_play(self):
        print(f"{self.card.player.name} played {self.name} ({self.land.name} Spell)\n")
        super().on_play()

class Building(Entity):
    def __init__(self, name, landscape, cost, ability_text, cw_lang):
        super().__init__(name, landscape, cost, ability_text, cw_lang)
        self.entity_type = EntityType.Building

    def on_play(self):
        print(f"{self.card.player.name} played {self.name} ({self.land.name} Building)\n")
        super().on_play()
    def place_on_lane(self, lane):
        lane.building = self
    def destroy(self):
        print(self.name, 'destroyed')
        self.card.lane.building = None
        self.self_exits_play.invoke()
        self.card.destroy()

def create_creature_from_card_data(card_data) -> Creature:
    name = card_data['name']
    landscape = Landscape.get_landscape_from_str(card_data['landscape'])
    cost = int(card_data['cost'])
    ability_text = card_data['ability']
    cw_lang = card_data['cw-lang']
    attack = int(card_data['attack'])
    defense = int(card_data['defense'])
    return Creature(name, landscape, cost, ability_text, cw_lang, attack, defense)

def create_spell_from_card_data(card_data) -> Spell:
    name = card_data['name']
    landscape = Landscape.get_landscape_from_str(card_data['landscape'])
    cost = int(card_data['cost'])
    ability_text = card_data['ability']
    cw_lang = card_data['cw-lang']
    return Spell(name, landscape, cost, ability_text, cw_lang)

def create_building_from_card_data(card_data) -> Building:
    name = card_data['name']
    landscape = Landscape.get_landscape_from_str(card_data['landscape'])
    cost = int(card_data['cost'])
    ability_text = card_data['ability']
    cw_lang = card_data['cw-lang']
    return Building(name, landscape, cost, ability_text, cw_lang)

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