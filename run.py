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

    for player in game.players:
        print(player.hand)

if __name__== "__main__":
    run()