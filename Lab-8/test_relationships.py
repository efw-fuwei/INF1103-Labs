from inventory_manager import (
    Supplier,
    PhysicalProduct,
    DigitalProduct,
    Inventory,
    Order,
    Product,
    show_product_details
)


def test_association() -> None:
    print("--- Association Test ---")
    supplier = Supplier("S010", "Apex Electronics", "sales@apex.com")
    laptop = PhysicalProduct("T001", "Gaming Laptop", 1500.00, 10, supplier, 2.5)
    ebook = DigitalProduct("T002", "Python Guide", 29.99, 50, supplier, 15.0)

    del supplier

    laptop.get_supplier().display_information()
    ebook.get_supplier().display_information()
    print()


def test_aggregation() -> None:
    print("--- Aggregation Test ---")
    supplier = Supplier("S011", "Global Tech", "info@globaltech.com")
    keyboard = PhysicalProduct("T003", "Mechanical Keyboard", 120.00, 15, supplier, 0.9)

    inv_a = Inventory()
    inv_b = Inventory()

    inv_a.add_product(keyboard)
    print("In Inventory A:", inv_a.find_product("T003") is not None)

    inv_a.remove_product("T003")
    print("After removal from Inventory A:", inv_a.find_product("T003"))
    keyboard.display_information()

    inv_b.add_product(keyboard)
    print("In Inventory B:", inv_b.find_product("T003") is keyboard)
    print()


def test_composition() -> None:
    print("--- Composition Test ---")
    supplier = Supplier("S012", "AudioWorld", "hello@audioworld.com")
    headset = PhysicalProduct("T004", "Studio Headset", 199.99, 20, supplier, 0.35)
    software = DigitalProduct("T005", "Audio Mixer App", 49.99, 100, supplier, 250.0)

    order1 = Order("ORD-001")
    order1.add_order_line(headset, 2)
    order1.add_order_line(software, 1)

    order2 = Order("ORD-002")
    order2.add_order_line(headset, 1)

    line_from_order1 = order1.get_order_lines()[0]
    line_from_order2 = order2.get_order_lines()[0]

    print("Same OrderLine object?", line_from_order1 is line_from_order2)
    print("Same Product object?", line_from_order1.get_product() is line_from_order2.get_product())
    print("OrderLine 1 id:", id(line_from_order1), "OrderLine 2 id:", id(line_from_order2))
    print("Product id:", id(headset))

    order1.display_order()
    order1.remove_order_line("T005")
    print("After removing T005 from Order 1:")
    order1.display_order()
    software.display_information()
    del order2
    headset.display_information()
    print()


def test_lsp_and_polymorphism() -> None:
    print("--- LSP & Polymorphism Test ---")
    supplier = Supplier("S013", "OmniStore", "support@omnistore.com")
    monitor = PhysicalProduct("T006", "4K Monitor", 450.00, 8, supplier, 5.2)
    antivirus = DigitalProduct("T007", "Security Suite", 39.99, 80, supplier, 180.0)

    print("Testing show_product_details:")
    show_product_details(monitor)
    show_product_details(antivirus)

    inventory = Inventory()
    inventory.add_product(monitor)
    inventory.add_product(antivirus)

    print("\nUpdating stock via Product abstraction:")
    for product in inventory.get_products():
        product.update_stock(product.get_stock() + 5)

    print("\nPolymorphic loop over Inventory:")
    for product in inventory.get_products():
        product.display_information()
        print(product.get_fulfilment_info())
    print()


if __name__ == "__main__":
    test_association()
    test_aggregation()
    test_composition()
    test_lsp_and_polymorphism()
