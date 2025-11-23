from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap
import os


class WelcomePage(QWidget):

    continue_clicked = Signal()

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        # ---------- LOGO CONTAINER (FOR PERFECT CENTERING) ----------
        logo_container = QHBoxLayout()
        logo_container.setAlignment(Qt.AlignCenter)

        logo = QLabel()
        logo.setAlignment(Qt.AlignCenter)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        LOGO_PATH = os.path.join(BASE_DIR, "assets", "icons", "logo.png")

        pixmap = QPixmap(LOGO_PATH)

        if not pixmap.isNull():
            logo.setPixmap(
                pixmap.scaled(
                    200,
                    200,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )
        else:
            logo.setText("LOGO NOT FOUND")

        logo_container.addWidget(logo)

        # ---------- TITLE ----------
        title = QLabel("CLUE AI FORECASTING")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #00e5ff;
        """)

        # ---------- SUBTITLE ----------
        subtitle = QLabel("Smart Financial Prediction Platform")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 15px;
            color: #b0bec5;
        """)

        # ---------- START BUTTON ----------
        start_button = QPushButton("START")
        start_button.setCursor(Qt.PointingHandCursor)
        start_button.setFixedHeight(45)
        start_button.setStyleSheet("""
            QPushButton {
                background-color: #00e5ff;
                color: black;
                font-size: 16px;
                font-weight: bold;
                border-radius: 22px;
                padding: 10px 30px;
            }
            QPushButton:hover {
                background-color: #18ffff;
            }
        """)
        start_button.clicked.connect(self.continue_clicked.emit)

        # ---------- FINAL LAYOUT ----------
        main_layout.addStretch()
        main_layout.addLayout(logo_container)
        main_layout.addSpacing(20)
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addSpacing(40)
        main_layout.addWidget(start_button, alignment=Qt.AlignCenter)
        main_layout.addStretch()
