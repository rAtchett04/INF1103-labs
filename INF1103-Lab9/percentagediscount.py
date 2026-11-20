from discountstrategy import DiscountStrategy


class PercentageDiscount(DiscountStrategy):
    # Applies a percentage discount
    def __init__(self, percentage: float) -> None:
        self.percentage: float = float(percentage)

    def apply(self, total: float) -> float:
        return max(0.0, total * (1.0 - self.percentage / 100.0))