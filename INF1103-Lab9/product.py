from abc import ABC, abstractmethod
from supplier import Supplier


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
        pass

    def update_stock(self, new_stock: int) -> None:
        # Updates stock quantity and records transactions
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
        # Deferred local imports prevent circular dependency during module evaluation
        from physicalproduct import PhysicalProduct
        from digitalproduct import DigitalProduct

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
        # Prints a detailed view of the product
        print(f"ID: {self.id}")
        print(f"Name: {self.name}")
        print(f"Price: ${self.price:.2f}")
        print(f"Stock: {self.stock}")
        if self.supplier:
            print("Supplier Info:")
            self.supplier.display_information()

    def display_information(self) -> None:
        self.display_details()