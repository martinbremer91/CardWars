from enum import IntEnum

class CustomEnum(IntEnum):
    def __str__(self):
        return self.name

class TurnPhase(CustomEnum):
    P1_Main = 0
    P1_Battle = 1
    P2_Main = 2
    P2_Battle = 3

class CollectionType(CustomEnum):
    Deck = 0
    Hand = 1
    InPlay = 2
    Discard = 3

class EntityType(CustomEnum):
    Creature = 0
    Spell = 1
    Building = 2

class Landscape(CustomEnum):
    Rainbow = 0
    BluePlains = 1
    NiceLands = 2
    Cornfield = 3
    IcyLands = 4
    SandyLands = 5
    UselessSwamp = 6
    LavaFlats = 7

    @staticmethod
    def get_landscape_from_str(string):
        match string:
            case 'Rainbow':
                return Landscape.Rainbow
            case 'BluePlains':
                return Landscape.BluePlains
            case 'NiceLands':
                return Landscape.NiceLands
            case 'CornFields':
                return Landscape.Cornfield
            case 'IcyLands':
                return Landscape.IcyLands
            case 'SandyLands':
                return Landscape.SandyLands
            case 'UselessSwamp':
                return Landscape.UselessSwamp
            case 'LavaFlats':
                return Landscape.LavaFlats
            case _:
                raise Exception("Invalid string: cannot return Landscape")

class TargetTag(CustomEnum):
    Player = 0
    Opponent = 1
    All_Players = 2
    Self = 3
    All_Creatures = 4
    Own_Creatures = 5
    Foe_Creatures = 6
    Adjacent_Creatures = 7
    Opposite_Creature = 8

class StatType(CustomEnum):
    Attack = 0
    Defense = 1
    Damage = 2

class ConditionType(CustomEnum):
    Equals = 0
    NotEquals = 1
    Greater_Than = 2
    Less_Than = 3
    Greater_Equal = 4
    Less_Equal = 5
    Is = 6
    Is_Not = 7



'''
TRIGGERS

NAME                | CODE  | VARIANTS              | EFFECTS TRIGGER                         
----------------------------------------------------------------------------------------------
start of turn       | SOT   | SOT, SOT(<condition>) | game_object.get_player().start_of_turn  
end of turn         | EOT   | EOT, EOT(<condition>) | game_object.get_player().end_of_turn    
self enters play    | SEP   | SEP, SEP(<condition>) | game_object.self_enters_play            
self exits play     | SXP   | SXP, SXP(<condition>) | game_object.self_exits_play             
when self attacks   | WSA   | WSA, WSA(<target>)    | game_object.self_attacks                
cost paid           | CST   | CST([<effect>])       | cost_trigger (append to cost_triggers)  
'''
