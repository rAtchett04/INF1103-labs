from discountstrategy import DiscountStrategy


class BulkDiscount(DiscountStrategy):
    # Subtracts a fixed amount when total meets/exceeds threshold
    def __init__(self, threshold: float, amount: float) -> None:
        self.threshold: float = float(threshold)
        self.amount: float = float(amount)

    def apply(self, total: float) -> float:
        return max(0.0, total - self.amount) if total >= self.threshold else total