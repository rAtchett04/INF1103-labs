import csv
from inventory import Inventory
from product import Product
from productfactory import ProductFactory
from supplier import Supplier


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    # Reads products from a CSV file using ProductFactory and adds them to Inventory
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded: int = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header row
            for row in reader:
                if not row:
                    continue
                try:
                    product_type, product_id, name, price_str, stock_str = row
                    product: Product = ProductFactory.create(
                        product_type=product_type,
                        product_id=product_id.strip(),
                        name=name.strip(),
                        price=float(price_str),
                        stock_quantity=int(stock_str),
                        supplier=supplier
                    )
                    if inventory.add_product(product):
                        loaded += 1
                except ValueError as e:
                    print(f"Skipping invalid row {row}: {e}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


def show_product_details(product: Product) -> None:
    product.display_information()
    print(f"Fulfilment Info: {product.get_fulfilment_info()}")


def get_user_option() -> str:
    try:
        return input("Enter option: ").strip()
    except EOFError:
        print("\nEOF detected. Exiting program gracefully...")
        return "7"


def main() -> None:
    print("==================================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("==================================================\n")

    inventory: Inventory = Inventory()
    default_supplier: Supplier = Supplier("SUP001", "Global Tech Wholesale", "contact@globaltech.com")
    
    # Load initial products from CSV
    load_products("products.csv", inventory, default_supplier)
    print()

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
            while True:
                p_type: str = input("Select Product Type (1 or 2): ").strip()
                if p_type in ["1", "2"]:
                    break
                print("Invalid choice! Please enter 1 or 2.")

            p_id: str = input("Product ID: ").strip()
            name: str = input("Product Name: ").strip()
            while True:
                try:
                    price: float = float(input("Price: "))
                    stock: int = int(input("Stock Quantity: "))
                    sup_id: str = input("Supplier ID: ").strip()
                    sup_name: str = input("Supplier Name: ").strip()
                    sup_email: str = input("Supplier Contact Email: ").strip()
                    supplier_obj: Supplier = Supplier(sup_id, sup_name, sup_email)

                    if p_type == "1":
                        weight: float = float(input("Weight (kg): "))
                        new_item = ProductFactory.create("physical", p_id, name, price, stock, supplier=supplier_obj, weight=weight)
                    else:
                        download_size: float = float(input("Download Size (MB): "))
                        new_item = ProductFactory.create("digital", p_id, name, price, stock, supplier=supplier_obj, download_size=download_size)

                    inventory.add_product(new_item)
                    break
                except ValueError as e:
                    print(f"Invalid input ({e}). Please try again.")

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
            except ValueError as e:
                print(f"Invalid quantity entered: {e}")

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