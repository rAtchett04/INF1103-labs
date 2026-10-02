import json
import os

FILENAME = "inventory.json"


# --- Data Persistence Functions ---

def load_inventory():
    """
    Checks if inventory.json exists and loads the data.
    If not found, starts with initial default inventory.
    """
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                inventory = json.load(file)
                print("inventory.json found.")
                print("Inventory loaded successfully.\n")
                return inventory
        except (json.JSONDecodeError, IOError):
            print("Error loading inventory file. Starting fresh.\n")

    # Default starting inventory if file is missing/empty
    default_inventory = [
        {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15, "history": [15]},
        {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40, "history": [40]},
        {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25, "history": [25]}
    ]
    return default_inventory

def save_inventory(inventory, silent=False):
    """Saves inventory data to inventory.json."""
    if not silent:
        print("Saving inventory...")
    try:
        with open(FILENAME, "w") as file:
            json.dump(inventory, file, indent=4)
        if not silent:
            print("Inventory saved successfully to inventory.json.")
        else:
            print("Inventory saved successfully.")
    except IOError as e:
        print(f"Error saving inventory: {e}")


# --- Data Manipulation Functions ---

def display_all(inventory):
    """Displays current inventory list with formatted rows."""
    print("\nCurrent Inventory")
    print("--------------------------------------------------")
    for item in inventory:
        print(f"ID: {item['id']} | Name: {item['name']} | Price: ${item['price']:.2f} | Stock: {item['stock']}")
    print("--------------------------------------------------")


def add_product(inventory):
    """Adds a new product by taking Product ID, Name, Price, and Stock Quantity."""
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    
    # Check if ID already exists
    for item in inventory:
        if item["id"].upper() == product_id.upper():
            print("Product ID already exists!")
            return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))

        new_product = {
            "id": product_id,
            "name": name,
            "price": price,
            "stock": stock,
            "history": [stock]
        }
        inventory.append(new_product)
        print("\nProduct added successfully!")
    except ValueError:
        print("Invalid input for price or stock quantity.")


def update_stock(inventory):
    """Updates the stock quantity of a product searching by Product ID."""
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()

    for item in inventory:
        if item["id"].upper() == product_id.upper():
            print("\nProduct Found:")
            print(f"Name: {item['name']}")
            print(f"Current Stock: {item['stock']}\n")
            
            try:
                new_stock = int(input("New Stock Quantity: "))
                # Track transaction diff in history list
                diff = new_stock - item["stock"]
                item["history"].append(diff)
                item["stock"] = new_stock
                print("\nStock updated successfully!")
            except ValueError:
                print("Invalid quantity entered.")
            return

    print("Product not found.")


def search_product(inventory):
    """Searches for a specific product using its Product ID."""
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()

    for item in inventory:
        if item["id"].upper() == product_id.upper():
            print("\nProduct Found")
            print("--------------------------------------------------")
            print(f"ID: {item['id']}")
            print(f"Name: {item['name']}")
            print(f"Price: ${item['price']:.2f}")
            print(f"Stock: {item['stock']}")
            print("--------------------------------------------------")
            return

    print("\nProduct not found.")


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

        option = input("Enter option: ").strip()

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
        
        print()  # Spacer line between commands

if __name__ == "__main__":
    main()