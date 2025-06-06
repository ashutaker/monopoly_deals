from enum import Enum
from typing import List, Optional, Annotated
from pydantic import BaseModel, BeforeValidator, Field
from models.player import Player, PlayerInGameResponse
from models.cards import Card, PropertyColor

PyObjectId = Annotated[str, BeforeValidator(str)]
class GameState(str, Enum):
    WAITING = "waiting"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Game(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    players: List[Player] = []
    draw_pile: List[str] = []
    discard_pile: List[str] = []
    state: GameState = GameState.WAITING
    winner: Optional[str] = None
    cards: List[Card] = []
    current_player_index: int = 0
    action_remaining_per_turn: int = 0

class GameResponseModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    players: List[PlayerInGameResponse] = []
    draw_pile: List[str] = []
    discard_pile: List[str] = []
    state: GameState
    winner: Optional[str] = None
    # cards: List[Card] = []
    current_player_index: int = 0
    action_remaining_per_turn: int = 0

class GameCreateModel(BaseModel):
    player_name: str

class GameJoinModel(BaseModel):
    player_name: str

class GameCollection(BaseModel):
    games: List[str]   # List of Game IDs

class PlayerCardPlayRequest(BaseModel):
    card_id: str
    target_player_id: Optional[str] = None
    target_property_color: Optional[PropertyColor] = None
    target_property_id: Optional[str] = None
    self_property_color: Optional[PropertyColor] = None
    self_property_id: Optional[str] = None