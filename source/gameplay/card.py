from player import Player
from game_entities import Entity

class Card:
    def __init__(self, owner : Player, game_entity : Entity, collection : list):
        self.owner : Player = owner
        self.game_entity : Entity = game_entity
        self.collection : list[Card] = collection
        self.collection.append(self)