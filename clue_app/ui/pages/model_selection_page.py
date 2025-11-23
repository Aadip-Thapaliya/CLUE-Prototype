from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QSlider
from PySide6.QtCore import Signal, Qt


class ModelSelectionPage(QWidget):
    model_selected = Signal(str, int)  # model type + horizon

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Select Forecasting Model"))

        self.model_combo = QComboBox()
        self.model_combo.addItems(["AUTO_ARIMA", "XGBOOST"])
        layout.addWidget(self.model_combo)

        layout.addWidget(QLabel("Forecast Horizon (days):"))

        self.horizon_slider = QSlider(Qt.Horizontal)
        self.horizon_slider.setMinimum(7)
        self.horizon_slider.setMaximum(90)
        self.horizon_slider.setValue(30)
        layout.addWidget(self.horizon_slider)

        self.horizon_label = QLabel("30 days")
        layout.addWidget(self.horizon_label)

        self.horizon_slider.valueChanged.connect(
            lambda v: self.horizon_label.setText(f"{v} days")
        )

        btn = QPushButton("Next")
        btn.clicked.connect(self._on_next)
        layout.addWidget(btn)

    def _on_next(self):
        model_type = self.model_combo.currentText()
        horizon = self.horizon_slider.value()
        self.model_selected.emit(model_type, horizon)
