from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    # Abstract base class defining order discount strategies
    @abstractmethod
    def apply(self, total: float) -> float:
        pass