# Initial product list represented as a list of dictionaries
products = [
    {"name": "Laptop", "price": 800, "stock": 50},
    {"name": "Mouse", "price": 20, "stock": 100},
    {"name": "Keyboard", "price": 50, "stock": 80},
]

# 1. Display all product names from the product list
print("Product Names:")
for product in products:
    print(product["name"])

# 2. Add a new product to the existing product list
new_product = {"name": "Headphones", "price": 40, "stock": 40}
products.append(new_product)

print("\nAfter Adding New Product:")
for product in products:
    print(product["name"])

# 3. Update the stock quantity of an existing product after a sale
# Example: Mouse stock updated from 100 to 95 after selling 5 units
for product in products:
    if product["name"] == "Mouse":
        product["stock"] -= 5  # 100 - 5 = 95

print("\nAfter Updating Mouse Stock:")
for product in products:
    print(f"{product['name']} - Stock: {product['stock']}")

# 4. Identify products priced above $30 and display their names
print("\nProducts Priced Above $30:")
for product in products:
    if product["price"] > 30:
        print(product["name"])