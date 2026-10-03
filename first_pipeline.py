
# first_pipeline.py
# Simulating one row of data a pipeline might receive from an API

order_id = "ORD-10234"        # str — identifiers are almost always strings, even if they look numeric
customer_name = "Priya Shah"  # str
quantity = 3                  # int
unit_price = 499.99           # float
is_prime_member = True        # bool

# Compute something — a common pipeline task
total_price = quantity * unit_price

print("Order:", order_id)
print("Customer:", customer_name)
print("Total price:", total_price)
print("Type of total_price:", type(total_price))

# A classic real-world bug: data from APIs often arrives as STRINGS, even numbers
quantity_from_api = "3"       # looks like a number, but it's actually text
# total_price_broken = quantity_from_api * unit_price   # this line would CRASH

quantity_fixed = int(quantity_from_api)   # explicit conversion
total_price_fixed = quantity_fixed * unit_price
print("Fixed total:", total_price_fixed)
discount_percent = "10"
dis_amnt = int(discount_percent)
discount_amount =( total_price_fixed*dis_amnt)//100
print("Total_discount:", discount_amount)
Final_purchase_amount=(total_price_fixed-discount_amount)
print("Final_price :",Final_purchase_amount)
