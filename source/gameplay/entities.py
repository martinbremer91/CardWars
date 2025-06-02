from source.gameplay.game_enums import Landscape, EntityType
from source.gameplay.trigger import Trigger
from source.gameplay.cw_lang import parse
from source.gameplay.stat import Stat, IntStat

class GameObject:
    def __init__(self, name, ability_text, cw_lang):
        self.name = Stat(name)
        self.ability_text = ability_text
        self.cw_lang = cw_lang
        self.abilities = list()

    def __str__(self):
        return self.name.__str__()
    def get_parsed_abilities(self):
        parsed_abilities = parse(self.cw_lang, self)
        if parsed_abilities:
            self.abilities.append(parsed_abilities)

class Hero(GameObject):
    def __init__(self, name, player, ability_text, cw_lang):
        super().__init__(name, ability_text, cw_lang)
        self.player = player
        self.self_enters_play = Trigger()
        self.get_parsed_abilities()

    def get_player(self):
        return self.player

class Entity(GameObject):
    def __init__(self, name, landscape, cost, ability_text, cw_lang):
        super().__init__(name, ability_text, cw_lang)
        self.entity_type = Stat(None)
        self.card = None
        self.self_enters_play = Trigger()
        self.self_exits_play = Trigger()
        self.start_of_turn = Trigger()
        self.end_of_turn = Trigger()
        self.land = Stat(landscape)
        self.cost = IntStat(cost)
        self.get_parsed_abilities()

    def __str__(self):
        return self.name.__str__()

    def get_player(self):
        return self.card.player

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
        self.damage_taken_changed = Trigger()
        super().__init__(name, landscape, cost, ability_text, cw_lang)
        self.entity_type = Stat(EntityType.Creature)
        self.attack = IntStat(attack)
        self.defense = IntStat(defense)
        self.damage = Stat(0)
        self.exhausted = Stat(False)
        self.flooped = Stat(False)

    def on_play(self):
        print(f"{self.card.player.name} played {self.name} ({self.land} Creature)\n")
        super().on_play()
    def place_on_lane(self, lane):
        lane.creature = self
    def take_damage(self, damage):
        if damage > 0:
            self.damage.add_modifier(self.damage + damage, self.self_exits_play)
            self.damage_taken_changed.invoke()
        if self.damage >= self.defense:
            self.destroy()
    def heal_damage(self, value):
        if value > 0:
            self.damage.add_modifier(max(0, self.damage - value), self.self_exits_play)
            self.damage_taken_changed.invoke()
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
        print(f"{self.card.player.name} played {self} ({self.land} Spell)\n")
        super().on_play()

class Building(Entity):
    def __init__(self, name, landscape, cost, ability_text, cw_lang):
        super().__init__(name, landscape, cost, ability_text, cw_lang)
        self.entity_type = EntityType.Building

    def on_play(self):
        print(f"{self.card.player} played {self.name} ({self.land.value} Building)\n")
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
