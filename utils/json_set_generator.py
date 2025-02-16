import json

database : dict[int, dict[str, ]] = json.loads(open("card_database.json", "r").read())
decks : dict[str, list[(int, int)]] = json.loads(open("decks.json", "r").read())

for deck in decks:
    data : list[(int, int)] = decks[deck]

    for item in data:
        name = database[str(item[1])]["name"]
        print(f"{deck}, {item[1]}, {name}, {item[0]}")

print("---")

for deck in decks:
    counter = 0

    data : list[(int, int)] = decks[deck]

    for item in data:
        counter += item[0]

    print(deck, counter)

exit()
decks : dict[str, list[(int, int)]] = json.loads(open("decks.json", "r").read())

for deck in decks:
    counter = 0

    data : list[(int, int)] = decks[deck]

    for item in data:
        counter += item[0]

    print(deck, counter)

exit()
with open('decks.json', 'w', encoding='utf-8') as f:
    json.dump(decks, f)#, ensure_ascii=False, indent=4)