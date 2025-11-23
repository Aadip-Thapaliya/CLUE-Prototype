from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap
import os


class WelcomePage(QWidget):

    continue_clicked = Signal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # ✅ Correct absolute path resolution
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        logo_path = os.path.join(base_dir, "assets", "icons", "logo.png")

        logo = QLabel()

        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            logo.setPixmap(pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            logo.setText("LOGO NOT FOUND")

        logo.setAlignment(Qt.AlignCenter)

        title = QLabel("CLUE Financial Forecasting")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")

        description = QLabel("AI-Powered Forecasting for Smarter Decisions")
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
