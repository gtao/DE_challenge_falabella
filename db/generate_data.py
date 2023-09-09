from faker import Faker
import random
from decimal import Decimal
from datetime import date
from db.conn import create_connection

# Tabla a validar
table_name = "raw_data"

# Instancia de clase Faker para datos random
fake = Faker()

# Seteo de variables para cargar en tabla PSQL
def set_data():
    id_value = random.randint(1, 1000000)
    name = fake.name()
    email = fake.email()
    date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=80)
    address = fake.address()
    purchase_amount = Decimal(random.uniform(10.0, 500.0)).quantize(Decimal("0.01"))
    last_purchase = fake.date_between(start_date='-90d', end_date='today')
    return (id_value, name, email, date_of_birth, address, purchase_amount, last_purchase)

# Genwración e inserción de registros en tabla raw
def generate_random_data():
    connection = create_connection()
    for _ in range(100):
        data = set_data()
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO {table_name} (id, name, email, date_of_birth, address, purchase_amount, last_purchase) VALUES (%s, %s, %s, %s, %s, %s, %s)", data)
        connection.commit()
        cursor.close()
    connection.close()
