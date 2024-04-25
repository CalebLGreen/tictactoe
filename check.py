import pandas as pd
import numpy as np


def check_win(board, row, col, symbol):
    count_symbol_row = (board.loc[row, :] == symbol).sum()
    count_symbol_col = (board.loc[:, col] == symbol).sum()
    diagonal_a = sum(np.diag(board.loc[:, :] == symbol))
    diagonal_b = sum(np.diag(np.fliplr(board.loc[:, :] == symbol)))
    max_in_row = max([count_symbol_row, count_symbol_col, diagonal_a, diagonal_b])
    if max_in_row == 3:
        win = True
        return win, max_in_row
    else:
        win = False
        return win, max_in_row

