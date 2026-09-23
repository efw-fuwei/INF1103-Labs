def get_valid_input():
    user_input = input("Enter stock quantity (or type 'quit' to stop): ").strip()
    if user_input.lower() == 'quit':
        return 'quit'
    try:
        int_value = int(user_input)
        if int_value > 0:
            return int_value
        else:
            return None
    except ValueError:
        return None

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount * 0.1

def generate_report(total_units, failed_attempts):
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Total Failed Entries: {failed_attempts}")


inventory = 0
deliveries_processed = 0
failed_attempts = 0

while True:
    entry = get_valid_input()
    if entry == 'quit':
        break
    elif entry is None:
        failed_attempts += 1
        print("Error: Invalid entry! Please enter a whole number or 'quit' to exit.")
    else:
        inventory = process_delivery(inventory, entry)
        deliveries_processed += 1
        tax = calculate_tax(entry)
        print(f"Added: {entry} units\nTax: {tax:.2f}\nNew Total: {inventory}")

generate_report(deliveries_processed, failed_attempts)
