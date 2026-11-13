from product import Product
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from supplier import Supplier


class ProductFactory:
    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        weight: float = 0.0,
        download_size: float = 0.0,
        history: list[int] | None = None
    ) -> Product:
        p_type: str = product_type.strip().lower()

        if p_type == "physical":
            return PhysicalProduct(
                product_id=product_id,
                name=name,
                price=price,
                stock=stock_quantity,
                weight=weight,
                supplier=supplier,
                history=history
            )
        elif p_type == "digital":
            return DigitalProduct(
                product_id=product_id,
                name=name,
                price=price,
                stock=stock_quantity,
                download_size=download_size,
                supplier=supplier,
                history=history
            )
        else:
            raise ValueError(f"Unknown product type: {product_type}")