from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PySide6.QtCore import Signal


class ModelResultPage(QWidget):
    continue_to_forecast_clicked = Signal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Model Training Results"))

        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        layout.addWidget(self.results_text)

        btn = QPushButton("Continue to Forecast")
        btn.clicked.connect(self.continue_to_forecast_clicked.emit)
        layout.addWidget(btn)

    def set_results(self, model_type: str, model_order, metrics: dict):
        lines = [
            f"Model: {model_type}",
            f"Order: {model_order}",
            "",
            "Metrics:",
        ]
        for k, v in metrics.items():
            lines.append(f"  {k}: {v:.4f}")

        self.results_text.setPlainText("\n".join(lines))
    def set_forecast_plot(self, fig):
        self.canvas.draw_figure(fig)
