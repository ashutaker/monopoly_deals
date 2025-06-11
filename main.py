from fastapi import FastAPI, Body, HTTPException
import db.mongo as DB
from game_engine import *
from models.cards import Card
from models.game import Game, GameCreateModel, GameCollection, GameState, PlayerCardPlayRequest, GameResponseModel, \
    GameInDB
from models.player import Player, PlayerRequest
import game_engine

app = FastAPI()

@app.post("/game", response_model=GameResponseModel)
async def create_game(request: GameCreateModel):
    player_id = str(uuid.uuid4())
    player = Player(id=player_id,name= request.player_name)
    cards_in_db = game_engine.setup_deck()
    draw_pile = [card["id"] for card in cards_in_db]
    game = GameInDB(players = [player], cards= cards_in_db, draw_pile=draw_pile)
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
async def join_game(game_id: str, request: PlayerRequest = Body(...)):
    existing_game = GameInDB(**(await DB.get_game_by_id(game_id)))
    if existing_game.state == GameState.WAITING:
        # player = {
        #     k: v for k,v in request.model_dump(by_alias = True).items() if v is not None
        # }
        new_player = Player(id=str(uuid.uuid4()),
                            name= request.name,
                            )

        update_game = await DB.add_player_game_by_id(
            game_id = game_id,
            player = new_player.model_dump(by_alias=True)
        )
        return update_game
    else:
        raise HTTPException(status_code=403,detail=f"Game {game_id} is not waiting for players to join.")

@app.post("/games/{game_id}/start", response_model=GameResponseModel)
async def start_game(game_id: str):
    existing_game = GameInDB(**(await DB.get_game_by_id(game_id)))
    if len(existing_game.players) < 2:
        raise HTTPException(status_code=400,detail=f"Need 2 or more players to start the game")
    update_state = await DB.update_game_state(game_id, GameState.IN_PROGRESS.value)
    deal_card = deal_cards(update_state)
    update_game = await DB.update_card_play(deal_card)
    return update_game


@app.post("/game/{game_id}/play", response_model= GameResponseModel)
async def play_card(game_id: str, card_request: PlayerCardPlayRequest, player_id: str):
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
    current_player = get_current_player(current_index=current_player_index,
                                        players= game.players,
                                        player_id=player_id)
    if not current_player:
        raise HTTPException(status_code=400, detail="Not your turn")
    # check card validity
    if not is_valid_card(card_id=card_id,player_hand=current_player.hand):
        raise HTTPException(status_code=400, detail="Card not found in player hand")

    # Handle Cards
    card = next(card for card in game.cards if card.id == card_id)
    player = game.players[current_player_index]
    ## collect money
    if card.card_type == CardType.MONEY:
        # existing_game["players"][current_player_index]["hand"].remove(card_id)
        game.players[current_player_index].hand.remove(card_id)
        game.players[current_player_index].money_pile.append(card_id)
        game.action_remaining_per_turn -= 1
        card_play = await DB.update_card_play(game.model_dump(by_alias=True))
        return card_play

    ## play property
    if card.card_type == CardType.PROPERTY:
        print(card)
        property_card = card
        color = property_card.color
        if color not in player.property_set:
            player.property_set[color] = []
        player.hand.remove(card_id)
        player.property_set[color].append(card_id)
        game.action_remaining_per_turn -= 1
        game.players[current_player_index] = player
        property_played = await DB.update_card_play(game.model_dump(by_alias=True))
        return property_played
    if card.card_type == CardType.WILD_PROPERTY:
        wild_property = card
        if not card_request.self_property_color:
            raise HTTPException(status_code=400, detail="Property color must be specified for wild property card")
        if card_request.self_property_color not in wild_property.colors:
            raise HTTPException(status_code=400, detail="Invalid color specified for wild property card")
        wild_property.assigned_color = card_request.self_property_color
        if wild_property.assigned_color not in player.property_set:
            player.property_set[wild_property.assigned_color] = []
        print("its wild wild")
        player.hand.remove(card_id)
        player.property_set[wild_property.assigned_color].append(card_id)
        game.action_remaining_per_turn -= 1
        await update_wild_property(game_id,wild_property)
        wild_property_played = await DB.update_card_play(game.model_dump(by_alias=True))
        return wild_property_played
    ## play action
    if card.card_type in CardType.ACTION:
        print("ACTION TIME")

    return existing_game
