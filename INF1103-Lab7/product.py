from abc import ABC, abstractmethod


# --- CanBeShipped Interface ---

class CanBeShipped(ABC):
    """
    Interface defining a contract for any shippable object.
    Contains no product-specific attributes or implementation details.
    """
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Abstract method to calculate shipping costs."""
        pass


# --- Abstract Base Class Product ---

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int, history: list = None):
        self.id = product_id
        self.name = name
        self.price = float(price)
        self.stock = int(stock)
        self.history = history if history is not None else [self.stock]

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Abstract method returning fulfilment information."""
        pass

    def update_stock(self, new_stock: int):
        """Updates stock quantity and records transaction delta in history."""
        diff = new_stock - self.stock
        self.history.append(diff)
        self.stock = new_stock

    def to_dict(self) -> dict:
        """Converts the Product object into a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "history": self.history
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Product instance from a dictionary based on specific attributes."""
        if "weight" in data:
            return PhysicalProduct(
                product_id=data["id"],
                name=data["name"],
                price=data["price"],
                stock=data["stock"],
                weight=data["weight"],
                history=data.get("history", [data["stock"]])
            )
        elif "download_size" in data:
            return DigitalProduct(
                product_id=data["id"],
                name=data["name"],
                price=data["price"],
                stock=data["stock"],
                download_size=data["download_size"],
                history=data.get("history", [data["stock"]])
            )
        
        return PhysicalProduct(
            product_id=data["id"],
            name=data["name"],
            price=data["price"],
            stock=data["stock"],
            weight=0.0,
            history=data.get("history", [data["stock"]])
        )

    def display_row(self):
        """Prints a single-line summary of the product for the list view."""
        print(f"ID: {self.id} | Name: {self.name} | Price: ${self.price:.2f} | Stock: {self.stock}")

    def display_details(self):
        """Prints a detailed view of the product."""
        print(f"ID: {self.id}")
        print(f"Name: {self.name}")
        print(f"Price: ${self.price:.2f}")
        print(f"Stock: {self.stock}")

    def display_information(self):
        """Displays common product information."""
        self.display_details()


# --- PhysicalProduct ---

class PhysicalProduct(Product, CanBeShipped):
    """
    Physical product that inherits common product traits and implements CanBeShipped.
    """
    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float, history: list = None):
        super().__init__(product_id, name, price, stock, history)
        self.weight = float(weight)

    # Implementation of CanBeShipped interface method
    def calculate_shipping_cost(self) -> float:
        """Calculates shipping cost based on product weight ($5.00 base fee + $2.50 per kg)."""
        base_fee = 5.00
        rate_per_kg = 2.50
        return base_fee + (self.weight * rate_per_kg)

    def get_fulfilment_info(self) -> str:
        """Returns a message explaining physical shipping requirements and cost."""
        shipping_cost = self.calculate_shipping_cost()
        return f"Physical shipping required (Weight: {self.weight:.2f} kg, Shipping Cost: ${shipping_cost:.2f})."

    def display_information(self):
        """Displays parent details along with weight and calculated shipping cost."""
        super().display_information()
        print(f"Weight: {self.weight:.2f} kg")
        print(f"Shipping Cost: ${self.calculate_shipping_cost():.2f}")
        print(f"Fulfilment Info: {self.get_fulfilment_info()}")

    def display_row(self):
        """Overrides display_row to include weight information."""
        print(f"ID: {self.id} | Name: {self.name} | Price: ${self.price:.2f} | Stock: {self.stock} | Weight: {self.weight:.2f} kg")

    def to_dict(self) -> dict:
        """Overrides to_dict to include the weight attribute."""
        data = super().to_dict()
        data["weight"] = self.weight
        return data


# --- DigitalProduct ---

class DigitalProduct(Product):
    """
    Digital product inheriting from Product. Does NOT implement CanBeShipped.
    """
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float, history: list = None):
        super().__init__(product_id, name, price, stock, history)
        self.download_size = float(download_size)

    def get_fulfilment_info(self) -> str:
        """Returns a message explaining digital delivery."""
        return f"Delivered digitally via email/download link. Size: {self.download_size:.2f} MB."

    def display_information(self):
        """Displays parent details along with download size."""
        super().display_information()
        print(f"Download Size: {self.download_size:.2f} MB")
        print(f"Fulfilment Info: {self.get_fulfilment_info()}")

    def display_row(self):
        """Overrides display_row to include download size."""
        print(f"ID: {self.id} | Name: {self.name} | Price: ${self.price:.2f} | Stock: {self.stock} | Size: {self.download_size:.2f} MB")

    def to_dict(self) -> dict:
        """Overrides to_dict to include the download_size attribute."""
        data = super().to_dict()
        data["download_size"] = self.download_size
        return data