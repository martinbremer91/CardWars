import source.gameplay.gameplay_manager as gm
from source.gameplay.card import try_play_card

gm.init()
gm.start_play()

print('Player One first card')
try_play_card(gm.player_one, gm.player_one.hand.cards[0])
print('Player One second card')
try_play_card(gm.player_one, gm.player_one.hand.cards[0])

print('P1 combat phase')
gm.advance_turn_phase()

print('Player Two first card')
try_play_card(gm.player_two, gm.player_two.hand.cards[0])
print('Player Two second card')
try_play_card(gm.player_two, gm.player_two.hand.cards[0])

print('P2 combat phase')
gm.advance_turn_phase()