#!/usr/bin/env python3
import time
import platform
from os import system

# players
human_player = -1  # represent the human player as -1
computer_player = +1  # represent the computer player as +1

# scores for winning and losing
win_score = 10  # score for winning
lose_score = -10  # score for losing
tie_score = 0  # score for a tie

# 3x3 game board initialized with zeros
game_board = [[0, 0, 0],  # first row
              [0, 0, 0],  # second row
              [0, 0, 0]]  # third row

def evaluate_board(current_board):
    """
    check the current state of the board to determine the game outcome.
    returns +10 if the computer wins, -10 if the human wins, and 0 for a draw.
    """
    if check_winner(current_board, computer_player):  # check if computer has won
        return win_score  # return win score for computer
    elif check_winner(current_board, human_player):  # check if human has won
        return lose_score  # return lose score for human
    return tie_score  # return tie score if no winner

def check_winner(current_board, current_player):
    """
    check if the current player has achieved a winning condition.
    """
    # define winning conditions as all combinations of rows, columns, and diagonals
    win_conditions = [
        [current_board[0][0], current_board[0][1], current_board[0][2]],  # first row
        [current_board[1][0], current_board[1][1], current_board[1][2]],  # second row
        [current_board[2][0], current_board[2][1], current_board[2][2]],  # third row
        [current_board[0][0], current_board[1][0], current_board[2][0]],  # first column
        [current_board[0][1], current_board[1][1], current_board[2][1]],  # second column
        [current_board[0][2], current_board[1][2], current_board[2][2]],  # third column
        [current_board[0][0], current_board[1][1], current_board[2][2]],  # diagonal from top-left to bottom-right
        [current_board[2][0], current_board[1][1], current_board[0][2]]   # diagonal from bottom-left to top-right
    ]
    # check if any winning condition is met for the current player
    return [current_player, current_player, current_player] in win_conditions

def is_game_over(current_board):
    """
    check if the game has ended.
    a game is over if there is a winner or if there are no empty cells left.
    """
    return check_winner(current_board, human_player) or check_winner(current_board, computer_player) or not get_empty_cells(current_board)

def get_empty_cells(current_board):
    """
    get a list of empty cells (cells with value 0) in the board.
    """
    return [[row_index, col_index] for row_index, row in enumerate(current_board) for col_index, cell in enumerate(row) if cell == 0]

def is_valid_move(row, col):
    """
    check if a move is valid (the cell is empty).
    """
    return [row, col] in get_empty_cells(game_board)  # return true if the cell is empty

def make_move(row, col, current_player):
    """
    make a move on the board if the chosen cell is valid.
    """
    if is_valid_move(row, col):  # check if the move is valid
        game_board[row][col] = current_player  # place the player's mark in the chosen cell
        return True  # move successful
    return False  # move failed, cell not empty

def minimax_algorithm(board_state, depth, current_player):
    """
    ai function to find the best move using the minimax strategy.
    recursively explores all possible moves and their outcomes.
    """
    if is_game_over(board_state) or depth == 0:  # check if the game is over or if max depth is reached
        return [-1, -1, evaluate_board(board_state)]  # return the evaluation score of the board

    if current_player == computer_player:  # if it's the computer's turn
        best_move = [-1, -1, float('-inf')]  # initialize best move for computer
        for cell in get_empty_cells(board_state):  # iterate through available cells
            row, col = cell  # get row and column of the cell
            board_state[row][col] = computer_player  # simulate the move for computer
            move_score = minimax_algorithm(board_state, depth - 1, human_player)  # recursively call minimax for the next move
            board_state[row][col] = 0  # undo the move
            move_score[0], move_score[1] = row, col  # set the cell coordinates for the move score

            if move_score[2] > best_move[2]:  # if this move is better than the best move found so far
                best_move = move_score  # update best move
    else:  # if it's the human's turn
        best_move = [-1, -1, float('inf')]  # initialize best move for human
        for cell in get_empty_cells(board_state):  # iterate through available cells
            row, col = cell  # get row and column of the cell
            board_state[row][col] = human_player  # simulate the move for human
            move_score = minimax_algorithm(board_state, depth - 1, computer_player)  # recursively call minimax for the next move
            board_state[row][col] = 0  # undo the move
            move_score[0], move_score[1] = row, col  # set the cell coordinates for the move score

            if move_score[2] < best_move[2]:  # if this move is better than the best move found so far
                best_move = move_score  # update best move

    return best_move  # return the best move found

def clear_console():
    """
    clear the console output based on the operating system.
    """
    os_type = platform.system().lower()  # get the operating system type
    # clear the console using the appropriate command
    system('cls' if 'windows' in os_type else 'clear')

