# Initialise and maintain state of game elements
import random
import uuid
from typing import Optional

from db.mongo import *
from core.util import *
from models.cards import *
from models.game import PlayerCardPlayRequest
from models.player import Player


def setup_deck() -> list[CardInDB]:
    cards : list[CardInDB] = []
    # # Create complete deck of the playable cards and add them to draw pile
    # # shuffle the pile before dealing cards to player
    # ## Action Cards x 34
    action_cards = [ # action, value, count
        (ActionCardType.DEAL_BREAKER, 5, 2),
        (ActionCardType.FORCED_DEAL, 3, 3),
        (ActionCardType.SLY_DEAL, 3, 3),
        (ActionCardType.JUST_SAY_NO, 4, 3),
        (ActionCardType.DEBT_COLLECTOR, 3, 3),
        (ActionCardType.ITS_MY_BIRTHDAY, 2, 3),
        (ActionCardType.PASS_GO, 1, 10),
        (ActionCardType.HOUSE, 3, 3),
        (ActionCardType.HOTEL, 4, 2),
        (ActionCardType.DOUBLE_RENT, 1, 2)
    ]
    for action,value,count in action_cards:
        cards.extend([ActionCard(
            id=str(uuid.uuid4()),
            card_type= CardType.ACTION,
            action_type = action,
            name=f"Action : {action.name}",
            value = value
        ).model_dump()
        for _ in range(count)]
    )
    # ## Property Cards x 28
    for color in PropertyColor:
        property_value = 1 if color in [PropertyColor.BROWN, PropertyColor.LIGHT_BLUE] else \
                        2 if color in [PropertyColor.PINK, PropertyColor.ORANGE] else \
                        3 if color in [PropertyColor.RED, PropertyColor.YELLOW] else \
                        4 if color in [PropertyColor.GREEN, PropertyColor.DARK_BLUE] else \
                        2 if color in [PropertyColor.RAILROAD, PropertyColor.UTILITY] else 0
        for _ in range(PROPERTY_SET_SIZE[color]):
            cards.append(PropertyCard(
                card_type= CardType.PROPERTY,
                id = str(uuid.uuid4()),
                value= property_value,
                name=f"Property: {color.name}",
                color = color
            ).model_dump()
            )

    # ## Wild Property Cards x 11
    cards.append(WildPropertyCard(id=str(uuid.uuid4()),name="Property: Dark Blue/Green", value = 4,
                                  card_type= CardType.WILD_PROPERTY,
                                  colors=[PropertyColor.DARK_BLUE,PropertyColor.GREEN]).model_dump())
    cards.append(WildPropertyCard(id=str(uuid.uuid4()), name="Property: Light Blue/ Brown", value=1,
                                  card_type=CardType.WILD_PROPERTY,
                                  colors=[PropertyColor.LIGHT_BLUE, PropertyColor.BROWN]).model_dump())
    cards.append(WildPropertyCard(id=str(uuid.uuid4()), name="Property: Orange/Pink", value=2,
                                  card_type=CardType.WILD_PROPERTY,
                                  colors=[PropertyColor.ORANGE,PropertyColor.PINK]).model_dump())
    cards.append(WildPropertyCard(id=str(uuid.uuid4()), name="Property: Orange/Pink", value=2,
                                  card_type=CardType.WILD_PROPERTY,
                                  colors=[PropertyColor.ORANGE, PropertyColor.PINK]).model_dump())
    cards.append(WildPropertyCard(id=str(uuid.uuid4()), name="Property: RailRoad/Green", value=4,
                                  card_type=CardType.WILD_PROPERTY,
                                  colors=[PropertyColor.RAILROAD, PropertyColor.GREEN]).model_dump())
    cards.append(WildPropertyCard(id=str(uuid.uuid4()), name="Property: RailRoad/light blue", value=4,
                                  card_type=CardType.WILD_PROPERTY,
                                  colors=[PropertyColor.RAILROAD, PropertyColor.LIGHT_BLUE]).model_dump())
    cards.append(WildPropertyCard(id=str(uuid.uuid4()), name="Property: RailRoad/utility", value=2,
                                  card_type=CardType.WILD_PROPERTY,
                                  colors=[PropertyColor.RAILROAD, PropertyColor.UTILITY]).model_dump())
    cards.append(WildPropertyCard(id=str(uuid.uuid4()), name="Property: Red/Yellow", value=3,
                                  card_type=CardType.WILD_PROPERTY,
                                  colors=[PropertyColor.RED, PropertyColor.YELLOW]).model_dump())
    cards.append(WildPropertyCard(id=str(uuid.uuid4()), name="Property: Red/Yellow", value=3,
                                  card_type=CardType.WILD_PROPERTY,
                                  colors=[PropertyColor.RED, PropertyColor.YELLOW]).model_dump())
    cards.append(WildPropertyCard(id=str(uuid.uuid4()), name="Property: Red/Yellow", value=0,
                                  card_type=CardType.WILD_PROPERTY,
                                  colors=[color for color in PropertyColor]).model_dump())
    cards.append(WildPropertyCard(id=str(uuid.uuid4()), name="Property: Red/Yellow", value=0,
                                  card_type=CardType.WILD_PROPERTY,
                                  colors=[color for color in PropertyColor]).model_dump())

    # ## Rent Cards x 13
    for _ in range(2):
        for color_set in [[PropertyColor.DARK_BLUE, PropertyColor.GREEN],
                          [PropertyColor.LIGHT_BLUE, PropertyColor.BROWN],
                          [PropertyColor.ORANGE,PropertyColor.PINK],
                          [PropertyColor.RAILROAD, PropertyColor.UTILITY],
                          [PropertyColor.RED, PropertyColor.YELLOW]]:
            cards.append(RentCard(
                id = str(uuid.uuid4()),
                name = f"Rent : {"/".join([c.name for c in color_set])}",
                card_type=CardType.RENT,
                colors= color_set,
                value= 1
            ).model_dump())
    cards.extend([RentCard(
        id=str(uuid.uuid4()),
        name=f"Wild Rent",
        card_type=CardType.RENT,
        value=3
        ).model_dump() for _ in range(3)]
    ) # all color

    ## Money Cards x20
    for value, count in [(10,1), (5,2), (4,3), (3,3), (2,5), (1,6)]:
        for _ in range(count):
            cards.append(Card(
                id=str(uuid.uuid4()),
                name= f"Money: {value}M",
                card_type=CardType.MONEY,
                value=value).model_dump())
    random.shuffle(cards)
    return cards

