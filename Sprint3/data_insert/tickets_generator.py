import mysql.connector
import random
from faker import Faker
from datetime import timedelta


def generate_tickets(events):
    print(f"Generating tickets...")
    # fake = Faker()
    tickets = []
    ticket_id = 1
    
    for i, event in enumerate(events):
        total_tickets = event['total_tickets']
        num_tickets_per_type = total_tickets // 2
        for ticket_type in ['VIP', 'General Admission']:
            event = random.choice(events)
            # ticket_type = random.choice(['VIP', 'General Admission'])
            
            ticket = {
                'ticket_id': ticket_id,
                'event_id': (i + 1),
                'ticket_type': ticket_type,
                'quantity': num_tickets_per_type,
                'price': random.uniform(100, 200) if ticket_type == 'VIP' else random.uniform(50, 100)
            }
            tickets.append(ticket)
            ticket_id += 1

    print(f"Generated {len(tickets)} orders.")
    return tickets


def insert_tickets(tickets, cursor, conn, batch_size=50):
    print("Inserting tickets into the database...")
    insert_query = """
    INSERT INTO `Ticket` (
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

