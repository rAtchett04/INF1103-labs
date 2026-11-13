
class DiscountStrategy:
    def __init__(
        self,
        strategy_type: str = "none",
        percentage: float = 0.0,
        threshold: float = 0.0,
        amount: float = 0.0
    ) -> None:
        
        self.strategy_type: str = strategy_type.lower().strip()
        self.percentage: float = float(percentage)
        self.threshold: float = float(threshold)
        self.amount: float = float(amount)

    def apply(self, total: float) -> float:
        # Calculates and returns discounted total
        if self.strategy_type == "none":
            return total

        elif self.strategy_type == "percentage":
            discount_factor: float = 1.0 - (self.percentage / 100.0)
            return max(0.0, total * discount_factor)

        elif self.strategy_type == "bulk":
            if total >= self.threshold:
                return max(0.0, total - self.amount)
            return total

        elif self.strategy_type == "student":
            # Defaults to 5% discount
            rate: float = self.percentage if self.percentage > 0 else 5.0
            return max(0.0, total * (1.0 - rate / 100.0))

        else:
            raise ValueError(f"Unknown discount strategy type: '{self.strategy_type}'")

    @classmethod
    def no_discount(cls) -> "DiscountStrategy":
        return cls(strategy_type="none")

    @classmethod
    def percentage_discount(cls, percentage: float) -> "DiscountStrategy":
        return cls(strategy_type="percentage", percentage=percentage)

    @classmethod
    def bulk_discount(cls, threshold: float, amount: float) -> "DiscountStrategy":
        return cls(strategy_type="bulk", threshold=threshold, amount=amount)

    @classmethod
    def student_discount(cls, percentage: float = 5.0) -> "DiscountStrategy":
        return cls(strategy_type="student", percentage=percentage)