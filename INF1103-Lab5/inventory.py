import json
import os
from product import Product


class Inventory:
    def __init__(self, filename: str = "inventory.json"):
        self.filename = filename
        self.products: list[Product] = []

    def load(self):
        """Loads inventory from disk or initializes default products if missing."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    raw_data = json.load(file)
                    self.products = [Product.from_dict(item) for item in raw_data]
                    print(f"{self.filename} found.")
                    print("Inventory loaded successfully.\n")
                    return
            except (json.JSONDecodeError, IOError, KeyError):
                print("Error loading inventory file. Starting fresh.\n")

        # Default starting inventory
        self.products = [
            Product("P001", "Laptop", 1200.00, 15),
            Product("P002", "Mouse", 25.50, 40),
            Product("P003", "Keyboard", 45.00, 25)
        ]

    def save(self, silent: bool = False):
        """Saves current inventory list to JSON."""
        if not silent:
            print("Saving inventory...")
        try:
            data_to_save = [product.to_dict() for product in self.products]
            with open(self.filename, "w") as file:
                json.dump(data_to_save, file, indent=4)
            if not silent:
                print(f"Inventory saved successfully to {self.filename}.")
            else:
                print("Inventory saved successfully.")
        except IOError as e:
            print(f"Error saving inventory: {e}")

    def display_all(self):
        """Displays formatted list of all items."""
        print("\nCurrent Inventory")
        print("--------------------------------------------------")
        for product in self.products:
            product.display_row()
        print("--------------------------------------------------")

    def find_by_id(self, product_id: str) -> Product | None:
        """Helper method to look up a product by ID."""
        for product in self.products:
            if product.id.upper() == product_id.strip().upper():
                return product
        return None

    def add_product(self, product_id: str, name: str, price: float, stock: int) -> bool:
        """Adds a new Product instance if ID does not already exist."""
        if self.find_by_id(product_id):
            print("Product ID already exists!")
            return False

        new_product = Product(product_id, name, price, stock)
        self.products.append(new_product)
        print("\nProduct added successfully!")
        return True

    def update_stock(self, product_id: str, new_stock: int) -> bool:
        """Updates stock quantity of a target product."""
        product = self.find_by_id(product_id)
        if product:
            print("\nProduct Found:")
            print(f"Name: {product.name}")
            print(f"Current Stock: {product.stock}\n")
            product.update_stock(new_stock)
            print("\nStock updated successfully!")
            return True

        print("Product not found.")
        return False

    def search_product(self, product_id: str) -> bool:
        """Searches and prints full product details."""
        product = self.find_by_id(product_id)
        if product:
            print("\nProduct Found")
            print("--------------------------------------------------")
            product.display_details()
            print("--------------------------------------------------")
            return True

        print("\nProduct not found.")
        return False