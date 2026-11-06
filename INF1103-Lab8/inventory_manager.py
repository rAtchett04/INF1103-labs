# inventory_manager.py
from inventory import Inventory
from product import PhysicalProduct, DigitalProduct
from supplier import Supplier
from order import Order, OrderLine


def test_composition():
    # Test implementation
    print("==================================================")
    print("--- Testing Composition (Order & OrderLine) ---")
    print("==================================================")

    # Create a Supplier and Products
    sup = Supplier("SUP300", "Logitech Direct", "b2b@logitech.com")
    prod1 = PhysicalProduct("P301", "Prof Jerry's Coffee", 30.00, 100, weight=0.15, supplier=sup)
    prod2 = PhysicalProduct("P302", "SIT Table", 75.00, 50, weight=0.3, supplier=sup)
    prod3 = DigitalProduct("D301", "INF1103 Software", 49.99, 200, download_size=50.0, supplier=sup)

    # Create Order 1 and add multiple products
    order1 = Order("ORD-1001")
    order1.add_order_line(prod1, 2) 
    order1.add_order_line(prod2, 1)  
    order1.add_order_line(prod3, 3)  

    # Display Order 1 summary and calculate total
    order1.display_order_summary()

    # Create Order 2
    order2 = Order("ORD-1002")
    order2.add_order_line(prod1, 5)  

    print("--- Comparing OrderLine objects vs Product references across Orders ---")
    line_from_order1 = order1.order_lines[0]
    line_from_order2 = order2.order_lines[0]

    # Verification of OrderLine composition independence
    print(f"Order 1 Line Object ID: {id(line_from_order1)}")
    print(f"Order 2 Line Object ID: {id(line_from_order2)}")
    print(f"Are OrderLines the same object? {line_from_order1 is line_from_order2}")

    # Verification of shared Product reference
    print(f"Order 1 Line Product Reference ID: {id(line_from_order1.product)}")
    print(f"Order 2 Line Product Reference ID: {id(line_from_order2.product)}")
    print(f"Do both OrderLines reference the exact same Product instance? {line_from_order1.product is line_from_order2.product}")

    # Remove an order line through an Order method
    print("\n--- Removing Line Item from Order 1 ---")
    order1.remove_order_line("P302")
    order1.display_order_summary()

    # Verify Product still exists after Order modification/deletion
    print("--- Verifying Product Existence After Order Line Removal ---")
    print(f"Product '{prod2.name}' still exists in system memory (Price: ${prod2.price:.2f}).")
    print("Composition test passed successfully!")
    print("--------------------------------------------------\n")


def get_user_option() -> str:
    # Helper guard against EOFError in non-interactive environments
    try:
        return input("Enter option: ").strip()
    except EOFError:
        print("\nEOF detected. Exiting program gracefully...")
        return "7"


def main():
    # Execute Composition test first
    test_composition()

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