import json
from abc import ABC, abstractmethod

FILE_NAME = "inventory.json"


class Supplier:

    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        self.__supplier_id: str = str(supplier_id).strip()
        self.__name: str = str(name).strip()
        self.__contact_email: str = str(contact_email).strip()

    def get_supplier_id(self) -> str:
        return self.__supplier_id

    def get_name(self) -> str:
        return self.__name

    def get_contact_email(self) -> str:
        return self.__contact_email

    def display_information(self) -> None:
        print(f"Supplier ID: {self.__supplier_id} | Name: {self.__name} | Email: {self.__contact_email}")

    def to_dict(self) -> dict[str, str]:
        return {
            "supplier_id": self.__supplier_id,
            "name": self.__name,
            "contact_email": self.__contact_email
        }


class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass


class Product(ABC):

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier) -> None:
        self.__product_id: str = str(product_id).strip()
        self.__name: str = str(name).strip()
        self.__price: float = float(price)
        self.__stock: int = int(stock)
        self.__supplier: Supplier = supplier

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = int(quantity)

    def display_information(self) -> None:
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock} | Supplier: {self.__supplier.get_name()}", end="")

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict[str, object]:
        pass


class PhysicalProduct(Product, CanBeShipped):

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = float(weight)

    def get_weight(self) -> float:
        return self.__weight

    def calculate_shipping_cost(self) -> float:
        return round(self.__weight * 5.0, 2)

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping."

    def display_information(self) -> None:
        super().display_information()
        print(f" | Weight: {self.__weight}kg")

    def to_dict(self) -> dict[str, object]:
        return {
            "type": "physical",
            "id": self.get_product_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "stock": self.get_stock(),
            "supplier": self.get_supplier().to_dict(),
            "weight": self.__weight
        }


class DigitalProduct(Product):

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = float(download_size)

    def get_download_size(self) -> float:
        return self.__download_size

    def get_fulfilment_info(self) -> str:
        return "Delivered digitally."

    def display_information(self) -> None:
        super().display_information()
        print(f" | Download Size: {self.__download_size}MB")

    def to_dict(self) -> dict[str, object]:
        return {
            "type": "digital",
            "id": self.get_product_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "stock": self.get_stock(),
            "supplier": self.get_supplier().to_dict(),
            "download_size": self.__download_size
        }


class Inventory:

    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.__products.append(product)

    def remove_product(self, product_id: str) -> bool:
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
            return True
        return False

    def find_product(self, product_id: str) -> Product | None:
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

    def get_products(self) -> list[Product]:
        return self.__products

    def __iter__(self):
        return iter(self.__products)

    def __len__(self) -> int:
        return len(self.__products)


class OrderLine:

    def __init__(self, product: Product, quantity: int) -> None:
        self.__product: Product = product
        self.__quantity: int = int(quantity)

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return round(self.__product.get_price() * self.__quantity, 2)

    def display_information(self) -> None:
        print(f"{self.__product.get_name()} (ID: {self.__product.get_product_id()}) x {self.__quantity} = ${self.calculate_subtotal():.2f}")


