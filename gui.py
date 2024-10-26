from PySide6.QtWidgets import QMainWindow, QPushButton, QGridLayout, QWidget, QMessageBox
from constants import HUMAN_PLAYER, COMPUTER_PLAYER, game_board
from game_logic import TicTacToeLogic

class TicTacToeGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic-Tac-Toe")
        self.setFixedSize(300, 300)
        self.current_player = HUMAN_PLAYER
        self.logic = TicTacToeLogic()
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        layout = QGridLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.buttons = {}
        for i in range(3):
            for j in range(3):
                button = QPushButton("")
                button.setFixedSize(80, 80)
            
                # Create a QFont object and set it to bold
                font = button.font()
                font.setBold(True)
                button.setFont(font)
            
                button.clicked.connect(lambda _, row=i, col=j: self.human_move(row, col))
                layout.addWidget(button, i, j)
                self.buttons[(i, j)] = button
        self.show()

    def human_move(self, row, col):
        if game_board[row][col] == 0:
            self.buttons[(row, col)].setText("X")
            game_board[row][col] = HUMAN_PLAYER
            if self.check_game_over():
                return
            self.computer_move()

    def computer_move(self):
        row, col, _ = self.logic.minimax(game_board, COMPUTER_PLAYER, len(self.logic.get_empty_cells(game_board)))
        game_board[row][col] = COMPUTER_PLAYER
        self.buttons[(row, col)].setText("O")
        self.check_game_over()

    def check_game_over(self):
        if self.logic.check_winner(game_board, HUMAN_PLAYER):
            self.show_game_result("You Win!")
            return True
        elif self.logic.check_winner(game_board, COMPUTER_PLAYER):
            self.show_game_result("Computer Wins!")
            return True
        elif not self.logic.get_empty_cells(game_board):
            self.show_game_result("It's a Draw!")
            return True
        return False

    def show_game_result(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Game Over")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setButtonText(QMessageBox.Yes, "Play Again")
        msg_box.setButtonText(QMessageBox.No, "Exit")
        response = msg_box.exec()
        if response == QMessageBox.Yes:
            self.reset_game()
        else:
            self.close()

    def reset_game(self):
        global game_board
        game_board = [[0] * 3 for _ in range(3)]
        for button in self.buttons.values():
            button.setText("")
