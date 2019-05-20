# Run tests with command:
# python TestInventoryAllocator.py -v

# warehouses: [{"name": name, "inventory": {item: quantity}}, {"name": name2, "inventory": {item2: quantity2}}, ...]
# order: {item: quantity, item2: quantity2, item3: quantity3, ...}
# Assumes correct parameters.


class InventoryAllocator:

    def __init__ (self, warehouses):
        self.warehouses = warehouses

    def allocate_order(self, order):
        total_allocation = []

        for warehouse in self.warehouses:
            warehouse_allocation = {}
            for item in order.keys():
                if item in warehouse["inventory"].keys():
                    item_supply = warehouse["inventory"][item]
                    item_demand = order[item]
                    if item_demand <= 0:  # Ignore orders of 0 quantity.
                        del order[item]
                    elif item_supply >= item_demand:
                        warehouse_allocation[item] = item_demand
                        del order[item]
                    else:
                        if not item_supply <= 0:  # Ignore listings of 0 supply.
                            warehouse_allocation[item] = item_supply
                            order[item] = item_demand - item_supply

            if warehouse_allocation:
                total_allocation.append( {warehouse["name"] : warehouse_allocation} )

            if not order:
                return total_allocation  # Order list is empty; allocation complete.

        return []