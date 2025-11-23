from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
from PySide6.QtCore import Signal


class ReportPage(QWidget):
    generate_report_clicked = Signal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Report Generation"))

        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("Output PDF path (e.g. reports/report.pdf)")
        layout.addWidget(self.path_edit)

        btn = QPushButton("Generate Report")
        btn.clicked.connect(self._on_generate)
        layout.addWidget(btn)

    def _on_generate(self):
        path = self.path_edit.text().strip()
        if path:
            self.generate_report_clicked.emit(path)
