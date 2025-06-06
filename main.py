from fastapi import FastAPI, Body, HTTPException
import db.mongo as DB
from game_engine import *
from models.game import Game, GameCreateModel, GameCollection, GameState, PlayerCardPlayRequest, GameResponseModel
from models.player import Player, PlayerRequest
import game_engine

app = FastAPI()

@app.post("/game", response_model=GameResponseModel)
async def create_game(request: GameCreateModel):
    player_id = str(uuid.uuid4())
    player = Player(id=player_id,name= request.player_name)
    card_deck = game_engine.setup_deck()
    draw_pile = [card.id for card in card_deck]
    game = Game(players = [player], cards= card_deck,draw_pile=draw_pile)
    created_game = await DB.create_game(game)
    return created_game

@app.get(
    "/games",
        response_model=GameCollection,
        response_description="List all created games"
    )
async def list_games():
    return GameCollection(games = await DB.list_games())


@app.post("/games/{game_id}/join",
         response_model=GameResponseModel,
         description="Add player to a game")
async def join_game(game_id: str, player: PlayerRequest = Body(...)):
    existing_game = await DB.get_game_by_id(game_id)
    if existing_game["state"] == GameState.WAITING:
        player = {
            k: v for k,v in player.model_dump(by_alias = True).items() if v is not None
        }
        new_player = Player(id=str(uuid.uuid4()),
                            name= player["name"],
                            )
        if len(player) >= 1:
            update_game = await DB.add_player_game_by_id(
                game_id = game_id,
                player = new_player.model_dump(by_alias=True)
            )
            return update_game
    else:
        raise HTTPException(status_code=403,detail=f"Game {game_id} is not waiting for players to join.")
    return existing_game

@app.post("/games/{game_id}/start", response_model=GameResponseModel)
async def start_game(game_id: str):
    update_state = await DB.update_game_state(game_id, GameState.IN_PROGRESS.value)
    deal_card = deal_cards(update_state)
    update_game = await DB.update_player_hand(deal_card)

    return update_game


@app.post("/game/{game_id}/play", response_model= GameResponseModel)
async def play_card(game_id: str, request: PlayerCardPlayRequest,player_id: str):
    existing_game = await DB.get_game_by_id(game_id)
    card_id = request.card_id

    # check game state and
    print(f"existing game state : {existing_game["state"]}")
    if existing_game["state"] != GameState.IN_PROGRESS:
        raise HTTPException(status_code=400, detail="Game is not in progress.")
    # player validity
    if not any(player["id"] == player_id for player in existing_game["players"]):
        raise HTTPException(status_code=404, detail=f"Player ID: {player_id} not found in the game {game_id}")
    # check player turn
    current_player = get_current_player(current_index=int(existing_game["current_player_index"]),
                             players=existing_game["players"],
                             player_id=player_id )
    if not current_player:
        raise HTTPException(status_code=400, detail="Not your turn")
    # check card validity
    if not is_valid_card(card_id=card_id,player_hand=current_player.get("hand")):
        raise HTTPException(status_code=400, detail="Card not found in player hand")

    # Handle Cards
    ## collect money
    ## play property
    ## play action

    return existing_game
