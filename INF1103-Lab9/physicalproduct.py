from product import Product
from canbeshipped import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    # Inherit from Product, implement CanBeShipped.
    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float, supplier: Supplier, history: list[int] | None = None) -> None:
        super().__init__(product_id, name, price, stock, supplier, history)
        self.weight: float = float(weight)

    def calculate_shipping_cost(self) -> float:
        # Calculates shipping cost based on product weight
        base_fee: float = 5.00
        rate_per_kg: float = 2.50
        return base_fee + (self.weight * rate_per_kg)

    def get_fulfilment_info(self) -> str:
        # Physical shipping requirements.
        shipping_cost: float = self.calculate_shipping_cost()
        return f"Physical shipping required (Weight: {self.weight:.2f} kg, Shipping Cost: ${shipping_cost:.2f})."

    def display_information(self) -> None:
        # Displays parent details
        super().display_information()
        print(f"Weight: {self.weight:.2f} kg")
        print(f"Shipping Cost: ${self.calculate_shipping_cost():.2f}")

    def display_row(self) -> None:
        # Include weight information
        sup_name: str = self.supplier.name if self.supplier else "N/A"
        print(f"ID: {self.id} | Name: {self.name} | Price: ${self.price:.2f} | Stock: {self.stock} | Weight: {self.weight:.2f} kg | Supplier: {sup_name}")

    def to_dict(self) -> dict:
        data: dict = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.weight
        return data