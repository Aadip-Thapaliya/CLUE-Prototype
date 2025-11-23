# forecasting/model_selector.py
from typing import Dict, Literal

from forecasting.auto_arima import AutoARIMAModel, train_auto_arima
from forecasting.xgboost_model import XGBoostModel, train_xgboost_model


ModelType = Literal["AUTO_ARIMA", "XGBOOST"]


class ModelSelector:
    """Factory / selector for forecasting models."""

    @staticmethod
    def get_model_class(model_type: ModelType):
        if model_type == "AUTO_ARIMA":
            return AutoARIMAModel
        elif model_type == "XGBOOST":
            return XGBoostModel
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

    @staticmethod
    def train_model(model_type: ModelType, X, y=None):
        if model_type == "AUTO_ARIMA":
            # X is expected to be a Series
            return train_auto_arima(X)
        elif model_type == "XGBOOST":
            # X: DataFrame, y: Series
            return train_xgboost_model(X,y)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
