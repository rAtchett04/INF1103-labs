from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    # Digital product inheriting from Product
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float, supplier: Supplier, history: list[int] | None = None) -> None:
        super().__init__(product_id, name, price, stock, supplier, history)
        self.download_size: float = float(download_size)

    def get_fulfilment_info(self) -> str:
        return f"Delivered digitally via email/download link. Size: {self.download_size:.2f} MB."

    def display_information(self) -> None:
        # Displays parent details
        super().display_information()
        print(f"Download Size: {self.download_size:.2f} MB")

    def display_row(self) -> None:
        # Include download size.
        sup_name: str = self.supplier.name if self.supplier else "N/A"
        print(f"ID: {self.id} | Name: {self.name} | Price: ${self.price:.2f} | Stock: {self.stock} | Size: {self.download_size:.2f} MB | Supplier: {sup_name}")

    def to_dict(self) -> dict:
        # Include the 'type' identifier and download_size attribute
        data: dict = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.download_size
        return data