def deal_cards(game: dict) -> dict:
    # add 5 card to each player hand
    print("Dealing cards to players ...")
    for _ in range(5):
        for player in game["players"]:
            card = game["draw_pile"].pop()
            player["hand"].append(card)
    game["action_remaining_per_turn"] = 3
    return game

def draw_card(game,player: Player, draw_count: int = 2):
    # game engine will check the draw_pile count for each player to deal card
    # to them default is 2 for start of turn and PASS GO
    for _ in range(draw_count):
        if not game.draw_pile:
            print("No cards left in draw pile. Reshuffling discard pile back to draw pile !!")
            game.draw_pile = game.discard_pile
            game.discard_pile = []
            random.shuffle(game.draw_pile)
            print("Done reshuffling !!!")
        if game.draw_pile:
            player.hand.append(game.draw_pile.pop())
    print(f"{draw_count} cards added to {player.name}'s hand")

def get_current_player(current_index: int, players: list[Player], player_id: str) -> Player:
    for idx, player in enumerate(players):
        if player.id == player_id and idx == current_index:
            return player
    return None

def is_valid_card(card_id: str, player_hand: list[str]) -> bool:
    if card_id in player_hand:
        return True
    return False

def next_player(game: GameInDB):
    # pick next player in turn, set it to current player
    game.current_player_index = (game.current_player_id + 1) % len(game.players)
    return game.current_player_index

def play_property(card_request: PlayerCardPlayRequest, card: CardInDB ,player: Player):
    print(card_request)
    card_id = card_request.card_id
    if card.card_type == CardType.PROPERTY:
        property_card = card
        color = property_card.color
        if color not in player.property_set:
            player.property_set[color] = []
        player.hand.remove(card_id)
        player.property_set[color].append(card_id)
        return  True

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
        return True
    return False

