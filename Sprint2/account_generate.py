import mysql.connector
import random
from faker import Faker


# Function to generate a formatted phone number
def generate_phone_number():
    area_code = random.randint(100, 999)  # Generate a random area code
    central_office_code = random.randint(100, 999)  # Generate a random central office code
    line_number = random.randint(1000, 9999)  # Generate a random line number
    return f"({area_code}) {central_office_code} {line_number}"  # Format the phone number


# Function to generate synthetic accounts
def generate_accounts(num_accounts, account_type):
    print(f"Generating {num_accounts} synthetic accounts...")
    fake = Faker()
    accounts = []

    for _ in range(num_accounts):
        account = {
            'account_type': account_type,
            'username': fake.user_name(),
            'password': fake.password(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'phone': generate_phone_number(),  # Use the custom phone number generator
            'accessibility_needs': random.choice(['Wheelchair Accessible', 'Hearing Impaired', 'Visual Impaired']),
            'account_status': random.choice(['Active', 'Inactive']),
            'last_activity': fake.date_time_this_year(),
            'account_creation_time': fake.date_time_this_year()
        }
        accounts.append(account)

    print(f"Generated {len(accounts)} accounts.")
    return accounts


# Function to insert accounts into the database
def insert_accounts(accounts, cursor, conn, batch_size=50):
    print("Inserting accounts into the database...")
    insert_query = """
    INSERT INTO `Account` (
        `account_type`, `username`, `password`, `first_name`, `last_name`, 
        `email`, `phone`, `accessibility_needs`, 
        `account_status`, `last_activity`, `account_creation_time`
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    for i in range(0, len(accounts), batch_size):
        batch = accounts[i:i + batch_size]
        cursor.executemany(insert_query, [
            (
                account['account_type'],
                account['username'],
                account['password'],
                account['first_name'],
                account['last_name'],
                account['email'],
                account['phone'],
                account['accessibility_needs'],
                account['account_status'],
                account['last_activity'],
                account['account_creation_time']
            ) for account in batch
        ])
        conn.commit()  # Commit after each batch
        print(f"Inserted batch {i // batch_size + 1} successfully.")

    print("All accounts inserted successfully.")


# Generate and insert synthetic accounts
def generate_and_insert_accounts(cursor, conn):  # Accept conn as a parameter
    num_organizers = 50
    num_users = 450 
    num_admins = 1
    num_accessibility_needs = 50  # Number of accounts with accessibility needs

    # Generate organizers
    organizers = generate_accounts(num_organizers, 'organizer')
    # Set accessibility needs for 50 organizers (if needed, otherwise keep as 'None')
    for i in range(num_organizers):
        organizers[i]['accessibility_needs'] = 'None'
    
    # Generate users
    users = generate_accounts(num_users, 'user')
    # Set accessibility needs for 50 users
    for i in range(num_accessibility_needs):
        users[i]['accessibility_needs'] = random.choice(['Wheelchair Accessible', 'Hearing Impaired', 'Visual Impaired'])

    # Generate admins
    admins = generate_accounts(num_admins, 'admin')
    # Set accessibility needs for admins (if needed, otherwise keep as 'None')
    for i in range(num_admins):
        admins[i]['accessibility_needs'] = 'None'

    # Combine all accounts
    synthetic_accounts = users + organizers + admins

    # Insert all accounts into the database
    insert_accounts(synthetic_accounts, cursor, conn)  # Now conn is defined
