from source.gameplay.gameplay_enums import Landscape, EntityType, TargetTag
from source.gameplay.game_logic import Ability, Trigger, DealDamage, Choice

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
        self.abilities = list()
        self.parse_cw_lang()

    def __str__(self):
        return self.name

    def parse_cw_lang(self):
        ...
        # self.abilities.append(Ability(Trigger(), [DealDamage(self, Choice(TargetTag.Foe_Creatures), 1)]))
    def assign_card(self, card):
        self.card = card
    def on_play(self):
        # <placeholder>
        self.abilities[0].trigger.invoke(None)
        # </placeholder>
    def place_on_lane(self, lane):
        pass

class Creature(Entity):
    def __init__(self, name, landscape, cost, ability_text, cw_lang, attack, defense):
        super().__init__(name, landscape, cost, ability_text, cw_lang, )
        self.entity_type = EntityType.Creature
        self.base_attack = attack
        self.base_defense = defense
        self.attack = self.base_attack
        self.defense = self.base_defense
        self.exhausted = False
        self.flooped = False

    def on_play(self):
        print(f"{self.card.player.name} played {self.name} ({self.land.name} Creature)\n")
        super().on_play()
    def place_on_lane(self, lane):
        lane.creature = self
        self.on_play()
    def take_damage(self, damage):
        self.defense = max(self.defense - damage, 0)
        if self.defense == 0:
            self.destroy()
    def destroy(self):
        self.card.lane.creature = None
        self.card.destroy()
        # TODO: invoke on_leave_play
        print(self.name, 'destroyed')

class Spell(Entity):
    def __init__(self, name, landscape, cost, ability_text, cw_lang):
        super().__init__(name, landscape, cost, ability_text, cw_lang)
        self.entity_type = EntityType.Creature

    def play_spell(self):
        # structurally analogous to Creature.place_on_lane
        self.on_play()
    def on_play(self):
        print(f"{self.card.player.name} played {self.name} ({self.land.name} Spell)\n")

class Building(Entity):
    def __init__(self, name, landscape, cost, ability_text, cw_lang):
        super().__init__(name, landscape, cost, ability_text, cw_lang)
        self.entity_type = EntityType.Building

    def on_play(self):
        print(f"{self.card.player.name} played {self.name} ({self.land.name} Building)\n")
    def place_on_lane(self, lane):
        lane.building = self
        self.on_play()
    def destroy(self):
        self.card.lane.building = None
        self.card.destroy()
        # TODO: invoke on_leave_play
        print(self.name, 'destroyed')

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