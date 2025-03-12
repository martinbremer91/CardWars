from source.gameplay.game_enums import CollectionType, TargetTag
from source.gameplay.target import Target, get_targets_from_tag

class Effect:
    def __init__(self, entity, targets, condition = None):
        self.entity = entity
        self.targets = targets
        self.condition = condition
    def assign_condition(self, condition):
        self.condition = condition
    def resolve(self):
        targets_to_evaluate = self.resolve_targets()
        current_targets = self.filter_targets_with_condition(targets_to_evaluate)

        if current_targets:
            if isinstance(current_targets, list):
                for target in current_targets:
                    self.perform_effect(target)
            else:
                self.perform_effect(current_targets)
        else:
            print(f"{self.entity.name}'s ability fizzled\n")
    def resolve_targets(self):
        targets_to_evaluate = self.targets.resolve(self.entity) \
            if isinstance(self.targets, Target) else self.targets
        return get_targets_from_tag(self.targets, self.entity) \
            if isinstance(self.targets, TargetTag) else targets_to_evaluate
    def filter_targets_with_condition(self, targets_to_evaluate):
        current_targets = None
        if isinstance(targets_to_evaluate, list):
            current_targets = list()
            for target in targets_to_evaluate:
                if not self.condition or self.condition.resolve():
                    current_targets.append(target)
        elif not self.condition or self.condition.resolve():
            current_targets = targets_to_evaluate
        return current_targets
    def perform_effect(self, target):
        pass

class GainActionPoints(Effect):
    def __init__(self, entity, targets, amount, condition = None):
        super().__init__(entity, targets, condition)
        self.amount = amount
    def perform_effect(self, target):
        target.action_points.add_modifier(self.amount, target.end_of_turn)

class SpendActionPoints(Effect):
    def __init__(self, entity, targets, amount, condition = None):
        super().__init__(entity, targets, condition)
        self.amount = amount
    def perform_effect(self, target):
        new_value = target.action_points - self.amount
        if new_value < 0:
            raise Exception(f"{target}: player cannot have negative number of action points\n"
                            f"(Player has {target.action_points}. To be deducted: {self.amount}")
        target.action_points.add_modifier(new_value, target.end_of_turn)

class DrawCards(Effect):
    def __init__(self, entity, targets, amount, condition = None):
        super().__init__(entity, targets, condition)
        self.amount = amount
    def perform_effect(self, target):
        from source.gameplay.card import move_between_collections
        move_between_collections(target, CollectionType.Deck, CollectionType.Hand, self.amount)

class DealDamage(Effect):
    def __init__(self, entity, targets, value, condition = None):
        super().__init__(entity, targets, condition)
        self.value = value
    def perform_effect(self, target):
        print(f'{self.entity} deals {self.value} damage to {target}. '
              f'Current damage: {min(target.damage + self.value, target.defense)}/{target.defense}')
        target.take_damage(self.value)

class HealDamage(Effect):
    def __init__(self, entity, targets, value, condition = None):
        super().__init__(entity, targets, condition)
        self.value = value
    def perform_effect(self, target):
        target.heal_damage(self.value)
        print(f'{self.entity} heals {self.value} damage from {target}. Current damage: {target.damage}/{target.defense}')

class ModAttack(Effect):
    def __init__(self, entity, targets, value, deactivation_trigger, condition = None):
        super().__init__(entity, targets, condition)
        self.value = value
        self.deactivation_trigger = deactivation_trigger
    def perform_effect(self, target):
        target.attack.add_modifier(self.value, self.deactivation_trigger)
        print(f"{self.entity} changes {target}'s attack by {self.value}. Current attack: {target.attack.value}")