from enum import Enum, auto
from typing import List, Optional
from pydantic import BaseModel

class CardType(str,Enum):
    MONEY = "money"
    PROPERTY = "property"
    RENT = "rent"
    ACTION = "action"
    WILD_PROPERTY = "wild_property"
    WILD_RENT = "wild_rent"

class PropertyColor(str,Enum):
    BROWN = "brown"
    LIGHT_BLUE = "light_blue"
    PINK = "pink"
    ORANGE = "orange"
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"
    DARK_BLUE = "dark_blue"
    UTILITY = "utility"
    RAILROAD = "railroad"

class ActionCardType(str,Enum):
    JUST_SAY_NO = auto()
    DEAL_BREAKER = auto()
    SLY_DEAL = auto()
    FORCED_DEAL = auto()
    ITS_MY_BIRTHDAY = auto()
    HOUSE = auto()
    HOTEL = auto()
    PASS_GO = auto()
    DEBT_COLLECTOR = auto()
    DOUBLE_RENT = auto()

PROPERTY_SET_SIZE = {
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
PROPERTY_RENT = {
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

class Card(BaseModel):
    id: str
    name: str
    card_type: CardType
    value: int = 0

class PropertyCard(Card):
    color: PropertyColor

class WildPropertyCard(Card):
    colors: List[PropertyColor]
    assigned_color: Optional[PropertyColor] = None

class RentCard(Card):
    colors: Optional[List[PropertyColor]] = None

class ActionCard(Card):
    action_type: ActionCardType