from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Signal

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class ForecastPage(QWidget):

    continue_to_evaluation_clicked = Signal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Matplotlib Canvas
        self.canvas = FigureCanvas(None)
        layout.addWidget(self.canvas)

        # Continue Button
        self.continue_btn = QPushButton("Continue to Evaluation")
        self.continue_btn.clicked.connect(self.continue_to_evaluation_clicked.emit)
        layout.addWidget(self.continue_btn)

    # ✅ This now WORKS
    def set_forecast_plot(self, fig):
        self.canvas.figure = fig
        self.canvas.draw()
