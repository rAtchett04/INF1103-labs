# inventory_manager.py
from inventory import Inventory
from product import Product, PhysicalProduct, DigitalProduct


def test_display_information_overriding():
    """
    2.2 Test implementation:
    Creates one physical product and one digital product, calling display_information()
    on each object to verify that both common product information and type-specific details are shown.
    """
    print("==================================================")
    print("--- 2.2 Testing display_information() Overriding ---")
    print("==================================================")
    
    # Create one physical product
    phys_product = PhysicalProduct("P099", "Gaming Laptop", 1500.00, 5, weight=3.2)
    print("\n--- Physical Product Information ---")
    phys_product.display_information()

    # Create one digital product
    digi_product = DigitalProduct("D099", "Photo Editing Software", 89.99, 100, download_size=450.5)
    print("\n--- Digital Product Information ---")
    digi_product.display_information()
    
    print("--------------------------------------------------\n")


def get_user_option() -> str:
    """Helper guard against EOFError in non-interactive environments."""
    try:
        return input("Enter option: ").strip()
    except EOFError:
        print("\nEOF detected. Exiting program gracefully...")
        return "6"


def main():
    test_display_information_overriding()

    print("==================================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("==================================================\n")

    inventory = Inventory()
    inventory.load()

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
            inventory.display_all()

        elif option == "2":
            print("\nAdd New Product")
            p_type = input("Product Type (1: Physical, 2: Digital, 3: Standard): ").strip()
            p_id = input("Product ID: ").strip()
            name = input("Product Name: ").strip()
            try:
                price = float(input("Price: "))
                stock = int(input("Stock Quantity: "))
                
                if p_type == "1":
                    weight = float(input("Weight (kg): "))
                    new_item = PhysicalProduct(p_id, name, price, stock, weight)
                elif p_type == "2":
                    size = float(input("Download Size (MB): "))
                    new_item = DigitalProduct(p_id, name, price, stock, size)
                else:
                    new_item = Product(p_id, name, price, stock)
                    
                inventory.add_product(new_item)
            except ValueError:
                print("Invalid numerical input.")

        elif option == "3":
            print("\nUpdate Stock")
            p_id = input("Enter Product ID: ").strip()
            try:
                product = inventory.find_by_id(p_id)
                if product:
                    print("\nProduct Found:")
                    print(f"Name: {product.name}")
                    print(f"Current Stock: {product.stock}\n")
                    new_stock = int(input("New Stock Quantity: "))
                    product.update_stock(new_stock)
                    print("\nStock updated successfully!")
                else:
                    print("Product not found.")
            except ValueError:
                print("Invalid quantity entered.")

        elif option == "4":
            print("\nSearch Product")
            p_id = input("Enter Product ID: ").strip()
            inventory.search_product(p_id)

        elif option == "5":
            print()
            inventory.save()

        elif option == "6":
            print("\nSaving inventory before exit...")
            inventory.save(silent=True)
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break

        else:
            print("Invalid option. Please try again.\n")

        print()


if __name__ == "__main__":
    main()