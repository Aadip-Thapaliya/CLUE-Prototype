from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PySide6.QtCore import Signal

class EvaluationPage(QWidget):

    continue_to_report_clicked = Signal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Model Evaluation Dashboard")
        title.setStyleSheet("font-size:18px;font-weight:bold;")
        layout.addWidget(title)

        self.metrics_box = QTextEdit()
        self.metrics_box.setReadOnly(True)
        layout.addWidget(self.metrics_box)

        self.report_button = QPushButton("Generate Detailed Report")
        self.report_button.setFixedHeight(40)
        layout.addWidget(self.report_button)

        self.report_button.clicked.connect(self.continue_to_report_clicked.emit)

    def set_metrics(self, metrics: dict):
        """Accepts dict and converts to formatted evaluation display"""

        if not isinstance(metrics, dict):
            self.metrics_box.setPlainText(str(metrics))
            return

        detailed_text = "MODEL PERFORMANCE METRICS\n\n"

        for key, value in metrics.items():
            if isinstance(value, float):
                detailed_text += f"{key:<15}: {value:.6f}\n"
            else:
                detailed_text += f"{key:<15}: {value}\n"

        self.metrics_box.setPlainText(detailed_text)
