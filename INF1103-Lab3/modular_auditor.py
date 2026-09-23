# auditor.py

# function for user input validation
def get_valid_input():
    """
    Prompts the user, handles input validation, and returns:
    - 'quit' if the user wants to exit
    - an integer for valid stock entries
    - None for invalid entries (after printing an error)
    """
    user_input = input("Enter stock quantity (or type 'quit' to exit): ").strip()
    
    if user_input.lower() == "quit":
        return "quit"
    
    if not user_input.isdigit():
        print("Error: Invalid input. Please enter a positive whole number.")
        return None
    
    quantity = int(user_input)
    
    if quantity < 0:
        print("Error: Stock value entered cannot be negative.")
        return None
        
    return quantity


def process_delivery(current_total, new_value):
    # Calculates and returns the updated total inventory
    return current_total + new_value


def calculate_tax(amount):
    # Calculates and returns 10% tax on a specific delivery amount
    return amount * 0.10


def generate_report(total_units, deliveries_count, failed_attempts):
    # Prints the final summary report
    print("\n------------------------")
    print(f"Total Deliveries Processed: {deliveries_count}")
    print(f"Total Units Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


# Initialize inventory and tracking variables to 0
total_inventory = 0
failed_entries = 0
deliveries_processed = 0

# Continuous loop with functions called 
while True:
    # Input validation -> get_valid_input()
    result = get_valid_input()

    if result == "quit":
        break

    if result is None:
        failed_entries += 1
        continue

    # Handle valid delivery values
    quantity = result
    
    # Calculate tax for user stock input
    delivery_tax = calculate_tax(quantity)
    
    # Process the new inventory total
    total_inventory = process_delivery(total_inventory, quantity)
    deliveries_processed += 1

    print(f"Added {quantity} units (Tax: ${delivery_tax:.2f}). Current total: {total_inventory}")

    # Overstock alert check
    if total_inventory > 500:
        print("Overstock limit exceeded (>500 units)! Audit process stopped.")
        break

# Final report output -> generate_report()
generate_report(total_inventory, deliveries_processed, failed_entries)