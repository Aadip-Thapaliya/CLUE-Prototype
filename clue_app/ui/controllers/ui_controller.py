# ui/controllers/ui_controller.py

from typing import Dict

from ui.main_window import MainWindow
from preprocessing.eda import eda_summary, generate_eda_charts, generate_preview_charts
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

        # Navigation history for Back button
        self.page_history = []

        self._connect_signals()

    # ================= SAFE NAVIGATION =================

    def go_to(self, page):
        """Navigate and store history safely."""
        current = None
        if hasattr(self.main_window, "stack"):
            current = self.main_window.stack.currentWidget()
        if current:
            self.page_history.append(current)
        self.main_window.go_to_page(page)

    def go_back(self):
        if self.page_history:
            self.main_window.go_to_page(self.page_history.pop())

    # ================= SIGNAL CONNECTIONS =================

    def _connect_signals(self):
        w = self.main_window

        w.welcome_page.continue_clicked.connect(lambda: self.go_to(w.data_source_page))
        w.data_source_page.data_config_ready.connect(self._on_data_selected)
        w.model_selection_page.model_selected.connect(self._on_model_selected)
        w.before_eda_page.run_eda_clicked.connect(self._run_eda)
        w.after_eda_page.continue_to_model_clicked.connect(self._run_training)
        w.model_result_page.continue_to_forecast_clicked.connect(self._run_forecast)

        if hasattr(w.forecast_page, "continue_to_evaluation_clicked"):
            w.forecast_page.continue_to_evaluation_clicked.connect(self._show_evaluation)

        if hasattr(w.evaluation_page, "continue_to_report_clicked"):
            w.evaluation_page.continue_to_report_clicked.connect(lambda: self.go_to(w.report_page))

        if hasattr(w.report_page, "generate_report_clicked"):
            w.report_page.generate_report_clicked.connect(self._generate_report)

    # ================= DATA PREVIEW (BEFORE EDA) =================

    def _on_data_selected(self, config: dict):
        self.source_config = config
        df = load_financial_data(**self.source_config)

        summary = eda_summary(df)
        preview_fig = generate_preview_charts(df)

        page = self.main_window.before_eda_page
        page.set_status("Preview of raw data (Before Cleaning)")
        page.set_eda_summary(self._format_eda_summary(summary))
        page.set_preview_plot(preview_fig)

        self.go_to(page)

    # ================= MODEL SELECTED =================

    def _on_model_selected(self, model_type: str, horizon: int = 30):
        self.current_model_type = model_type
        self.forecast_horizon = horizon
        self.go_to(self.main_window.before_eda_page)

    # ================= FULL EDA =================

    def _run_eda(self):
        df = load_financial_data(**self.source_config)

        summary = eda_summary(df)
        fig = generate_eda_charts(df)

        page = self.main_window.after_eda_page
        page.set_eda_summary(self._format_eda_summary(summary))
        page.set_eda_plot(fig)

        self.go_to(page)

    # ================= TRAIN MODEL =================

    def _run_training(self):
        result = run_training(
            self.current_model_type,
            self.source_config,
            forecast_periods=self.forecast_horizon,
        )

        self.last_training_result = result
        self.last_metrics = result.get("metrics", {})

        model_order = result.get("model_order", "N/A")

        self.main_window.model_result_page.set_results(
            model_type=self.current_model_type,
            model_order=model_order,
            metrics=self.last_metrics,
        )

        self.go_to(self.main_window.model_result_page)

    # ================= FORECAST =================

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
            result.get("forecast"),
            result.get("confidence_intervals"),
        )

        page = self.main_window.forecast_page
        page.set_forecast_plot(fig)

        if hasattr(page, "set_predicted_values"):
            page.set_predicted_values(result.get("forecast"))

        self.go_to(page)

    # ================= EVALUATION =================

    def _show_evaluation(self):
        if hasattr(self.main_window.evaluation_page, "set_metrics"):
            self.main_window.evaluation_page.set_metrics(
                self._format_metrics(self.last_metrics)
            )
        self.go_to(self.main_window.evaluation_page)

    # ================= REPORT =================

    def _generate_report(self, output_path: str):
        if not output_path:
            output_path = "clue_report.pdf"
        if not output_path.lower().endswith(".pdf"):
            output_path += ".pdf"

        df = load_financial_data(**self.source_config)

        generate_report(
            output_path=output_path,
            title="CLUE Forecasting Report",
            model_results={
                "model_type": self.current_model_type,
                **self.last_training_result,
            },
            metrics=self.last_metrics,
            eda_summary=self._format_eda_summary(eda_summary(df)),
            eda_fig=generate_eda_charts(df),
            forecast_fig=plot_forecast(
                df,
                self.last_forecast_result.get("forecast"),
                self.last_forecast_result.get("confidence_intervals"),
            ),
            predicted_values=self.last_forecast_result.get("forecast"),
            notes="Generated by CLUE AI Forecasting System",
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
            f"MAE  : {metrics.get('MAE', 0.0):.4f}\n"
            f"MSE  : {metrics.get('MSE', 0.0):.4f}\n"
            f"RMSE : {metrics.get('RMSE', 0.0):.4f}\n"
            f"MAPE : {metrics.get('MAPE', 0.0):.4f}%"
        )