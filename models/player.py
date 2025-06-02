from typing import List, Annotated, Dict
from pydantic import BaseModel, BeforeValidator, Field

from core.cards import PropertyColor

PyObjectId = Annotated[str, BeforeValidator(str)]

class Player(BaseModel):
    id: str
    name : str = Field(...)
    hand : List[str] = []
    money_pile : List[str] = []
    property_set : Dict[PropertyColor, List[str]] = {} # Property color > Card ID

class PlayerRequest(BaseModel):
    name : str = Field(...)
    # hand : List[str] = []
    # money_pile : List[str] = []
    # property_set : Dict[PropertyColor, List[str]] = {} # Property color > Card ID