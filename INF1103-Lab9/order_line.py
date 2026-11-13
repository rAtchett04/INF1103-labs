from product import Product

class OrderLine:
    # Represents one line item
    def __init__(self, product: Product, quantity: int) -> None:
        self.product: Product = product
        self.quantity: int = int(quantity)

    def calculate_subtotal(self) -> float:
        # Calculates total price
        return self.product.price * self.quantity

    def display_line(self) -> None:
        subtotal: float = self.calculate_subtotal()
        print(f"Product: {self.product.name:<20} | Qty: {self.quantity:<4} | Unit Price: ${self.product.price:<8.2f} | Subtotal: ${subtotal:.2f}")