from uuid import uuid4
from fastapi import FastAPI, Body, Response, HTTPException, Depends, WebSocket, WebSocketException
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketDisconnect

import db.mongo as DB
from exceptions import NotYourTurn, CustomError, GameNotInProgress, InvalidPlayer, InvalidCard
from game_engine import *
from models.game import GameCreateModel, GameCollection, GameState, PlayerCardPlayRequest, GameResponseModel, \
    GameInDB, PlayerCardSDiscardRequest
from models.player import Player, PlayerRequest
import game_engine
from sessions.session import SessionData, backend, cookie, verifier
from websocket import connection_manager

origins = ["http://localhost:5173"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/game", response_model=GameResponseModel)
async def create_game(request: GameCreateModel, response: Response):
    player_id = str(uuid.uuid4())
    player = Player(id=player_id, name=request.player_name)
    cards_in_db = game_engine.setup_deck()
    draw_pile = [card["id"] for card in cards_in_db]
    game = GameInDB(players=[player], cards=cards_in_db, draw_pile=draw_pile)

    created_game = await DB.create_game(game)

    session = uuid4()
    print(session)
    session_data = SessionData(player_id=player_id, game_id=str(created_game["_id"]))
    await backend.create(session, session_data)

    cookie.attach_to_response(response, session)

    return created_game


@app.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    return session_data.player_id


@app.get(
    "/games",
    response_model=GameCollection,
    response_description="List all created games"
)
async def list_games():
    return GameCollection(games=await DB.list_games())


@app.post("/games/{game_id}/join",
          response_model=GameResponseModel,
          description="Add player to a game")
async def join_game(game_id: str, request: PlayerRequest = Body(...)):
    existing_game = GameInDB(**(await DB.get_game_by_id(game_id)))
    if existing_game.state == GameState.WAITING:
        # player = {
        #     k: v for k,v in request.model_dump(by_alias = True).items() if v is not None
        # }
        new_player = Player(id=str(uuid.uuid4()),
                            name=request.name,
                            )

        update_game = await DB.add_player_game_by_id(
            game_id=game_id,
            player=new_player.model_dump(by_alias=True)
        )
        return update_game
    else:
        raise HTTPException(status_code=403, detail=f"Game {game_id} is not waiting for players to join.")


@app.post("/games/{game_id}/start", response_model=GameResponseModel)
async def start_game(game_id: str):
    existing_game = GameInDB(**(await DB.get_game_by_id(game_id)))
    if len(existing_game.players) < 2:
        raise HTTPException(status_code=400, detail=f"Need 2 or more players to start the game")
    if existing_game.state in [GameState.IN_PROGRESS, GameState.COMPLETED]:
        raise HTTPException(status_code=400, detail=f"Cannot start a game that is already running or complete.")

    existing_game.state = GameState.IN_PROGRESS
    await DB.update_game_state(game_id, existing_game.state)
    existing_game.deal_cards()
    update_game = await DB.update_card_play(existing_game.model_dump(by_alias=True))
    return update_game


@app.websocket("/ws/{game_id}/{player_id}")
async def websocket_game(websocket: WebSocket, game_id: str, player_id: str) -> None:
    await connection_manager.connect(websocket, game_id=game_id, player_id=player_id)
    try:
        while True:
            card_play_json = await websocket.receive_json()
            card_play_request = PlayerCardPlayRequest(**card_play_json)
            game = GameInDB(**(await DB.get_game_by_id(game_id)))

            # check player turn
            current_player_index = int(game.current_player_index)
            current_player = game.is_valid_player(player_id)
            if game.state != GameState.IN_PROGRESS:
                raise GameNotInProgress()
                # player validity
            elif not any(player.id == player_id for player in game.players):
                raise InvalidPlayer()
            elif not current_player:
                raise NotYourTurn()
            # check card validity
            elif not game.is_valid_card(card_id=card_play_request.card_id):
                raise InvalidCard()
            ''' 
            {
                    "card_id": "a8b9a3cc-8802-4d87-b6a7-08a23a6ff43e",
                    "target_player_id": "string",
                    "target_property_color": "brown",
                    "target_property_id": "string",
                    "self_property_color": "brown",
                    "self_property_id": "string"
                }
            '''
            result = game.play_card(card_request=card_play_request,game_id=game_id,player_id=player_id)
            if result:
                await DB.update_card_play(game.model_dump(by_alias=True))
                game_response = GameResponseModel(**game.model_dump(by_alias=True))
                await connection_manager.broadcast_game(game_response)

                for player in game.players:
                    player_hand = [game.get_card_details(card) for card in player.hand]
                    await connection_manager.send_personal_game_data(player.id, game_id, player_hand)
                    print(f"message sent to {player.name}")


    except CustomError as error:
        await connection_manager.send_personal_message(
            player_id,
            game_id,
            {"error": error.default_message})
    except WebSocketDisconnect:
        await connection_manager.disconnect(websocket, game_id, player_id)


@app.post("/game/{game_id}/play", response_model=GameResponseModel, dependencies=[Depends(cookie)])
async def play_card(game_id: str, card_request: PlayerCardPlayRequest, player_id: str, session_data: SessionData):
    session_data = SessionData()
    existing_game = await DB.get_game_by_id(game_id)
    card_id = card_request.card_id
    game = GameInDB(**existing_game)
    # check game state
    if game.state != GameState.IN_PROGRESS:
        raise HTTPException(status_code=400, detail="Game is not in progress.")
    # player validity
    if not any(player.id == player_id for player in game.players):
        raise HTTPException(status_code=404, detail=f"Player ID: {player_id} not found in the game {game_id}")
    # check player turn
    current_player_index = int(game.current_player_index)
    current_player = game.is_valid_player(player_id)
    if not current_player:
        raise HTTPException(status_code=400, detail="Not your turn")
    # check card validity
    if not game.is_valid_card(card_id=card_id):
        raise HTTPException(status_code=400, detail="Card not found in player hand")

    # Handle Cards
    card = next(card for card in game.cards if card.id == card_id)
    player = game.players[current_player_index]
    ## collect money
    if card.card_type == CardType.MONEY:
        game.players[current_player_index].hand.remove(card_id)
        game.players[current_player_index].money_pile.append(card_id)
        game.action_remaining_per_turn -= 1
        updated_game = await DB.update_card_play(game.model_dump(by_alias=True))
        # return card_play

    ## play property
    if card.card_type in [CardType.PROPERTY, CardType.WILD_PROPERTY]:
        if card.card_type == CardType.WILD_PROPERTY:
            wild_property = card
            if not card_request.self_property_color:
                raise HTTPException(status_code=400, detail="Property color must be specified for wild property card")
            if card_request.self_property_color not in wild_property.colors:
                raise HTTPException(status_code=400, detail="Invalid color specified for wild property card")

        if game.play_property(card_request, card):
            game.update_remaining_actions()
            game.players[current_player_index] = player
            if card.card_type == CardType.WILD_PROPERTY:
                await update_wild_property(game_id, card)
                updated_game = await DB.update_card_play(game.model_dump(by_alias=True))
        else:
            raise HTTPException(status_code=400, detail="Failed to play property.")

    ## play action
    if card.card_type in CardType.ACTION:
        print("ACTION TIME")
        if card.action_type in [ActionCardType.PASS_GO, ActionCardType.ITS_MY_BIRTHDAY]:
            play_action_card(game, action_card=card)
            game.update_remaining_actions()
        action_played = await update_card_play(game.model_dump(by_alias=True))
        return action_played
    if card.action_type in [ActionCardType.DEAL_BREAKER,
                            ActionCardType.SLY_DEAL,
                            ActionCardType.FORCED_DEAL,
                            ActionCardType.DEBT_COLLECTOR]:
        pass

    if card.card_type in [CardType.RENT, CardType.WILD_RENT]:
        print("time to pay rent")

    if game.action_remaining_per_turn == 0:
        game.next_player()

    if game.check_winner():
        existing_game = await DB.update_game_state(game_id, game.state)

    return game


@app.post("/game/{game_id}/discard", response_model=GameResponseModel)
async def discard_card(game_id: str, discard_request: PlayerCardSDiscardRequest, player_id):
    existing_game = GameInDB(**(await DB.get_game_by_id(game_id)))
    existing_game.discard_card()
