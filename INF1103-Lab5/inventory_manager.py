# inventory_manager.py
import json
import os
from product import Product

FILENAME = "inventory.json"


# --- Data Persistence Functions ---

def load_inventory() -> list[Product]:
    """
    Checks if inventory.json exists and loads data as Product instances.
    If not found, starts with initial default inventory.
    """
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                raw_data = json.load(file)
                inventory = [Product.from_dict(item) for item in raw_data]
                print("inventory.json found.")
                print("Inventory loaded successfully.\n")
                return inventory
        except (json.JSONDecodeError, IOError, KeyError):
            print("Error loading inventory file. Starting fresh.\n")

    # Default starting inventory if file is missing/corrupted
    return [
        Product("P001", "Laptop", 1200.00, 15),
        Product("P002", "Mouse", 25.50, 40),
        Product("P003", "Keyboard", 45.00, 25)
    ]


def save_inventory(inventory: list[Product], silent=False):
    """Saves inventory data by converting Product objects back to dictionaries for JSON."""
    if not silent:
        print("Saving inventory...")
    try:
        data_to_save = [product.to_dict() for product in inventory]
        with open(FILENAME, "w") as file:
            json.dump(data_to_save, file, indent=4)
        if not silent:
            print("Inventory saved successfully to inventory.json.")
        else:
            print("Inventory saved successfully.")
    except IOError as e:
        print(f"Error saving inventory: {e}")


# --- Data Manipulation Functions ---

def display_all(inventory: list[Product]):
    """Displays current inventory list with formatted rows."""
    print("\nCurrent Inventory")
    print("--------------------------------------------------")
    for product in inventory:
        product.display_row()
    print("--------------------------------------------------")


def add_product(inventory: list[Product]):
    """Adds a new Product instance to the inventory."""
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()

    # Check if ID already exists
    for product in inventory:
        if product.id.upper() == product_id.upper():
            print("Product ID already exists!")
            return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))

        new_product = Product(product_id, name, price, stock)
        inventory.append(new_product)
        print("\nProduct added successfully!")
    except ValueError:
        print("Invalid input for price or stock quantity.")


def update_stock(inventory: list[Product]):
    """Updates the stock quantity of a product searching by Product ID."""
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()

    for product in inventory:
        if product.id.upper() == product_id.upper():
            print("\nProduct Found:")
            print(f"Name: {product.name}")
            print(f"Current Stock: {product.stock}\n")

            try:
                new_stock = int(input("New Stock Quantity: "))
                product.update_stock(new_stock)
                print("\nStock updated successfully!")
            except ValueError:
                print("Invalid quantity entered.")
            return

    print("Product not found.")


def search_product(inventory: list[Product]):
    """Searches for a specific product using its Product ID."""
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()

    for product in inventory:
        if product.id.upper() == product_id.upper():
            print("\nProduct Found")
            print("--------------------------------------------------")
            product.display_details()
            print("--------------------------------------------------")
            return

    print("\nProduct not found.")


# --- Helper Guard for Non-Interactive / EOF Environments ---

def get_user_option() -> str:
    try:
        return input("Enter option: ").strip()
    except EOFError:
        print("\nEOF detected. Exiting program gracefully...")
        return "6"


# --- Main Menu System ---

def main():
    print("==================================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("==================================================\n")

    inventory = load_inventory()

    while True:
        print("--------- MENU ---------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("------------------------\n")

        option = get_user_option()

        if option == "1":
            display_all(inventory)
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            print()
            save_inventory(inventory)
        elif option == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory, silent=True)
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please try again.\n")

        print()


if __name__ == "__main__":
    main()