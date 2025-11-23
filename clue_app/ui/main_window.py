# ui/main_window.py

from PySide6.QtWidgets import QMainWindow, QStackedWidget

from ui.pages.welcome_page import WelcomePage
from ui.pages.model_selection_page import ModelSelectionPage
from ui.pages.before_eda_page import BeforeEDAPage
from ui.pages.after_eda_page import AfterEDAPage
from ui.pages.model_result_page import ModelResultPage
from ui.pages.forecast_page import ForecastPage
from ui.pages.evaluation_page import EvaluationPage
from ui.pages.report_page import ReportPage
from ui.pages.data_source_page import DataSourcePage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CLUE - Financial Forecasting")

        # ✅ USE ONE NAME ONLY
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self._init_pages()

        # ✅ THIS ENSURES WELCOME PAGE APPEARS FIRST
        self.stacked_widget.setCurrentWidget(self.welcome_page)

    def _init_pages(self):
        self.welcome_page = WelcomePage()
        self.data_source_page = DataSourcePage()
        self.model_selection_page = ModelSelectionPage()
        self.before_eda_page = BeforeEDAPage()
        self.after_eda_page = AfterEDAPage()
        self.model_result_page = ModelResultPage()
        self.forecast_page = ForecastPage()
        self.evaluation_page = EvaluationPage()
        self.report_page = ReportPage()

        # ✅ ADD PAGES IN CORRECT ORDER
        self.stacked_widget.addWidget(self.welcome_page)
        self.stacked_widget.addWidget(self.data_source_page)
        self.stacked_widget.addWidget(self.model_selection_page)
        self.stacked_widget.addWidget(self.before_eda_page)
        self.stacked_widget.addWidget(self.after_eda_page)
        self.stacked_widget.addWidget(self.model_result_page)
        self.stacked_widget.addWidget(self.forecast_page)
        self.stacked_widget.addWidget(self.evaluation_page)
        self.stacked_widget.addWidget(self.report_page)

    def go_to_page(self, widget):
        self.stacked_widget.setCurrentWidget(widget)
