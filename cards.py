from enum import Enum, auto
from typing import List


class CardType(Enum):
    MONEY = auto()
    PROPERTY = auto()
    RENT = auto()
    ACTION = auto()
    WILD_PROPERTY = auto()
    WILD_RENT = auto()

class PropertyColor(Enum):
    BROWN = auto()
    LIGHT_BLUE = auto()
    PINK = auto()
    ORANGE = auto()
    RED = auto()
    YELLOW = auto()
    GREEN = auto()
    DARK_BLUE = auto()
    UTILITY = auto()
    RAILROAD = auto()

class ActioCardType(Enum):
    JUST_SAY_NO = auto()
    DEAL_BREAKER = auto()
    SLY_DEAL = auto()
    FORCE_DEAL = auto()
    ITS_MY_BIRTHDAY = auto()
    HOUSE = auto()
    HOTEL = auto()
    PASS_GO = auto()
    DEBT_COLLECTOR = auto()
    DOUBLE_RENT = auto()


class Card:
    def __init__(self,name: str, card_type: CardType,value: int=0):
        self.name = name
        self.card_type = card_type
        self.value = value
    
    def __str__(self):
        return f"{self.name} (${self.value})"

class MoneyCard(Card):
    def __init__(self, value: int):
        super().__init__(F"{value}M", CardType.MONEY, value)

class PropertyCard(Card):
    def __init__(self, name: str, color: PropertyColor, value: int,rent_values: List[int],set_size: int):
        super().__init__(name, CardType.PROPERTY, value)
        self.color = color
        self.rent_values = rent_values
        self.set_size=set_size

class RentCard(Card):
    def __init__(self, colors: List[PropertyColor], value: int):
        color_names = "/".join([c.name for c in colors])
        super().__init__(f"Rent : {color_names}", CardType.RENT, value)
        self.colors = colors

class ActionCard(Card):
    def __init__(self, action_type: ActioCardType, value: int):
        super().__init__(action_type.name, CardType.ACTION, value)
        self.action_type = action_type

class WildPropertyCard(Card):
    def __init__(self, name, colors: List[PropertyColor], value: int):
        super().__init__(name, CardType.WILD_PROPERTY, value)
        self.colors = colors
        self.assigned_color = None

class WildRentCard(Card):
    def __init__(self, value: int):
        super().__init__("Wild Rent", CardType.WILD_RENT, value)