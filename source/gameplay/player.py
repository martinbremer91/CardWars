from source.gameplay.game_enums import CollectionType, TriggerType
from source.gameplay.card import Collection
from source.gameplay.trigger import Trigger

class Player:
    def __init__(self, name):
        self.name = name
        self.opponent = None
        self.damage = 0
        self.defense = 25
        self.action_points = 0
        self.lanes = list()
        self.landscapes = dict()
        self.deck = Collection(self, CollectionType.Deck)
        self.hand = Collection(self, CollectionType.Hand)
        self.cards_in_play = Collection(self, CollectionType.In_Play)
        self.discard = Collection(self, CollectionType.Discard)
        self.start_of_turn = Trigger(TriggerType.Start_of_Turn)
        self.end_of_turn = Trigger(TriggerType.End_of_Turn)
    def __str__(self):
        return self.name

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

    def win_game(self):
        print(self.name, 'wins!')
        exit()
    def lose_game(self):
        self.opponent.win_game()

    def take_damage(self, amount):
        self.damage += amount
        if self.get_hp() < 1:
            self.lose_game()
    def heal_damage(self, amount):
        self.damage = max(self.damage - amount, 0)
    def get_hp(self):
        return max(self.defense - self.damage, 0)

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