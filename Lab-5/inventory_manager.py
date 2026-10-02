import json

FILE_NAME = "inventory.json"
TAX_RATE = 0.1
ID_PREFIX = "P"
FIRST_ORDER_NUMBER = 1

def format_order_id(number):
    return f"{ID_PREFIX}{number:03d}"


def load_inventory():
    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
            return data["orders"]
    except FileNotFoundError:
        return []


def save_inventory(orders):
    total = 0
    for order in orders:
        total = process_delivery(total, order["quantity"])
    data = {
        "Total_Inventory": total,
        "Total_Tax": calculate_tax(total),
        "Current_Inventory": orders
    }
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def display_current_orders(orders):
    print("Current Inventory:")
    if len(orders) == 0:
        print(" (No previous orders found)")
    else:
        for order in orders:
            print(f"{order['order_id']}, {order['item']}, {order['quantity']}")
    print("-" * 30)


def get_product_name():
    return input("Enter Product Name (or 'quit' to exit): ").strip()


def get_valid_input():
    user_input = input("Enter Quantity: ").strip()
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
    return amount * TAX_RATE


def generate_report(total_transactions, total_units, failed_attempts):
    print("\n=== Audit Report ===")
    print(f"Total Transactions Recorded: {total_transactions}")
    print(f"Total Units Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")

def has_digits(name):
    for char in name:
        if char.isdigit():
            return True
    return False


products = load_inventory()
display_current_orders(products)

total_inventory = 0
for order in products:
    total_inventory = process_delivery(total_inventory, order["quantity"])

order_history = []
failed_attempts = 0

while True:
    product_name = get_product_name()

    if product_name.lower() == "quit":
        break

    if product_name == "":
        failed_attempts += 1
        print("Error: Product name cannot be empty!\n")
        continue

    if has_digits(product_name):
        failed_attempts += 1
        print("Error: Product name cannot contain numbers!\n")
        continue

    quantity = get_valid_input()
    if quantity is None:
        failed_attempts += 1
        print("Error: Invalid entry! Please enter a whole number greater than 0.\n")
        continue

    if len(products) > 0:
        new_id = products[-1]["order_id"] + 1
    else:
        new_id = FIRST_ORDER_NUMBER

    new_order = {"order_id": new_id, "item": product_name, "quantity": quantity}
    products.append(new_order)
    order_history.append(quantity)

    total_inventory = process_delivery(total_inventory, quantity)
    tax = calculate_tax(quantity)

    print("\nNew Order Added:")
    print(f"{format_order_id(new_order['order_id'])}, {new_order['item']}, {new_order['quantity']}")
    print(f"Tax: ${tax:.2f} | Total Inventory: {total_inventory}\n")

save_inventory(products)
print("Order successfully saved to inventory.json")

generate_report(len(order_history), sum(order_history), failed_attempts)
