from source.gameplay.effect import DealDamage
from source.gameplay.lane import Lane, get_opposite_lane

def get_active_combat_lanes(player) -> list[Lane]:
    active_lanes = list()
    for lane in player.lanes:
        if lane.creature and not lane.creature.exhausted.value and not lane.creature.flooped.value:
            active_lanes.append(lane)
    return active_lanes

def resolve_attack(lane):
    opposite_lane = get_opposite_lane(lane)
    attacker = lane.creature
    defender = opposite_lane.creature

    if defender is not None:
        fight(attacker, defender)
    else:
        DealDamage(attacker, opposite_lane.player, attacker.attack.value).resolve()

def fight(creature_a, creature_b):
    DealDamage(creature_a, creature_b, creature_a.attack.value).resolve()
    DealDamage(creature_b, creature_a, creature_b.attack.value).resolve()