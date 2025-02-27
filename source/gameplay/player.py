from source.gameplay.game_enums import CollectionType, Landscape
from source.gameplay.card import Collection
from source.gameplay.trigger import Trigger
from source.gameplay.stat import Stat

class Player:
    def __init__(self, name):
        self.name = name
        self.opponent = None
        self.damage = Stat(0)
        self.defense = Stat(25)
        self.action_points = Stat(0)
        self.lanes = list()
        self.deck = Collection(self)
        self.hand = Collection(self)
        self.cards_in_play = Collection(self)
        self.discard = Collection(self)
        self.start_of_turn = Trigger()
        self.end_of_turn = Trigger()
        self.end_of_game = Trigger()
        self.start_of_turn.subscribe(self.invoke_active_entities_start_of_turn)
        self.end_of_turn.subscribe(self.invoke_active_entities_end_of_turn)
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

    def invoke_active_entities_start_of_turn(self):
        for card in self.cards_in_play.cards:
            card.entity.start_of_turn.invoke()
    def invoke_active_entities_end_of_turn(self):
        for card in self.cards_in_play.cards:
            card.entity.end_of_turn.invoke()

    def win_game(self):
        print(self, 'wins!')
        self.end_of_game.invoke()
        exit()
    def lose_game(self):
        self.opponent.win_game()
        self.end_of_game.invoke()

    def take_damage(self, amount):
        self.damage.add_modifier(self.damage + amount, self.end_of_game)
        if self.get_hp() < 1:
            self.lose_game()
    def heal_damage(self, amount):
        self.damage.add_modifier(max(self.damage - amount, 0), self.end_of_game)
    def get_hp(self):
        return max(self.defense - self.damage, 0)

    @property
    def landscapes(self):
        return [lane.landscape for lane in self.lanes]
    def landscape_count(self, land = None):
        if not land:
            return len([l for l in self.landscapes if l is not None])
        return len([l for l in self.landscapes if l is land])