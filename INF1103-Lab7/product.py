class Product:
    def __init__(self, product_id: str, name: str, price: float, stock: int, history: list = None):
        self.id = product_id
        self.name = name
        self.price = float(price)
        self.stock = int(stock)
        self.history = history if history is not None else [self.stock]

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
        """Creates a Product object from a dictionary based on its specific attributes."""
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
        return cls(
            product_id=data["id"],
            name=data["name"],
            price=data["price"],
            stock=data["stock"],
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


# --- PhysicalProduct Class ---

class PhysicalProduct(Product):
    """
    Inherits from Product and introduces a weight attribute in kilograms.
    """
    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float, history: list = None):
        super().__init__(product_id, name, price, stock, history)
        self.weight = float(weight)

    def display_information(self):
        """Displays product information alongside its weight."""
        self.display_details()
        print(f"Weight: {self.weight:.2f} kg")

    def display_row(self):
        """Overrides display_row to include weight information in list views."""
        print(f"ID: {self.id} | Name: {self.name} | Price: ${self.price:.2f} | Stock: {self.stock} | Weight: {self.weight:.2f} kg")

    def to_dict(self) -> dict:
        """Overrides to_dict to include the weight attribute in JSON persistence."""
        data = super().to_dict()
        data["weight"] = self.weight
        return data


# --- DigitalProduct Class ---

class DigitalProduct(Product):
    """
    Inherits from Product and introduces a download_size attribute in megabytes (MB).
    """
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float, history: list = None):
        # 9. Reuse the existing Product constructor using super()
        super().__init__(product_id, name, price, stock, history)
        # 10. Initialize the additional download_size attribute
        self.download_size = float(download_size)

    # 11. Provide its own display_information() method displaying details alongside download size
    def display_information(self):
        """Displays product information alongside its download size in MB."""
        self.display_details()
        print(f"Download Size: {self.download_size:.2f} MB")

    def display_row(self):
        """Overrides display_row to include download size in list views."""
        print(f"ID: {self.id} | Name: {self.name} | Price: ${self.price:.2f} | Stock: {self.stock} | Size: {self.download_size:.2f} MB")

    def to_dict(self) -> dict:
        """Overrides to_dict to include the download_size attribute in JSON persistence."""
        data = super().to_dict()
        data["download_size"] = self.download_size
        return data