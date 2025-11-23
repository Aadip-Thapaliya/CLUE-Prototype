"""
Model Evaluation Module for CLUE Financial Forecasting
Provides unified evaluation metrics for all forecasting models.
"""

import pandas as pd
import numpy as np
from typing import Dict


class ModelEvaluator:

    @staticmethod
    def mae(y_true: pd.Series, y_pred: pd.Series) -> float:
        return float(np.mean(np.abs(y_true - y_pred)))

    @staticmethod
    def mse(y_true: pd.Series, y_pred: pd.Series) -> float:
        return float(np.mean((y_true - y_pred) ** 2))

    @staticmethod
    def rmse(y_true: pd.Series, y_pred: pd.Series) -> float:
        return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))

    @staticmethod
    def mape(y_true, y_pred):
        y_true, y_pred = np.array(y_true), np.array(y_pred)
        mask = y_true != 0
        return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100)


    @staticmethod
    def evaluate_all(y_true: pd.Series, y_pred: pd.Series) -> Dict[str, float]:
        return {
            "MAE": ModelEvaluator.mae(y_true, y_pred),
            "MSE": ModelEvaluator.mse(y_true, y_pred),
            "RMSE": ModelEvaluator.rmse(y_true, y_pred),
            "MAPE": ModelEvaluator.mape(y_true, y_pred),
        }


# -------------------- GUI FRIENDLY FUNCTION --------------------

def evaluate_model(y_true: pd.Series, y_pred: pd.Series) -> Dict[str, float]:
    return ModelEvaluator.evaluate_all(y_true, y_pred)
def compare_models(metrics_a: dict, metrics_b: dict, name_a: str, name_b: str) -> dict:
    """Return simple comparison between two models based on RMSE."""
    rmse_a = metrics_a.get("RMSE", float("inf"))
    rmse_b = metrics_b.get("RMSE", float("inf"))

    if rmse_a < rmse_b:
        best = name_a
    elif rmse_b < rmse_a:
        best = name_b
    else:
        best = "TIE"

    return {
        "model_a": name_a,
        "model_b": name_b,
        "metrics_a": metrics_a,
        "metrics_b": metrics_b,
        "best_model": best,
    }
