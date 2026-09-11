inventory = 0
failed_entries = 0

while True:
    user_input = input("Enter stock quantity (or type 'quit' to stop): ").strip()

    if user_input.lower() == 'quit':
        break
    elif user_input.isdigit():
        stock = int(user_input)
        inventory += stock
        print(f"Current Inventory: {inventory}")
        if inventory > 500:
            failed_entries += 1
            print("Warning: Inventory exceeds 500 units!")
            break
    else:
        failed_entries += 1
        print("Error: Invalid entry! Please enter a positive number or 'quit' to exit.")
        continue

print(f"Final Inventory Count: {inventory}")
print(f"Total Failed Entries: {failed_entries}")