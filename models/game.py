from enum import Enum
from random import random
from typing import List, Optional, Annotated
from pydantic import BaseModel, BeforeValidator, Field
from models.player import Player, PlayerInGameResponse
from models.cards import Card, PropertyColor, CardInDB

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

class GameInDB(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    players: List[Player] = []
    draw_pile: List[str] = []
    discard_pile: List[str] = []
    state: GameState = GameState.WAITING
    winner: Optional[str] = None
    cards: List[CardInDB] = []
    current_player_index: int = 0
    action_remaining_per_turn: int = 0

    def update_remaining_actions(self):
        self.action_remaining_per_turn -= 1
        if self.action_remaining_per_turn == 0:
            self.current_player_index = (self.current_player_index + 1) % (len(self.players))
            draw_count = 2
            if len(self.players[self.current_player_index].hand) == 0:
                draw_count = 5
            self.draw_card(self.players[self.current_player_index],draw_count=draw_count)


    def check_winner(self):
        # check property set of each player and set winner and game state
        current_player = self.players[self.current_player_index]
        complete_property_set = 0
        for color in current_player.property_sets:
            if current_player.has_complete_property_set(color):
                complete_property_set += 1
        if complete_property_set == 3:
            self.winner = current_player.id
            self.state = GameState.COMPLETED
        return None

    def deal_cards(self):
        # add 5 card to each player hand
        print("Dealing cards to players ...")
        for _ in range(5):
            for player in self.players:
                card = self.draw_pile.pop()
                player.hand.append(card)
        self.action_remaining_per_turn= 3
        return self

    def draw_card(self, player: Player, draw_count: int):
        # game engine will check the draw_pile count for each player to deal card
        # to them default is 2 for start of turn and PASS GO
        for _ in range(draw_count):
            if not self.draw_pile:
                print("No cards left in draw pile. Reshuffling discard pile back to draw pile !!")
                self.draw_pile = self.discard_pile
                self.discard_pile = []
                random.shuffle(self.draw_pile)
                print("Done reshuffling !!!")
            if self.draw_pile:
                player.hand.append(self.draw_pile.pop())
        print(f"{draw_count} cards added to {player.name}'s hand")

    def discard_card(self, player_id: str, card_id: str):
        player = next(player for player in self.players if player.id == player_id)
        player.hand.remove(card_id)
        self.draw_pile.append(card_id)
class GameResponseModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    players: List[PlayerInGameResponse] = []
    draw_pile: List[str] = []
    discard_pile: List[str] = []
    state: GameState
    winner: Optional[str] = None
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

class PlayerCardSDiscardRequest(BaseModel):
    id: str