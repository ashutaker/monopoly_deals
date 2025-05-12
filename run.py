# Initialise and maintainer the game session
from game_engine import GameEngine


def run():
    print("Welcome to Monopoly Deals!")
    # num_players = int(input("Enter number of players (2-5): "))

    # if num_players< 2 or num_players > 5:
    #     print("Invalid number of players. Setting to 2.")
    #     num_players = 2

    # player_names= []
    # for i in range(num_players):
    #     name = input(f"Enter the name of player {i+1}: ")
    #     player_names.append(name)

    player_names = ["Ashu", "Neha"]
    game = GameEngine(player_names)
    Winner = None

    # for player in game.players:
    #     print(player.hand)
    while not Winner:
        current_player = game.current_player()
        ''' TODO
        1. draw 2 cards at the beginning or 5 cards if hand is empty
        2. Show player its hand and property and money pile
        3. Take upto three actions
            a. Ask which card to play by index or end turn
            b. take valid action as per selection
        4. Check for winner at end of turn
        5. Select next player if no winner.
        '''
        print(f"{current_player.name} to play !!")
        
        # Draw cards at the beginning of the turn
        draw_count = 2
        if len(current_player.hand) == 0: 
        # if no cards left in player's hand
            draw_count = 5
        game.draw_card(current_player, draw_count)

        # Display player its hand, property and money
        ## player hand
        for i, card in enumerate(current_player.hand):
            print(f"{i+1} - {card}")
        
        ## properties
        for color in 


if __name__== "__main__":
    run()