from source.gameplay.game_manager import init, start_play

init()
start_play()

# from source.gameplay.gameplay_manager import player_one
# from source.gameplay.card import Card
# from source.gameplay.entities import Creature
# from source.gameplay.cw_lang import parse

# cw_lang = "SEP:DEAL_DMG(CHOICE(FOE_CREATURES, 1), 1)"
#
# card = Card(player_one, Creature("Test Meister", Landscape.Rainbow, 1, "ability goes here",
#                                  cw_lang, 1, 3), player_one.deck)
#
# parse(card.entity.cw_lang, card.entity)