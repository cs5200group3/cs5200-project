import mysql.connector
import random
from faker import Faker
from datetime import timedelta

def generate_orders(events, num_orders=10):
    print(f"Generating {num_orders} orders...")
    fake = Faker()
    orders = []
    order_id = 1
    
    for i, event in enumerate(events):
        for _ in range(num_orders):
            event = random.choice(events)
            start_date = event['event_date'] - timedelta(days=30)
            ticket_type = random.choice(['VIP', 'General Admission'])
            
            order = {
                'order_id': order_id,
                'payment_id': order_id,
                'user': random.randint(1, 450),
                'order_time': fake.date_time_between(start_date=start_date, end_date=event['event_date']),
                'price': random.uniform(100, 200) if ticket_type == 'VIP' else random.uniform(50, 100),
                'order_status': random.choices(['Confirmed', 'Refunded'], weights = [92, 8], k=1)[0],
                'event_id': (i + 1),
                'ticket_type': ticket_type
            }
            orders.append(order)
            order_id += 1

    print(f"Generated {len(orders)} orders.")
    return orders


def insert_orders(orders, cursor, conn, batch_size=50):
    print("Inserting orders into the database...")
    insert_query = """
    INSERT INTO `Order` (
        `order_id`, `payment_id`, `user`, `order_time`, `price`, `order_status`, `event_id`, `ticket_type`
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    for i in range(0, len(orders), batch_size):
        batch = orders[i:i + batch_size]
        cursor.executemany(insert_query, [
            (
                order['order_id'],
                order['payment_id'],
                order['user'],
                order['order_time'],
                order['price'],
                order['order_status'],
                order['event_id'],
                order['ticket_type']
            ) for order in batch
        ])
        conn.commit()  # Commit after each batch
        print(f"Inserted batch {i // batch_size + 1} successfully.")

    print("All orders inserted successfully.")


def generate_and_insert_orders(cursor, conn, organizers, events, num_orders):
    # num_orders = 1000
    orders = generate_orders(events, num_orders)
    insert_orders(orders, cursor, conn)


# Database connection configuration for Aiven MySQL
db_config = {
    'host': 'g3-sprint2-just4thedreamland-5e30.h.aivencloud.com',  # Replace with your Aiven hostname
    'port': 26740, 
    'user': 'avnadmin',  # Replace with your Aiven username
    'password': 'AVNS_k8-EKEKB0de1fhIa09w',  # Replace with your Aiven password
    'database': 'Sprint'  # Replace with your database name
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

