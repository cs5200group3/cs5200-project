import mysql.connector
import random
from faker import Faker


def generate_payments(num_items):
    print(f"Generating {num_items} payments...")
    fake = Faker()
    payments = []

    for _ in range(num_items):
        payment_status = random.choices (
            ['Pending', 'Paid', 'Cancelled', 'Refunded'],
            weights=[5, 85, 5, 5],
            k=1
        )[0]
        payment = {
            'payment_method': random.choice(['Credit Card','Debit Card','PayPal','Apple Pay','Google Pay']),
            'payment_status': payment_status,
            'payment_time': fake.date_time_this_year(),
            'refunded': True if payment_status == 'Refunded' else False
        }
        payments.append(payment)

    print(f"Generated {len(payments)} payments.")
    return payments


def insert_payments(payments, cursor, conn, batch_size=50):
    print("Inserting payments into the database...")
    insert_query = """
    INSERT INTO `Payment` (
        `payment_method`, `payment_status`, `payment_time`, `refunded`
    ) VALUES (%s, %s, %s, %s)
    """
    
    for i in range(0, len(payments), batch_size):
        batch = payments[i:i + batch_size]
        cursor.executemany(insert_query, [
            (
                payment['payment_method'],
                payment['payment_status'],
                payment['payment_time'],
                payment['refunded']
            ) for payment in batch
        ])
        conn.commit()  # Commit after each batch
        print(f"Inserted batch {i // batch_size + 1} successfully.")

    print("All payments inserted successfully.")


def generate_and_insert_payments(cursor, conn):  # Accept conn as a parameter
    num_payments = 1000
    payments = generate_payments(num_payments)
    insert_payments(payments, cursor, conn)  # Now conn is defined


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
        generate_and_insert_payments(cursor, conn)  # Pass conn to the function
    finally:
        # Close the database connection
        cursor.close()
        conn.close()
        print("Database connection closed.")


if __name__ == "__main__":
    main()

