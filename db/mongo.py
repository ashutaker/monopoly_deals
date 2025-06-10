from bson import ObjectId
from fastapi import HTTPException
from pymongo.asynchronous.collection import ReturnDocument
import motor.motor_asyncio
from models.game import Game, GameInDB

MONGODB_URL="mongodb://localhost:27017/"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.get_database("monopoly_deals")
game_collection = db.get_collection("games")

async def create_game(game: dict):
    new_game = await game_collection.insert_one(game.model_dump(by_alias=True, exclude=["id"]))
    created_game = await game_collection.find_one({"_id": new_game.inserted_id})
    return created_game

async def get_game_by_id(game_id):
    if (existing_game := await game_collection.find_one({"_id": ObjectId(game_id)})) is not None:
        return existing_game
    else:
        raise HTTPException(status_code=404, detail=f"Game {game_id} does not exist")

async def list_games() -> list[str]:
    all_waiting_games = await game_collection.find({"state": "waiting"},{"_id": 1}).to_list(100)
    games_list = [str(game["_id"] )for game in all_waiting_games]
    return games_list

async def add_player_game_by_id(game_id: str,player: dict):
    update_game = await game_collection.find_one_and_update(
                {"_id": ObjectId(game_id)},
                {"$push": {"players": player}},
                return_document=ReturnDocument.AFTER
            )
    if update_game:
        return update_game
    else:
        raise HTTPException(status_code=404, detail=f"Failed to add player {player.get("name")} to the game {game_id} .")

async def update_game_state(game_id: str, game_state:str):
    update = await game_collection.find_one_and_update(
        {"_id": ObjectId(game_id)},
        {"$set": {"state": game_state}},
        return_document=ReturnDocument.AFTER
    )
    if update is not None:
        return update
    else:
        raise HTTPException(status_code=404, detail=f"Failed to update game state.")

async def update_card_play(game: dict):
    update = await game_collection.find_one_and_update(
        {"_id": ObjectId(game["_id"])},
        {"$set": { "players": game["players"],
                   "draw_pile": game["draw_pile"],
                   "discard_pile": game["discard_pile"],
                   "action_remaining_per_turn": game["action_remaining_per_turn"]}
         },
        return_document=ReturnDocument.AFTER
    )
    if update is not None:
        return update
    else:
        raise HTTPException(status_code=404, detail=f"Failed to update game state.")

async def get_card(game_id: str, card_id: str):
    pass

async  def update_current_player(game: dict):
    update = await game_collection.find_one_and_update(
        {"_id": ObjectId(game["_id"])},
        {"$set": {"players": game["players"],
                  "draw_pile": game["draw_pile"],
                  "discard_pile": game["discard_pile"]}
         },
        return_document=ReturnDocument.AFTER
    )



