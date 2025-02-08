import json

class CardData:
    def __init__(self, name, path, card_type, card_set, land, ability, cost, atk, defense):
        self.name = name
        self.image_path = path
        self.card_type = card_type
        self.set = card_set
        self.landscape = land
        self.ability = ability
        self.cost = cost
        self.attack = atk
        self.defense = defense

    def to_dict(self) -> dict[str, str]:
        as_dict : dict[str, str] = dict()
        as_dict["name"] = self.name
        as_dict["image-path"] = self.image_path
        as_dict["type"] = self.card_type
        as_dict["set"] = self.set
        as_dict["landscape"] = self.landscape
        as_dict["ability"] = self.ability
        as_dict["cost"] = self.cost
        as_dict["attack"] = self.attack
        as_dict["defense"] = self.defense
        return as_dict

def get_data(entry_text : str, start_marker : str) -> str:
    start_index : int = entry_text.find(start_marker) + len(start_marker) + 2
    end_index : int = entry_text.find("*", start_index) - 1

    return entry_text[start_index : end_index]

with open('C:/Users/marti/PycharmProjects/CardWars/Card Dweeb - Card Database.txt', 'r') as file:
    data = file.read()

individual_entries : list[str] = list()
cards : dict[int, dict[str, str]] = dict()

current = ""
for character in data:
    if character == '\n':
        individual_entries.append(current)
        current = ""
        continue

    current += character

for entry in individual_entries:
    e_id : int = int(get_data(entry, "data-id"))
    e_name = get_data(entry, "data-name")
    e_path = get_data(entry, "data-card-image")
    e_type = get_data(entry, "data-card-type")
    e_set = get_data(entry, "data-set")
    e_land = get_data(entry, "data-landscape")
    e_ability = get_data(entry, "data-ability")
    e_cost = get_data(entry, "data-cost")
    e_atk = get_data(entry, "data-attack")
    e_def = get_data(entry, "data-defense")

    card_data = CardData(e_name, e_path, e_type, e_set, e_land, e_ability, e_cost, e_atk, e_def)
    cards[e_id] = card_data.to_dict()

cards_json : str = json.dumps(cards, default=lambda o: o.__dict__, sort_keys=False, indent=4)
print(cards_json)