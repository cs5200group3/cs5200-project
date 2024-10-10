# ticket_generator.py
import random
from faker import Faker

# Function to generate synthetic tickets
def generate_tickets(valid_orders, valid_users, valid_events, num_tickets=100):
    print(f"Generating {num_tickets} synthetic tickets...")
    fake = Faker()
    ticket_types = ['General Admission', 'VIP']
    tickets = []

    for _ in range(num_tickets):
        ticket = {
            'order_id': random.choice(valid_orders),  # Select a valid order_id
            'user': random.choice(valid_users),  # Select a valid user_id
            'event_id': random.choice(valid_events),  # Select a valid event_id
            'ticket_type': random.choice(ticket_types),
            'current_price': round(random.uniform(20.0, 200.0), 2),  # current_price between 20 and 200
            'perks': fake.sentence(nb_words=5),  # perks description
            'sold': random.choice([True, False])  # sold status
        }
        tickets.append(ticket)

    print(f"Generated {len(tickets)} tickets.")
    return tickets

# Function to insert tickets into the database
def insert_tickets(tickets, cursor, conn, batch_size=50):
    print("Inserting tickets into the database...")
    insert_query = """
    INSERT INTO `Ticket` (
        `order_id`, `user`, `event_id`, `ticket_type`, `current_price`, `perks`, `sold`
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    for i in range(0, len(tickets), batch_size):
        batch = tickets[i:i + batch_size]
        cursor.executemany(insert_query, [
            (
                ticket['order_id'],
                ticket['user'],
                ticket['event_id'],
                ticket['ticket_type'],
                ticket['current_price'],
                ticket['perks'],
                ticket['sold']
            ) for ticket in batch
        ])
        conn.commit()  # Commit after each batch
        print(f"Inserted batch {i // batch_size + 1} successfully.")

    print("All tickets inserted successfully.")