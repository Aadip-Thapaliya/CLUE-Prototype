from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PySide6.QtCore import Signal


class EvaluationPage(QWidget):
    continue_to_report_clicked = Signal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Model Evaluation"))

        self.metrics_text = QTextEdit()
        self.metrics_text.setReadOnly(True)
        layout.addWidget(self.metrics_text)

        btn = QPushButton("Generate Report")
        btn.clicked.connect(self.continue_to_report_clicked.emit)
        layout.addWidget(btn)

    def set_metrics(self, text: str):
        self.metrics_text.setPlainText(text)
