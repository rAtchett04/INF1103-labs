# Initialise inventory to 0
total_inventory = 0
failed_entries = 0

# Run in a continuous loop until the user types quit or triggers an alert
while True:
    user_input = input("Enter stock quantity (or type 'quit' to exit): ").strip()

    # Check for quit command (case-insensitive)
    if user_input.lower() == "quit":
        break

    # Handle invalid string inputs
    if not user_input.isdigit():
        print("Error: Invalid input. Please enter a positive whole number.")
        failed_entries += 1
        continue

    # Convert user input to an integer 
    quantity = int(user_input)

    # Enforce business rules: reject negative numbers
    if quantity < 0:
        print("Error: Stock value entered cannot be negative.")
        failed_entries += 1
    else:
        # Update running total
        total_inventory += quantity
        print(f"Added {quantity} units. Current total inventory: {total_inventory}")

        # Overstock alert
        if total_inventory > 500:
            print("Overstock limit exceeded (>500 units)! Audit process stopped.")
            break

# Reporting section after loop ends
print("\n------------------------")
print(f"Total Units Processed: {total_inventory}")
print(f"Number of Failed/Rejected Entries: {failed_entries}")