class Order:

    def __init__(self, order_id: str) -> None:
        self.__order_id: str = str(order_id).strip()
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def get_order_lines(self) -> list[OrderLine]:
        return self.__order_lines

    def add_order_line(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        target = str(product_id).strip().lower()
        for line in self.__order_lines:
            if line.get_product().get_product_id().lower() == target:
                self.__order_lines.remove(line)
                return True
        return False

    def calculate_total(self) -> float:
        return round(sum(line.calculate_subtotal() for line in self.__order_lines), 2)

    def display_order(self) -> None:
        print(f"Order ID: {self.__order_id}")
        print("-" * 48)
        for line in self.__order_lines:
            line.display_information()
        print("-" * 48)
        print(f"Order Total: ${self.calculate_total():.2f}")


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


def load_inventory() -> Inventory:
    inventory = Inventory()
    suppliers: dict[str, Supplier] = {}
    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
            print(f"{FILE_NAME} found.")
            print("Inventory loaded successfully.")
            for item in data:
                product_type = str(item.get("type", "physical")).lower()
                product_id = str(item.get("id") or item.get("order_id", ""))
                name = str(item.get("name", ""))
                price = float(item.get("price", 0.0))
                stock = int(item.get("stock", 0))

                sup_data = item.get("supplier", {})
                sup_id = str(sup_data.get("supplier_id", "S001"))
                if sup_id not in suppliers:
                    suppliers[sup_id] = Supplier(
                        sup_id,
                        str(sup_data.get("name", "Default Supplier")),
                        str(sup_data.get("contact_email", "contact@supplier.com"))
                    )
                supplier = suppliers[sup_id]

                if product_type == "digital":
                    download_size = float(item.get("download_size", 0.0))
                    product: Product = DigitalProduct(product_id, name, price, stock, supplier, download_size)
                else:
                    weight = float(item.get("weight", 0.0))
                    product = PhysicalProduct(product_id, name, price, stock, supplier, weight)

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
    print("4. Remove Product")
    print("5. Search Product")
    print("6. Create Order")
    print("7. Save Inventory")
    print("8. Exit")
    print("-" * 28)


def find_existing_supplier(inventory: Inventory, supplier_id: str) -> Supplier | None:
    target = supplier_id.strip().lower()
    for product in inventory.get_products():
        if product.get_supplier().get_supplier_id().lower() == target:
            return product.get_supplier()
    return None


def add_product(inventory: Inventory) -> None:
    print("Add New Product")
    while True:
        product_type = input("Product Type (1 for Physical, 2 for Digital): ").strip()
        if product_type in ["1", "2"]:
            break
        print("Invalid choice. Please enter 1 or 2.")

    while True:
        product_id = input("Product ID: ").strip()
        if not product_id:
            print("Product ID cannot be empty.")
            continue
        if inventory.find_product(product_id) is not None:
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

    while True:
        supplier_id = input("Supplier ID: ").strip()
        if supplier_id:
            break
        print("Supplier ID cannot be empty.")

    supplier = find_existing_supplier(inventory, supplier_id)
    if supplier is not None:
        print(f"Using existing supplier: {supplier.get_name()}")
    else:
        while True:
            sup_name = input("Supplier Name: ").strip()
            if sup_name:
                break
            print("Supplier Name cannot be empty.")
        while True:
            sup_email = input("Supplier Contact Email: ").strip()
            if sup_email:
                break
            print("Supplier Email cannot be empty.")
        supplier = Supplier(supplier_id, sup_name, sup_email)

    if product_type == "1":
        while True:
            try:
                weight = float(input("Weight (kg): "))
                if weight <= 0:
                    print("Weight must be greater than 0.")
                    continue
                break
            except ValueError:
                print("Invalid input! Please enter a valid number.")
        new_product: Product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
    else:
        while True:
            try:
                download_size = float(input("Download Size (MB): "))
                if download_size <= 0:
                    print("Download size must be greater than 0.")
                    continue
                break
            except ValueError:
                print("Invalid input! Please enter a valid number.")
        new_product = DigitalProduct(product_id, name, price, stock, supplier, download_size)

    inventory.add_product(new_product)
    print("Product added successfully!")


def update_stock(inventory: Inventory) -> None:
    print("Update Stock")
    product_id = input("Enter Product ID: ").strip()

    found_product = inventory.find_product(product_id)

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


def remove_product(inventory: Inventory) -> None:
    print("Remove Product")
    product_id = input("Enter Product ID: ").strip()
    if inventory.remove_product(product_id):
        print("Product removed from inventory.")
    else:
        print("Product not found.")


def search_product(inventory: Inventory) -> None:
    print("Search Product")
    product_id = input("Enter Product ID: ").strip()

    found_product = inventory.find_product(product_id)

    if found_product:
        print("Product Found")
        print("-" * 48)
        show_product_details(found_product)
        if isinstance(found_product, CanBeShipped):
            print(f"Shipping Cost: ${found_product.calculate_shipping_cost():.2f}")
        found_product.get_supplier().display_information()
        print("-" * 48)
    else:
        print("Product not found.")


def create_order(inventory: Inventory) -> None:
    print("Create Order")
    order_id = input("Enter Order ID: ").strip()
    if not order_id:
        print("Order ID cannot be empty.")
        return

    order = Order(order_id)
    while True:
        product_id = input("Enter Product ID to add (or 'done' to finish): ").strip()
        if product_id.lower() == "done":
            break
        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue
        while True:
            try:
                quantity = int(input("Quantity: "))
                if quantity <= 0:
                    print("Quantity must be greater than 0.")
                    continue
                break
            except ValueError:
                print("Invalid input! Please enter a valid number.")
        order.add_order_line(product, quantity)
        print("Item added to order.")

    if len(order.get_order_lines()) == 0:
        print("No items added to order.")
    else:
        order.display_order()


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
            remove_product(inventory)
            print()
        elif choice == "5":
            search_product(inventory)
            print()
        elif choice == "6":
            create_order(inventory)
            print()
        elif choice == "7":
            print("Saving inventory...")
            save_inventory(inventory)
            print(f"Inventory saved successfully to {FILE_NAME}.")
            print()
        elif choice == "8":
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
