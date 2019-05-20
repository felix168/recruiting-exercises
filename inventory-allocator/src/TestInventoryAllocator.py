# Run tests with command: 
# python TestInventoryAllocator.py -v

import unittest
from InventoryAllocator import InventoryAllocator


class TestInventoryAllocator(unittest.TestCase):

    # warehouses: [{ "name": name, "inventory": { item: quantity }}, { "name": name2, "inventory": { item2: quantity2 }}, ...]
    # order: { item: quantity, item2: quantity2, item3: quantity3, ...}

    def test_insufficient_inventory(self):
        order = {"apple": 10}
        warehouses = [{"name": "owd", "inventory": {"apple": 5} }, {"name": "dm", "inventory": {"apple": 4}}]
        result = InventoryAllocator(warehouses).allocate_order(order)

        self.assertEqual(result, [])

    def test_basic_exact_inventory(self):
        order = {"apple": 1}
        warehouses = [{"name": "owd", "inventory": {"apple": 1}}]
        result = InventoryAllocator(warehouses).allocate_order(order)
    
        self.assertEqual(result, [{"owd": {"apple": 1}}])

    def test_basic_exact_split_inventory(self):
        order = {"apple": 10}
        warehouses = [{"name": "owd", "inventory": {"apple": 5}}, {"name": "dm", "inventory": {"apple": 5}}]
        result = InventoryAllocator(warehouses).allocate_order(order)

        self.assertEqual(result, [{"owd": {"apple": 5}}, {"dm": {"apple": 5}}])

    def test_correct_price_priority(self):
        order = {"apple": 100}
        warehouses = [{"name": "w1", "inventory": {"apple": 3}}, {"name": "w2", "inventory": {"apple": 50000}}, {"name": "w3", "inventory": {"apple": 300}}]
        result = InventoryAllocator(warehouses).allocate_order(order)

        self.assertEqual(result, [{"w1": {"apple": 3}}, {"w2": {"apple": 97}}])

    def test_basic_multiple_item_order(self):
        order = {"apple": 1, "trolldolls": 5000}
        warehouses = [{"name": "w1", "inventory": {"trolldolls": 50}}, {"name": "w2", "inventory": {"apple": 50000}}, 
            {"name": "w3", "inventory": {"apple": 300, "trolldolls": 24250}}]
        result = InventoryAllocator(warehouses).allocate_order(order)

        self.assertEqual(result, [{"w1": {"trolldolls": 50}}, {"w2": {"apple": 1}}, {"w3": {"trolldolls": 4950}}])

    def test_empty_order(self):
        order = {}
        warehouses = [{"name": "owd", "inventory": {"apple": 5}}, {"name": "dm", "inventory": {"apple": 5}}]
        result = InventoryAllocator(warehouses).allocate_order(order)

        self.assertEqual(result, [])

    def test_empty_warehouse_list(self):
        order = {"apple": 1}
        warehouses = []
        result = InventoryAllocator(warehouses).allocate_order(order)

        self.assertEqual(result, [])

    def test_complex_exact_split_inventory_multiple_item_order(self):
        order = {"apple": 10, "ball": 20}
        warehouses = [{"name": "w1", "inventory": {"apple": 2, "ball": 3}}, {"name": "w2", "inventory": {"corks": 40, "ball": 4}}, 
            {"name": "w3", "inventory": {"apple": 4, "grass": 4000}}, {"name": "w4", "inventory": {"ball": 5, "apple": 4}},
            {"name": "w5", "inventory": {"ball": 8}}]
        result = InventoryAllocator(warehouses).allocate_order(order)

        self.assertEqual(result, [{"w1": {"apple": 2, "ball": 3}}, {"w2": {"ball": 4}}, {"w3": {"apple": 4}}, {"w4": {"ball": 5, "apple": 4}},
            {"w5": {"ball": 8}}])

    def test_only_expensive_warehouses(self):
        order = {"pie": 15, "cake": 15}
        warehouses = [{"name": "w1", "inventory": {}}, {"name": "w2", "inventory": {}}, {"name": "w3", "inventory": {}}, {"name": "w4", "inventory": {}}, 
            {"name": "w5", "inventory": {}}, {"name": "w6", "inventory": {"pie": 15, "cake": 15}}]
        result = InventoryAllocator(warehouses).allocate_order(order)

        self.assertEqual(result, [{"w6": {"pie": 15, "cake": 15}}])

    def test_complex_multiple_item_order(self):
        order = {"coke": 2, "sprite": 3, "dew": 1, "fanta": 6, "pepsi": 9}
        warehouses = [{"name": "w1", "inventory": {"sprite": 1, "pepsi": 5}}, {"name": "w2", "inventory": {"sprite": 5, "coke": 1}}, 
            {"name": "w3", "inventory": {"fanta": 2, "coke": 3, "dew": 90}}, {"name": "w4", "inventory": { "fanta": 6, "pepsi": 10, "coke": 100}}]
        result = InventoryAllocator(warehouses).allocate_order(order)

        self.assertEqual(result, [{"w1": {"sprite": 1, "pepsi": 5}}, {"w2": {"sprite": 2, "coke": 1}}, {"w3": {"fanta": 2, "coke": 1, "dew": 1}},
            {"w4": {"fanta": 4, "pepsi": 4}}])

    def test_warehouses_with_no_inventory(self):
        order = {"coke": 2, "sprite": 3, "dew": 1, "fanta": 6, "pepsi": 9}
        warehouses = [{"name": "w1", "inventory": {}}, {"name": "w2", "inventory": {}}, {"name": "w3", "inventory": {}}]
        result = InventoryAllocator(warehouses).allocate_order(order)

        self.assertEqual(result, [])

    def test_order_quantities_of_zero(self):
        order = {"coke": 0, "sprite": 1}
        warehouses = [{"name": "w1", "inventory": {"sprite": 0, "pepsi": 5}}, {"name": "w2", "inventory": {"sprite": 0, "coke": 1}}, 
            {"name": "w3", "inventory": {"fanta": 2, "coke": 3, "dew": 90}}, {"name": "w4", "inventory": {"sprite": 6, "pepsi": 10, "coke": 100}}]
        result = InventoryAllocator(warehouses).allocate_order(order)

        self.assertEqual(result, [{"w4": {"sprite": 1}}])

    def test_warehouses_with_supplies_of_zero(self):
        order = {"coke": 1, "sprite": 1}
        warehouses = [{"name": "w1", "inventory": {"sprite": 0, "sprite": 0}}, {"name": "w2", "inventory": {"sprite": 0, "coke": 0}}, 
            {"name": "w3", "inventory": {"coke": 1, "sprite": 1}}]
        result = InventoryAllocator(warehouses).allocate_order(order)

        self.assertEqual(result, [{"w3": {"coke": 1, "sprite": 1}}])

    def test_zero_supply_zero_demand(self):
        order = {"coke": 0}
        warehouses = [{"name": "w1", "inventory": {"coke": 0}}]
        result = InventoryAllocator(warehouses).allocate_order(order)

        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()
    