def play_action_card(game: GameInDB,action_card: CardInDB, target_player: Optional[Player] = None) -> bool:
    # depending on the type of action card manage the money and properties etc
    current_player = game.players[game.current_player_index]
    if action_card.action_type == ActionCardType.PASS_GO:
        draw_card(game,current_player)
        current_player.hand.remove(action_card.id)
        game.discard_pile.append(action_card.id)
        return True
    elif action_card.action_type == ActionCardType.DEBT_COLLECTOR:
        amount = 5
        transferred = collect_money(target_player, current_player, amount)
        if transferred:
           print(f"Successfully transferred {transferred}M from {target_player.name} to {current_player.name}.")
        current_player.hand.remove(action_card.id)
        game.discard_pile.append(action_card.id)
        return True
    elif action_card.action_type == ActionCardType.ITS_MY_BIRTHDAY:
        # collect money from all the other players
        amount = 2
        for player in game.players:
            if player != current_player:
                if player.total_worth() == 0:
                    print(f"{player.name} has 0M ")
                    continue
                transferred = collect_money(player, current_player,amount)
                if transferred:
                    print(f"Successfully transferred {transferred}M from {player.name} to {current_player.name}.")
        current_player.hand.remove(action_card.id)
        game.discard_pile.append(action_card.id)
        return True
    #     elif action_card.action_type == ActionCardType.DEAL_BREAKER:
    #         full_set_dict = {}
    #         for i,color in enumerate(target_player.property_sets):
    #             if target_player.has_full_propertyset(color):
    #                 print(f"{i + 1} - {color}" )
    #                 full_set_dict[i] = color
    #         if not full_set_dict:
    #            print(f"{target_player.name} has no full set to steal. Cannot play {ActionCardType.DEAL_BREAKER.name}")
    #            return False
    #         property_color = int(input(f"{current_player.name} Which color do you want to steal? ")) - 1
    #         if property_color in full_set_dict.keys():
    #             steal_property_set = target_player.property_sets.pop(full_set_dict[property_color])
    #             current_player.property_sets[full_set_dict[property_color]].extend(steal_property_set)
    #             return True
    #         else:
    #             print("Invalid Choice !!")
    #     elif action_card.action_type == ActionCardType.SLY_DEAL:
    #         full_set_dict = {}
    #         if not target_player.property_sets:
    #             print(f"{target_player.name} has no property to steal. Cannot play {ActionCardType.SLY_DEAL.name}")
    #             return False
    #         for i, color in enumerate(target_player.property_sets):
    #             if target_player.property_sets[color]:
    #                 print(f"{i + 1} - {color}")
    #                 full_set_dict[i] = color
    #         property_color = int(input(f"{current_player.name} From which color do you want to steal? ")) - 1
    #         if property_color in full_set_dict.keys():
    #             for j,prop in enumerate(target_player.property_sets[full_set_dict[property_color]]):
    #                 print(f"{ j + 1 } - {prop}")
    #                 steal_prop = int(input(f"{current_player.name} From which prop do you want to steal? ")) - 1
    #                 if steal_prop in range(len(target_player.property_sets[full_set_dict[property_color]])):
    #                     # check for just say no
    #                     stolen = target_player.property_sets[full_set_dict[property_color]].pop(steal_prop)
    #                     current_player.property_sets[full_set_dict[property_color]].append(stolen)
    #                     return True
    #             else:
    #                 print("Invalid Choice !!")
    #         else:
    #             print("Invalid Choice !!")
    #     elif action_card.action_type == ActionCardType.FORCE_DEAL:
    #         full_set_dict = {}
    #         take_property_color = None
    #         take_property_index = None
    #         give_property_color = None
    #         give_property_index = None
    #         if not current_player.property_sets:
    #             print(f"YOU do not have any property to swap cannot play {ActionCardType.FORCE_DEAL.name}")
    #             return False
    #         # property to give
    #         full_set_dict = {}
    #         for i, color in enumerate(current_player.property_sets):
    #             if current_player.property_sets[color]:
    #                 print(f"{i + 1} - {color}")
    #                 full_set_dict[i] = color
    #         give_property_choice = int(input(f"{current_player.name} From which color do you want to GIVE? ")) - 1
    #         if give_property_choice in full_set_dict.keys():
    #             give_property_color = full_set_dict[give_property_choice]
    #             for j, prop in enumerate(current_player.property_sets[full_set_dict[give_property_color]]):
    #                 print(f"{j + 1} - {prop}")
    #             give_prop = int(input(f"{current_player.name} Which prop do you want to GIVE? ")) - 1
    #             if give_prop in range(len(current_player.property_sets[full_set_dict[give_property_color]])):
    #                 # check for just say no
    #                 give_property_index = give_prop
    #             else:
    #                 print("Invalid Choice !!")
    #         else:
    #             print("Invalid Choice !!")
    #         # property to take
    #         full_set_dict = {}
    #         for i, color in enumerate(target_player.property_sets):
    #             if target_player.property_sets[color]:
    #                 print(f"{i + 1} - {color}")
    #                 full_set_dict[i] = color
    #         take_property_choice = int(input(f"{current_player.name} From which color do you want to STEAL? ")) - 1
    #         if take_property_choice in full_set_dict.keys():
    #             take_property_color = full_set_dict[take_property_choice]
    #             for j, prop in enumerate(target_player.property_sets[full_set_dict[take_property_color]]):
    #                 print(f"{j + 1} - {prop}")
    #             steal_prop = int(input(f"{current_player} Which prop do you want to STEAL? ")) - 1
    #             if steal_prop in range(len(target_player.property_sets[full_set_dict[take_property_color]])):
    #                 # check for just say no
    #                 take_property_index = steal_prop
    #             else:
    #                 print("Invalid Choice !!")
    #         else:
    #             print("Invalid Choice !!")
    #
    #         if take_property_index and give_property_index:
    #             take_card = target_player.property_sets[take_property_color].pop(take_property_index)
    #             current_player.property_sets[take_property_color].append(take_card)
    #
    #             give_card = current_player.property_sets[give_property_color].pop(give_property_index)
    #             target_player.property_sets[give_property_color].append(give_card)
    #             return True
    #         return False
    #
    # elif action_card.card_type == CardType.RENT:
    #     # check if player has the called color in property set
    #     # calculate the amount as per properties in set
    #     # collect money from every player
    #     rent_card = action_card
    #
    #     all_rents=[]
    #     for color in rent_card.colors:
    #         if current_player.property_sets[color]:
    #             set_size = len(current_player.property_sets[color])
    #             rent_value = PropertyCard._property_set_rent_values[color][set_size - 1]
    #             all_rents.append(rent_value)
    #     if all_rents:
    #         amount = int(max(all_rents)) * self.RENT_MULTIPLIER
    #         for player in self.players:
    #             if player != current_player:
    #                 transferred = self.collect_money(player, current_player,amount)
    #                 if transferred:
    #                     print(f"Successfully transferred {transferred}M from {player.name} to {current_player.name}.")
    #         self.RENT_MULTIPLIER = 1 # resetting multiplier after collecting all rents
    #         return True
    #     else:
    #         print("Cannot collect rent no properties played. Returning card to player hand !!")
    #         current_player.add_to_hand(rent_card)
    #         return False
    # elif action_card.card_type == CardType.WILD_RENT:
    #     if target_player:
    #         all_rents=[]
    #         for color in current_player.property_sets:
    #             set_size = len(current_player.property_sets[color])
    #             rent_value = PropertyCard._property_set_rent_values[color][(set_size - 1)]
    #             all_rents.append(rent_value)
    #         amount = int(max(all_rents)) * self.RENT_MULTIPLIER
    #         if amount:
    #             transferred = self.collect_money(target_player,current_player,amount)
    #             if transferred:
    #                     print(f"Successfully transferred {transferred}M from {target_player.name} to {current_player.name}.")
    #         self.RENT_MULTIPLIER = 1 # resetting multiplier
    #         return True
    return False

