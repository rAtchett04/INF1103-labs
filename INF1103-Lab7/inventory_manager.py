from inventory import Inventory
from product import PhysicalProduct, DigitalProduct, CanBeShipped


def test_can_be_shipped_interface():
    """
    4.2 Test implementation:
    Tests calculate_shipping_cost() with physical products of different weights,
    and verifies interface adherence.
    """
    print("==================================================")
    print("--- 4.2 Testing CanBeShipped Interface ---")
    print("==================================================")

    light_item = PhysicalProduct("P010", "Computer Mouse", 20.00, 50, weight=0.2)
    medium_item = PhysicalProduct("P011", "Mechanical Keyboard", 80.00, 30, weight=1.2)
    heavy_item = PhysicalProduct("P012", "Desktop Tower", 1200.00, 10, weight=14.5)
    digital_item = DigitalProduct("D010", "Video Editor", 99.99, 100, download_size=1500.0)

    shippable_items = [light_item, medium_item, heavy_item]

    for item in shippable_items:
        print(f"\nItem: {item.name} (Weight: {item.weight} kg)")
        print(f"Is CanBeShipped Instance? {isinstance(item, CanBeShipped)}")
        print(f"Calculated Shipping Cost: ${item.calculate_shipping_cost():.2f}")

    print(f"\nDigital Item: {digital_item.name}")
    print(f"Is CanBeShipped Instance? {isinstance(digital_item, CanBeShipped)}")

    print("--------------------------------------------------\n")


def get_user_option() -> str:
    """Helper guard against EOFError in non-interactive environments."""
    try:
        return input("Enter option: ").strip()
    except EOFError:
        print("\nEOF detected. Exiting program gracefully...")
        return "6"


def main():
    # Run interface test suite first
    test_can_be_shipped_interface()

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
            p_type = input("Product Type (1: Physical, 2: Digital): ").strip()
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
                    print("Invalid product type chosen.")
                    continue

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