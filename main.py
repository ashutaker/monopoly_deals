import uuid

from bson import ObjectId
from fastapi import FastAPI, Body, HTTPException
from pymongo.asynchronous.collection import ReturnDocument

import db.mongo as db
from models.game import Game,GameCreateModel
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

# @app.get(
#     "/games",
#         response_model=GameCollection,
#         response_description="List all created games"
#     )
# async def list_games():
#     return GameCollection(games = await db.game_collection.find({"state": "waiting"}).to_list(100))
#
# @app.put("/games/{game_id}/join",
#          response_model=GameCreateModel,
#          description="Add player to a game")
# async def join_game(game_id: str, player: PlayerRequest = Body(...)):
#     player = {
#         k: v for k,v in player.model_dump(by_alias = True).items() if v is not None
#     }
#     player["id"] = str(uuid.uuid4())
#
#     if len(player) >= 1:
#         update_game = await db.game_collection.find_one_and_update(
#             {"_id": ObjectId(game_id)},
#             {"$push": {"players": player}},
#             return_document=ReturnDocument.AFTER
#         )
#         if update_game is not None:
#             return update_game
#         else:
#             raise HTTPException(status_code=404, detail="Game {game_id} not found")
#     if(existing_game := await db.game_collection.find_one({"_id": game_id})) is not None:
#         return existing_game
#     raise HTTPException(status_code=404, detail="Game {game_id} not found")

# @app.put("/games/{game_id}/start")
# async def start_game(game_id: str):
#
#     game = await db.game_collection.find_one({"_id": ObjectId(game_id)})
#
#     if start_game is not None:
#         return start_game
#     raise HTTPException(status_code=404, detail="Game {game_id} not found")