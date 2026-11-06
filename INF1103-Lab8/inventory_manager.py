from inventory import Inventory
from product import PhysicalProduct, DigitalProduct
from supplier import Supplier


def test_supplier_association():
    print("==================================================")
    print("--- 2.2 Testing Supplier-Product Association ---")
    print("==================================================")

    # Create a Supplier object
    test_supplier = Supplier("SUP100", "Acme Supplies", "support@acme.com")

    # Create PhysicalProduct and DigitalProduct associated with the Supplier
    phys_item = PhysicalProduct("P100", "Mechanical Keyboard", 89.99, 20, weight=1.1, supplier=test_supplier)
    digi_item = DigitalProduct("D100", "Antivirus Key", 29.99, 50, download_size=150.0, supplier=test_supplier)

    # Display supplier information through each Product
    print("\n[Physical Product Supplier Info via Product]:")
    phys_item.display_information()

    print("\n[Digital Product Supplier Info via Product]:")
    digi_item.display_information()

    # Predict & Test Independence (del supplier)
    print("\n--- Testing Independent Existence (Deleting local supplier variable) ---")
    del test_supplier  # Deletes local variable reference

    # Ensure products still hold reference to Supplier object in memory
    print("\nAccessing Supplier after local 'del test_supplier':")
    print(f"Physical Product's Supplier Name: {phys_item.supplier.name}")
    print(f"Digital Product's Supplier Email: {digi_item.supplier.contact_email}")
    print("Association test passed successfully!")
    print("--------------------------------------------------\n")


def get_user_option() -> str:
    try:
        return input("Enter option: ").strip()
    except EOFError:
        print("\nEOF detected. Exiting program gracefully...")
        return "6"


def main():
    # Association test first
    test_supplier_association()

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