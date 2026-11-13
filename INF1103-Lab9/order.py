# order.py
from product import Product


class OrderLine:
    # Represents one line item within an order (product reference + quantity).
    def __init__(self, product: Product, quantity: int) -> None:
        self.product: Product = product
        self.quantity: int = int(quantity)

    def calculate_subtotal(self) -> float:
        # Calculates and returns the product price multiplied by the ordered quantity.
        return self.product.price * self.quantity

    def display_line(self) -> None:
        # Displays details of this specific order line.
        subtotal: float = self.calculate_subtotal()
        print(f"Product: {self.product.name:<20} | Qty: {self.quantity:<4} | Unit Price: ${self.product.price:<8.2f} | Subtotal: ${subtotal:.2f}")


class Order:
    # Manages an order composed of internally created OrderLine objects.
    def __init__(self, order_id: str) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        # Creates an OrderLine object internally and adds it to the order collection.
        order_line: OrderLine = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        # Removes an OrderLine from this order by matching product ID.
        for line in self.order_lines:
            if line.product.id.upper() == product_id.strip().upper():
                self.order_lines.remove(line)
                print(f"Removed line item for Product ID '{product_id}' from Order '{self.order_id}'.")
                return True
        print(f"Product ID '{product_id}' not found in Order '{self.order_id}'.")
        return False

    def calculate_total(self) -> float:
        # Calculates and returns the total value of the order by asking each OrderLine for its subtotal.
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def display_order_summary(self) -> None:
        # Displays the entire order details and calculated total.
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