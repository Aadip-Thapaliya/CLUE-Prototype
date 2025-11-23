from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class AfterEDAPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.eda_summary_box = QTextEdit()
        self.eda_summary_box.setReadOnly(True)

        self.canvas = FigureCanvas(None)

        self.continue_btn = QPushButton("Continue to Model")
        self.continue_to_model_clicked = self.continue_btn.clicked

        layout.addWidget(self.eda_summary_box)
        layout.addWidget(self.canvas)
        layout.addWidget(self.continue_btn)

    def set_eda_summary(self, text: str):
        self.eda_summary_box.setText(text)

    def set_eda_plot(self, fig):
        self.canvas.figure = fig
        self.canvas.draw()
