#####
import json

FILE_NAME = "inventory.json"


def load_inventory():
    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
            print(f"{FILE_NAME} found.")
            print("Inventory loaded successfully.")
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return data.get("Current_Inventory", data.get("inventory", []))
            return []
    except FileNotFoundError:
        print(f"{FILE_NAME} not found.")
        return []


def save_inventory(inventory):
    with open(FILE_NAME, "w") as file:
        json.dump(inventory, file, indent=4)


def display_all(inventory):
    print("Current Inventory")
    print("-" * 48)
    for item in inventory:
        print(f"ID: {item['id']} | Name: {item['name']} | Price: ${float(item['price']):.2f} | Stock: {item['stock']}")
    print("-" * 48)


def add_product(inventory):
    print("Add New Product")
    product_id = input("Product ID: ").strip()
    name = input("Product Name: ").strip()
    price = float(input("Price: ").strip().replace("$", ""))
    stock = int(input("Stock Quantity: ").strip())

    new_product = {
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock
    }
    inventory.append(new_product)
    print("Product added successfully!")


def update_stock(inventory):
    print("Update Stock")
    product_id = input("Enter Product ID: ").strip()

    found_product = None
    for item in inventory:
        if item["id"].lower() == product_id.lower():
            found_product = item
            break

    if found_product:
        print("Product Found:")
        print(f"Name: {found_product['name']}")
        print(f"Current Stock: {found_product['stock']}")
        new_stock = int(input("New Stock Quantity: ").strip())
        found_product["stock"] = new_stock
        print("Stock updated successfully!")
    else:
        print("Product not found.")


def search_product(inventory):
    print("Search Product")
    product_id = input("Enter Product ID: ").strip()

    found_product = None
    for item in inventory:
        if item["id"].lower() == product_id.lower():
            found_product = item
            break

    if found_product:
        print("Product Found")
        print("-" * 48)
        print(f"ID: {found_product['id']}")
        print(f"Name: {found_product['name']}")
        print(f"Price: ${float(found_product['price']):.2f}")
        print(f"Stock: {found_product['stock']}")
        print("-" * 48)
    else:
        print("Product not found.")


def display_menu():
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("-" * 28)


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()
    display_menu()

    while True:
        choice = input("Enter option: ").strip()

        if choice == "1":
            display_all(inventory)
            print()
        elif choice == "2":
            add_product(inventory)
            print()
        elif choice == "3":
            update_stock(inventory)
            print()
        elif choice == "4":
            search_product(inventory)
            print()
        elif choice == "5":
            print("Saving inventory...")
            save_inventory(inventory)
            print(f"Inventory saved successfully to {FILE_NAME}.")
            print()
        elif choice == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please try again.")
            print()


if __name__ == "__main__":
    main()
