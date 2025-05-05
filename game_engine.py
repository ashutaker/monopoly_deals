# Initialise and maintain state of game elements

from typing import List, Optional

from monopoly_deals.cards import Card
from monopoly_deals.player import Player

MAX_IN_HAND_CARD_COUNT = 7

class GameEngine:
    def __init__(self,player_names: List[str]):
        self.players = player_names
        self.current_player_id = 0
        self.draw_pile = []
        self.discard_pile = []
        self.setup_cards()
        self.deal_cards()

        def setup_cards():
            # Create complete deck of the playable cards and add them to draw pile
            # shuffle the pile before dealing cards to player
            pass

        def deal_cards():
            # add 5 card to each player hand
            pass

        def draw_card(self,player: Player, draw_count: int = 2):
            # game engine will check the draw_pile count for each player to deal card
            # to them default is 2 for start of turn and PASS GO
            pass

        def current_player(self) -> Player:
            # returns current player
            pass

        def next_player(self):
            # pick next player, update the current player index
            pass

        def process_action_card(self,action_card: Card, target_player: Optional[Player] = None) -> bool:
            # depeding on the type of action manage the money and properties etc
            # pass go
            # debt collector
            # rent/wild rent
            # birthday
            # 
            pass

        def collect_money(self, from_player: Player, to_player: Player, amount: int) -> int:
            # find the closest denomination to pay with money or property
            pass

        def Check_winner(self) -> Optional[Player]:
            # check propertyset of each player before changing turn
            pass
