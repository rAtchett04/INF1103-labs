# Initialise inventory to 0
total_inventory = 0
failed_entries = 0
total_entries = 0
quantity = 0

def get_valid_input(user_input):
    # Check for quit command (case-insensitive)
    if user_input.lower() == "quit":
        return False

    # Handle invalid string inputs
    if not user_input.isdigit():
        print("Error: Invalid input. Please enter a positive whole number.")
        failed_entries += 1
        return True, total_entries, total_inventory, total_tax

    # Convert user input to an integer 
    quantity = int(user_input)

    # Enforce business rules: reject negative numbers
    if quantity < 0:
        print("Error: Stock value entered cannot be negative.")
        failed_entries += 1
        return True, total_entries, total_inventory, total_tax
    else:
        # Update running total
        total_entries += 1
        total_inventory += quantity
        print(f"Added {quantity} units. Current total inventory: {total_inventory}")
        total_tax = total_inventory * 0.10
        print(f"Current delivery tax: ${total_tax}")
        return True, total_entries, total_inventory, total_tax

    # Overstock alert
    if total_inventory > 500:
        print("Overstock limit exceeded (>500 units)! Audit process stopped.")
        return False
            
    

# Run in a continuous loop until the user types quit or triggers an alert
while True:
    user_input = get_valid_input(input("Enter stock quantity (or type 'quit' to exit): ").strip())

# Reporting section after loop ends
print("\n------------------------")
print(f"Total Units Processed: {total_inventory}")
print(f"Total tax for delivery: ${total_tax}")
print(f"Total deliveries processed: {total_entries}")
print(f"Number of Failed/Rejected Entries: {failed_entries}")