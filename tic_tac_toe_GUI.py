from tkinter import *
import numpy as np
from random import randint
from time import sleep

root = Tk()
root.title("Noughts and Crosses")
root.geometry("480x320")

turn = 0
gameOn = True


def start():
    START = Button(root, height=3, width=18, text="START GAME")
    START.configure(command=(lambda: single_multi(START)))
    START.place(relx=0.5, rely=0.5, anchor=CENTER)


def single_multi(button):
    global ButtonA, ButtonB
    button.destroy()
    ButtonA = Button(root, height=3, width=15, text="Multi Player")
    ButtonA.place(relx=0.2, y=50)
    ButtonB = Button(root, height=3, width=15, text="Single Player")
    ButtonA.configure(command=(lambda: button_creation()))
    ButtonB.configure(command=(lambda: AIOn()))
    ButtonB.place(relx=0.5, y=50)


def AIOn():
    global AI
    AI = True
    ButtonA.configure(text="Difficulty: Easy", command=(lambda: difficulty_selector("Easy")))
    ButtonB.configure(text="Difficulty Medium", command=(lambda: difficulty_selector("Medium")))

def difficulty_selector(selection):
    global DIFF
    if selection == "Easy":
        DIFF = 1
    elif selection == "Medium":
        DIFF = 2
    ButtonA.configure(text="Go First", command=(lambda: first_second(1)))
    ButtonB.configure(text="Go Second", command=(lambda: first_second(2)))

def first_second(goWhen):
    global AI_TURN
    if goWhen == 1:
        AI_TURN = "even"
        button_creation()   
    elif goWhen == 2:
        AI_TURN = "odd"
        button_creation()
        check_diff(symbol="X")

def button_creation():
    global AI
    # Block to create the AI variable as False if it doesn't already exist
    try:
        AI = True if AI else False
        print(f"AI is on and difficulty = {DIFF}")
    except NameError:
        AI = False
    ButtonA.destroy()
    ButtonB.destroy()
    global tl, cl, bl, tc, cc, bc, tr, cr, br

    tl = Button(root, height=3, width=6)
    tl.configure(command=(lambda: clicked(tl)))
    tl.grid(column=1, row=0)

    cl = Button(root, height=3, width=6)
    cl.configure(command=(lambda: clicked(cl)))
    cl.grid(column=1, row=1)

    bl = Button(root, height=3, width=6)
    bl.configure(command=(lambda: clicked(bl)))
    bl.grid(column=1, row=2)

    tc = Button(root, height=3, width=6)
    tc.configure(command=(lambda: clicked(tc)))
    tc.grid(column=2, row=0)

    tr = Button(root, height=3, width=6)
    tr.configure(command=(lambda: clicked(tr)))
    tr.grid(column=3, row=0)

    cc = Button(root, height=3, width=6)
    cc.configure(command=(lambda: clicked(cc)))
    cc.grid(column=2, row=1)

    cr = Button(root, height=3, width=6)
    cr.configure(command=(lambda: clicked(cr)))
    cr.grid(column=3, row=1)

    bc = Button(root, height=3, width=6)
    bc.configure(command=(lambda: clicked(bc)))
    bc.grid(column=2, row=2)

    br = Button(root, height=3, width=6)
    br.configure(command=(lambda: clicked(br)))
    br.grid(column=3, row=2)

    reset = Button(root, height=3, width = 12, text="Reset Game")
    reset.configure(command=(lambda: reset_game([tl, tc, tr, cl, cc, cr, bl, bc, br, reset])))
    reset.place(relx=0.2, rely=0.8)

    global output_text
    output_text = Label(root, text="Please click on a box")
    output_text.grid(column=4, row=0)

    global stored_places
    global valid_choices
    stored_places = []
    valid_choices = [tl, tc, tr, cl, cc, cr, bl, bc, br]

def reset_game(tbdestoryed):
    global valid_choices
    for button in tbdestoryed:
        button.destroy()
        global gameOn, turn
        turn = 1
        gameOn = True
    start()
        

def clicked(button):
    global AI, turn, output_text, gameOn
    if gameOn == True:
        symbol = "X" if turn % 2 == 1 else "O"
        colour = "red" if turn % 2 == 1 else "blue"
        if turn == 0:
            button.configure(text="")
        elif button["text"] == "":
            stored_places.append(button)
            button.configure(text=symbol, fg=colour)
            turn += 1
            output_text.configure(
                text=f"It is {'X' if turn % 2 == 1 else 'O'}'s turn to play"
            )
            check_win(symbol)            
            if turn >= 10 and gameOn:
                output_text.configure(text=f"It is a tie! Game Over")
                gameOn = False
            if AI == True and turn <= 9:
                check_turn(turn)
        else:
            output_text.configure(
                text=f"Select an empty box, it is {'X' if turn % 2 == 1 else 'O'}'s turn to play"
            )
    elif gameOn == False and button == None:
        output_text.configure(
            text=f"Game is over {'X' if turn % 2 == 0 else 'O'} wins!"
        )

