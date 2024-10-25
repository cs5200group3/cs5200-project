import mysql.connector
import random

# Function to get the current max user ID from the database
def get_max_user_id(cursor):
    cursor.execute("SELECT IFNULL(MAX(user), 0) FROM UserNotificationType")
    result = cursor.fetchone()
    return result[0]

# Function to generate user notifications, starting from the next available user ID
def generate_user_notifications(start_user_id, num_users=50):
    user_notifications = []
    for user_id in range(start_user_id, start_user_id + num_users):
        for notification_type_id in range(1, 6):  # Loop through notification_type_id 1 to 5
            # Randomly assign True or False for is_enabled
            is_enabled = random.choice([True, False])
            user_notifications.append((user_id, notification_type_id, is_enabled))
    return user_notifications

# Function to generate user notifications for grganizer
def generate_organizer_notifications(start_user_id, num_users=50):
    user_notifications = []
    for user_id in range(start_user_id, start_user_id + num_users):
        for notification_type_id in [1, 4]:  # Loop through notification_type_id 1 and 4 only
            # Randomly assign True or False for is_enabled
            is_enabled = random.choice([True, False])
            user_notifications.append((user_id, notification_type_id, is_enabled))
    return user_notifications

# Function to generate user notifications for admin
def generate_admin_notifications(start_user_id, num_users=50):
    user_notifications = []
    for user_id in range(start_user_id, start_user_id + num_users):
        for notification_type_id in [1]:  # Loop through notification_type_id 1 and 4 only
            # Randomly assign True or False for is_enabled
            is_enabled = random.choice([True, False])
            user_notifications.append((user_id, notification_type_id, is_enabled))
    return user_notifications

# Function to insert user notifications into the database
def insert_user_notifications(user_notifications, cursor, conn, batch_size=50):
    print("Inserting user notifications into the database...")
    insert_query = """
    INSERT INTO `UserNotificationType` (`user`, `notification_type_id`, `is_enabled`)
    VALUES (%s, %s, %s)
    """
    for i in range(0, len(user_notifications), batch_size):
        batch = user_notifications[i:i + batch_size]
        cursor.executemany(insert_query, batch)
        conn.commit()  # Commit the transaction after each batch

# Database connection configuration (adjust these parameters)
db_config = {
    'host': 'g3-sprint2-just4thedreamland-5e30.h.aivencloud.com',  # Replace with your Aiven hostname
    'port': 26740, 
    'user': 'avnadmin',  # Replace with your Aiven username
    'password': 'AVNS_k8-EKEKB0de1fhIa09w',  # Replace with your Aiven password
    'database': 'sprint3'  # Replace with your database name
}

# Connect to the database
def connect_to_database():
    print("Connecting to the database...")
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("Database connection established.")
    return conn, cursor

# Main function to generate and insert the user notifications
def generate_and_insert_user_notifications(num_new_users=450):
    conn, cursor = connect_to_database()
    try:
        # Get the current maximum user ID
        max_user_id = get_max_user_id(cursor)
        print(f"Max user ID in the database is {max_user_id}")
        
        # Generate the random user notifications starting from the next user ID
        user_notifications = generate_user_notifications(start_user_id=max_user_id + 1, num_users=num_new_users)
        
        # Insert the user notifications into the database
        insert_user_notifications(user_notifications, cursor, conn)
        
        print("Data insertion complete.")
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")

def generate_and_insert_organizer_notifications(num_new_users=50):
    conn, cursor = connect_to_database()
    try:
        # Get the current maximum user ID
        max_user_id = get_max_user_id(cursor)
        print(f"Max user ID in the database is {max_user_id}")
        
        # Generate the random user notifications starting from the next user ID
        user_notifications = generate_organizer_notifications(start_user_id=max_user_id + 1, num_users=num_new_users)
        
        # Insert the user notifications into the database
        insert_user_notifications(user_notifications, cursor, conn)
        
        print("Data insertion complete.")
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")

def generate_and_insert_admin_notifications(num_new_users=1):
    conn, cursor = connect_to_database()
    try:
        # Get the current maximum user ID
        max_user_id = get_max_user_id(cursor)
        print(f"Max user ID in the database is {max_user_id}")
        
        # Generate the random user notifications starting from the next user ID
        user_notifications = generate_admin_notifications(start_user_id=max_user_id + 1, num_users=num_new_users)
        
        # Insert the user notifications into the database
        insert_user_notifications(user_notifications, cursor, conn)
        
        print("Data insertion complete.")
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    generate_and_insert_user_notifications(num_new_users=450)
    generate_and_insert_organizer_notifications(num_new_users=50)
    generate_and_insert_admin_notifications(num_new_users=1)
