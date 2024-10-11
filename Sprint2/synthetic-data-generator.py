import mysql.connector
from account_generate import generate_accounts, insert_accounts
from events_generator import generate_events
from ticket_generator import generate_tickets, insert_tickets
from Userrequest_generator import generate_user_requests, insert_user_requests
from payment_generate2 import generate_payments, insert_payments
from Notification_generator import generate_notifications, insert_notifications
from Genre_generator import insert_genres
from UserGenre_generator import generate_random_combinations, insert_combinations

# Global configuration for account generation
NUM_ORGANIZERS = 50
NUM_USERS = 450 
NUM_ADMINS = 1
NUM_INACTIVE_USERS = 30
NUM_EVENTS = 100
NUM_ORDERS = 1000
NUM_REVIEWS = 200
NUM_REFUNTS = 50

# Database connection configuration for Aiven MySQL
db_config = {
    'host': 'g3-sprint2-just4thedreamland-5e30.h.aivencloud.com',  # Replace with your Aiven hostname
    'port': 26740, 
    'user': 'avnadmin',  # Replace with your Aiven username
    'password': 'AVNS_k8-EKEKB0de1fhIa09w',  # Replace with your Aiven password
    'database': 'test_sprint2_shiyuan'  # Replace with your database name
}


# Connect to the database
def connect_to_database():
    print("Connecting to the database...")
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("Database connection established.")
    return conn, cursor

def clean_all_tables(cursor):
    # drop all data in tables
    cursor.execute("DELETE FROM Account")
    cursor.execute("DELETE FROM Genre")
    cursor.execute("DELETE FROM UserGenre")
    cursor.execute("DELETE FROM UserNotificationType")
    cursor.execute("DELETE FROM NotificationType")
    cursor.execute("DELETE FROM Event")
    cursor.execute("DELETE FROM Ticket")
    cursor.execute("DELETE FROM Order")
    cursor.execute("DELETE FROM Payment")
    cursor.execute("DELETE FROM Notification")
    cursor.execute("DELETE FROM Feedback")
    cursor.execute("DELETE FROM Review")
    cursor.execute("DELETE FROM UserRequest")
    cursor.execute("DELETE FROM Refund")


# Main function
def main():
    conn, cursor = connect_to_database()  # Ensure conn is defined
    try:
        # clean all tables
        clean_all_tables(cursor)

        # Generate users
        users = generate_accounts(NUM_USERS, 'user')
        # Set inactive account status for 30 users
        for i in range(NUM_INACTIVE_USERS):
            users[i]['account_status'] = 'Inactive'    
        # Generate organizers
        organizers = generate_accounts(NUM_ORGANIZERS, 'organizer')       
        # Generate admins
        admins = generate_accounts(NUM_ADMINS, 'admin')

    finally:
        # Close the database connection
        cursor.close()
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()