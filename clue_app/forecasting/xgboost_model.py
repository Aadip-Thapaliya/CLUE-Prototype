"""
XGBoost Model Module for CLUE Financial Forecasting
Handles training and forecasting for engineered univariate time series features.
Designed for AutoML pipeline and GUI integration.
"""

import pandas as pd
from typing import Tuple
from xgboost import XGBRegressor


class XGBoostModel:
    def __init__(self):
        self.model = XGBRegressor(
            n_estimators=500,
            learning_rate=0.05,
            max_depth=5,
            subsample=0.8,
            colsample_bytree=0.8,
            objective="reg:squarederror"
        )

    # -------------------- TRAINING --------------------

    def fit(self, X_train: pd.DataFrame, y_train: pd.Series):
        self.model.fit(X_train, y_train)
        return self

    # -------------------- PREDICTION --------------------

    def predict(self, X_test: pd.DataFrame) -> pd.Series:
        predictions = self.model.predict(X_test)
        return pd.Series(predictions, index=X_test.index, name="Predicted")

    # -------------------- FORECASTING --------------------

    def recursive_forecast(self, last_known_data: pd.DataFrame, future_steps: int = 30) -> pd.Series:
        """
        Recursive forecasting for future time steps using last available row.
        """
        predictions = []
        current_input = last_known_data.copy()

        for _ in range(future_steps):
            pred = self.model.predict(current_input)[0]
            predictions.append(pred)

            # shift lag features
            lag_cols = [col for col in current_input.columns if col.startswith("lag_")]
            for lag in reversed(lag_cols):
                lag_num = int(lag.split("_")[1])
                if lag_num == 1:
                    current_input[lag] = pred
                else:
                    current_input[f"lag_{lag_num}"] = current_input[f"lag_{lag_num-1}"]
        
        return pd.Series(predictions, name="Forecast")


# -------------------- GUI FRIENDLY FUNCTIONS --------------------

def train_xgboost_model(X_train: pd.DataFrame, y_train: pd.Series) -> XGBoostModel:
    model = XGBoostModel()
    model.fit(X_train, y_train)
    return model


def predict_xgboost(model: XGBoostModel, X_test: pd.DataFrame) -> pd.Series:
    return model.predict(X_test)