from abc import ABC, abstractmethod
from supplier import Supplier


# --- CanBeShipped Interface ---

class CanBeShipped(ABC):
    # Interface defining a contract for any shippable object
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        # Abstract method to calculate shipping costs
        pass


# --- Abstract Base Class Product ---

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, history: list[int] | None = None) -> None:
        self.id: str = product_id
        self.name: str = name
        self.price: float = float(price)
        self.stock: int = int(stock)
        self.supplier: Supplier = supplier
        self.history: list[int] = history if history is not None else [self.stock]

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        # Abstract method returning fulfilment information
        pass

    def update_stock(self, new_stock: int) -> None:
        # Updates stock quantity and records transaction delta in history
        diff: int = new_stock - self.stock
        self.history.append(diff)
        self.stock = new_stock

    def to_dict(self) -> dict:
        # Converts the Product object into a base dictionary for JSON serialization
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "supplier": self.supplier.to_dict() if self.supplier else None,
            "history": self.history
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        # Creates the appropriate Product subclass instance using JSON data
        product_type: str = data.get("type", "").lower()

        supplier_data: dict | None = data.get("supplier")
        supplier_obj: Supplier = Supplier.from_dict(supplier_data) if isinstance(supplier_data, dict) else Supplier("SUP001", "TechDistro Ltd", "sales@techdistro.com")

        if product_type == "physical" or "weight" in data:
            return PhysicalProduct(
                product_id=data["id"],
                name=data["name"],
                price=data["price"],
                stock=data["stock"],
                weight=data.get("weight", 0.0),
                supplier=supplier_obj,
                history=data.get("history", [data["stock"]])
            )
        elif product_type == "digital" or "download_size" in data:
            return DigitalProduct(
                product_id=data["id"],
                name=data["name"],
                price=data["price"],
                stock=data["stock"],
                download_size=data.get("download_size", 0.0),
                supplier=supplier_obj,
                history=data.get("history", [data["stock"]])
            )
        
        return PhysicalProduct(
            product_id=data["id"],
            name=data["name"],
            price=data["price"],
            stock=data["stock"],
            weight=0.0,
            supplier=supplier_obj,
            history=data.get("history", [data["stock"]])
        )

    def display_row(self) -> None:
        # Prints a single-line summary of the product for list views
        sup_name: str = self.supplier.name if self.supplier else "N/A"
        print(f"ID: {self.id} | Name: {self.name} | Price: ${self.price:.2f} | Stock: {self.stock} | Supplier: {sup_name}")

    def display_details(self) -> None:
        # Prints a detailed view of the product including supplier info
        print(f"ID: {self.id}")
        print(f"Name: {self.name}")
        print(f"Price: ${self.price:.2f}")
        print(f"Stock: {self.stock}")
        if self.supplier:
            print("Supplier Info:")
            self.supplier.display_information()

    def display_information(self) -> None:
        # Displays common product information
        self.display_details()


# --- PhysicalProduct Class ---

class PhysicalProduct(Product, CanBeShipped):
    # Physical product inheriting from Product and implementing CanBeShipped.
    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float, supplier: Supplier, history: list[int] | None = None) -> None:
        super().__init__(product_id, name, price, stock, supplier, history)
        self.weight: float = float(weight)

    def calculate_shipping_cost(self) -> float:
        # Calculates shipping cost based on product weight.
        base_fee: float = 5.00
        rate_per_kg: float = 2.50
        return base_fee + (self.weight * rate_per_kg)

    def get_fulfilment_info(self) -> str:
        # Returns a message explaining physical shipping requirements
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
        # Include the 'type' identifier and weight attribute
        data: dict = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.weight
        return data


# --- DigitalProduct Class ---

class DigitalProduct(Product):
    # Digital product inheriting from Product
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float, supplier: Supplier, history: list[int] | None = None) -> None:
        super().__init__(product_id, name, price, stock, supplier, history)
        self.download_size: float = float(download_size)

    def get_fulfilment_info(self) -> str:
        # Returns a message explaining digital delivery
        return f"Delivered digitally via email/download link. Size: {self.download_size:.2f} MB."

    def display_information(self) -> None:
        # Displays parent details
        super().display_information()
        print(f"Download Size: {self.download_size:.2f} MB")

    def display_row(self) -> None:
        # Include download size
        sup_name: str = self.supplier.name if self.supplier else "N/A"
        print(f"ID: {self.id} | Name: {self.name} | Price: ${self.price:.2f} | Stock: {self.stock} | Size: {self.download_size:.2f} MB | Supplier: {sup_name}")

    def to_dict(self) -> dict:
        # Include the 'type' identifier and download_size attribute
        data: dict = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.download_size
        return data