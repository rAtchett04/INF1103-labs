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
        """Creates a Product object from a dictionary."""
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