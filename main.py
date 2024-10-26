import sys
from PySide6.QtWidgets import QApplication
from gui import TicTacToeGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TicTacToeGUI()
    sys.exit(app.exec())
