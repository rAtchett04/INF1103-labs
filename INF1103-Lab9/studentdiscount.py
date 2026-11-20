from discountstrategy import DiscountStrategy


class StudentDiscount(DiscountStrategy):
    # Applies a student percentage discount
    def __init__(self, percentage: float = 5.0) -> None:
        self.percentage: float = float(percentage)

    def apply(self, total: float) -> float:
        return max(0.0, total * (1.0 - self.percentage / 100.0))