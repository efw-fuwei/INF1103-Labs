import io
import os
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from inventory_manager import (
    BulkDiscount,
    DigitalProduct,
    Inventory,
    NoDiscount,
    Order,
    OrderLine,
    PercentageDiscount,
    PhysicalProduct,
    Product,
    ProductFactory,
    StudentDiscount,
    Supplier,
    get_positive_float,
    load_products,
)


class TestDiscounts(unittest.TestCase):

    def setUp(self) -> None:
        self.supplier = Supplier("S001", "TechSupply Co", "orders@techsupply.com")
        self.item = ProductFactory.create("physical", "P100", "Monitor", 125.00, 10, self.supplier, weight=3.0)

    def test_no_discount(self) -> None:
        order = Order("ORD-1")
        order.add_order_line(self.item, 2)
        self.assertEqual(order.calculate_total(), 250.00)

    def test_bulk_and_switch(self) -> None:
        order = Order("ORD-2", BulkDiscount(200, 20))
        order.add_order_line(self.item, 2)
        self.assertEqual(order.calculate_total(), 230.00)

        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225.00)

    def test_bulk_below_threshold(self) -> None:
        order = Order("ORD-3", BulkDiscount(300, 20))
        order.add_order_line(self.item, 2)
        self.assertEqual(order.calculate_total(), 250.00)

    def test_student_discount(self) -> None:
        order = Order("ORD-4", StudentDiscount())
        order.add_order_line(self.item, 2)
        self.assertEqual(order.calculate_total(), 237.50)

    def test_shared_strategy(self) -> None:
        shared = PercentageDiscount(10)
        order1 = Order("ORD-5", shared)
        order2 = Order("ORD-6", shared)
        order1.add_order_line(self.item, 2)
        order2.add_order_line(self.item, 1)
        self.assertIs(order1.get_discount(), order2.get_discount())
        self.assertEqual(order1.calculate_total(), 225.00)
        self.assertEqual(order2.calculate_total(), 112.50)


class TestFactory(unittest.TestCase):

    def setUp(self) -> None:
        self.supplier = Supplier("S002", "GadgetHub", "sales@gadgethub.com")

    def test_physical_product(self) -> None:
        product = ProductFactory.create("physical", "P201", "Desk Lamp", 25.00, 10, self.supplier, weight=1.5)
        self.assertIsInstance(product, Product)
        self.assertIsInstance(product, PhysicalProduct)

    def test_digital_product(self) -> None:
        product = ProductFactory.create("digital", "D201", "Photo Editor", 49.90, 100, self.supplier, download_size=500.0)
        self.assertIsInstance(product, Product)
        self.assertIsInstance(product, DigitalProduct)

    def test_unknown_type(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("service", "S201", "Installation", 30.00, 5, self.supplier)


class TestValidation(unittest.TestCase):

    def setUp(self) -> None:
        self.supplier = Supplier("S003", "SoftWarez Ltd", "support@softwarez.io")
        self.valid_product = ProductFactory.create("digital", "D301", "Antivirus", 20.00, 10, self.supplier)

    def test_invalid_price(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P301", "Bad Price Zero", 0.0, 5, self.supplier)
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P302", "Bad Price Neg", -10.0, 5, self.supplier)

    def test_invalid_stock(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D302", "Bad Stock", 15.0, -1, self.supplier)
        with self.assertRaises(ValueError):
            self.valid_product.update_stock(-5)

    def test_invalid_quantity(self) -> None:
        with self.assertRaises(ValueError):
            OrderLine(self.valid_product, 0)
        with self.assertRaises(ValueError):
            OrderLine(self.valid_product, -3)


class TestErrors(unittest.TestCase):

    def setUp(self) -> None:
        self.supplier = Supplier("S001", "TechSupply Co", "orders@techsupply.com")

    def test_positive_float_input(self) -> None:
        buffer = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            with redirect_stdout(buffer):
                result = get_positive_float("Price: ")
        output = buffer.getvalue()
        self.assertEqual(result, 12.50)
        self.assertIn("Please enter a valid number, e.g. 12.50", output)
        self.assertIn("Please enter a number greater than zero.", output)

    def test_csv_skips_bad_rows(self) -> None:
        inventory = Inventory()
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "products.csv")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            load_products(csv_path, inventory, self.supplier)
        output = buffer.getvalue()
        self.assertEqual(len(inventory), 3)
        self.assertIn("3 products loaded.", output)
        self.assertIn("Load attempt finished.", output)

    def test_csv_missing_file(self) -> None:
        inventory = Inventory()
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            load_products("missing_products.csv", inventory, self.supplier)
        output = buffer.getvalue()
        self.assertEqual(len(inventory), 0)
        self.assertIn("Products file not found: missing_products.csv", output)
        self.assertIn("Load attempt finished.", output)


if __name__ == "__main__":
    unittest.main()
