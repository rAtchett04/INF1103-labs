import json
import os
from product import Product, PhysicalProduct, DigitalProduct
from supplier import Supplier


class Inventory:
    def __init__(self, filename: str = "inventory.json") -> None:
        self.filename: str = filename
        self.products: list[Product] = []

    def load(self) -> None:
        # Loads inventory from disk
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    raw_data: list[dict] = json.load(file)
                    self.products = [Product.from_dict(item) for item in raw_data]
                    print(f"{self.filename} found.")
                    print("Inventory loaded successfully.\n")
                    return
            except (json.JSONDecodeError, IOError, KeyError):
                print("Error loading inventory file. Starting fresh.\n")

        default_supplier: Supplier = Supplier("SUP001", "Global Tech Wholesale", "contact@globaltech.com")

        self.products = [
            PhysicalProduct("P001", "Laptop", 1200.00, 15, weight=2.5, supplier=default_supplier),
            PhysicalProduct("P002", "Mouse", 25.50, 40, weight=0.1, supplier=default_supplier),
            DigitalProduct("D001", "E-Book Guide", 15.00, 100, download_size=12.5, supplier=default_supplier)
        ]

    def save(self, silent: bool = False) -> None:
        # Saves current inventory list to JSON
        if not silent:
            print("Saving inventory...")
        try:
            data_to_save: list[dict] = [product.to_dict() for product in self.products]
            with open(self.filename, "w") as file:
                json.dump(data_to_save, file, indent=4)
            if not silent:
                print(f"Inventory saved successfully to {self.filename}.")
            else:
                print("Inventory saved successfully.")
        except IOError as e:
            print(f"Error saving inventory: {e}")

    # Work with the Product abstraction
    def display_all_products(self) -> None:
        # Asks each Product to display its information polymorphically
        print("\nCurrent Inventory (LSP Abstraction View)")
        print("--------------------------------------------------")
        for product in self.products:
            product.display_information()
            print("--------------------------------------------------")

    def add_product(self, product: Product) -> bool:
        # Adds an existing Product object to the inventory
        if self.find_product(product.id):
            print("Product ID already exists in this inventory!")
            return False

        self.products.append(product)
        print("\nProduct added successfully!")
        return True

    def remove_product(self, product_id: str) -> Product | None:
        # Removes matching Product reference from inventory and returns it
        product: Product | None = self.find_product(product_id)
        if product:
            self.products.remove(product)
            print(f"\nProduct '{product.name}' (ID: {product.id}) removed from inventory.")
            return product
        
        print("\nProduct not found for removal.")
        return None

    def find_product(self, product_id: str) -> Product | None:
        # Returns matching Product, or None if it cannot be found
        for product in self.products:
            if product.id.upper() == product_id.strip().upper():
                return product
        return None

    def find_by_id(self, product_id: str) -> Product | None:
        return self.find_product(product_id)

    def display_all(self) -> None:
        # Displays formatted list of all items
        print("\nCurrent Inventory")
        print("--------------------------------------------------")
        for product in self.products:
            product.display_row()
        print("--------------------------------------------------")

    def search_product(self, product_id: str) -> bool:
        # Searches and prints full product details polymorphically
        product: Product | None = self.find_product(product_id)
        if product:
            print("\nProduct Found")
            print("--------------------------------------------------")
            product.display_information()
            print("--------------------------------------------------")
            return True

        print("\nProduct not found.")
        return False