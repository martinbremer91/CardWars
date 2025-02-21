from source.gameplay.gameplay_enums import CollectionType
from source.gameplay.card import Collection

class Player:
    def __init__(self, name, hp):
        self.name = name
        self.opponent = None
        self.hp = hp
        self.action_points = 0
        self.lanes = list()
        self.landscapes = dict()
        self.deck = Collection(self, CollectionType.Deck)
        self.hand = Collection(self, CollectionType.Hand)
        self.cards_in_play = Collection(self, CollectionType.In_Play)
        self.discard = Collection(self, CollectionType.Discard)

    def assign_opponent(self, opponent):
        self.opponent = opponent
    def get_collection(self, collection_type) -> Collection:
        match collection_type:
            case CollectionType.Deck:
                return self.deck
            case CollectionType.Hand:
                return self.hand
            case CollectionType.In_Play:
                return self.cards_in_play
            case CollectionType.Discard:
                return self.discard
            case _:
                raise Exception("No valid Collection given")

    def take_damage(self, amount):
        self.hp = max(self.hp - amount, 0)
    def heal_damage(self, amount):
        self.hp = min(self.hp + amount, 25)

    def gain_action_points(self, amount):
        self.action_points += amount
    def spend_action_points(self, amount):
        if self.action_points - amount < 0:
            raise Exception(f"{self.name}: player cannot have negative number of action points")
        else:
            self.action_points -= amount

    def add_landscape(self, landscape):
        if landscape in self.landscapes.keys():
            self.landscapes[landscape] += 1
        else:
            self.landscapes[landscape] = 1
    def remove_landscape(self, landscape):
        if landscape not in self.landscapes.keys():
            raise Exception(f"{self.name}: attempted to remove landscape type ({landscape.name}) "
                            f"but player has none")
        else:
            self.landscapes[landscape] -= 1
            if self.landscapes[landscape] == 0:
                self.landscapes.pop(landscape)