from enum import Enum

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
    Creature = 0
    Spell = 1
    Building = 2

class Landscape(Enum):
    Rainbow = 0
    BluePlains = 1
    NiceLands = 2
    Cornfield = 3
    IcyLands = 4
    SandyLands = 5
    UselessSwamp = 6
    LavaFlats = 7