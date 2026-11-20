import csv
import json
import re
from abc import ABC, abstractmethod
from collections.abc import Iterator

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
        price_val = float(price)
        stock_val = int(stock)
        if price_val <= 0:
            raise ValueError("Price must be greater than zero.")
        if stock_val < 0:
            raise ValueError("Stock cannot be negative.")
        self.__product_id: str = str(product_id).strip()
        self.__name: str = str(name).strip()
        self.__price: float = price_val
        self.__stock: int = stock_val
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
        weight_val = float(weight)
        if weight_val <= 0:
            raise ValueError("Weight must be greater than zero.")
        self.__weight: float = weight_val

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
        size_val = float(download_size)
        if size_val <= 0:
            raise ValueError("Download size must be greater than zero.")
        self.__download_size: float = size_val

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


class ProductFactory:

    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        weight: float = 1.0,
        download_size: float = 100.0
    ) -> Product:
        ptype = str(product_type).strip().lower()
        if ptype == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier, weight)
        elif ptype == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, supplier, download_size)
        else:
            raise ValueError(f"Unknown product type: {product_type}")


class DiscountStrategy(ABC):

    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):

    def apply(self, total: float) -> float:
        return round(total, 2)


class PercentageDiscount(DiscountStrategy):

    def __init__(self, percentage: float) -> None:
        pct = float(percentage)
        if pct < 0 or pct > 100:
            raise ValueError("Discount percentage must be between 0 and 100.")
        self.__percentage: float = pct

    def get_percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return round(total * (1 - self.__percentage / 100), 2)


class BulkDiscount(DiscountStrategy):

    def __init__(self, threshold: float, amount: float) -> None:
        threshold_val = float(threshold)
        amount_val = float(amount)
        if threshold_val <= 0:
            raise ValueError("Threshold must be greater than zero.")
        if amount_val < 0:
            raise ValueError("Discount amount cannot be negative.")
        self.__threshold: float = threshold_val
        self.__amount: float = amount_val

    def get_threshold(self) -> float:
        return self.__threshold

    def get_amount(self) -> float:
        return self.__amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return round(max(0.0, total - self.__amount), 2)
        return round(total, 2)


class StudentDiscount(DiscountStrategy):

    def __init__(self, percentage: float = 5.0) -> None:
        pct = float(percentage)
        if pct < 0 or pct > 100:
            raise ValueError("Student discount percentage must be between 0 and 100.")
        self.__percentage: float = pct

    def get_percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return round(total * (1 - self.__percentage / 100), 2)


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

    def __iter__(self) -> Iterator[Product]:
        return iter(self.__products)

    def __len__(self) -> int:
        return len(self.__products)


class OrderLine:

    def __init__(self, product: Product, quantity: int) -> None:
        qty = int(quantity)
        if qty <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.__product: Product = product
        self.__quantity: int = qty

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return round(self.__product.get_price() * self.__quantity, 2)

    def display_information(self) -> None:
        print(f"{self.__product.get_name()} (ID: {self.__product.get_product_id()}) x {self.__quantity} = ${self.calculate_subtotal():.2f}")


class Order:

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.__order_id: str = str(order_id).strip()
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def get_order_id(self) -> str:
        return self.__order_id

    def get_order_lines(self) -> list[OrderLine]:
        return self.__order_lines

    def get_discount(self) -> DiscountStrategy:
        return self.__discount

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
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
        total = sum(line.calculate_subtotal() for line in self.__order_lines)
        return self.__discount.apply(total)

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


def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    loaded = 0
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if len(row) < 5:
                    print(f"Skipping invalid row: {row}")
                    continue
                product_type, product_id, name, price_str, stock_str = row[:5]
                try:
                    price = float(price_str)
                    stock_quantity = int(stock_str)
                    product = ProductFactory.create(
                        product_type, product_id, name, price, stock_quantity, supplier
                    )
                    inventory.add_product(product)
                    loaded += 1
                except ValueError as err:
                    print(f"Skipping invalid row {row}: {err}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


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

                try:
                    weight = float(item.get("weight", 1.0))
                    download_size = float(item.get("download_size", 100.0))
                    product = ProductFactory.create(
                        product_type, product_id, name, price, stock, supplier,
                        weight=weight, download_size=download_size
                    )
                    inventory.add_product(product)
                except ValueError as err:
                    print(f"Skipping invalid product {product_id}: {err}")
            return inventory
    except FileNotFoundError:
        print(f"{FILE_NAME} not found.")
        return inventory
    except json.JSONDecodeError:
        print(f"{FILE_NAME} is not valid JSON.")
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
    print("7. Load Products from CSV")
    print("8. Save Inventory")
    print("9. Exit")
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
        product_choice = input("Product Type (1 for Physical, 2 for Digital): ").strip()
        if product_choice in ["1", "2"]:
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

    price = round(get_positive_float("Price: "), 2)

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
            if not sup_email:
                print("Supplier Email cannot be empty.")
                continue
            if not re.match(r"^[^@\s]+@([^@\s.]+\.)+[^@\s.]+$", sup_email):
                print("Invalid email format. Please enter a valid email (e.g. name@example.com).")
                continue
            break
        supplier = Supplier(supplier_id, sup_name, sup_email)

    if product_choice == "1":
        weight = get_positive_float("Weight (kg): ")
        new_product = ProductFactory.create("physical", product_id, name, price, stock, supplier, weight=weight)
    else:
        download_size = get_positive_float("Download Size (MB): ")
        new_product = ProductFactory.create("digital", product_id, name, price, stock, supplier, download_size=download_size)

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
                found_product.update_stock(new_stock)
                break
            except ValueError as err:
                print(err)
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


def choose_discount_strategy() -> DiscountStrategy:
    print("Select Discount Strategy:")
    print("1. No Discount")
    print("2. Percentage Discount (10%)")
    print("3. Bulk Discount ($20 off $200+)")
    print("4. Student Discount (5%)")
    while True:
        choice = input("Discount option (1-4): ").strip()
        if choice == "1":
            return NoDiscount()
        elif choice == "2":
            return PercentageDiscount(10)
        elif choice == "3":
            return BulkDiscount(200, 20)
        elif choice == "4":
            return StudentDiscount()
        print("Invalid option. Please choose 1 to 4.")


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
                order.add_order_line(product, quantity)
                break
            except ValueError as err:
                print(err)
        print("Item added to order.")

    if len(order.get_order_lines()) == 0:
        print("No items added to order.")
    else:
        discount = choose_discount_strategy()
        order.set_discount(discount)
        order.display_order()


def load_csv_menu(inventory: Inventory) -> None:
    path = input("Enter CSV file path (default: products.csv): ").strip()
    if not path:
        path = "products.csv"
    supplier = find_existing_supplier(inventory, "S001")
    if supplier is None:
        supplier = Supplier("S001", "TechSupply Co", "orders@techsupply.com")
    load_products(path, inventory, supplier)


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
            load_csv_menu(inventory)
            print()
        elif choice == "8":
            print("Saving inventory...")
            save_inventory(inventory)
            print(f"Inventory saved successfully to {FILE_NAME}.")
            print()
        elif choice == "9":
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
