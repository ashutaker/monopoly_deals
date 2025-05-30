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

class ActionCardType(Enum):
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
    def __repr__(self):
        return f"{self.name} (${self.value})"

class MoneyCard(Card):
    def __init__(self, value: int):
        super().__init__(F"{value}M", CardType.MONEY, value)

class PropertyCard(Card):
    def __init__(self, name: str, color: PropertyColor, value: int,rent_values: List[int],set_size: int):
        super().__init__(name, CardType.PROPERTY, value)
        self.color = color
        self.rent_values = self._property_set_rent_values[self.color]
        self.set_size = self._property_set_size[self.color]
    _property_set_size = {
        PropertyColor.BROWN: 2,
        PropertyColor.DARK_BLUE: 2,
        PropertyColor.GREEN: 3,
        PropertyColor.LIGHT_BLUE: 3,
        PropertyColor.ORANGE: 3,
        PropertyColor.PINK: 3,
        PropertyColor.RED: 3,
        PropertyColor.YELLOW: 3,
        PropertyColor.RAILROAD: 4,
        PropertyColor.UTILITY: 2
    }
    _property_set_rent_values = {
        PropertyColor.BROWN: [1, 2],
        PropertyColor.DARK_BLUE: [3, 8],
        PropertyColor.GREEN: [2, 4, 7],
        PropertyColor.LIGHT_BLUE: [1, 2, 3],
        PropertyColor.ORANGE: [1, 3, 5],
        PropertyColor.PINK: [1, 2, 4],
        PropertyColor.RED: [2, 3, 6],
        PropertyColor.YELLOW: [2, 4, 6],
        PropertyColor.RAILROAD: [1, 2, 3, 4],
        PropertyColor.UTILITY: [1, 2]
    }

class RentCard(Card):
    def __init__(self, colors: List[PropertyColor], value: int):
        color_names = "/".join([c.name for c in colors])
        super().__init__(f"Rent : {color_names}", CardType.RENT, value)
        self.colors = colors

class ActionCard(Card):
    def __init__(self, action_type: ActionCardType, value: int):
        super().__init__(action_type.name, CardType.ACTION, value)
        self.action_type = action_type

class WildPropertyCard(Card):
    def __init__(self, name, colors: List[PropertyColor], value: int):
        super().__init__(name, CardType.WILD_PROPERTY, value)
        self.colors = colors
        self.assigned_color = None
        # self.acquired_set_size = None
        # self.acquired_rent_values = None

    def assign_color(self,color: PropertyColor):
        self.assigned_color = color
        # self.acquired_set_size = PropertyCard._property_set_size[color]
        # self.acquired_rent_values = PropertyCard._property_set_rent_values[color]

class WildRentCard(Card):
    def __init__(self, value: int):
        super().__init__("Wild Rent", CardType.WILD_RENT, value)