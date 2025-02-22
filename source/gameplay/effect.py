from source.gameplay.game_enums import CollectionType
from source.gameplay.choice import Choice

class Effect:
    def __init__(self, entity):
        self.entity = entity
    def resolve(self):
        pass

class GainActionPoints(Effect):
    def __init__(self, entity, player, amount):
        super().__init__(entity)
        self.player = player
        self.amount = amount
    def resolve(self):
        self.player.action_points += self.amount

class SpendActionPoints(Effect):
    def __init__(self, entity, player, amount):
        super().__init__(entity)
        self.player = player
        self.amount = amount
    def resolve(self):
        to_be_deducted = self.player.action_points if self.amount == -1 else self.amount
        if self.player.action_points - to_be_deducted < 0:
            raise Exception(f"{self.player.name}: player cannot have negative number of action points\n"
                            f"(Player has {self.player.action_points}. To be deducted: {to_be_deducted}")
        self.player.action_points -= to_be_deducted

class DrawCards(Effect):
    def __init__(self, entity, player, amount):
        super().__init__(entity)
        self.player = player
        self.amount = amount
    def resolve(self):
        from source.gameplay.card import move_between_collections
        move_between_collections(self.player, CollectionType.Deck, CollectionType.Hand, self.amount)

class DealDamage(Effect):
    def __init__(self, entity, target, value):
        super().__init__(entity)
        self.target = target
        self.value = value
    def resolve(self):
        if isinstance(self.target, Choice):
            self.target = self.target.resolve(self.entity)
        if self.target is not None:
            self.target.take_damage(self.value)
            print(f'{self.entity} deals {self.value} damage to {self.target}. HP: {self.target.defense}')
        else:
            print(f"{self.entity.name}'s ability fizzled")