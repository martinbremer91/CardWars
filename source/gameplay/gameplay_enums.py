from enum import IntEnum

class TurnPhase(IntEnum):
    P1_Main = 0
    P1_Battle = 1
    P2_Main = 2
    P2_Battle = 3

class CollectionType(IntEnum):
    Deck = 0
    Hand = 1
    In_Play = 2
    Discard = 3

class EntityType(IntEnum):
    Creature = 0
    Spell = 1
    Building = 2

class Landscape(IntEnum):
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

class TargetTag(IntEnum):
    Player = 0
    Opponent = 1
    All_Players = 2
    Self = 3
    All_Creatures = 4
    Own_Creatures = 5
    Foe_Creatures = 6
    Adjacent_Creatures = 7
    Opposite_Creature = 8

class TriggerType(IntEnum):
    Start_of_Turn = 0
    End_of_Turn = 1
    Self_Enters_Play = 2
    Self_Exits_Play = 3
    While_in_Play = 4
    When_Self_Attacks = 5
    Cost_Paid = 6

'''
SOT -> global   | SOT, SOT(<condition>)         | only while in play
EOT -> global   | EOT, maybe EOT(<condition>)   | 
SEP -> local    | SEP, SEP(<condition>)         | 
SXP -> local    | SXP, SXP(<condition>)         | 
WIP -> local    | WIP, maybe WIP(<condition>)   | 
WSA -> local    | WSA, WSA(<target>)            | 
CST -> local    | CST([<effect>])               | 
'''