from gameplay_enums import Landscape

class Player:
    def __init__(self, name: str, hp : int):
        from lane import Lane
        self.name : str = name
        self.hp : int  = hp
        self.action_points : int = 0
        self.lanes : list[Lane] = list()
        self.stack = Lane(None, self, None)
        self.landscapes : dict[Landscape, int] = dict()

    def take_damage(self, amount : int):
        self.hp = max(self.hp - amount, 0)
    def heal_damage(self, amount : int):
        self.hp = min(self.hp + amount, 25)

    def gain_action_points(self, amount : int):
        self.action_points += amount
    def spend_action_points(self, amount: int):
        if self.action_points - amount < 0:
            raise Exception(f"{self.name}: player cannot have negative number of action points")
        else:
            self.action_points -= amount

    def add_landscape(self, landscape : Landscape):
        if landscape in self.landscapes.keys():
            self.landscapes[landscape] += 1
        else:
            self.landscapes[landscape] = 1
    def remove_landscape(self, landscape : Landscape):
        if landscape not in self.landscapes.keys():
            raise Exception(f"{self.name}: attempted to remove landscape type ({landscape.name}) "
                            f"but player has none")
        else:
            self.landscapes[landscape] -= 1
            if self.landscapes[landscape] == 0:
                self.landscapes.pop(landscape)