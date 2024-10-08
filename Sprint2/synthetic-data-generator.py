import mysql.connector
import random
from faker import Faker
from account_generate import generate_accounts, insert_accounts, \
    generate_and_insert_accounts

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
        generate_and_insert_accounts(cursor, conn)  # Pass conn to the function
    finally:
        # Close the database connection
        cursor.close()
        conn.close()
        print("Database connection closed.")


if __name__ == "__main__":
    main()