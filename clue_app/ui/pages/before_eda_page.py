from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton,
    QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt
from ui.widgets.matplotlib_canvas import MatplotlibCanvas


class BeforeEDAPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        self.title = QLabel("Before EDA - Raw Data Preview")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.title)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.summary_box = QTextEdit()
        self.summary_box.setReadOnly(True)
        self.summary_box.setMinimumHeight(200)
        self.summary_box.setStyleSheet("""
            background:#1e1e1e;
            color:white;
            padding:10px;
            font-family: Consolas;
        """)
        layout.addWidget(self.summary_box)

        # SCROLL AREA FOR PLOT
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

        self.run_eda_btn = QPushButton("Run Full EDA")
        self.run_eda_btn.setFixedHeight(40)
        layout.addWidget(self.run_eda_btn)

    def set_status(self, text):
        self.status_label.setText(text)

    def set_eda_summary(self, text):
        self.summary_box.setPlainText(text)

    def set_preview_plot(self, fig):
        self.canvas.draw_figure(fig)

    @property
    def run_eda_clicked(self):
        return self.run_eda_btn.clicked
