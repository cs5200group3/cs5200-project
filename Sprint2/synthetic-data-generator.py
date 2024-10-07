import mysql.connector
import random
from faker import Faker

# Database connection configuration for Aiven MySQL
db_config = {
    'host': 'g3-sprint2-just4thedreamland-5e30.h.aivencloud.com',  # Replace with your Aiven hostname
    'port': 26740,  # Default MySQL port
    'user': 'avnadmin',  # Replace with your Aiven username
    'password': 'AVNS_k8-EKEKB0de1fhIa09w',  # Replace with your Aiven password
    'database': 'Sprint2'  # Replace with your database name
}

# Connect to the database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()


# Function to generate synthetic accounts
def generate_accounts(num_accounts):
    fake = Faker()
    accounts = []

    for _ in range(num_accounts):
        account = {
            'account_type': random.choice(['user', 'organizer', 'admin']),
            'username': fake.user_name(),
            'password': fake.password(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'social_media_link': fake.url(),
            'accessibility_needs': random.choice(['Wheelchair Accessible', 'Hearing Impaired', 'Visual Impaired']),
            'account_status': random.choice(['Active', 'Inactive']),
            'last_activity': fake.date_time_this_year(),
            'account_creation_time': fake.date_time_this_year()
        }
        accounts.append(account)

    return accounts


# Function to insert accounts into the database
def insert_accounts(accounts):
    insert_query = """
    INSERT INTO `Account` (
        `account_type`, `username`, `password`, `first_name`, `last_name`, 
        `email`, `phone`, `social_media_link`, `accessibility_needs`, 
        `account_status`, `last_activity`, `account_creation_time`
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    for account in accounts:
        cursor.execute(insert_query, (
            account['account_type'],
            account['username'],
            account['password'],
            account['first_name'],
            account['last_name'],
            account['email'],
            account['phone'],
            account['social_media_link'],
            account['accessibility_needs'],
            account['account_status'],
            account['last_activity'],
            account['account_creation_time']
        ))
    
    conn.commit()


# Generate and insert synthetic accounts
def generate_and_insert_accounts():
    num_accounts_to_generate = 10  # Specify how many accounts you want to generate
    synthetic_accounts = generate_accounts(num_accounts_to_generate)
    insert_accounts(synthetic_accounts)


# Close the database connection
cursor.close()
conn.close()