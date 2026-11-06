from inventory import Inventory
from product import Product, PhysicalProduct, DigitalProduct
from supplier import Supplier


# Test substitutability helper function
def show_product_details(product: Product) -> None:
    # Accepts a Product object and uses behaviour that every Product supports
    product.display_information()
    print(product.get_fulfilment_info())


def test_liskov_substitution() -> None:
    # Test implementation verifying LSP
    print("==================================================")
    print("--- 6.2 Testing Liskov Substitution Principle (LSP) ---")
    print("==================================================")

    sup: Supplier = Supplier("SUP500", "LSP Test Supplier", "lsp@test.com")
    phys_item: PhysicalProduct = PhysicalProduct("P501", "Mechanical Keyboard", 120.00, 25, weight=1.1, supplier=sup)
    digi_item: DigitalProduct = DigitalProduct("D501", "Cloud Antivirus", 39.99, 100, download_size=320.0, supplier=sup)

    print("\n--- 1. Testing show_product_details() with PhysicalProduct ---")
    show_product_details(phys_item)

    print("\n--- 2. Testing show_product_details() with DigitalProduct ---")
    show_product_details(digi_item)

    # Test that both product types can be added to an Inventory and used by normal operations
    test_inventory: Inventory = Inventory("lsp_test.json")
    test_inventory.add_product(phys_item)
    test_inventory.add_product(digi_item)

    print("\n--- 3. Testing Inventory.display_all_products() (LSP Polymorphism) ---")
    test_inventory.display_all_products()
    print("LSP Test passed successfully!")
    print("--------------------------------------------------\n")


def get_user_option() -> str:
    try:
        return input("Enter option: ").strip()
    except EOFError:
        print("\nEOF detected. Exiting program gracefully...")
        return "7"


def main() -> None:
    # Run LSP Test
    test_liskov_substitution()

    print("==================================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("==================================================\n")

    inventory: Inventory = Inventory()
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

        option: str = get_user_option()

        if option == "1":
            inventory.display_all()

        elif option == "2":
            print("\nAdd New Product")
            print("1. Physical Product")
            print("2. Digital Product")
            p_type: str = input("Select Product Type (1 or 2): ").strip()

            if p_type not in ["1", "2"]:
                print("Invalid choice! Please select 1 for Physical or 2 for Digital.")
                print()
                continue

            p_id: str = input("Product ID: ").strip()
            name: str = input("Product Name: ").strip()
            try:
                price: float = float(input("Price: "))
                stock: int = int(input("Stock Quantity: "))
                
                sup_id: str = input("Supplier ID: ").strip()
                sup_name: str = input("Supplier Name: ").strip()
                sup_email: str = input("Supplier Contact Email: ").strip()
                supplier_obj: Supplier = Supplier(sup_id, sup_name, sup_email)

                new_item: Product
                if p_type == "1":
                    weight: float = float(input("Weight (kg): "))
                    new_item = PhysicalProduct(p_id, name, price, stock, weight, supplier=supplier_obj)
                else:
                    download_size: float = float(input("Download Size (MB): "))
                    new_item = DigitalProduct(p_id, name, price, stock, download_size, supplier=supplier_obj)

                inventory.add_product(new_item)
            except ValueError:
                print("Invalid numerical input. Product addition canceled.")

        elif option == "3":
            print("\nRemove Product")
            p_id: str = input("Enter Product ID to remove: ").strip()
            inventory.remove_product(p_id)

        elif option == "4":
            print("\nUpdate Stock")
            p_id: str = input("Enter Product ID: ").strip()
            try:
                product: Product | None = inventory.find_product(p_id)
                if product:
                    print("\nProduct Found:")
                    print(f"Name: {product.name}")
                    print(f"Current Stock: {product.stock}\n")
                    new_stock: int = int(input("New Stock Quantity: "))
                    product.update_stock(new_stock)
                    print("\nStock updated successfully!")
                else:
                    print("Product not found.")
            except ValueError:
                print("Invalid quantity entered.")

        elif option == "5":
            print("\nSearch Product")
            p_id: str = input("Enter Product ID: ").strip()
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