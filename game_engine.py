# Initialise and maintain state of game elements

import random
from typing import List, Optional

from cards import *
from player import Player

MAX_IN_HAND_CARD_COUNT = 7

class GameEngine:
    def __init__(self,player_names: List[str]):
        self.players = [Player(name) for name in player_names]
        self.current_player_id = 0
        self.draw_pile = []
        self.discard_pile = []
        self.setup_deck()
        self.deal_cards()

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
                print("Done reshuffling, Continue !!!")
            if self.draw_pile:
                player.add_to_hand(self.draw_pile.pop())

    def current_player(self) -> Player:
        # returns current player
        return self.players[self.current_player_id]

    def next_player(self):
        # pick next player, update the current player index
        self.current_player_id = (self.current_player_id + 1) % len(self.players)
        return self.players[self.current_player_id]

    def process_action_card(self,action_card: Card, target_player: Optional[Player] = None) -> bool:
        # depeding on the type of action manage the money and properties etc
        # pass go
        # debt collector
        # rent/wild rent
        # birthday
        # 
        pass

    def collect_money(self, from_player: Player, to_player: Player, amount: int) -> int:
        # find the closest denomination to pay with money or property
        # first preference will be money pile then property will be chosen
        # TODO : Player property for payment
        money_available = from_player.total_worth()
        if money_available > amount:
            payment_cards = []
            transferred_money = 0
            
            for card in sorted(from_player.money_pile, key=lambda card: card.value):
                if transferred_money + card.value <= amount:
                    payment_cards.append(card)
                    transferred_money +=card.value
                if transferred_money >= amount:
                    break
            
            for card in payment_cards:
                from_player.money_pile.remove(card)
                to_player.money_pile.append(card)
            
            return transferred_money
        else:
            for card in from_player.money_pile:
                from_player.money_pile.remove(card)
                to_player.money_pile.append(card)
            
            return transferred_money



    def Check_winner(self) -> Optional[Player]:
        # check propertyset of each player before changing turn
        pass
