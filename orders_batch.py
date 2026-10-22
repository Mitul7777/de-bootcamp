

# A list = many records
raw_orders = [ 
    {"order_id": "ORD-1001", "customer": "Priya Shah", "quantity": 3, "unit_price": 499.99, "is_prime_member": True}, 
    {"order_id": "ORD-1002", "customer": "Rahul Mehta", "quantity": 1, "unit_price": 1200.00, "is_prime_member": False}, 
    {"order_id": "ORD-1003", "customer": "Ayesha Khan", "quantity": 5, "unit_price": 89.50, "is_prime_member": False}, 
    {"order_id": "ORD-1004", "customer": "Abid Ali", "quantity": 6, "unit_price": 102.50, "is_prime_member": True}, 
    {"order_id": "ORD-1005", "customer": "Zara Patel", "quantity": 0, "unit_price": 00.00, "is_prime_member": True}, 
    {"order_id": "ORD-1006", "customer": "Axar Patel", "quantity": -1, "unit_price": 100.00, "is_prime_member": True}, 
    {"order_id": "ORD-1007", "customer": "Neeraj Pandey", "quantity": 2, "unit_price": 00.00, "is_prime_member": False},
    {"order_id": "ORD-1007", "customer": "Neeraj Pandey", "quantity": 2, "unit_price": 00.00, "is_prime_member": False},
    {"order_id": "ORD-1007", "customer": "Neeraj Pandey", "quantity": 2, "unit_price": 00.00, "is_prime_member": False}
]

counts = {}
for order in raw_orders:
    key = order["order_id"]
    counts[key] = counts.get(key, 0) + 1
    if counts[key] > 1:
        print(f"!!! WARNING !!! : DUPLICATE ORDER ID DETECTED! Order ID: {key}, Count: {counts[key]}")


duplicate_orders = []
for key,count in counts.items():
    if count > 1:
        duplicate_orders.append(key)
print(f"Duplicate Order IDs: {duplicate_orders}")


# Extra copies
extra_orders_copies = len(raw_orders) - len(counts)
print(f"Duplicate Order were removed: {extra_orders_copies}")




# Using a dictionary keyed by ID automatically overrides older duplicates . Keeping the last copy

orders_dict = {order.get("order_id"): order for order in raw_orders}
orders = list(orders_dict.values())

# creating functions to validate orders, calculate total amounts, and count total orders

def is_valid_order(item) :
    """ return True if order has valid quantity and unit price"""
    return item["quantity"] > 0 and item["unit_price"]> 0

def calculate_total (item) :
    """Return price times quantity for one item."""
    return item["unit_price"] * item["quantity"]



# Filtering out the valid orders and calculating their total amounts
for order in orders:
    if is_valid_order(order):
        # for individual valid order and its total amount
        accepted_orders = (f" Individual order and its total amount: {order['order_id']} -> {round(calculate_total(order), 2)}")
        print(accepted_orders)
# Filtering out the invalid orders and printing a warning message for each 
    else:
        Rejected = (f"!!! WARNING !!! ORDER : {order['order_id']} has an invalid quantity or unit price.")
        print(Rejected)
        

# Counting the total number of orders, accepted orders, and rejected orders
num_total_order = (len(raw_orders))
num_accepted_order = (len([order for order in orders if is_valid_order(order)]))
num_Rejected_order = (len([order for order in orders if not is_valid_order(order)]))
print (f" Count of total orders : {num_total_order}")
print(f" Count of accepted orders : {num_accepted_order}")
print(f" Count of rejected orders : {num_Rejected_order}")

#Reconciliation check of number of orders: The total number of orders should equal the sum of num_accepted_order  and num_Rejected_order and extra_orders_copies.
reconciliation_check_orders = (num_total_order == (num_accepted_order + num_Rejected_order + extra_orders_copies))
if reconciliation_check_orders == True:
    print("Reconciliation check of number of orders: The total number of orders matches the sum of accepted and rejected orders.")
else:
    print("!!!WARNING!!!: The total number of orders does NOT match the sum of accepted and rejected orders.")



# The money from each prime member and non-prime member, and total counts of members. 

prime_count = len([order for order in orders if is_valid_order(order) and order["is_prime_member"] == True])
prime_total_amount = 0

non_prime_total_amount = 0
non_prime_count = len([order for order in orders if is_valid_order(order) and order["is_prime_member"] == False])

for order in orders:
    if order["is_prime_member"] == True and is_valid_order(order):
        prime_total_amount += calculate_total(order)
    elif order["is_prime_member"] == False and is_valid_order(order):
        non_prime_total_amount += calculate_total(order)

print(f"Prime member count: {prime_count}        ; Total amount from prime members: {round(prime_total_amount, 2)}")
print(f"Non-prime member count: {non_prime_count} ; Total amount from non-prime members: {round(non_prime_total_amount, 2)}")


# Accumulate a running total across accepted orders — classic pipeline aggregation
grand_total = 0
for order in orders:
    grand_total += calculate_total(order) if is_valid_order(order) else 0  

print("Grand total across accepted orders:", round(grand_total, 2))

# Reconciliation check of grand total with the sum of prime and non-prime totals
reconciliation_check_grand_total = (round(grand_total,2) == round (prime_total_amount + non_prime_total_amount,2))
if reconciliation_check_grand_total == True:
    print("Reconciliation check of grand total: The grand total matches the sum of prime and non-prime totals.")
else:
    print("!!!WARNING!!!: The grand total does NOT match the sum of prime and non-prime totals.")


# High value oders: Details and count of orders with total amount greater than 500.00
high_value_orders = [order for order in orders if calculate_total(order) > 500 and is_valid_order(order)]

print(f"High value orders: {[{'order_id': order['order_id'], 'order_total': calculate_total(order)} for order in high_value_orders]}")
print(f"Count of high value orders: {len(high_value_orders)}")


# Final summary block:
print(f"\n--- Final Summary ---\nTotal Received orders: {num_total_order}\nAccepted orders: {num_accepted_order}\nRejected orders: {num_Rejected_order}\nDuplicate Order were removed: {extra_orders_copies}\nGrand total: {round(grand_total, 2)}\nPrime members total: {round(prime_total_amount, 2)}\nNon-prime members total: {round(non_prime_total_amount, 2)}\nPrime members: {prime_count}\nNon-prime members: {non_prime_count}\nHigh value orders count: {len(high_value_orders)}")

