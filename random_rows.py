import csv
import random
from datetime import datetime, timedelta

# Listas con valores posibles para las columnas
status_options = ["pending", "shipped", "delivered"]
hours_options = ["morning", "afternoon", "evening"]
source_options = ["website", "phone", "in-store"]
warehouse_options = ["A", "B", "C"]
sales_person_options = ["Alice", "Bob", "Charlie"]
role_options = ["FARMER", "SALES"]
type_options = ["scheduled", "express"]
payment_options = ["credit card", "cash", "check"]

# Crear cinco filas con información aleatoria
data = []
for i in range(5):
    order_number = f"#{random.randint(10000, 99999)}"
    order_status = random.choice(status_options)
    customer_email = f"customer{i}@example.com"
    preferred_delivery_date = datetime.today() + timedelta(days=random.randint(1, 30))
    preferred_delivery_hours = random.choice(hours_options)
    sales_person = random.choice(sales_person_options)
    notes = f"Notes for order {order_number}"
    address = f"{random.randint(1, 999)} Main St."
    neighbourhood = f"Neighbourhood {random.randint(1, 10)}"
    city = "City Name"
    creation_date = datetime.today()
    source = random.choice(source_options)
    warehouse = random.choice(warehouse_options)
    shopify_id = f"shopify-{random.randint(100000, 999999)}"
    sales_person_role = random.choice(role_options)
    order_type = random.choice(type_options)
    is_pitayas = random.choice(["0", "1"])
    discount_applications = f"Discount for order {order_number}"
    payment_method = random.choice(payment_options)
    row = [
        order_number,
        order_status,
        customer_email,
        preferred_delivery_date.strftime('%Y-%m-%d'),
        preferred_delivery_hours,
        sales_person,
        notes,
        address,
        neighbourhood,
        city,
        creation_date.strftime('%Y-%m-%d'),
        source,
        warehouse,
        shopify_id,
        sales_person_role,
        order_type,
        is_pitayas,
        discount_applications,
        payment_method
    ]
    data.append(row)

# Agregar las filas al archivo CSV
with open('pipeline-test/data/data.csv', mode='a', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(data)