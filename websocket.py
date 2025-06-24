from collections import defaultdict
from typing import Any

from fastapi import WebSocket

from models.game import GameInDB


class ConnectionManager:
    def __init__(self):
        self.games: dict[str, dict] = defaultdict(lambda: defaultdict(dict))

    async def connect(self, websocket: WebSocket, game_id: str, player_id) -> None:
        await websocket.accept()
        self.games[game_id][player_id] = websocket

    async def disconnect(self, websocket: WebSocket, game_id: str, player_id) -> None:
        for player, ws in self.games[game_id]:
            if ws == websocket:
                self.games[game_id].remove(player)

    async def broadcast_game(self,game: GameInDB) -> None:
        game_json_data = game.model_dump(by_alias=True)
        for player in self.games[game.id]:
            print(player)
            connection = self.games[game.id][player]
            await connection.send_json(game_json_data)

    async def send_personal_game_data(self,player_id: str,game_id: str, data: dict):
        if player_id in self.games[game_id]:
            connection = self.games[game_id][player_id]
            await connection.send_json(data)

    async def send_personal_message(self,player_id: str,game_id: str, data: dict):
        if player_id in self.games[game_id]:
            connection = self.games[game_id][player_id]
            await connection.send_json(data)


connection_manager = ConnectionManager()
