# order.py
from product import Product
from order_line import OrderLine
from discountstrategy import DiscountStrategy


class Order:
    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []
        # Defaults to 'none' DiscountStrategy
        self.discount: DiscountStrategy = discount if discount is not None else DiscountStrategy("none")

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        # Creates an OrderLine object
        order_line: OrderLine = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        # Removes an OrderLine from this order by matching product ID
        for line in self.order_lines:
            if line.product.id.upper() == product_id.strip().upper():
                self.order_lines.remove(line)
                print(f"Removed line item for Product ID '{product_id}' from Order '{self.order_id}'.")
                return True
        print(f"Product ID '{product_id}' not found in Order '{self.order_id}'.")
        return False

    def calculate_total(self) -> float:
        # Adds up order line subtotals
        total: float = sum(line.calculate_subtotal() for line in self.order_lines)
        return self.discount.apply(total)

    def display_order_summary(self) -> None:
        # Displays entire order details and total
        print(f"\nOrder Summary [ID: {self.order_id}]")
        print("--------------------------------------------------")
        if not self.order_lines:
            print("No items in this order.")
        else:
            for line in self.order_lines:
                line.display_line()
        print("--------------------------------------------------")
        print(f"ORDER TOTAL: ${self.calculate_total():.2f}")
        print("--------------------------------------------------\n")