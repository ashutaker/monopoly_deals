import random
from typing import List, Optional, Annotated
from pydantic import BaseModel, BeforeValidator, Field
from exceptions import NoPropertyColor, InValidPropertyColor
import utilities as util
from models.player import Player, PlayerInGameResponse
from models.cards import *

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


class PlayerCardPlayRequest(BaseModel):
    card_id: str
    target_player_id: Optional[str] = None
    target_property_color: Optional[PropertyColor] = None
    target_property_id: Optional[str] = None
    self_property_color: Optional[PropertyColor] = None
    self_property_id: Optional[str] = None


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

    def is_valid_card(self, card_id: str) -> bool:
        if card_id in self.players[self.current_player_index].hand:
            return True
        return False

    def is_valid_player(self, player_id: str):
        for idx, player in enumerate(self.players):
            if player.id == player_id and idx == self.current_player_index:
                return player
        return None

    def update_remaining_actions(self):
        self.action_remaining_per_turn -= 1
        if self.action_remaining_per_turn == 0:
            self.next_player()
            draw_count = 2
            if len(self.players[self.current_player_index].hand) == 0:
                draw_count = 5
            self.draw_card(self.players[self.current_player_index], draw_count=draw_count)

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

    def next_player(self):
        self.current_player_index = (self.current_player_id + 1) % len(self.players)

    def deal_cards(self):
        # add 5 card to each player hand
        print("Dealing cards to players ...")
        for _ in range(5):
            for player in self.players:
                card = self.draw_pile.pop()
                player.hand.append(card)
        self.action_remaining_per_turn = 3
        return self

    def get_card_details(self, card_id: str):
        return next(card.model_dump() for card in self.cards if card.id == card_id)

    def draw_card(self, player: Player, draw_count: int) -> None:
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

    def play_card(self, card_request: PlayerCardPlayRequest, player_id: str):
        card = next(card for card in self.cards if card.id == card_request.card_id)
        if card.card_type == CardType.MONEY:
            self.play_money(card_request.card_id)
            return True
        if card.card_type in [CardType.PROPERTY, CardType.WILD_PROPERTY]:
            if card.card_type == CardType.WILD_PROPERTY:
                wild_property = card
                if not card_request.self_property_color:
                    raise NoPropertyColor()
                if card_request.self_property_color not in wild_property.colors:
                    raise InValidPropertyColor()
            self.play_property(card_request, card)
            return True

    def play_money(self, card_id: str):
        self.players[self.current_player_index].hand.remove(card_id)
        self.players[self.current_player_index].money_pile.append(card_id)
        self.update_remaining_actions()

    def play_property(self, card_request: PlayerCardPlayRequest, card: CardInDB):
        # print(card_request)
        card_id = card_request.card_id
        player = self.players[self.current_player_index]
        if card.card_type == CardType.PROPERTY:
            property_card = card
            color = property_card.color
            if color not in player.property_set:
                player.property_set[color] = []
            player.hand.remove(card_id)
            player.property_set[color].append(card_id)
            self.update_remaining_actions()

        if card.card_type == CardType.WILD_PROPERTY:
            wild_property = card
            wild_property.assigned_color = card_request.self_property_color
            if wild_property.assigned_color not in player.property_set:
                player.property_set[wild_property.assigned_color] = []
            player.hand.remove(card_id)
            player.property_set[wild_property.assigned_color].append(card_id)
            self.update_remaining_actions()

    def play_action_card(self, action_card: CardInDB, target_player: Optional[Player] = None) -> bool:
        # depending on the type of action card manage the money and properties etc
        current_player = self.players[self.current_player_index]
        if action_card.action_type == ActionCardType.PASS_GO:
            self.draw_card(current_player, draw_count=2)
            current_player.hand.remove(action_card.id)
            self.discard_pile.append(action_card.id)
            return True
        elif action_card.action_type == ActionCardType.DEBT_COLLECTOR:
            amount = 5
            # transferred = game_engine.collect_money(target_player, current_player, amount)
            # if transferred:
            #     print(f"Successfully transferred {transferred}M from {target_player.name} to {current_player.name}.")
            current_player.hand.remove(action_card.id)
            self.discard_pile.append(action_card.id)
            return True
        elif action_card.action_type == ActionCardType.ITS_MY_BIRTHDAY:
            # collect money from all the other players
            amount = 2
            for player in self.players:
                if player != current_player:
                    if player.total_worth() == 0:
                        print(f"{player.name} has 0M ")
                        continue
                    # transferred = game_engine.collect_money(player, current_player, amount)
                    # if transferred:
                    #     print(f"Successfully transferred {transferred}M from {player.name} to {current_player.name}.")
            current_player.hand.remove(action_card.id)
            self.discard_pile.append(action_card.id)
            return True
        elif action_card.action_type == ActionCardType.DEAL_BREAKER:
            pass
        elif action_card.action_type == ActionCardType.FORCED_DEAL:
            pass
        elif action_card.action_type == ActionCardType.SLY_DEAL:
            pass
        elif action_card.action_type == ActionCardType.HOUSE:
            pass
        elif action_card.action_type == ActionCardType.HOTEL:
            pass
        elif action_card.action_type == ActionCardType.DOUBLE_RENT:
            pass
        elif action_card.action_type == ActionCardType.JUST_SAY_NO:
            pass
        return False


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
    games: List[str]  # List of Game IDs


class PlayerCardSDiscardRequest(BaseModel):
    id: str
