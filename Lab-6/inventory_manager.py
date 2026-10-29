import json

FILE_NAME = "inventory.json"


class Product:

    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self.__product_id = str(product_id).strip()
        self.__name = str(name).strip()
        self.__price = float(price)
        self.__stock = int(stock)

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def update_stock(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = int(quantity)

    def display_information(self) -> None:
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def to_dict(self) -> dict:
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }

    def __repr__(self) -> str:
        return f"Product('{self.__product_id}', '{self.__name}', {self.__price}, {self.__stock})"


class Inventory:

    def __init__(self):
        self.__products = []

    def add_product(self, product: Product) -> None:
        self.__products.append(product)

    def search_product(self, product_id: str):
        if not product_id:
            return None
        target = str(product_id).strip().lower()
        for product in self.__products:
            if product.get_product_id().lower() == target:
                return product
        return None

    def display_all(self) -> None:
        print("Current Inventory")
        print("-" * 48)
        for product in self.__products:
            product.display_information()
        print("-" * 48)

    def get_products(self) -> list:
        return self.__products

    def __iter__(self):
        return iter(self.__products)

    def __len__(self) -> int:
        return len(self.__products)


def load_inventory() -> Inventory:
    inventory = Inventory()
    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
            print(f"{FILE_NAME} found.")
            print("Inventory loaded successfully.")
            for item in data:
                product_id = item.get("id") or item.get("order_id", "")
                name = item.get("name", "")
                price = float(item.get("price", 0.0))
                stock = int(item.get("stock", 0))
                product = Product(product_id, name, price, stock)
                inventory.add_product(product)
            return inventory
    except FileNotFoundError:
        print(f"{FILE_NAME} not found.")
        return inventory


def save_inventory(inventory: Inventory) -> None:
    data = [product.to_dict() for product in inventory.get_products()]
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def display_menu() -> None:
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("-" * 28)


def add_product(inventory: Inventory) -> None:
    print("Add New Product")
    while True:
        product_id = input("Product ID: ").strip()
        if not product_id:
            print("Product ID cannot be empty.")
            continue
        if inventory.search_product(product_id) is not None:
            print("Product ID already exists. Please enter a different ID.")
            continue
        break

    while True:
        name = input("Product Name: ").strip()
        if not name:
            print("Product Name cannot be empty.")
            continue
        break

    while True:
        try:
            price = round(float(input("Price: ")), 2)
            if price < 0:
                print("Price cannot be negative. Please enter again.")
                continue
            break
        except ValueError:
            print("Invalid input! Please enter a valid number.")

    while True:
        try:
            stock = int(input("Stock Quantity: "))
            if stock < 0:
                print("Stock cannot be negative. Please enter again.")
                continue
            break
        except ValueError:
            print("Invalid input! Please enter a valid number.")

    new_product = Product(product_id, name, price, stock)
    inventory.add_product(new_product)
    print("Product added successfully!")


def update_stock(inventory: Inventory) -> None:
    print("Update Stock")
    product_id = input("Enter Product ID: ").strip()

    found_product = inventory.search_product(product_id)

    if found_product:
        print("Product Found:")
        print(f"Name: {found_product.get_name()}")
        print(f"Current Stock: {found_product.get_stock()}")
        while True:
            try:
                new_stock = int(input("New Stock Quantity: "))
                if new_stock < 0:
                    print("Stock cannot be negative. Please enter again.")
                    continue
                break
            except ValueError:
                print("Invalid input! Please enter a valid number.")
        found_product.update_stock(new_stock)
        print("Stock updated successfully!")
    else:
        print("Product not found.")


def search_product(inventory: Inventory) -> None:
    print("Search Product")
    product_id = input("Enter Product ID: ").strip()

    found_product = inventory.search_product(product_id)

    if found_product:
        print("Product Found")
        print("-" * 48)
        print(f"ID: {found_product.get_product_id()}")
        print(f"Name: {found_product.get_name()}")
        print(f"Price: ${found_product.get_price():.2f}")
        print(f"Stock: {found_product.get_stock()}")
        print("-" * 48)
    else:
        print("Product not found.")


def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()

    while True:
        display_menu()
        choice = input("Enter option: ").strip()

        if choice == "1":
            inventory.display_all()
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
