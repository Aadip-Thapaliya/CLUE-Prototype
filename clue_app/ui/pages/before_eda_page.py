from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Signal


class BeforeEDAPage(QWidget):

    run_eda_clicked = Signal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.status_label = QLabel("No data loaded yet")
        self.status_label.setStyleSheet("font-size: 14px; padding: 10px;")

        self.run_eda_button = QPushButton("Run EDA")
        self.run_eda_button.setFixedHeight(40)
        self.run_eda_button.clicked.connect(self.run_eda_clicked.emit)

        layout.addWidget(self.status_label)
        layout.addStretch()
        layout.addWidget(self.run_eda_button)

    def set_status(self, text: str):
        self.status_label.setText(text)