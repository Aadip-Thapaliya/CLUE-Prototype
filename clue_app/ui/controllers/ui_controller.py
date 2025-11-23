# ui/controllers/ui_controller.py

from typing import Dict

from ui.main_window import MainWindow
from preprocessing.eda import eda_summary, generate_eda_charts
from pipeline.training_pipeline import run_training
from pipeline.forecasting_pipeline import run_forecast
from core.report_generator import generate_report
from core.data_loader import load_financial_data
from visualization.forecast_plot import plot_forecast


class UIController:
    def __init__(self, main_window: MainWindow):
        self.main_window = main_window

        self.current_model_type: str = "AUTO_ARIMA"
        self.source_config: Dict = {}
        self.last_training_result: Dict = {}
        self.last_forecast_result: Dict = {}
        self.last_metrics: Dict = {}
        self.forecast_horizon: int = 30

        self._connect_signals()

    # ================= SIGNAL CONNECTIONS =================

    def _connect_signals(self):
        w = self.main_window

        # -------- Welcome → Data Source --------
        # WelcomePage has: continue_clicked = Signal()
        if hasattr(w.welcome_page, "continue_clicked"):
            w.welcome_page.continue_clicked.connect(
                lambda: w.go_to_page(w.data_source_page)
            )

        # -------- Data Source → Pre-EDA --------
        w.data_source_page.data_config_ready.connect(self._on_data_selected)

        # -------- Model selection --------
        w.model_selection_page.model_selected.connect(self._on_model_selected)

        # -------- Pre-EDA → Run EDA --------
        # BeforeEDAPage has: run_eda_clicked = Signal()
        if hasattr(w.before_eda_page, "run_eda_clicked"):
            w.before_eda_page.run_eda_clicked.connect(self._run_eda)

        # -------- After EDA → Train Model --------
        # AfterEDAPage has: continue_to_model_clicked (usually a signal alias)
        if hasattr(w.after_eda_page, "continue_to_model_clicked"):
            w.after_eda_page.continue_to_model_clicked.connect(self._run_training)

        # -------- Model Results → Forecast --------
        # ModelResultPage has: continue_to_forecast_clicked = Signal()
        if hasattr(w.model_result_page, "continue_to_forecast_clicked"):
            cont = w.model_result_page.continue_to_forecast_clicked
            # If it's a button, use .clicked; if it's a Signal, use .connect directly
            if hasattr(cont, "clicked"):
                cont.clicked.connect(self._run_forecast)
            else:
                cont.connect(self._run_forecast)

        # -------- Forecast → Evaluation --------
        # ForecastPage may expose a signal OR a button under this name
        if hasattr(w.forecast_page, "continue_to_evaluation_clicked"):
            cont = w.forecast_page.continue_to_evaluation_clicked
            if hasattr(cont, "clicked"):
                cont.clicked.connect(self._show_evaluation)
            else:
                cont.connect(self._show_evaluation)

        # -------- Evaluation → Report --------
        if hasattr(w.evaluation_page, "continue_to_report_clicked"):
            cont = w.evaluation_page.continue_to_report_clicked
            if hasattr(cont, "clicked"):
                cont.clicked.connect(lambda: w.go_to_page(w.report_page))
            else:
                cont.connect(lambda: w.go_to_page(w.report_page))

        # -------- Report → Generate PDF --------
        if hasattr(w.report_page, "generate_report_clicked"):
            cont = w.report_page.generate_report_clicked
            # Usually this will be a Signal(str)
            cont.connect(self._generate_report)

    # ================= DATA SELECTED =================

    def _on_data_selected(self, config: dict):
        self.source_config = config

        if hasattr(self.main_window.before_eda_page, "set_status"):
            self.main_window.before_eda_page.set_status(
                "Data loaded successfully. Click 'Run EDA' to analyze."
            )

        self.main_window.go_to_page(self.main_window.before_eda_page)

    # ================= MODEL SELECTED =================

    def _on_model_selected(self, model_type: str, horizon: int = 30):
        self.current_model_type = model_type
        self.forecast_horizon = horizon
        self.main_window.go_to_page(self.main_window.before_eda_page)

    # ================= RUN EDA =================

    def _run_eda(self):
        df = load_financial_data(**self.source_config)

        summary = eda_summary(df)
        fig = generate_eda_charts(df)

        if hasattr(self.main_window.after_eda_page, "set_eda_summary"):
            formatted = self._format_eda_summary(summary)
            self.main_window.after_eda_page.set_eda_summary(formatted)

        if hasattr(self.main_window.after_eda_page, "set_eda_plot"):
            self.main_window.after_eda_page.set_eda_plot(fig)

        self.main_window.go_to_page(self.main_window.after_eda_page)

    # ================= RUN TRAINING =================

    def _run_training(self):
        result = run_training(
            self.current_model_type,
            self.source_config,
            forecast_periods=self.forecast_horizon,
        )

        self.last_training_result = result
        self.last_metrics = result.get("metrics", {})

        model_order = result.get("model_order", "N/A")

        if hasattr(self.main_window.model_result_page, "set_results"):
            self.main_window.model_result_page.set_results(
                model_type=self.current_model_type,
                model_order=model_order,
                metrics=self.last_metrics,
            )

        self.main_window.go_to_page(self.main_window.model_result_page)

    # ================= RUN FORECAST =================

    def _run_forecast(self):
        result = run_forecast(
            self.current_model_type,
            self.source_config,
            forecast_periods=self.forecast_horizon,
        )

        self.last_forecast_result = result

        df = load_financial_data(**self.source_config)

        fig = plot_forecast(
            df,
            result["forecast"],
            result.get("confidence_intervals"),
        )

        if hasattr(self.main_window.forecast_page, "set_forecast_plot"):
            self.main_window.forecast_page.set_forecast_plot(fig)

        self.main_window.go_to_page(self.main_window.forecast_page)

    # ================= SHOW EVALUATION =================

    def _show_evaluation(self):
        if hasattr(self.main_window.evaluation_page, "set_metrics"):
            self.main_window.evaluation_page.set_metrics(
                self._format_metrics(self.last_metrics)
            )

        self.main_window.go_to_page(self.main_window.evaluation_page)

    # ================= GENERATE REPORT =================

    def _generate_report(self, output_path: str):
        if not output_path:
            output_path = "clue_report.pdf"
        if not output_path.lower().endswith(".pdf"):
            output_path += ".pdf"

        model_results = {
            "model_type": self.current_model_type,
            **self.last_training_result,
        }

        generate_report(
            output_path=output_path,
            title="CLUE Forecasting Report",
            model_results=model_results,
            metrics=self.last_metrics,
            notes="Generated via CLUE application.",
        )

    # ================= HELPERS =================

    def _format_eda_summary(self, summary: dict) -> str:
        stats = summary.get("basic_stats", {})
        returns = summary.get("returns_stats", {})

        return (
            "DATA OVERVIEW\n"
            f"Start Date   : {stats.get('start_date')}\n"
            f"End Date     : {stats.get('end_date')}\n"
            f"Observations : {stats.get('n_observations')}\n\n"
            "PRICE STATISTICS\n"
            f"Min  : {stats.get('min'):.2f}\n"
            f"Max  : {stats.get('max'):.2f}\n"
            f"Mean : {stats.get('mean'):.2f}\n"
            f"Std  : {stats.get('std'):.2f}\n\n"
            "RETURNS\n"
            f"Mean Daily Return : {returns.get('mean_daily_return'):.4f}\n"
            f"Volatility        : {returns.get('volatility'):.4f}\n"
        )

    def _format_metrics(self, metrics: dict) -> str:
        if not metrics:
            return "No metrics available."

        return (
            f"MAE : {metrics.get('MAE', 0.0):.4f}\n"
            f"MSE : {metrics.get('MSE', 0.0):.4f}\n"
            f"RMSE: {metrics.get('RMSE', 0.0):.4f}\n"
            f"MAPE: {metrics.get('MAPE', 0.0):.4f}%"
        )