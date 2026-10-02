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

if __name__ == "__main__":
    main()