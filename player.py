from collections import defaultdict
from typing import Dict, List, Optional, Tuple
from cards import *
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
        if 0 <= card_index < len(self.hand):
            card = self.hand[card_index]
            if card.card_type != CardType.PROPERTY:
                self.hand.pop(card_index)
                self.money_pile.append(card)
                return True
            else:
                print("Property card cannot be played into money pile")
            
        return False


    def play_property(self,card_index: int, assign_color: Optional[PropertyColor]=None):
        # for property card add it to propertyset
        # for wild property card assign color and add to that set
        if 0 <= card_index < len(self.hand):
            card = self.hand[card_index]
            if card.card_type == CardType.PROPERTY:
                self.hand.pop(card_index)
                self.property_sets[card.color].append(card)
                return True
            if card.card_type == CardType.WILD_PROPERTY:    
                if assign_color and assign_color in card.colors:
                    self.hand.pop(card_index)
                    card.assign_color(assign_color)
                    self.property_sets[assign_color].append(card)
                    return True
        return False

    def play_action(self, card_index: int) -> Optional[Card]:
        # if card is rent,action or wild rent return card
        # if card is house or hotel play add to action pile of player
        if 0 <= card_index < len(self.hand):
            card = self.hand[card_index]
            if card.card_type in [CardType.ACTION, CardType.RENT,CardType.WILD_RENT]:
                self.hand.pop(card_index)
                if (card.card_type == CardType.ACTION and 
                    card.action_type in [ActionCardType.HOUSE,ActionCardType.HOTEL]):
                    self.action_pile.append(card)
            return card
        return None

    def total_worth(self) -> int:
        # calculate total money in bank and values of property
        money_in_bank = sum(card.value for card in self.money_pile)
        property_value = 0
        for property in self.property_sets:
            property_value += sum([card.value for card in self.property_sets[property]])
        return money_in_bank + property_value

    def has_full_propertyset(self,color: PropertyColor) -> bool:
        set_size = Card._property_set_size[color]
        return len(self.property_sets[color]) >= set_size

    def get_owned_property_info(self) -> Dict[PropertyColor,Tuple[int, int]]:
        # get players owned property state vs required info for each color
        result = {}
        for color in PropertyColor:
            if self.property_sets[color]:
                current_set_size = len(self.property_sets[color])
                required_set_size = self.property_sets[color][0].set_size
                result[color] = (current_set_size,required_set_size)
        return result
    
    def discard_card(self,card_index: int) -> Card:
        if 0 <= card_index < len(self.hand):
            discard_card = self.hand.pop(card_index)
        return discard_card

