from discountstrategy import DiscountStrategy


class NoDiscount(DiscountStrategy):
    # Returns the order total unchanged
    def apply(self, total: float) -> float:
        return total