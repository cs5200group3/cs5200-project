import mysql.connector
import random
from faker import Faker
from datetime import timedelta

NUM_TICKETS_PER_TYPE = 100

def generate_tickets(events):
    print(f"Generating tickets...")
    # fake = Faker()
    tickets = []
    ticket_id = 1
    
    for i in enumerate(events):
        for ticket_type in ['VIP', 'General Admission']:
            # event = random.choice(events)
            # ticket_type = random.choice(['VIP', 'General Admission'])
            
            ticket = {
                'ticket_id': ticket_id,
                'event_id': (i + 1),
                'ticket_type': ticket_type,
                'quantity': NUM_TICKETS_PER_TYPE,
                'price': random.uniform(100, 200) if ticket_type == 'VIP' else random.uniform(50, 100)
            }
            tickets.append(ticket)
            ticket_id += 1

    print(f"Generated {len(tickets)} orders.")
    return tickets


def insert_tickets(tickets, cursor, conn, batch_size=50):
    print("Inserting tickets into the database...")
    insert_query = """
    INSERT INTO `Tickets` (
        `ticket_id`, `event_id`, `ticket_type`, `quantity`, `price`
    ) VALUES (%s, %s, %s, %s, %s)
    """
    
    for i in range(0, len(tickets), batch_size):
        batch = tickets[i:i + batch_size]
        cursor.executemany(insert_query, [
            (
                ticket['ticket_id'],
                ticket['event_id'],
                ticket['ticket_type'],
                ticket['quantity'],
                ticket['price'],
            ) for ticket in batch
        ])
        conn.commit()  # Commit after each batch
        print(f"Inserted batch {i // batch_size + 1} successfully.")

    print("All tickets inserted successfully.")


def generate_and_insert_tickets(cursor, conn, events, num_orders):
    # num_orders = 1000
    tickets = generate_tickets(events)
    insert_tickets(tickets, cursor, conn)


# # Database connection configuration for Aiven MySQL
# db_config = {
#     'host': 'g3-sprint2-just4thedreamland-5e30.h.aivencloud.com',  # Replace with your Aiven hostname
#     'port': 26740, 
#     'user': 'avnadmin',  # Replace with your Aiven username
#     'password': 'AVNS_k8-EKEKB0de1fhIa09w',  # Replace with your Aiven password
#     'database': 'Sprint'  # Replace with your database name
# }


# # Connect to the database
# def connect_to_database():
#     print("Connecting to the database...")
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()
#     print("Database connection established.")
#     return conn, cursor


# # Main function
# def main():
#     conn, cursor = connect_to_database()  # Ensure conn is defined
#     try:
#         print("Starting synthetic data generation...")
#         generate_and_insert_orders(cursor, conn)  # Pass conn to the function
#     finally:
#         # Close the database connection
#         cursor.close()
#         conn.close()
#         print("Database connection closed.")


# if __name__ == "__main__":
#     main()

