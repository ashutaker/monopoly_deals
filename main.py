import uuid
from fastapi import FastAPI, Body, HTTPException
import db.mongo as db
from models.game import Game, GameCreateModel, GameCollection, GameState
from models.player import Player, PlayerRequest
import game_engine

app = FastAPI()

@app.post("/game", response_model=Game)
async def create_game(request: GameCreateModel):
    player_id = str(uuid.uuid4())
    player = Player(id=player_id,name= request.player_name)
    card_deck = game_engine.setup_deck()
    draw_pile = [card.id for card in card_deck]
    game = Game(players = [player], cards= card_deck,draw_pile=draw_pile)
    created_game = await db.create_game(game)
    return created_game

@app.get(
    "/games",
        response_model=GameCollection,
        response_description="List all created games"
    )
async def list_games():
    return GameCollection(games=await db.list_games())


@app.put("/games/{game_id}/join",
         response_model=Game,
         description="Add player to a game")
async def join_game(game_id: str, player: PlayerRequest = Body(...)):
    player = {
        k: v for k,v in player.model_dump(by_alias = True).items() if v is not None
    }
    new_player = Player(id=str(uuid.uuid4()),
                        name= player["name"],
                        )
    if len(player) >= 1:
        update_game = await db.add_player_game_by_id(
            game_id = game_id,
            player = new_player.model_dump(by_alias=True)
        )
        if update_game is not None:
            return update_game
        else:
            raise HTTPException(status_code=404, detail=f"Game {game_id} not found")
    if(existing_game := db.get_game_by_id(game_id)) is not None:
        return existing_game
    raise HTTPException(status_code=400, detail=f"failed to add player")

@app.put("/games/{game_id}/start", response_model=Game)
async def start_game(game_id: str):
    update_state = await db.update_game_state(game_id, GameState.IN_PROGRESS.value)
    deal_cards = game_engine.deal_cards(update_state)
    update_game = await db.update_player_hand(deal_cards)

    return update_game