def collect_money(self, from_player: Player, to_player: Player, amount: int) -> int:
    # find the closest denomination to pay with money or property
    # first preference will be money pile then property will be chosen
    # TODO : Player property for payment
    money_available = from_player.total_worth()
    money_transferred = 0

    if 0 < money_available >= amount:
        sort_money_cards = sorted(from_player.money_pile, key=lambda card: card.value, reverse=True)
        sort_money_value = [card.value for card in sort_money_cards]
        cards_to_transfer_by_value = get_cards_by_value(sort_money_value, amount)

        for card_value in cards_to_transfer_by_value:
            pay_card = ([card for card in from_player.money_pile if card.value == card_value][0])
            from_player.money_pile.remove(pay_card)
            to_player.money_pile.append(pay_card)

        money_transferred =  sum(cards_to_transfer_by_value)
    elif money_available < amount:
        for card in from_player.money_pile:
            from_player.money_pile.remove(card)
            to_player.money_pile.append(card)
        money_transferred =  sum(card.value for card in from_player.money_pile)
    return money_transferred

def get_game_state(self):
    # Shows all player money and property
    pass

def display_player_hand(self,player: Player):
    print(f"\n{player.name}'s hand", "-" * 20)
    for i, card in enumerate(player.hand):
        print(f"{i+1} - {card}")

def display_player_properties(self,player: Player):
    if player.property_sets:
        print(f"\n{player.name}'s Property in play","-" * 20)
        for color, (current_size,required_size) in player.get_owned_property_info().items():
            properties = player.property_sets[color]
            print(f"{color.name} : {current_size}/{required_size}")
            print([card.name for card in properties])
    else:
        print(f"\n{player.name} has no properties in play.")

def check_winner(self) -> Optional[Player]:
    # check propertyset of each player before changing turn
    current_player = self.current_player()
    complete_property_set = 0
    for color in current_player.property_sets:
        if current_player.has_full_propertyset(color):
            complete_property_set +=1
    if complete_property_set == 3:
        return current_player
    return None

