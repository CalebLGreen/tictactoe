from IPython.display import display
import pandas as pd
from board import create_board
from check import check_win
from random import randint
from time import sleep

board = create_board()
display(board)
print("\n", "_" * 50, "\n")

gameOn = True
turn = 1
valid_choices = ["a1", "a2", "a3", "b1", "b2", "b3", "c1", "c2", "c3"]
stored_places = []


def game():
    print("Welcome to the game")
    players = input("Would you like to play against the computer? ")
    if players.lower() == "y":
        first = int(input("Would you like to go First(1) or Second(2): "))
        diff = int(input("Select a difficulty level of 1 to 2: "))
        singleplayer(diff, first)
    elif players.lower() == "s":
        diff = int(
            input("Select an intelligence level for the simulation from 1 to 3: ")
        )
        simulate(diff)
    else:
        multiplayer()


def singleplayer(diff, first):
    global gameOn
    global turn
    while gameOn:
        print("-" * 22, f"Turn {turn}", "-" * 22)
        if turn % 2 and first == 1:
            symbol = "X"
            c = input("Please input coords like a3: ")
            place(c, symbol)
        elif turn % 2 and first == 2:
            sleep(1)
            difficulty_selector(diff, symbol="X")
        elif first == 1:
            sleep(1)
            difficulty_selector(diff, symbol="O")
        else:
            symbol = "O"
            c = input("Please input coords like a3: ")
            place(c, symbol)


def simulate(diff):
    global gameOn
    global turn
    while gameOn:
        print("-" * 22, f"Turn {turn}", "-" * 22)
        if turn % 2:
            difficulty_selector(diff, symbol="X")
            sleep(1)
        else:
            difficulty_selector(diff, symbol="O")
            sleep(1)


def place(c, symbol):
    global gameOn
    global turn
    global board
    if c in valid_choices:
        row, col = c[0], c[1]
        if board.loc[row, col] not in ["X", "O"]:
            global stored_places
            stored_places.append(row + col)
            board.loc[row, col] = symbol
            win, _ = check_win(board, row, col, symbol)
            # _
            if win:
                print(f"Game Over, {symbol} wins")
                gameOn = False
            turn += 1
            display(board)
        else:
            print("Choose new coords")
    if turn == 10:
        print("The game is a tie")
        gameOn = False


def multiplayer():
    global gameOn
    global turn
    while gameOn:
        print("-" * 22, f"Turn {turn}", "-" * 22)
        if turn % 2:
            symbol = "X"
            c = input("Please input coords like a3: ")
            place(c, symbol)
        else:
            symbol = "O"
            c = input("Please input coords like a3: ")
            place(c, symbol)


def difficulty_selector(diff, symbol):
    if diff == 1:
        AI_turn_easy(symbol)
    elif diff == 2:
        AI_turn_med(symbol)
    else:
        AI_turn_easy(symbol)


def AI_turn_easy(symbol):
    global stored_places
    global board
    generate_loc = True
    while generate_loc:
        available_choices = [c for c in valid_choices if c not in stored_places]
        if not available_choices:
            return  # No valid moves left
        index = randint(0, len(available_choices) - 1)
        c = available_choices[index]
        place(c, symbol)
        generate_loc = False


def AI_turn_med(symbol):
    global stored_places
    global board
    player_symbol = "X" if symbol == "O" else "O"
    available_choices = [c for c in valid_choices if c not in stored_places]

    # Check if AI can in in next move and play it
    for c in available_choices:
        temp_board = board.copy()
        row, col = c[0], c[1]
        temp_board.loc[row, col] = symbol
        win, _ = check_win(temp_board, row, col, symbol)
        if win:
            place(c, symbol)
            return

    # Check if opponent can win in the next move and block it
    for c in available_choices:
        temp_board = board.copy()
        row, col = c[0], c[1]
        temp_board.loc[row, col] = player_symbol
        win, _ = check_win(temp_board, row, col, player_symbol)
        if win:
            place(c, symbol)
            return

    # If neither wins, place the symbol randomly
    AI_turn_easy(symbol)


game()
