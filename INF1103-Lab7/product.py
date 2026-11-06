from abc import ABC, abstractmethod


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int, history: list = None):
        self.id = product_id
        self.name = name
        self.price = float(price)
        self.stock = int(stock)
        self.history = history if history is not None else [self.stock]

    # --- Abstract Method Declaration ---
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Abstract method returning fulfilment information. Must be implemented by subclasses."""
        pass

    def update_stock(self, new_stock: int):
        """Updates stock quantity and records the transaction delta in history."""
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
        """Creates a Product instance from a dictionary based on its specific attributes."""
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


# --- PhysicalProduct Implementation ---

class PhysicalProduct(Product):
    """
    Inherits from Product and introduces a weight attribute in kilograms.
    """
    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float, history: list = None):
        super().__init__(product_id, name, price, stock, history)
        self.weight = float(weight)

    # Implement get_fulfilment_info() for physical shipping
    def get_fulfilment_info(self) -> str:
        """Returns a message explaining physical shipping requirements."""
        return f"Physical shipping required. Item weight: {self.weight:.2f} kg."

    def display_information(self):
        """Calls super().display_information() then displays weight and fulfilment info."""
        super().display_information()
        print(f"Weight: {self.weight:.2f} kg")
        print(f"Fulfilment Info: {self.get_fulfilment_info()}")

    def display_row(self):
        """Overrides display_row to include weight information in list views."""
        print(f"ID: {self.id} | Name: {self.name} | Price: ${self.price:.2f} | Stock: {self.stock} | Weight: {self.weight:.2f} kg")

    def to_dict(self) -> dict:
        """Overrides to_dict to include the weight attribute in JSON persistence."""
        data = super().to_dict()
        data["weight"] = self.weight
        return data


# --- DigitalProduct Implementation ---

class DigitalProduct(Product):
    """
    Inherits from Product and introduces a download_size attribute in megabytes (MB).
    """
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float, history: list = None):
        super().__init__(product_id, name, price, stock, history)
        self.download_size = float(download_size)

    # Implement get_fulfilment_info() for digital delivery
    def get_fulfilment_info(self) -> str:
        """Returns a message explaining digital delivery."""
        return f"Delivered digitally via email/download link. Size: {self.download_size:.2f} MB."

    def display_information(self):
        """Calls super().display_information() then displays download size and fulfilment info."""
        super().display_information()
        print(f"Download Size: {self.download_size:.2f} MB")
        print(f"Fulfilment Info: {self.get_fulfilment_info()}")

    def display_row(self):
        """Overrides display_row to include download size in list views."""
        print(f"ID: {self.id} | Name: {self.name} | Price: ${self.price:.2f} | Stock: {self.stock} | Size: {self.download_size:.2f} MB")

    def to_dict(self) -> dict:
        """Overrides to_dict to include the download_size attribute in JSON persistence."""
        data = super().to_dict()
        data["download_size"] = self.download_size
        return data