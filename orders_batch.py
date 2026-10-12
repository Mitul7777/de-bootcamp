
# A dictionary = one record (one row)
order_1 = {
    "order_id": "ORD-1001",
    "customer": "Priya Shah",
    "quantity": 3,
    "unit_price": 499.99,
}

# Access fields by key, not position
print(order_1["order_id"])
print(order_1["quantity"] * order_1["unit_price"])

# A list = many records
orders = [
    {"order_id": "ORD-1001", "customer": "Priya Shah", "quantity": 3, "unit_price": 499.99, "is_prime_member": True},
    {"order_id": "ORD-1002", "customer": "Rahul Mehta", "quantity": 1, "unit_price": 1200.00, "is_prime_member": False},
    {"order_id": "ORD-1003", "customer": "Ayesha Khan", "quantity": 5, "unit_price": 89.50, "is_prime_member": False},
    {"order_id": "ORD-1004", "customer": "Abid Ali", "quantity": 6, "unit_price": 102.50, "is_prime_member": True},
    {"order_id": "ORD-1005", "customer": "Zara Patel", "quantity": 0, "unit_price": 00.00, "is_prime_member": True},
    {"order_id": "ORD-1006", "customer": "Axar Patel", "quantity": -1, "unit_price": 00.00, "is_prime_member": True}
]


total_orders = 0
for order in orders :
	if order["quantity"] <=0 or  order["quantity"] > 0:
		total_orders += 1

print(f" Total order recived : {total_orders} ")


# WARNIG: For data quality bug

for order in orders:
    if order["quantity"] <= 0 or order["unit_price"] <= 0:
        print(f"Warning: Order {order['order_id']} has an invalid quantity or unit price.")

rejected = 0
for order in orders:
    if order["quantity"] <= 0 or  order["unit_price"] <= 0:
        rejected += 1
print(f"Rejected Order : {rejected} ")



#Accepted Orders and Details

clean_orders = [order for order in orders if order["quantity"] > 0 and order["unit_price"] > 0]
print("Accepted Orders and Details:", clean_orders)


# Loop over every order and compute its total
for order in clean_orders:
    total = order["quantity"] * order["unit_price"]
    print(order["order_id"], "->", round(total,2))

# Accumulate a running total across accepted  orders — classic pipeline aggregation
grand_total = 0
for order in clean_orders:
    grand_total += order["quantity"] * order["unit_price"]

print("Grand total across accepted orders:", round(grand_total,2))


# Loop for total Prime_member and non_prime

prime_count =0
non_prime_count=0
prime_total_amount = 0
non_prime_total_amount = 0

for order in clean_orders:
	prime_total_amount += order["unit_price"]*order["quantity"] if order["is_prime_member"] == True else 0
	non_prime_total_amount += order["unit_price"]*order["quantity"] if order["is_prime_member"] == False else 0

	if order ["is_prime_member"]== True :
		prime_count += 1
	else :
		non_prime_count +=1

print(f"Prime member count: {prime_count}, Total amount from prime members: {round(prime_total_amount, 2)}")
print(f"Non-prime member count: {non_prime_count}, Total amount from non-prime members: {round(non_prime_total_amount, 2)}")



# Filtering — only process orders above a threshold (common real-world logic)
high_value_orders = []
for order in clean_orders:
    order_total = order["quantity"] * order["unit_price"]
    if order_total > 500:
   	 high_value_orders.append({"order_id": order["order_id"] ,"order_total": order_total})

print("High value orders:", high_value_orders)

print("count of high value order:", len(high_value_orders))



