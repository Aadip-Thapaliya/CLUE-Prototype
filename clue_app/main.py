"""
CLUE Application Entry Point
Initializes PySide6 Application and launches the MainWindow
connected with UIController.
"""

import sys
from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from ui.controllers.ui_controller import UIController


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    controller = UIController(window)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()