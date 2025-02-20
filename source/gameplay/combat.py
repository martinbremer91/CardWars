from typing import Optional
from source.gameplay.lane import Lane, get_opposite_lane
from source.gameplay.player import Player
from source.gameplay.entities import Creature

def get_active_combat_lanes(player : Player) -> list[Lane]:
    active_lanes : list[Lane] = list()
    for lane in player.lanes:
        if lane.creature and not lane.creature.exhausted and not lane.creature.flooped:
            active_lanes.append(lane)
    return active_lanes

def resolve_attack(lane : Lane):
    opposite_lane : Lane = get_opposite_lane(lane)
    attacker : Creature = lane.creature
    defender : Optional[Creature] = opposite_lane.creature

    if defender is not None:
        fight(attacker, defender)
    else:
        opposite_lane.player.take_damage(attacker.attack)
        print(f'{attacker.name} deals {attacker.attack} damage to {opposite_lane.player.name}')
        print(f'{opposite_lane.player.name} HP: {opposite_lane.player.hp}')

def fight(creature_a : Creature, creature_b : Creature):
    print(f'{creature_a.name} fights {creature_b.name}')