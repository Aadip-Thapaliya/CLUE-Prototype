# forecasting/base_model.py
from abc import ABC, abstractmethod
from typing import Any


class BaseModel(ABC):
    """Base interface for all forecasting models."""

    @abstractmethod
    def fit(self, X: Any, y: Any = None) -> "BaseModel":
        ...

    @abstractmethod
    def predict(self, X: Any) -> Any:
        ...

    @abstractmethod
    def forecast(self, periods: int) -> Any:
        ...
