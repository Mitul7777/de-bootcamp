import csv


with open("orders.csv", newline="")as f:
	reader = csv.DictReader(f)
	rows = list(reader)


#print(rows[0])
#print(type(rows[2]))
#print(type(rows[2]["quantity"]))


#Write a function parse_order(item) that returns a new dictionary with quantity as an int, unit_price as a float, and is_prime_member as a real bool.

def parse_order(item):
    """Parse an order row and return a new dictionary with the correct data types."""
    try:

         # Strip and lower the string first
        val = str(item["is_prime_member"]).strip().lower()
        if val == "true" :
            is_prime = True
        elif val == "false" :
            is_prime = False
        
        else :
            raise ValueError("I don't understand this prime member's value",{item['is_prime_member']})
            
        return {
            "order_id": str(item["order_id"]),
            "customer": str(item["customer"]),
            "quantity": int(item["quantity"]),
            "unit_price": float(item["unit_price"]),
            "is_prime_member": is_prime 
        }
    except (KeyError, ValueError, AttributeError) as e:
        print(f"Parsing error: {e}")
        return None


good_orders =[]
bad_orders = []
for row in rows :
    parsed_order = parse_order(row)
    if parsed_order is None:
        bad_orders.append(row["order_id"])
        print(f"!!! WARNING !!! ROW : order_id --> {row['order_id']} rejected due to bad data present.")
    else:
        good_orders.append(parsed_order)
    
print(f"GOOD ORDERS :{good_orders}")
print(f"BAD ORDERS :{bad_orders}")

counts = {}
for row in good_orders:
    order_id = row["order_id"]
    counts[order_id] = counts.get(order_id, 0) + 1
    if counts[order_id] > 1:
        print(f"Duplicate order found: {order_id}")
print(counts)

duplicate_orders =[]
for order_id, count in counts.items():
    if count > 1:
        duplicate_orders.append(order_id)
print(f"DUPLICATE:{duplicate_orders}")

dict_clean_orders = {order["order_id"]: order for order in good_orders}
clean_orders = list(dict_clean_orders.values())
print(f"CLEAN ORDERS: {clean_orders}")


def is_valid_order(item):
    """Return True if order has valid quantity and unit price."""
    return item["quantity"] > 0 and item["unit_price"] > 0

valid_orders = []
invalid_orders = []
for order in clean_orders:
    if is_valid_order(order)== True:
        valid_orders.append(order)
    else:
        invalid_orders.append(order)
        print(f"!!! WARNING !!! ORDER : {order['order_id']} has an invalid values.")

print(f"VALID ORDERS: {valid_orders}")
print(f"INVALID ORDERS: {invalid_orders}")


# Reconcile the total number of orders, accepted orders, and rejected orders
total_orders = len(rows)
accepted_orders = len(valid_orders)
rejected_orders = len(invalid_orders)
duplicate_orders_count = len(good_orders) - len(counts)
bad_orders_count = len(bad_orders)

reconciliation_check = (total_orders == (accepted_orders + rejected_orders + duplicate_orders_count + bad_orders_count))
if reconciliation_check:
    print("Reconciliation check of number of orders: Matches") 
else:
    print("!!!WARNING!!!: The total number of orders does NOT match the sum of accepted, rejected, duplicate, and bad orders.")


# Reconcilation check of prime and non-prime members
prime_members =[]
non_prime_members = []
for order in valid_orders:
    if order["is_prime_member"] == True:
        prime_members.append(order)
    else:
        non_prime_members.append(order)

reconciliation_check_members = (len(prime_members) + len(non_prime_members) == accepted_orders)
if reconciliation_check_members == True:
    print("Reconciliation check of prime and non-prime members: Matches")
else:
    print("!!!WARNING!!!: The total number of prime and non-prime members does NOT match the number of accepted orders.")

count_prime_members = len(prime_members)
count_non_prime_members = len(non_prime_members)
print( f"count of prime members : {count_prime_members}\ncount of non prime members : {count_non_prime_members}")

# Final summery block
print(f"\n-------Final Summary-------\nTotal Orders : {total_orders}\nAccepted orders : {accepted_orders}\nRejected orders : {rejected_orders}\nDuplicate orders : {duplicate_orders_count}\nBad Value orders : {bad_orders_count}\ncount of prime members : {count_prime_members}\ncount of non prime members : {count_non_prime_members} ")
