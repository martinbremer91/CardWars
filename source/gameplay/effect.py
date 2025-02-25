﻿from source.gameplay.game_enums import CollectionType
from source.gameplay.choice import Choice

class Effect:
    def __init__(self, entity, target):
        self.entity = entity
        self.targets = target
    def resolve(self):
        self.resolve_target()
    def resolve_target(self):
        if isinstance(self.targets, Choice):
            self.targets = self.targets.resolve(self.entity)
        if self.targets is not None:
            if isinstance(self.targets, list):
                for target in self.targets:
                    self.perform_effect(target)
            else:
                self.perform_effect(self.targets)
        else:
            print(f"{self.entity.name}'s ability fizzled\n")
    def perform_effect(self, target):
        pass

class GainActionPoints(Effect):
    def __init__(self, entity, targets, amount):
        super().__init__(entity, targets)
        self.amount = amount
    def perform_effect(self, target):
        target.action_points += self.amount

class SpendActionPoints(Effect):
    def __init__(self, entity, targets, amount):
        super().__init__(entity, targets)
        self.amount = amount
    def perform_effect(self, target):
        to_be_deducted = target.action_points if self.amount == -1 else self.amount
        if target.action_points - to_be_deducted < 0:
            raise Exception(f"{target.name}: player cannot have negative number of action points\n"
                            f"(Player has {target.action_points}. To be deducted: {to_be_deducted}")
        target.action_points -= to_be_deducted

class DrawCards(Effect):
    def __init__(self, entity, targets, amount):
        super().__init__(entity, targets)
        self.amount = amount
    def perform_effect(self, target):
        from source.gameplay.card import move_between_collections
        move_between_collections(target, CollectionType.Deck, CollectionType.Hand, self.amount)

class DealDamage(Effect):
    def __init__(self, entity, targets, value):
        super().__init__(entity, targets)
        self.value = value
    def perform_effect(self, target):
        target.take_damage(self.value)
        print(f'{self.entity} deals {self.value} damage to {target}. Current damage: {target.damage}/{target.defense}')

class HealDamage(Effect):
    def __init__(self, entity, targets, value):
        super().__init__(entity, targets)
        self.value = value
    def perform_effect(self, target):
        target.heal_damage(self.value)
        print(f'{self.entity} heals {self.value} damage from {target}. Current damage: {target.damage}/{target.defense}')

class ModAttack(Effect):
    def __init__(self, entity, targets, value):
        super().__init__(entity, targets)
        self.value = value
    def perform_effect(self, target):
        target.mod_attack(self.value)
        print(f"{self.entity} changes {target}'s attack by {self.value}. Current attack: {target.get_attack()}")