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