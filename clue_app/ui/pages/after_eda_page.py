from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton,
    QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt
from ui.widgets.matplotlib_canvas import MatplotlibCanvas


class AfterEDAPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Title
        self.title = QLabel("After EDA - Processed Data Analysis")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.title)

        # Summary Text
        self.summary_box = QTextEdit()
        self.summary_box.setReadOnly(True)
        self.summary_box.setMinimumHeight(220)
        self.summary_box.setStyleSheet("""
            background:#1e1e1e;
            color:white;
            padding:10px;
            font-family: Consolas;
        """)
        layout.addWidget(self.summary_box)

        # ---------- SCROLLABLE PLOT AREA ----------
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.plot_widget = QWidget()
        self.plot_layout = QVBoxLayout(self.plot_widget)
        self.plot_layout.setContentsMargins(0, 0, 0, 0)

        self.canvas = MatplotlibCanvas()
        self.canvas.setMinimumHeight(900)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.plot_layout.addWidget(self.canvas)
        self.scroll.setWidget(self.plot_widget)

        layout.addWidget(self.scroll, stretch=1)

        # Continue Button
        self.continue_btn = QPushButton("Continue to Model")
        self.continue_btn.setFixedHeight(40)
        layout.addWidget(self.continue_btn)

    # ===== UI setters =====
    def set_eda_summary(self, text: str):
        self.summary_box.setPlainText(text)

    def set_eda_plot(self, fig):
        self.canvas.draw_figure(fig)

    @property
    def continue_to_model_clicked(self):
        return self.continue_btn.clicked
