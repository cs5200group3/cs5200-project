import mysql.connector
import random
from faker import Faker

refund_payment_ids = [
    3, 18, 24, 40, 52, 79, 90, 95, 146, 155, 229, 241, 249, 252, 271, 279, 303, 
    347, 355, 376, 391, 396, 410, 414, 434, 453, 523, 537, 540, 552, 588, 651, 
    660, 666, 679, 720, 722, 763, 832, 843, 846, 859, 868, 875, 895, 922, 927, 
    956, 976
]


def generate_orders(num_items):
    print(f"Generating {num_items} orders...")
    fake = Faker()
    orders = []
    payment_id = 1

    for _ in range(num_items):
        order = {
            'payment_id': payment_id,
            'user': random.randint(1, 450),
            'order_time': fake.date_time_this_year(),
            'order_total': random.uniform(50.00, 1000.00),
            'order_status': 'refunded' if payment_id in refund_payment_ids else random.choice(['Pending', 'Paid', 'Cancelled']),
            'refund_requested': 1 if payment_id in refund_payment_ids else 0
        }
        orders.append(order)
        payment_id += 1

    print(f"Generated {len(orders)} orders.")
    return orders


def insert_orders(orders, cursor, conn, batch_size=50):
    print("Inserting orders into the database...")
    insert_query = """
    INSERT INTO `Payment` (
        `payment_method`, `payment_status`, `payment_time`, `refunded`
    ) VALUES (%s, %s, %s, %s)
    """
    
    for i in range(0, len(orders), batch_size):
        batch = orders[i:i + batch_size]
        cursor.executemany(insert_query, [
            (
                order['payment_method'],
                order['payment_status'],
                order['payment_time'],
                order['refunded']
            ) for order in batch
        ])
        conn.commit()  # Commit after each batch
        print(f"Inserted batch {i // batch_size + 1} successfully.")

    print("All orders inserted successfully.")


def generate_and_insert_orders(cursor, conn):  # Accept conn as a parameter
    num_orders = 1000
    orders = generate_orders(num_orders)
    insert_orders(orders, cursor, conn)  # Now conn is defined


# Database connection configuration for Aiven MySQL
db_config = {
    'host': 'g3-sprint2-just4thedreamland-5e30.h.aivencloud.com',  # Replace with your Aiven hostname
    'port': 26740, 
    'user': 'avnadmin',  # Replace with your Aiven username
    'password': 'AVNS_k8-EKEKB0de1fhIa09w',  # Replace with your Aiven password
    'database': 'Sprint2'  # Replace with your database name
}


# Connect to the database
def connect_to_database():
    print("Connecting to the database...")
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("Database connection established.")
    return conn, cursor


# Main function
def main():
    conn, cursor = connect_to_database()  # Ensure conn is defined
    try:
        print("Starting synthetic data generation...")
        generate_and_insert_orders(cursor, conn)  # Pass conn to the function
    finally:
        # Close the database connection
        cursor.close()
        conn.close()
        print("Database connection closed.")


if __name__ == "__main__":
    main()

