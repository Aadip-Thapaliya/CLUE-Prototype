# ui/pages/forecast_page.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QPushButton, QFrame
)
from PySide6.QtCore import Qt
from ui.widgets.matplotlib_canvas import MatplotlibCanvas


class ForecastPage(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)

        # ===== HEADER =====
        header = QLabel("Forecast Results & Predicted Values")
        header.setStyleSheet(
            """
            font-size: 22px;
            font-weight: bold;
            padding: 10px;
            """
        )
        main_layout.addWidget(header)

        # ===== CONTENT AREA =====
        content_layout = QHBoxLayout()

        # --- LEFT: Forecast Graph ---
        self.canvas = MatplotlibCanvas()
        self.canvas.setMinimumWidth(800)
        content_layout.addWidget(self.canvas, stretch=3)

        # --- RIGHT: Prediction Box ---
        side_panel = QFrame()
        side_panel.setFrameShape(QFrame.StyledPanel)
        side_panel.setStyleSheet(
            """
            QFrame {
                background-color: #1e1e1e;
                border: 1px solid #3a3a3a;
                border-radius: 10px;
                padding: 10px;
            }
            QLabel {
                color: #00e5ff;
            }
            QTextEdit {
                background-color: #252525;
                color: white;
                border-radius: 6px;
            }
            """
        )

        side_layout = QVBoxLayout(side_panel)

        pred_title = QLabel("Predicted Future Values")
        pred_title.setStyleSheet("font-size:16px; font-weight: bold;")

        self.prediction_box = QTextEdit()
        self.prediction_box.setReadOnly(True)

        confidence_label = QLabel("Model Confidence Indicator")
        confidence_label.setStyleSheet("font-size:14px; margin-top:8px;")

        self.confidence_box = QLabel("STABILITY: HIGH")
        self.confidence_box.setAlignment(Qt.AlignCenter)
        self.confidence_box.setStyleSheet(
            """
            background-color: #0f5132;
            color: #78ffd6;
            padding: 8px;
            border-radius: 8px;
            font-weight: bold;
            """
        )

        side_layout.addWidget(pred_title)
        side_layout.addWidget(self.prediction_box)
        side_layout.addSpacing(10)
        side_layout.addWidget(confidence_label)
        side_layout.addWidget(self.confidence_box)

        content_layout.addWidget(side_panel, stretch=1)
        main_layout.addLayout(content_layout)

        # ===== CONTINUE BUTTON =====
        self.continue_btn = QPushButton("Continue to Evaluation")
        self.continue_btn.setFixedHeight(38)
        self.continue_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #005f73;
                color: white;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #0a9396;
            }
            """
        )
        main_layout.addWidget(self.continue_btn)

    # ================= PUBLIC METHODS =================

    def set_forecast_plot(self, fig):
        self.canvas.draw_figure(fig)

    def set_predicted_values(self, values):
        """
        values: list or pandas Series of predicted prices
        """
        formatted = "".join([f"Day {i+1}: {v:.2f}\n" for i, v in enumerate(values)])
        self.prediction_box.setPlainText(formatted)

    def set_confidence_level(self, level: str):
        """
        level: HIGH / MEDIUM / LOW
        """
        level = level.upper()

        if level == "HIGH":
            color = "#0f5132"
        elif level == "MEDIUM":
            color = "#664d03"
        else:
            color = "#842029"

        self.confidence_box.setText(f"STABILITY: {level}")
        self.confidence_box.setStyleSheet(
            f"""
            background-color: {color};
            color: white;
            padding: 8px;
            border-radius: 8px;
            font-weight: bold;
            """
        )

    @property
    def continue_to_evaluation_clicked(self):
        return self.continue_btn.clicked