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
        # Converts the Product object into base dictionary
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
        from productfactory import ProductFactory

        supplier_data: dict | None = data.get("supplier")
        supplier_obj: Supplier = Supplier.from_dict(supplier_data) if isinstance(supplier_data, dict) else Supplier("SUP001", "TechDistro Ltd", "sales@techdistro.com")

        # Determine product type
        product_type: str = data.get("type", "").lower()
        if not product_type:
            product_type = "digital" if "download_size" in data else "physical"

        return ProductFactory.create(
            product_type=product_type,
            product_id=data["id"],
            name=data["name"],
            price=data["price"],
            stock_quantity=data["stock"],
            supplier=supplier_obj,
            weight=data.get("weight", 0.0),
            download_size=data.get("download_size", 0.0),
            history=data.get("history", [data["stock"]])
        )

    def display_row(self) -> None:
        # Prints summary of product
        sup_name: str = self.supplier.name if self.supplier else "N/A"
        print(f"ID: {self.id} | Name: {self.name} | Price: ${self.price:.2f} | Stock: {self.stock} | Supplier: {sup_name}")

    def display_details(self) -> None:
        # Prints detailed view of product
        print(f"ID: {self.id}")
        print(f"Name: {self.name}")
        print(f"Price: ${self.price:.2f}")
        print(f"Stock: {self.stock}")
        if self.supplier:
            print("Supplier Info:")
            self.supplier.display_information()

    def display_information(self) -> None:
        self.display_details()