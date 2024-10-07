import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'my-secret-pw',
    'database': 'ticcket_db'
}

# Connect to the database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Initialize Faker
fake = Faker()

# Helper function to execute INSERT queries
def execute_insert(query, data):
    try:
        cursor.execute(query, data)
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()

# Generate Account entries
def generate_accounts(num_accounts):
    account_types = ['user', 'organizer', 'admin']
    accessibility_needs = ['visual', 'auditory', 'mobility', None]
    account_statuses = ['active', 'inactive', 'suspended']
    account_ids = []

    for _ in range(num_accounts):
        account_type = random.choice(account_types)
        query = """
        INSERT INTO Account (account_type, username, password, first_name, last_name, email, phone, 
        social_media_link, accessibility_needs, account_status, last_activity, account_creation_time, 
        coordinate_accessibility)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (
            account_type,
            fake.user_name(),
            fake.sha256(),
            fake.first_name(),
            fake.last_name(),
            fake.email(),
            fake.phone_number(),
            f"https://social.com/{fake.user_name()}",
            random.choice(accessibility_needs) if account_type == 'user' else None,
            random.choice(account_statuses),
            fake.date_time_between(start_date="-1y", end_date="now"),
            fake.date_time_between(start_date="-5y", end_date="-1y"),
            random.choice(['yes', 'no']) if account_type == 'organizer' else None
        )
        execute_insert(query, data)
        account_ids.append(cursor.lastrowid)  # Store the generated account ID

    return account_ids
