from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap
import os


class WelcomePage(QWidget):

    continue_clicked = Signal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        logo = QLabel()

        # ✅ Absolute path resolution (works from anywhere)
        ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        LOGO_PATH = os.path.join(ROOT_DIR, "assets", "icons", "logo.png")

        pixmap = QPixmap(LOGO_PATH)

        if pixmap.isNull():
            # Debug fallback so you KNOW if path is wrong
            logo.setText("⚠ Logo not found\n" + LOGO_PATH)
            logo.setAlignment(Qt.AlignCenter)
        else:
            logo.setPixmap(
                pixmap.scaled(
                    180,
                    180,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )
            logo.setAlignment(Qt.AlignCenter)

        title = QLabel("CLUE Financial Forecasting")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        description = QLabel("Financial Forecasting System")
        description.setAlignment(Qt.AlignCenter)

        start_button = QPushButton("Start")
        start_button.setFixedHeight(40)
        start_button.clicked.connect(self.continue_clicked.emit)

        layout.addStretch()
        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(20)
        layout.addWidget(start_button)
        layout.addStretch()
