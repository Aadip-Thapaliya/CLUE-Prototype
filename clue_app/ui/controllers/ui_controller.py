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

        self._connect_signals()

    # ================= SIGNAL CONNECTIONS =================

    def _connect_signals(self):
        w = self.main_window

        # Welcome -> Data Source
        if hasattr(w.welcome_page, "continue_clicked"):
            w.welcome_page.continue_clicked.connect(
                lambda: w.go_to_page(w.data_source_page)
            )

        # Data Source -> Before EDA
        w.data_source_page.data_config_ready.connect(self._on_data_selected)

        # Model Selection
        w.model_selection_page.model_selected.connect(self._on_model_selected)

        # Before EDA -> Run EDA
        if hasattr(w.before_eda_page, "run_eda_clicked"):
            w.before_eda_page.run_eda_clicked.connect(self._run_eda)

        # After EDA -> Training
        if hasattr(w.after_eda_page, "continue_to_model_clicked"):
            w.after_eda_page.continue_to_model_clicked.connect(self._run_training)

        # Model Result -> Forecast
        if hasattr(w.model_result_page, "continue_to_forecast_clicked"):
            w.model_result_page.continue_to_forecast_clicked.connect(
                self._run_forecast
            )

        # Forecast -> Evaluation
        if hasattr(w.forecast_page, "continue_to_evaluation_clicked"):
            w.forecast_page.continue_to_evaluation_clicked.connect(
                self._show_evaluation
            )

        # Evaluation -> Report
        if hasattr(w.evaluation_page, "continue_to_report_clicked"):
            w.evaluation_page.continue_to_report_clicked.connect(
                lambda: w.go_to_page(w.report_page)
            )

        # Report -> Generate
        if hasattr(w.report_page, "generate_report_clicked"):
            w.report_page.generate_report_clicked.connect(self._generate_report)

    # ================= DATA SELECTED =================

    def _on_data_selected(self, config: dict):
        """Shows RAW preview EDA (Before Cleaning)"""
        self.source_config = config

        df = load_financial_data(**self.source_config)

        summary = eda_summary(df)
        preview_fig = generate_preview_charts(df)

        self.main_window.before_eda_page.set_status(
            "Preview of raw data (Before Cleaning)"
        )
        self.main_window.before_eda_page.set_eda_summary(
            self._format_eda_summary(summary)
        )
        self.main_window.before_eda_page.set_preview_plot(preview_fig)

        self.main_window.go_to_page(self.main_window.before_eda_page)

    # ================= MODEL SELECTED =================

    def _on_model_selected(self, model_type: str, horizon: int = 30):
        self.current_model_type = model_type
        self.forecast_horizon = horizon
        self.main_window.go_to_page(self.main_window.before_eda_page)

    # ================= RUN EDA =================

    def _run_eda(self):
        """Shows FULL EDA (After Processing)"""
        df = load_financial_data(**self.source_config)

        summary = eda_summary(df)
        fig = generate_eda_charts(df)

        self.main_window.after_eda_page.set_eda_summary(
            self._format_eda_summary(summary)
        )
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
            result.get("forecast"),
            result.get("confidence_intervals"),
        )

        self.main_window.forecast_page.set_forecast_plot(fig)
        self.main_window.go_to_page(self.main_window.forecast_page)

    # ================= SHOW EVALUATION =================

    def _show_evaluation(self):
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

# ================= UPGRADED EDA VISUALS =================
# Add the following functions to preprocessing/eda.py
# These create professional-grade EDA charts

import matplotlib.pyplot as plt
import pandas as pd


def generate_preview_charts(df: pd.DataFrame):
    """Lightweight preview shown in BEFORE EDA (raw data overview)"""
    fig, axes = plt.subplots(2, 1, figsize=(12, 6))

    # Close Price Line
    axes[0].plot(df.index, df['Close'], color="#00d4ff", linewidth=1.8)
    axes[0].set_title("Raw Close Price (Preview)")
    axes[0].set_ylabel("Price")
    axes[0].grid(True, alpha=0.3)

    # Simple Returns
    returns = df['Close'].pct_change()
    axes[1].plot(df.index, returns, color="#ffa500", linewidth=1)
    axes[1].axhline(0, color='white', linestyle='--', alpha=0.6)
    axes[1].set_title("Daily Returns (Preview)")
    axes[1].set_ylabel("Returns")
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def generate_eda_charts(df: pd.DataFrame):
    """Full professional EDA shown in AFTER EDA"""
    fig, axes = plt.subplots(4, 1, figsize=(14, 12))

    # 1. Close Price + Rolling Mean
    df['Rolling_20'] = df['Close'].rolling(20).mean()
    axes[0].plot(df.index, df['Close'], label="Close", color="#00d4ff")
    axes[0].plot(df.index, df['Rolling_20'], label="Rolling Mean (20)", color="#ff4081")
    axes[0].set_title("Price with Rolling Mean")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # 2. Histogram of Returns
    returns = df['Close'].pct_change()
    axes[1].hist(returns.dropna(), bins=50, color="#673ab7", alpha=0.8)
    axes[1].set_title("Distribution of Daily Returns")
    axes[1].set_xlabel("Returns")

    # 3. Volatility (Rolling Std)
    volatility = returns.rolling(20).std()
    axes[2].plot(df.index, volatility, color="#ffc107")
    axes[2].set_title("Rolling Volatility (20)")
    axes[2].set_ylabel("Volatility")
    axes[2].grid(True, alpha=0.3)

    # 4. Cumulative Returns
    cumulative = (1 + returns).cumprod()
    axes[3].plot(df.index, cumulative, color="#4caf50")
    axes[3].set_title("Cumulative Returns")
    axes[3].set_ylabel("Growth")
    axes[3].grid(True, alpha=0.3)

    plt.tight_layout()
    return fig

# ================= END UPGRADED VISUALS =================
