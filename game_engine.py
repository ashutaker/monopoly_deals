# Initialise and maintain state of game elements

import random
from typing import List, Optional
from util import * 
from cards import *
from player import Player



class GameEngine:
    def __init__(self,player_names: List[str]):
        self.players = [Player(name) for name in player_names]
        self.current_player_id = 0
        self.draw_pile = []
        self.discard_pile = []
        self.setup_deck()
        self.deal_cards()

    MAX_IN_HAND_CARD_COUNT = 7


    def setup_deck(self):
            # Create complete deck of the playable cards and add them to draw pile
            # shuffle the pile before dealing cards to player

            print("Unpacking a new deck of cards...")
            ## Action Cards x 34
            ### Deal Breaker x 2
            self.draw_pile.extend([ActionCard(ActionCardType.DEAL_BREAKER, 5) for _ in range(2)])

            ### Just Say No x 3
            self.draw_pile.extend([ActionCard(ActionCardType.JUST_SAY_NO, 4) for _ in range(3)])
            
            ### Debt Collector x3
            self.draw_pile.extend([ActionCard(ActionCardType.DEBT_COLLECTOR, 3) for _ in range(3)])

            ### Double the Rent x 2
            self.draw_pile.extend([ActionCard(ActionCardType.DOUBLE_RENT, 1) for _ in range(2)])    

            ### Force Deal x 3
            self.draw_pile.extend([ActionCard(ActionCardType.FORCE_DEAL, 3) for _ in range(3)])

            ### Hotel x 2
            self.draw_pile.extend([ActionCard(ActionCardType.HOTEL, 4) for _ in range(2)])

            ### House x 3
            self.draw_pile.extend([ActionCard(ActionCardType.HOUSE, 4) for _ in range(3)])

            ###  Its My Birthday x 3
            self.draw_pile.extend([ActionCard(ActionCardType.ITS_MY_BIRTHDAY, 2) for _ in range(3)])

            ### Pass GO x 10
            self.draw_pile.extend([ActionCard(ActionCardType.PASS_GO, 1) for _ in range(10)])

            ### Sly Deal x 3
            self.draw_pile.extend([ActionCard(ActionCardType.SLY_DEAL, 3) for _ in range(3)])


            ## Property Cards x 28
            ### Brown
            self.draw_pile.append(PropertyCard("Brown 1",PropertyColor.BROWN, 1, [1,2], 2))
            self.draw_pile.append(PropertyCard("Brown 2",PropertyColor.BROWN, 1, [1,2], 2))

            ### Dark Blue
            self.draw_pile.append(PropertyCard("Dark Blue 1",PropertyColor.DARK_BLUE, 4, [3,8], 2))
            self.draw_pile.append(PropertyCard("Dark Blue 2",PropertyColor.DARK_BLUE, 4, [3,8], 2))

            ### Green
            self.draw_pile.append(PropertyCard("Green 1",PropertyColor.GREEN, 4, [2,4,7], 3))                                
            self.draw_pile.append(PropertyCard("Green 2",PropertyColor.GREEN, 4, [2,4,7], 3))
            self.draw_pile.append(PropertyCard("Green 3",PropertyColor.GREEN, 4, [2,4,7], 3))  

            ### Light Blue
            self.draw_pile.append(PropertyCard("Light Blue 1", PropertyColor.LIGHT_BLUE, 1, [1,2,3], 3))
            self.draw_pile.append(PropertyCard("Light Blue 2", PropertyColor.LIGHT_BLUE, 1, [1,2,3], 3))
            self.draw_pile.append(PropertyCard("Light Blue 3", PropertyColor.LIGHT_BLUE, 1, [1,2,3], 3))

            ### Orange
            self.draw_pile.append(PropertyCard("Orange 1", PropertyColor.ORANGE, 2, [1,3,5], 3))
            self.draw_pile.append(PropertyCard("Orange 2", PropertyColor.ORANGE, 2, [1,3,5], 3))
            self.draw_pile.append(PropertyCard("Orange 3", PropertyColor.ORANGE, 2, [1,3,5], 3))

            ### Pink
            self.draw_pile.append(PropertyCard("Pink 1", PropertyColor.PINK, 2, [1,2,4], 3))
            self.draw_pile.append(PropertyCard("Pink 2", PropertyColor.PINK, 2, [1,2,4], 3))
            self.draw_pile.append(PropertyCard("Pink 3", PropertyColor.PINK, 2, [1,2,4], 3))

            ### RAILROAD
            self.draw_pile.append(PropertyCard("Railroad 1", PropertyColor.RAILROAD, 2, [1,2,3,4], 4))
            self.draw_pile.append(PropertyCard("Railroad 2", PropertyColor.RAILROAD, 2, [1,2,3,4], 4))
            self.draw_pile.append(PropertyCard("Railroad 3", PropertyColor.RAILROAD, 2, [1,2,3,4], 4))
            self.draw_pile.append(PropertyCard("Railroad 4", PropertyColor.RAILROAD, 2, [1,2,3,4], 4))

            ### Utility
            self.draw_pile.append(PropertyCard("Utility 1", PropertyColor.UTILITY, 2, [1,2], 2))
            self.draw_pile.append(PropertyCard("Utility 2", PropertyColor.UTILITY, 2, [1,2], 2))

            ### Red
            self.draw_pile.append(PropertyCard("Red 1", PropertyColor.RED, 3, [2,3,6], 3))
            self.draw_pile.append(PropertyCard("Red 2", PropertyColor.RED, 3, [2,3,6], 3))
            self.draw_pile.append(PropertyCard("Red 3", PropertyColor.RED, 3, [2,3,6], 3))

            ### Yellow
            self.draw_pile.append(PropertyCard("Yellow 1", PropertyColor.YELLOW, 3, [2,4,6], 3))
            self.draw_pile.append(PropertyCard("Yellow 2", PropertyColor.YELLOW, 3, [2,4,6], 3))
            self.draw_pile.append(PropertyCard("Yellow 3", PropertyColor.YELLOW, 3, [2,4,6], 3))


            ## Wild Cards x 11
            self.draw_pile.append(WildPropertyCard("Dark Blue/Green", 
                                                   [PropertyColor.DARK_BLUE,PropertyColor.GREEN], 4))
            self.draw_pile.append(WildPropertyCard("Light Blue/ Brown",
                                                   [PropertyColor.LIGHT_BLUE, PropertyColor.BROWN], 1))
            self.draw_pile.append(WildPropertyCard("Orange/Pink 1",
                                                   [PropertyColor.ORANGE,PropertyColor.PINK], 2))
            self.draw_pile.append(WildPropertyCard("Orange/Pink 2",
                                                   [PropertyColor.ORANGE,PropertyColor.PINK], 2))
            self.draw_pile.append(WildPropertyCard("RailRoad/Green",
                                                   [PropertyColor.RAILROAD, PropertyColor.GREEN], 4))
            self.draw_pile.append(WildPropertyCard("RailRoad/light blue",
                                                   [PropertyColor.RAILROAD, PropertyColor.LIGHT_BLUE], 4))
            self.draw_pile.append(WildPropertyCard("RailRoad/utility",
                                                   [PropertyColor.RAILROAD, PropertyColor.UTILITY], 2))
            self.draw_pile.append(WildPropertyCard("Red/Yellow 1",
                                                   [PropertyColor.RED, PropertyColor.YELLOW], 3))
            self.draw_pile.append(WildPropertyCard("Red/Yellow 2",
                                                   [PropertyColor.RED, PropertyColor.YELLOW], 3))
            self.draw_pile.append(WildPropertyCard("Multi",
                                                   list(PropertyColor), 0))
            self.draw_pile.append(WildPropertyCard("Multi",
                                                   list(PropertyColor), 0))

            ## Rent Cards x 13 
            self.draw_pile.extend([WildRentCard(0) for _ in range(3)]) # all color
            self.draw_pile.extend([RentCard([PropertyColor.DARK_BLUE, PropertyColor.GREEN], 1) for _ in range(2)])
            self.draw_pile.extend([RentCard([PropertyColor.LIGHT_BLUE, PropertyColor.BROWN], 1) for _ in range(2)])
            self.draw_pile.extend([RentCard([PropertyColor.ORANGE,PropertyColor.PINK], 1) for _ in range(2)])
            self.draw_pile.extend([RentCard([PropertyColor.RAILROAD, PropertyColor.UTILITY], 1) for _ in range(2)])
            self.draw_pile.extend([RentCard([PropertyColor.RED, PropertyColor.YELLOW], 1) for _ in range(2)])


            ## Money Cards x20 
            self.draw_pile.append(MoneyCard(10))
            self.draw_pile.extend([MoneyCard(5) for _ in range(2)])
            self.draw_pile.extend([MoneyCard(4) for _ in range(3)])
            self.draw_pile.extend([MoneyCard(3) for _ in range(3)])
            self.draw_pile.extend([MoneyCard(2) for _ in range(5)])
            self.draw_pile.extend([MoneyCard(1) for _ in range(6)])


            # Shuffle the deck
            random.shuffle(self.draw_pile)
            print("Shuffled the deck, it is ready to use !!!")


    def deal_cards(self):
        # add 5 card to each player hand
        print("Dealing cards to players ...")
        for _ in range(5):
            for player in self.players:
                if self.draw_pile:
                    player.add_to_hand(self.draw_pile.pop())

    def draw_card(self,player: Player, draw_count: int = 2):
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
                player.add_to_hand(self.draw_pile.pop())
        print(f"{draw_count} cards added to {player.name}'s hand")

    def current_player(self) -> Player:
        # returns current player
        return self.players[self.current_player_id]

    def next_player(self) -> Player:
        # pick next player in turn, set it to current player
        self.current_player_id = (self.current_player_id + 1) % len(self.players)
        return self.players[self.current_player_id]

    def process_action_card(self,action_card: Card, target_player: Optional[Player] = None) -> bool:
        # depending on the type of action card manage the money and properties etc
        
        current_player = self.current_player()
        if action_card.card_type == CardType.ACTION:
            if action_card.action_type == ActionCardType.PASS_GO:
                self.draw_card(current_player)
                return True
            elif action_card.action_type == ActionCardType.DEBT_COLLECTOR:
                amount = 5
                transferred = self.collect_money(target_player, current_player, amount)
                if transferred:
                    print(f"Successfully transferred {transferred}M from {target_player.name} to {current_player.name}.")
                    return True
            elif action_card.action_type == ActionCardType.ITS_MY_BIRTHDAY:
                # collect money from all the other players
                amount = 2
                for player in self.players:
                    if player != current_player:
                        if player.total_worth() == 0:
                            print(f"{player.name} has 0M ")
                            continue
                        transferred = self.collect_money(player, current_player,amount)
                        if transferred:
                            print(f"Successfully transferred {transferred}M from {player.name} to {current_player.name}.")
                return True
            elif action_card.action_type == ActionCardType.DEAL_BREAKER:
                # Check if target wants to play just say no
                response_card = None
                full_set_dict = {}
                steal_property_set = []
                dealbreaker_denied = input(f"\n{target_player.name} Do you want to play {ActionCardType.JUST_SAY_NO.name}? [ 0 - NO, 1 - YES]:")
                if dealbreaker_denied == 1:
                    for card in target_player.hand:
                        if card.action_type == ActionCardType.JUST_SAY_NO:
                            response_card = card
                            break
                    target_player.hand.remove(response_card)
                    self.discard_pile.append(response_card)
                    for card in current_player.hand:
                        if card.action_type == ActionCardType.JUST_SAY_NO:
                            deny_jsn = card
                            break
                    current_player.hand.remove(deny_jsn)
                    self.discard_pile.append(deny_jsn)
                    return True
                elif dealbreaker_denied == 0:
                    for i,color in enumerate(target_player.property_sets):
                        if target_player.has_full_propertyset(color):
                            print(f"{i + 1} - {color}" )
                            full_set_dict[i] = color
                    property_color = int(input("Which color you want to steal? ")) - 1
                    if property_color in full_set_dict.keys():
                        steal_property_set = target_player.property_sets.pop(full_set_dict[property_color])
                        current_player.property_sets[full_set_dict[property_color]].extend(steal_property_set)
                        return True
                    else:
                        print("Invalid Choice !!")
                else:
                    print("Invalid Choice !!")
            elif action_card.action_type == ActionCardType.SLY_DEAL:
                # TODO : process sly deal card
                pass
            elif action_card.action_type == ActionCardType.FORCE_DEAL:
                # TODO : process force deal  card
                pass
            elif action_card.action_type == ActionCardType.DOUBLE_RENT:
                # TODO : process double rent card
                pass
        elif action_card.card_type == CardType.RENT:
            # check if player has the called color in property set
            # calculate the amount as per properties in set
            # collect money from every player
            rent_card = action_card

            all_rents=[]
            for color in rent_card.colors:
                if current_player.property_sets[color]:
                    set_size = len(current_player.property_sets[color])
                    rent_value = PropertyCard._property_set_rent_values[color][set_size - 1]
                    all_rents.append(rent_value)
            if all_rents:
                amount = int(max(all_rents))
                for player in self.players:
                    if player != current_player:
                        transferred = self.collect_money(player, current_player,amount)
                        if transferred:
                            print(f"Successfully transferred {transferred}M from {player.name} to {current_player.name}.")
                return True
            else:
                print("Cannot collect rent no properties played. Returning card to player hand !!")
                current_player.add_to_hand(rent_card)
                return False
        elif action_card.card_type == CardType.WILD_RENT:
            if target_player:
                all_rents=[]
                for color in current_player.property_sets:
                    set_size = len(current_player.property_sets[color])
                    rent_value = PropertyCard._property_set_rent_values[color][(set_size - 1)]
                    all_rents.append(rent_value)
                amount = int(max(all_rents))
                if amount:
                    transferred = self.collect_money(target_player,current_player,amount)
                    if transferred:
                            print(f"Successfully transferred {transferred}M from {target_player.name} to {current_player.name}.")
                return True
        return False


    def collect_money(self, from_player: Player, to_player: Player, amount: int) -> int:
        # find the closest denomination to pay with money or property
        # first preference will be money pile then property will be chosen
        # TODO : Player property for payment
        money_available = from_player.total_worth()

        if 0 < money_available >= amount:
            sort_money_cards = sorted(from_player.money_pile, key=lambda card: card.value, reverse=True)
            sort_money_value = [card.value for card in sort_money_cards]
            cards_to_transfer_by_value = get_cards_by_value(sort_money_value, amount)

            for card_value in cards_to_transfer_by_value:
                pay_card = ([card for card in from_player.money_pile if card.value == card_value][0])
                from_player.money_pile.remove(pay_card)
                to_player.money_pile.append(pay_card)

                return sum(cards_to_transfer_by_value)
        else:
            for card in from_player.money_pile:
                from_player.money_pile.remove(card)
                to_player.money_pile.append(card)

            return amount

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
                print( [property.name for property in properties] )
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
