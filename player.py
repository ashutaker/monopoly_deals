from collections import defaultdict
from typing import Dict, List, Optional, Tuple
from cards import Card,PropertyColor
class Player:
    def __init__(self,name):
        self.name = name
        self.hand: List[Card] = []
        self.money_pile: List[Card] = []
        self.property_sets: Dict[PropertyColor,List[Card]] = defaultdict(list)
        self.action_pile: List[Card] = []

    def add_to_hand(self,card: Card) -> bool:
        self.hand.append(card)

    def play_money(self,card_index: int) -> bool:
        # which card from in hand cards goes into the money pile ?
        pass

    def play_property(self,card_index: int, assign_color: Optional[PropertyColor]=None):
        # for property card add it to propertyset
        # for wild property card assign color and add to that set
        pass

    def play_action(self,card_index:int) -> Optional[Card]:
        # if card is rent,action or wild rent return card
        # if card is house or hotel play add to action pile of player
        pass

    def total_money(self) -> int:
        pass

    def get_owned_property_info(self) -> Dict[PropertyColor,Tuple[int, int]]:
        # get players owned property state vs required info for each color
        pass