def display_board(board_state, computer_symbol, human_symbol):
    """
    display the current state of the board in the console.
    """
    symbols = {human_player: human_symbol, computer_player: computer_symbol, 0: ' '}  # mapping of player symbols
    board_border = '---------------'  # border for the board display

    print('\n' + board_border)  # print top border
    for row in board_state:  # iterate through each row of the board
        for cell in row:  # iterate through each cell in the row
            symbol = symbols[cell]  # get the symbol for the cell
            print(f'| {symbol} |', end='')  # print cell symbol
        print('\n' + board_border)  # print row border

def computer_turn(computer_symbol, human_symbol):
    """
    handle the computer's turn. it chooses the best move using the minimax algorithm.
    """
    available_depth = len(get_empty_cells(game_board))  # get the number of empty cells
    if available_depth == 0 or is_game_over(game_board):  # check if game is over or no moves left
        return  # no action if game is over

    clear_console()  # clear the console for a clean display
    print(f'computer\'s turn [{computer_symbol}]')  # notify whose turn it is
    display_board(game_board, computer_symbol, human_symbol)  # show the current board

    if available_depth == 9:  # if this is the first move, take center
        row, col = 1, 1  # take center
    else:  # otherwise, calculate the best move
        move = minimax_algorithm(game_board, available_depth, computer_player)  # find best move using minimax
        row, col = move[0], move[1]  # get the row and column of the move

    make_move(row, col, computer_player)  # make the move for the computer
    time.sleep(1)  # wait for a moment to simulate thinking time

def human_turn(computer_symbol, human_symbol):
    """
    handle the human player's turn. the player chooses a move.
    """
    available_depth = len(get_empty_cells(game_board))  # get the number of empty cells
    if available_depth == 0 or is_game_over(game_board):  # check if game is over or no moves left
        return  # no action if game is over

    # map for possible moves to their corresponding board coordinates
    possible_moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2]
    }

    while True:  # loop until a valid move is made
        clear_console()  # clear the console for a clean display
        print(f'your turn [{human_symbol}]')  # notify whose turn it is
        display_board(game_board, computer_symbol, human_symbol)  # show the current board

        # prompt the human player for their move
        try:
            move = int(input('choose your move (1-9): '))  # get move choice
            row, col = possible_moves[move]  # map the move to board coordinates
            if make_move(row, col, human_player):  # attempt to make the move
                break  # valid move made, exit loop
            else:
                print('invalid move, try again.')  # prompt for another move if invalid
        except (ValueError, KeyError):  # handle invalid inputs
            print('invalid input, please choose a number between 1 and 9.')

def start_game():
    """
    Main function to run the game.
    """
    clear_console()  # Clear the console for a fresh start
    human_symbol = ''  # Human chooses X or O
    computer_symbol = ''  # Computer gets the opposite symbol
    goes_first = ''  # Does the human go first?

    # Get the human's symbol (X or O)
    while human_symbol != 'X' and human_symbol != 'O':
        human_symbol = input('Choose X or O: ').upper()

    # Assign the computer's symbol based on the human's choice
    computer_symbol = 'O' if human_symbol == 'X' else 'X'

    clear_console()  # Clear the console again for a fresh display
    # Ask the player if they want to start first
    while goes_first != 'Y' and goes_first != 'N':
        goes_first = input('Do you want to start first? (Y/N): ').upper()

    # Main game loop
    while len(get_empty_cells(game_board)) > 0 and not is_game_over(game_board):
        if goes_first == 'N':  # If the human does not go first, let the computer go
            computer_turn(computer_symbol, human_symbol)
            goes_first = ''  # Reset goes_first so that human can play next

        # Human's turn
        human_turn(computer_symbol, human_symbol)
        # Computer's turn
        computer_turn(computer_symbol, human_symbol)

    # Check for the winner and display the result
    if check_winner(game_board, human_player):
        clear_console()  # Clear console for final display
        display_board(game_board, computer_symbol, human_symbol)  # Show final board
        print('YOU WIN!')  # Notify human player of victory
    elif check_winner(game_board, computer_player):
        clear_console()  # Clear console for final display
        display_board(game_board, computer_symbol, human_symbol)  # Show final board
        print('YOU LOSE!')  # Notify human player of defeat
    else:
        clear_console()  # Clear console for final display
        display_board(game_board, computer_symbol, human_symbol)  # Show final board
        print('DRAW!')  # Notify human player of a draw

    exit()  # End the game


# start the game
if __name__ == "__main__":
    start_game()  # call the main game function
