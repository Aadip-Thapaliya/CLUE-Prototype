from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton,
    QHBoxLayout, QFrame, QProgressBar
)
from PySide6.QtCore import Signal, Qt


class ModelResultPage(QWidget):
    continue_to_forecast_clicked = Signal()

    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QLabel { color: #EAEAEA; }
            QFrame { background: #1e1e1e; border-radius: 12px; }
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #00c6ff, stop:1 #0072ff);
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover { background: #0099ff; }
        """)

        main_layout = QVBoxLayout(self)

        # ===== TITLE =====
        title = QLabel("\ud83e\udd16 MODEL TRAINING DASHBOARD")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        main_layout.addWidget(title)

        # ===== MODEL INFO CARD =====
        self.model_info_card = QFrame()
        info_layout = QVBoxLayout(self.model_info_card)

        self.model_label = QLabel()
        self.order_label = QLabel()

        info_layout.addWidget(self.model_label)
        info_layout.addWidget(self.order_label)
        main_layout.addWidget(self.model_info_card)

        # ===== SCORE CARD AREA =====
        score_frame = QFrame()
        score_layout = QHBoxLayout(score_frame)

        self.mae_bar = self._create_metric_card("MAE")
        self.rmse_bar = self._create_metric_card("RMSE")
        self.mape_bar = self._create_metric_card("MAPE")
        self.confidence_label = QLabel()

        score_layout.addWidget(self.mae_bar)
        score_layout.addWidget(self.rmse_bar)
        score_layout.addWidget(self.mape_bar)
        main_layout.addWidget(score_frame)

        # ===== CONFIDENCE INDICATOR =====
        self.confidence_label.setAlignment(Qt.AlignCenter)
        self.confidence_label.setStyleSheet("font-size:16px; font-weight:bold;")
        main_layout.addWidget(self.confidence_label)

        # ===== COMPARISON PANEL =====
        comparison_title = QLabel("\ud83d\udcca Previous Model Comparisons")
        comparison_title.setStyleSheet("font-size: 16px; margin-top:10px;")
        main_layout.addWidget(comparison_title)

        self.history_box = QTextEdit()
        self.history_box.setReadOnly(True)
        self.history_box.setStyleSheet("background:#121212; color:#9cdcfe;")
        main_layout.addWidget(self.history_box)

        # ===== CONTINUE BUTTON =====
        btn = QPushButton("\u27a1 Continue to Forecast")
        btn.clicked.connect(self.continue_to_forecast_clicked.emit)
        main_layout.addWidget(btn)

    # ================= COMPONENT HELPERS =================

    def _create_metric_card(self, name):
        frame = QFrame()
        layout = QVBoxLayout(frame)

        label = QLabel(name)
        label.setAlignment(Qt.AlignCenter)
        progress = QProgressBar()
        progress.setMaximum(100)
        progress.setTextVisible(True)

        layout.addWidget(label)
        layout.addWidget(progress)

        frame.progress = progress
        return frame

    # ================= MAIN UPDATE METHOD =================

    def set_results(self, model_type: str, model_order, metrics: dict):
        # Model information
        self.model_label.setText(f"\ud83d\udcca Model Type: {model_type}")
        self.order_label.setText(f"\u2699 Order: {model_order}")

        mae = metrics.get("MAE", 0)
        rmse = metrics.get("RMSE", 0)
        mape = metrics.get("MAPE", 0)

        self.mae_bar.progress.setValue(min(int(mae * 5), 100))
        self.rmse_bar.progress.setValue(min(int(rmse * 5), 100))
        self.mape_bar.progress.setValue(min(int(mape * 10), 100))

        # Confidence Indicator
        if mape < 5:
            self.confidence_label.setText("\u2705 Model Confidence: EXCELLENT")
            self.confidence_label.setStyleSheet("color: #00ff99;")
        elif mape < 10:
            self.confidence_label.setText("\u26a0 Model Confidence: MODERATE")
            self.confidence_label.setStyleSheet("color: #ffaa00;")
        else:
            self.confidence_label.setText("\u274c Model Confidence: LOW")
            self.confidence_label.setStyleSheet("color: #ff4444;")

        # Model comparison history
        history_entry = (
            f"Model: {model_type}\n"
            f"Order: {model_order}\n"
            f"MAE: {mae:.4f} | RMSE: {rmse:.4f} | MAPE: {mape:.2f}%\n"
            f"{'-'*40}\n"
        )
        self.history_box.append(history_entry)
