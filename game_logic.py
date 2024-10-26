import random
from constants import HUMAN_PLAYER, COMPUTER_PLAYER, EMPTY, WIN_SCORE, LOSE_SCORE, TIE_SCORE, game_board

class TicTacToeLogic:
    @staticmethod
    def get_empty_cells(board):
        return [(row, col) for row in range(3) for col in range(3) if board[row][col] == EMPTY]

    @staticmethod
    def check_winner(board, player):
        win_conditions = [
            [board[0][0], board[0][1], board[0][2]],  # rows
            [board[1][0], board[1][1], board[1][2]],
            [board[2][0], board[2][1], board[2][2]],
            [board[0][0], board[1][0], board[2][0]],  # columns
            [board[0][1], board[1][1], board[2][1]],
            [board[0][2], board[1][2], board[2][2]],
            [board[0][0], board[1][1], board[2][2]],  # diagonals
            [board[2][0], board[1][1], board[0][2]]
        ]
        return [player, player, player] in win_conditions

    def minimax(self, board, player, depth):
        if self.check_winner(board, COMPUTER_PLAYER):
            return None, None, WIN_SCORE
        elif self.check_winner(board, HUMAN_PLAYER):
            return None, None, LOSE_SCORE
        elif not self.get_empty_cells(board):
            return None, None, TIE_SCORE

        best_score = float('-inf') if player == COMPUTER_PLAYER else float('inf')
        best_move = None
        for row, col in self.get_empty_cells(board):
            board[row][col] = player
            _, _, score = self.minimax(board, -player, depth - 1)
            board[row][col] = EMPTY
            if (player == COMPUTER_PLAYER and score > best_score) or \
               (player == HUMAN_PLAYER and score < best_score):
                best_score = score
                best_move = (row, col)
        return best_move[0], best_move[1], best_score