def check_turn(turn):
    if turn % 2 == 1 and AI_TURN == "odd":
        check_diff(symbol="O")
    elif turn % 2 == 0 and AI_TURN == "even":
        check_diff(symbol="X")
    else:
        pass

def check_diff(symbol):
    if DIFF == 1:
        AI_turn_easy()
    elif DIFF == 2:
        AI_turn_med(symbol)
        pass
    else:
        pass


def AI_turn_easy():
    global stored_places, valid_choices
    generate_loc = True
    while generate_loc:
        available_choices = [c for c in valid_choices if c not in stored_places]
        if not available_choices:
            return
        index = randint(0, len(available_choices) - 1)
        c = available_choices[index]
        clicked(button=c)
        generate_loc = False

def AI_turn_med(symbol):
    global stored_places, valid_choices
    available_choices = [c for c in valid_choices if c not in stored_places]
    print(available_choices)
    symbol = ("X" if symbol == "X" else "O")
    for pos in available_choices:
        board = get_simulated_board()
        print(symbol)
        idx = valid_choices.index(pos)
        board[idx] = symbol
        win = simulated_win(symbol, board)
        if win:
            clicked(button=pos)
            return
    symbol = ("O" if symbol == "X" else "X")
    for pos in available_choices:
        board = get_simulated_board()
        print(symbol)
        idx = valid_choices.index(pos)
        board[idx] = symbol
        win = simulated_win(symbol, board)
        if win:
            clicked(button=pos)
            return
    print("====")
    AI_turn_easy()

def get_simulated_board():
    global valid_choices
    # valid_choices = [tl, tc, tr, cl, cc, cr, bl, bc, br] for reference
    board = ["", "", "", "", "", "", "", "", ""]
    for idx, pos in enumerate(valid_choices):
        if pos['text'] == "X":
            board[idx] = "X"
        elif pos["text"] == "O":
            board[idx] = "O"
    return board

def simulated_win(symbol, board):
    lc_col = [s for s in board[::3] if s == symbol].count(symbol)
    cc_col = [s for s in board[1::3] if s == symbol].count(symbol)
    rc_col = [s for s in board[2::3] if s == symbol].count(symbol)
    tc_row = sum([int(board[0] == symbol) + int(board[1] == symbol) + int(board[2] == symbol)])
    cc_row = sum([int(board[3] == symbol) + int(board[4] == symbol) + int(board[5] == symbol)])
    bc_row = sum([int(board[6] == symbol) + int(board[7] == symbol) + int(board[8] == symbol)])
    diag = sum([int(board[0] == symbol) + int(board[4] == symbol) + int(board[8] == symbol)])
    a_diag = sum([int(board[2] == symbol) + int(board[4] == symbol) + int(board[6] == symbol)])
    # print([lc_col, cc_col, rc_col, tc_row, cc_row, bc_row, diag, a_diag])
    if 3 in [lc_col, cc_col, rc_col, tc_row, cc_row, bc_row, diag, a_diag]:
        return True
    else:
        return False



def check_win(symbol):
    t_row = [tl, tc, tr]
    c_row = [cl, cc, cr]
    b_row = [bl, bc, br]
    l_col = [tl, cl, bl]
    c_col = [tc, cc, bc]
    r_col = [tr, cr, br]
    diag = [tl, cc, br]
    anti_diag = [tr, cc, bl]
    global output_text
    t_count_row = len([lambda x: x for x in t_row if x["text"] == symbol])
    c_count_row = len([lambda x: x for x in c_row if x["text"] == symbol])
    b_count_row = len([lambda x: x for x in b_row if x["text"] == symbol])
    l_count_col = len([lambda x: x for x in l_col if x["text"] == symbol])
    c_count_col = len([lambda x: x for x in c_col if x["text"] == symbol])
    r_count_col = len([lambda x: x for x in r_col if x["text"] == symbol])
    diag_count = len([lambda x: x for x in diag if x["text"] == symbol])
    anti_diag_count = len([lambda x: x for x in anti_diag if x["text"] == symbol])
    win_count = [
        t_count_row,
        c_count_row,
        b_count_row,
        l_count_col,
        c_count_col,
        r_count_col,
        diag_count,
        anti_diag_count,
    ]
    if 3 in win_count:
        global gameOn
        gameOn = False
        clicked(None)


turn += 1


start()
root.mainloop()
