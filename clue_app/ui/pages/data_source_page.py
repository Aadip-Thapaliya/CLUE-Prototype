"""
Data Source Selection Page for CLUE
Allows user to choose between:
1. CSV File Upload
2. Yahoo Finance Input
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QComboBox,
    QDateEdit,
)
from PySide6.QtCore import Signal, QDate


class DataSourcePage(QWidget):
    data_config_ready = Signal(dict)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Select Data Source"))

        # ================= CSV SECTION (TOP) =================
        layout.addWidget(QLabel("CSV Upload"))

        self.csv_path_input = QLineEdit()
        self.csv_path_input.setPlaceholderText("Select CSV file...")
        layout.addWidget(self.csv_path_input)

        self.browse_btn = QPushButton("Browse CSV")
        self.browse_btn.clicked.connect(self._browse_file)
        layout.addWidget(self.browse_btn)

        # ================= YAHOO FINANCE SECTION (BOTTOM) =================
        layout.addWidget(QLabel("Yahoo Finance"))

        self.source_selector = QComboBox()
        self.source_selector.addItems(["CSV", "Yahoo Finance"])
        layout.addWidget(self.source_selector)

        # Dropdown ticker list (stock suggestions)
        self.ticker_input = QComboBox()
        self.ticker_input.addItems([
            "AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "META", "NVDA"
        ])
        layout.addWidget(self.ticker_input)

        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addYears(-2))
        layout.addWidget(self.start_date)

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        layout.addWidget(self.end_date)

        self.load_btn = QPushButton("Load Data")
        self.load_btn.clicked.connect(self._emit_config)
        layout.addWidget(self.load_btn)

    def _browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.csv_path_input.setText(file_path)

    def _emit_config(self):
        source = self.source_selector.currentText()

        if source == "CSV":
            config = {
                "source": "csv",
                "file_path": self.csv_path_input.text(),
            }
        else:
            config = {
                "source": "yahoo",
                "ticker": self.ticker_input.currentText(),
                "start": self.start_date.date().toString("yyyy-MM-dd"),
                "end": self.end_date.date().toString("yyyy-MM-dd"),
            }

        self.data_config_ready.emit(config)
