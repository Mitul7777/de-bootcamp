import csv
import json

rejected_rows = []

with open("orders.csv", newline="") as f:
    readers = csv.DictReader(f)
    rows = list(readers)





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
            raise ValueError(f"Unknown prime value: {item['is_prime_member']}")
            
        return {
            "order_id": str(item["order_id"]),
            "customer": str(item["customer"]),
            "quantity": int(item["quantity"]),
            "unit_price": float(item["unit_price"]),
            "is_prime_member": is_prime 
        }
    except (KeyError, ValueError, AttributeError) as e:
        rejected_rows.append({"order_id": item["order_id"], "reason": str(e)})
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

print("GOOD ORDERS : ", good_orders)
print("BAD ORDERS : ",bad_orders)


counts = {}
for row in good_orders:
    order_id = row["order_id"]
    counts[order_id] = counts.get(order_id, 0) + 1
    if counts[order_id] > 1:
        rejected_rows.append({"order_id": order_id, "reason": "Duplicate : extra copies of an earlier order"})
        print(f"Duplicate order found: {order_id}")
print ("COUNT :",counts)
duplicate_orders =[]  # Truncate the last row of the duplicate orders list to avoid duplicates in the final output.
for order_id, count in counts.items():
    if count > 1:
        duplicate_orders.append(order_id)
print("DUPLICATE :",duplicate_orders)

dict_clean_orders = {order["order_id"]: order for order in good_orders}

clean_orders = list(dict_clean_orders.values())

def is_valid_order(item):
    """Return True if order has valid quantity and unit price."""
    return item["quantity"] > 0 and item["unit_price"] > 0 
    

valid_orders = []
invalid_values = []
for order in clean_orders:
    if is_valid_order(order)== True:
        valid_orders.append(order)
    else:
        invalid_values.append(order)
        rejected_rows.append({"order_id": order["order_id"], "reason": "Invalid quantity or unit price,which is less than or equal to zero"})
        print(f"!!! WARNING !!! ORDER : {order['order_id']} has an invalid values.")

print(f"Valid orders: {valid_orders}")
print(f"InValid orders: {invalid_values}")

# Reconcile the total number of orders, accepted orders, and rejected orders
total_orders = len(rows)
accepted_orders = len(valid_orders)
invalid_orders = len(invalid_values) 
duplicate_orders_count = len(good_orders) - len(counts)
bad_orders_count = len(bad_orders)
total_rejected_orders = len(rejected_rows)

reconciliation_check = (total_orders == (accepted_orders + invalid_orders + duplicate_orders_count + bad_orders_count))
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

# Final summary block
print(f"\n-------Final Summary-------\nTotal Orders : {total_orders}\nAccepted orders : {accepted_orders}\nInvalid orders : {invalid_orders}\n Duplicate orders : {duplicate_orders_count}\nBad Value orders : {bad_orders_count}\nTotal Rejected Orders : {total_rejected_orders}\ncount of prime members : {count_prime_members}\ncount of non prime members : {count_non_prime_members} ")



with open("rejected_orders.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["order_id", "reason"])
    writer.writeheader()
    writer.writerows(rejected_rows)




summary = {
    "total_orders": total_orders,
    "accepted_orders": accepted_orders,
    "invalid_orders": invalid_orders,
    "duplicate_orders": duplicate_orders_count,
    "bad_value_orders": bad_orders_count,
    "total_rejected_orders": total_rejected_orders,
    "count_prime_members": count_prime_members,
    "count_non_prime_members": count_non_prime_members
}

with open("summary.json", "w") as f:
    json.dump(summary, f, indent=4)



# Final reconciliation check. TEST THE TEST.

if total_orders == (accepted_orders + total_rejected_orders) :
    print("Final Check is OK : every row is accounted for.")
else:
    print(f"!!!WARNING!!!: only {total_orders} rows are came in but {accepted_orders} + {total_rejected_orders} is accounted for. Something is missing.")



# Read the JSON back to Confirm you get a number, not text
with open ("summary.json", "r") as f :
    summary_data = json.load(f)
    print(summary_data["accepted_orders"] + 1) # should print a number, not text, confirming that the JSON was written and read correctly.
