# Initialise and maintainer the game session
from core.game_engine import GameEngine
from core.cards import CardType, ActionCardType


def run():
    print("Welcome to Monopoly Deals!!!")
    # num_players = int(input("Enter number of players (2-5): "))

    # if num_players< 2 or num_players > 5:
    #     print("Invalid number of players. Setting to 2.")
    #     num_players = 2

    # player_names= []
    # for i in range(num_players):
    #     name = input(f"Enter the name of player {i+1}: ")
    #     player_names.append(name)

    player_names = ["Ashu", "Neha", "Naval"]
    game = GameEngine(player_names)
    winner = None

    # for player in game.players:
    #     print(player.hand)
    while not winner:
        current_player = game.current_player()

        print("\n","=" *10,f"{current_player.name} to play !!","=" *10,)
        
        # Draw cards at the beginning of the turn
        draw_count = 2
        if len(current_player.hand) == 0: 
        # if no cards left in player's hand
            draw_count = 5
        game.draw_card(current_player, draw_count)

        # Upto 3 actions
        actions_performed = 0
        while actions_performed < 3:
            choice = None
            # Display player its hand, property and money
            ## properties
            print("=" * 40)
            for player in game.players:
                game.display_player_properties(player)
                print(f"Total money : {sum(card.value for card in player.money_pile)}")
            print("=" * 40)
            ## player hand
            game.display_player_hand(current_player)

            print("\nActions:", ("=" * 40))
            print("1. Add to money pile")
            print("2. Play a property card")
            print("3. Play an action card")
            print("4. Review hand")
            print("5. Review Property")
            print("0. End turn")

            choice = input(f"Choose an action (1-4) [{actions_performed + 1}/3]: ")
            if choice == "1" : # play into money pile
                card_index = int(input("Enter a card number from your hand to play into money pile: ")) - 1
                if current_player.play_money(card_index):
                    print("Card added to money pile !!!")
                    actions_performed += 1
                else:
                    print("Invalid card number entered.")

            elif choice == "2" : # play property
                card_index = int(input("Enter a card number from your hand to play property: ")) - 1
                if 0 <= card_index < len(current_player.hand):
                    if current_player.hand[card_index].card_type == CardType.WILD_PROPERTY:
                        wild_property = current_player.hand[card_index]
                        print("Available colors on wild property card : ")
                        for i, color in enumerate(wild_property.colors):
                            print(f"{i+1} - {color.name}")
                        wild_color_choice = int(input("Choose a color: ")) - 1
                        if 0 <= wild_color_choice < len(wild_property.colors):
                            assign_color = wild_property.colors[wild_color_choice]
                            if current_player.play_property(card_index,assign_color):
                                actions_performed +=1
                                print(f"Wild Property card played as {assign_color.name}")
                            else:
                                print("Failed to play wild property card")
                        else:
                            print("Invalid color selected.")
                    elif current_player.hand[card_index].card_type == CardType.PROPERTY:
                        if current_player.play_property(card_index):
                            actions_performed += 1
                        else:
                            print("Invalid card ")
                else:
                    print("Invalid card number entered.")
            elif choice == "3" : # play action
                card_index = int(input("Enter a card number from your hand to play: ")) - 1
                target_required = False
                target = None
                # Cheking for double rent card
                if (current_player.hand[card_index].card_type == CardType.ACTION and
                        current_player.hand[card_index].action_type == ActionCardType.DOUBLE_RENT):
                    if actions_performed < 2:
                        print(f"Select a rent card to play with {ActionCardType.DOUBLE_RENT.name}")
                        rent_card_index = int(input("Enter a rent card number from your hand to play: ")) - 1
                        if current_player.hand[rent_card_index].card_type in [CardType.RENT, CardType.WILD_RENT]\
                                and 0 <= rent_card_index < len(current_player.hand):
                            actions_performed += 1
                            current_player.hand.pop(card_index)
                            card_index = rent_card_index
                            game.RENT_MULTIPLIER = 2
                    else:
                        print(f"Must have 2 turns left to play {ActionCardType.DOUBLE_RENT.name}.")
                if 0 <= card_index < len(current_player.hand):
                    if current_player.hand[card_index].card_type in [
                        CardType.RENT, 
                        ActionCardType.ITS_MY_BIRTHDAY,
                        ActionCardType.PASS_GO
                    ]:
                        target_required = False

                    elif current_player.hand[card_index].card_type == CardType.WILD_RENT:
                        target_required = True

                    elif (current_player.hand[card_index].card_type == CardType.ACTION and
                        current_player.hand[card_index].action_type in [
                            ActionCardType.DEAL_BREAKER,
                            ActionCardType.SLY_DEAL,
                            ActionCardType.FORCE_DEAL,
                            ActionCardType.DEBT_COLLECTOR
                        ]):
                        target_required = True

                    if target_required:
                        print("Choose a target to play against.")
                        for i, player in enumerate(game.players):
                            if player != current_player:
                                print(f"{i+1} - {player.name}")
                        target = int(input("player: ")) - 1
                        if 0 <= target < len(game.players) and game.players[target] != current_player:
                            target = game.players[target]
                        else:
                            print("Invalid target selected")
                        
                    action_card = current_player.play_action(card_index)
                    if action_card:
                        if game.process_action_card(action_card,target_player = target):
                            actions_performed += 1
                    else:
                        print("Failed to play action card")
                else:
                    print("Invalid card number entered.")
            elif choice == "4" :
                game.display_player_hand(current_player)
            elif choice == "5" :
                game.display_player_properties(current_player)
            elif choice == "0" :
                break
            else:
                print("Invalid choice. Please choose between 1-4.")

        winner = game.check_winner()
        if winner:
            print(f"{current_player.name} WON THE GAME. CONGRATULATIONS  !!!!")
            break
        while len(current_player.hand) > game.MAX_IN_HAND_CARD_COUNT:
            game.display_player_hand(current_player)
            card_index = int(input("More than 7 cards in hand, you must discard. Please select a card: ")) -1
            if 0 <= card_index < len(current_player.hand):
                discard = current_player.discard_card(card_index)
                game.discard_pile.append(discard)
        
        game.next_player()
   
if __name__== "__main__":
    run()