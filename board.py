import pandas as pd


def create_board():
    table = [
        ["a", " ", "|", " ", "|", " "],
        [" ", "_", "|", "_", "|", "_"],
        ["b", " ", "|", " ", "|", " "],
        [" ", "_", "|", "_", "|", "_"],
        ["c", " ", "|", " ", "|", " "],
    ]
    board = pd.DataFrame(table, columns=["", "1", " ", "2", " ", "3"])
    board.set_index([""], inplace=True)
    return board
