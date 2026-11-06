# inventory_manager.py
from inventory import Inventory
from product import PhysicalProduct, DigitalProduct
from supplier import Supplier


def test_aggregation():
    # Test implementation for aggregation:
    print("==================================================")
    print("--- 3.2 Testing Aggregation (Inventory & Product) ---")
    print("==================================================")

    # Create a Supplier and standalone Product objects before creating any Inventory
    supplier = Supplier("SUP200", "Distributor", "sales@iloveSIT.com")
    item_a = PhysicalProduct("P201", "Prof Jerry's Coffee", 350.00, 10, weight=6.5, supplier=supplier)
    item_b = DigitalProduct("D201", "INF1103 Software", 199.99, 50, download_size=850.0, supplier=supplier)

    # Create Inventory A and add products
    inventory_a = Inventory("inventory_a.json")
    inventory_a.add_product(item_a)
    inventory_a.add_product(item_b)

    print("\n--- Inventory A Content ---")
    inventory_a.display_all()

    # Remove item_a from Inventory A
    removed_product = inventory_a.remove_product("P201")

    # Verify item_a still exists independently and can call its methods
    print("\n--- Verifying Product Existence After Removal from Inventory A ---")
    print(f"Removed Product Name: {removed_product.name}")
    print(f"Removed Product Price: ${removed_product.price:.2f}")
    removed_product.display_information()

    # Transfer product to Inventory B
    inventory_b = Inventory("inventory_b.json")
    print("\n--- Adding Removed Product to Inventory B ---")
    inventory_b.add_product(removed_product)

    print("\n--- Inventory B Content ---")
    inventory_b.display_all()
    print("Aggregation test passed successfully!")
    print("--------------------------------------------------\n")


def get_user_option() -> str:
    try:
        return input("Enter option: ").strip()
    except EOFError:
        print("\nEOF detected. Exiting program gracefully...")
        return "7"


def main():
    # Aggregation test first
    test_aggregation()

    print("==================================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("==================================================\n")

    inventory = Inventory()
    inventory.load()

    while True:
        print("--------- MENU ---------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Remove Product")
        print("4. Update Stock")
        print("5. Search Product")
        print("6. Save Inventory")
        print("7. Exit")
        print("------------------------\n")

        option = get_user_option()

        if option == "1":
            inventory.display_all()

        elif option == "2":
            print("\nAdd New Product")
            print("1. Physical Product")
            print("2. Digital Product")
            p_type = input("Select Product Type (1 or 2): ").strip()

            if p_type not in ["1", "2"]:
                print("Invalid choice! Please select 1 for Physical or 2 for Digital.")
                print()
                continue

            p_id = input("Product ID: ").strip()
            name = input("Product Name: ").strip()
            try:
                price = float(input("Price: "))
                stock = int(input("Stock Quantity: "))
                
                # Prompt for supplier info
                sup_id = input("Supplier ID: ").strip()
                sup_name = input("Supplier Name: ").strip()
                sup_email = input("Supplier Contact Email: ").strip()
                supplier_obj = Supplier(sup_id, sup_name, sup_email)

                if p_type == "1":
                    weight = float(input("Weight (kg): "))
                    new_item = PhysicalProduct(p_id, name, price, stock, weight, supplier=supplier_obj)
                else:
                    download_size = float(input("Download Size (MB): "))
                    new_item = DigitalProduct(p_id, name, price, stock, download_size, supplier=supplier_obj)

                inventory.add_product(new_item)
            except ValueError:
                print("Invalid numerical input. Product addition canceled.")

        elif option == "3":
            print("\nRemove Product")
            p_id = input("Enter Product ID to remove: ").strip()
            inventory.remove_product(p_id)

        elif option == "4":
            print("\nUpdate Stock")
            p_id = input("Enter Product ID: ").strip()
            try:
                product = inventory.find_product(p_id)
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

        elif option == "5":
            print("\nSearch Product")
            p_id = input("Enter Product ID: ").strip()
            inventory.search_product(p_id)

        elif option == "6":
            print()
            inventory.save()

        elif option == "7":
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