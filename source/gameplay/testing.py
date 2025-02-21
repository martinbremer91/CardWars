from source.gameplay.gameplay_enums import Landscape
from source.gameplay.gameplay_manager import init, start_play

init()

from source.gameplay.gameplay_manager import player_one
from source.gameplay.card import Card
from source.gameplay.entities import Creature
from source.gameplay.cw_lang import parse
card = Card(player_one, Creature("Test Meister", Landscape.Rainbow, 1, "ability goes here",
                                 "SEP:DEAL_DMG(SELECT(FOE_CREATURES, 1), 1)", 1, 3), player_one.deck)

parse(card.entity.cw_lang, card.entity)

#start_play()