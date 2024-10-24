import mysql.connector
import random
from datetime import datetime, timedelta

# Sample action types for requested_action
requested_actions = [
    "Activate", 
    "Deactivate"
]

# Sample reply messages
reply_messages = [
    "Your request has been processed successfully.",
    "We encountered an issue with your request.",
    "Please provide additional information.",
    "Your request is pending approval.",
    "The request was completed. Thank you for your patience."
]

# Function to generate random user requests
def generate_user_requests(num_requests=100):
    user_requests = []
    
    for _ in range(num_requests):
        # Random requester_account_id between 1 and 450
        requester_account_id = random.randint(1, 501)
        
        # Fixed processer_account_id = 501
        processer_account_id = 501
        
        # Random requested action
        requested_action = random.choice(requested_actions)
        
        # Random request time within the past year
        request_time = datetime.now() - timedelta(days=random.randint(1, 365), 
                                                  hours=random.randint(0, 23), 
                                                  minutes=random.randint(0, 59))
        
        # Random reply message
        reply_message = random.choice(reply_messages)
        
        # Random reply time (after request time)
        reply_time = request_time + timedelta(days=random.randint(0, 30), 
                                              hours=random.randint(0, 23), 
                                              minutes=random.randint(0, 59))
        
        # Random boolean value for addressed (True or False)
        addressed = random.choice([True, False])
        
        # Append the generated user request tuple to the list
        user_requests.append((requester_account_id, processer_account_id, requested_action, 
                              request_time, reply_message, reply_time, addressed))
    
    return user_requests

# Function to insert user requests into the UserRequest table
def insert_user_requests(user_requests, cursor, conn, batch_size=50):
    print("Inserting user requests into the database...")
    insert_query = """
    INSERT INTO `UserRequest` (
        `requester_account_id`, `processer_account_id`, `requested_action`, 
        `request_time`, `reply_message`, `reply_time`, `addressed`
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    for i in range(0, len(user_requests), batch_size):
        batch = user_requests[i:i + batch_size]
        cursor.executemany(insert_query, batch)
        conn.commit()  # Commit the transaction after each batch

# Database connection configuration (adjust these parameters)
db_config = {
    'host': 'g3-sprint2-just4thedreamland-5e30.h.aivencloud.com',  # Replace with your Aiven hostname
    'port': 26740, 
    'user': 'avnadmin',  # Replace with your Aiven username
    'password': 'AVNS_k8-EKEKB0de1fhIa09w',  # Replace with your Aiven password
    'database': 'sprint2'  # Replace with your database name
}

# Connect to the database
def connect_to_database():
    print("Connecting to the database...")
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("Database connection established.")
    return conn, cursor

# Main function to generate and insert user requests
def generate_and_insert_user_requests(num_requests=100):
    conn, cursor = connect_to_database()
    try:
        # Generate the random user requests
        user_requests = generate_user_requests(num_requests=num_requests)
        
        # Insert the user requests into the database
        insert_user_requests(user_requests, cursor, conn)
        
        print("Data insertion complete.")
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    generate_and_insert_user_requests(num_requests=100)
