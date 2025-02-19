import os
import json

asset_path : str = os.getcwd() + '/../../resources'

def get_database() -> dict[str, dict[str, ]]:
    cwd = os.getcwd()
    os.chdir(asset_path)
    database = json.loads(open('card_database.json', "r").read())
    os.chdir(cwd)
    return database

def get_decklists() -> dict[str, list[(int, int)]]:
    cwd = os.getcwd()
    os.chdir(asset_path)
    decklists = json.loads(open('decklists.json', "r").read())
    os.chdir(cwd)
    return decklists

def import_decklist(name : str)-> list[(int, int)]:
    decklists = get_decklists()
    if not name in decklists:
        raise Exception(f"Deck '{name}' does not exist")
    return decklists[name]