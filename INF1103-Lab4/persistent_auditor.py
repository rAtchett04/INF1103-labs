# persistent_auditor.py
import os

FILENAME = "inventory.txt"

# Function to read previously saved inventory total and transaction history from disk
def load_inventory():
    if not os.path.exists(FILENAME):
        return 0, []

    try:
        with open(FILENAME, "r") as file:
            lines = file.readlines()
            
            # Read saved running total
            total_inventory = int(lines[0].strip()) if len(lines) > 0 else 0
            
            # Read saved transaction history
            valid_transactions = []
            if len(lines) > 1 and lines[1].strip():
                valid_transactions = [int(val) for val in lines[1].strip().split(",")]
                
            print(f"Loaded existing inventory: {total_inventory} units across {len(valid_transactions)} past transactions.")
            return total_inventory, valid_transactions
            
    except (ValueError, IOError):
        print("Warning: Inventory file corrupted or unreadable. Starting fresh.")
        return 0, []

# Function to write the final total inventory and transaction history list to inventory.txt
def save_inventory(total_units, history):
    try:
        with open(FILENAME, "w") as file:
            # Running total
            file.write(f"{total_units}\n")
            # Comma-separated list of transactions
            history_str = ",".join(map(str, history))
            file.write(f"{history_str}\n")
        print(f"Inventory state successfully saved to {FILENAME}.")
    except IOError as e:
        print(f"Error saving inventory file: {e}")

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

# Function to calculate and return the updated total inventory
def process_delivery(current_total, new_value):
    return current_total + new_value

# Function to calculate and return 10% tax on a specific delivery amount.
def calculate_tax(amount):
    return amount * 0.10

# Function to print the final summary report
def generate_report(total_units, deliveries_count, failed_attempts, history):
    print("\n------------------------")
    print(f"Total Deliveries Processed (This Session): {deliveries_count}")
    print(f"Total Units Processed (Overall): {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")
    print(f"Transaction History: {history}")


def main():
    # Persistence - Load saved data at startup
    total_inventory, valid_transactions = load_inventory()
    
    # Session counters
    failed_entries = 0
    deliveries_processed = 0

    # Continuous loop
    while True:
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
        
        # History tracking and session counters
        valid_transactions.append(quantity)
        deliveries_processed += 1

        print(f"Added {quantity} units (Tax: ${delivery_tax:.2f}). Current total: {total_inventory}")

        # Overstock alert check
        if total_inventory > 500:
            print("Overstock limit exceeded (>500 units)! Audit process stopped.")
            break

    # Save inventory total and transaction history list to inventory.txt
    save_inventory(total_inventory, valid_transactions)

    # Final report output
    generate_report(total_inventory, deliveries_processed, failed_entries, valid_transactions)


if __name__ == "__main__":
    main()