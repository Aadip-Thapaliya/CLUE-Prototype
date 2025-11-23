from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class ForecastPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.canvas = None

        self.continue_to_evaluation_clicked = QPushButton("Continue to Evaluation")
        self.layout.addWidget(self.continue_to_evaluation_clicked)

    # ✅ THIS IS WHAT WAS MISSING
    def set_forecast_plot(self, fig):
        if self.canvas:
            self.layout.removeWidget(self.canvas)
            self.canvas.deleteLater()

        self.canvas = FigureCanvas(fig)
        self.layout.insertWidget(0, self.canvas)
