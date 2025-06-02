from bson import ObjectId
from pymongo.asynchronous.collection import ReturnDocument
import motor.motor_asyncio
from models.game import Game

MONGODB_URL="mongodb://localhost:27017/"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.get_database("monopoly_deals")
game_collection = db.get_collection("games")

async def create_game(game: Game):
    new_game = await game_collection.insert_one(game.model_dump(by_alias=True, exclude=["id"]))
    created_game = await game_collection.find_one({"_id": new_game.inserted_id})
    return created_game

async def get_game_by_id(game_id):
    pass

async def list_games() -> list[str]:
    all_waiting_games = await game_collection.find({"state": "waiting"},{"_id": 1}).to_list(100)
    games_list = [str(game["_id"] )for game in all_waiting_games]
    return games_list

async def update_game_by_id(game_id,update: dict):
    update_game = await db.game_collection.find_one_and_update(
                {"_id": ObjectId(game_id)},
                {"$push": update},
                return_document=ReturnDocument.AFTER
            )
    return update_game

async def update_player(game_id: str, player_id: str, hand):
    pass



