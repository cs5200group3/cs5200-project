import mysql.connector
from account_generate import generate_accounts, insert_accounts
from events_generator import generate_events, insert_events
from genre_generator import insert_genres
from review_generator import generate_reviews, insert_reviews
from feedback_generator import generate_feedbacks, insert_feedbacks
from order_generator import generate_orders, insert_orders
from payment_generator import generate_payments, insert_payments
from refund_generator import generate_refunds, insert_refunds
from orderticket_generator import generate_ordertickets, insert_ordertickets
from tickets_generator import generate_tickets, insert_tickets


# Global configuration for account generation
NUM_ORGANIZERS = 50
NUM_USERS = 450 
NUM_ADMINS = 1
NUM_INACTIVE_USERS = 30
NUM_EVENTS = 100
NUM_ORDERS = 1000
NUM_REVIEWS = 200
NUM_REFUNTS = 50
TABLE_LIST = ['Account', 'Genre', 'UserGenre', 'UserNotificationType', 'NotificationType', 'Event', 'Order', 'Payment', 'Notification', 'Feedback', 'Review', 'UserRequest', 'Refund', 'Ticket', 'OrderTicket']
# Database connection configuration for Aiven MySQL
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


def clean_all_tables(cursor, table_list):
    # Disable foreign key checks
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    
    # Drop all data in tables
    for table in table_list:
        cursor.execute(f"DELETE FROM `{table}`")  # Escaped table name
    
    # Re-enable foreign key checks
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")


def reset_indexes(cursor, table_list):
    for table in table_list:
        cursor.execute(f"ALTER TABLE `{table}` AUTO_INCREMENT = 1")  # Escaped table name


# Main function
def main():
    conn, cursor = connect_to_database()
    try:
        # clean all tables
        clean_all_tables(cursor, TABLE_LIST)
        reset_indexes(cursor, TABLE_LIST)
        
        # Generate users
        users = generate_accounts(NUM_USERS, 'user')
        # Set inactive account status for 30 users
        for i in range(NUM_INACTIVE_USERS):
            users[i]['account_status'] = 'Inactive'    
        # Generate organizers
        organizers = generate_accounts(NUM_ORGANIZERS, 'organizer')       
        # Generate admins
        admins = generate_accounts(NUM_ADMINS, 'admin')

        # Combine all accounts
        synthetic_accounts = users + organizers + admins

        # Insert all accounts into the database
        insert_accounts(synthetic_accounts, cursor, conn)

        # Insert genres into the database
        insert_genres(cursor)

        # Generate events and insert events 
        events = generate_events(organizers, NUM_EVENTS)
        insert_events(events, cursor, conn)
        
        # Generate tickets and insert tickets
        tickets = generate_tickets(events)
        insert_tickets(tickets, cursor, conn)

        # Generate and insert orders, payments, and refunds
        orders = generate_orders(events)
        payments = generate_payments(orders)
        refunds = generate_refunds(orders)
        insert_payments(payments, cursor, conn)
        insert_orders(orders, cursor, conn)
        insert_refunds(refunds, cursor, conn)

        # Generate and insert ordertickets
        ordertickets = generate_ordertickets(orders, tickets)
        insert_ordertickets(ordertickets, cursor, conn)

        reviews = generate_reviews(events, 2)
        insert_reviews(reviews, cursor, conn)
        feedbacks = generate_feedbacks(30)
        insert_feedbacks(feedbacks, cursor, conn)

    finally:
        # Close the database connection
        cursor.close()
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()