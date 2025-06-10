from typing import List, Annotated, Dict
from pydantic import BaseModel, BeforeValidator, Field

from models.cards import PropertyColor

PyObjectId = Annotated[str, BeforeValidator(str)]

class Player(BaseModel):
    id: str
    name : str = Field(...)
    hand : List[str] = []
    money_pile : List[str] = []
    property_set : Dict[PropertyColor, List[str]] = {} # Property color > Card ID

class PlayerRequest(BaseModel):
    name : str = Field(...)

class PlayerInGameResponse(BaseModel):
    id: str
    name: str = Field(...)
    money_pile: List[str] = []
    property_set: Dict[PropertyColor, List[str]] = {}  # Property color > Card ID
