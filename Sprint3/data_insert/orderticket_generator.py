import mysql.connector
import random
from faker import Faker
from datetime import timedelta

def generate_ordertickets(orders, tickets):
    print(f"Generating orderticket...")
    # fake = Faker()
    ordertickets = []
    # orderticket_id = 1
    
    for order in orders:
        ticket = random.choice(tickets)  # Randomly associate a ticket with the order
        order_ticket = {
            'order_id': order['order_id'],
            'ticket_id': ticket['ticket_id'],
            'quantity': random.randint(1, 80)  # Random quantity for each order-ticket link
        }
        ordertickets.append(order_ticket)

    print(f"Generated {len(ordertickets)} orders.")
    return ordertickets


def insert_ordertickets(ordertickets, cursor, conn, batch_size=50):
    print("Inserting orderticket into the database...")
    insert_query = """
    INSERT INTO `Tickets` (
        `order_id`, `ticket_id`, `quantity`
    ) VALUES (%s, %s, %s)
    """
    
    for i in range(0, len(ordertickets), batch_size):
        batch = ordertickets[i:i + batch_size]
        cursor.executemany(insert_query, [
            (
                orderticket['order_id'],
                orderticket['ticket_id'],
                orderticket['quantity'],
            ) for orderticket in batch
        ])
        conn.commit()  # Commit after each batch
        print(f"Inserted batch {i // batch_size + 1} successfully.")

    print("All orderticket inserted successfully.")


def generate_and_insert_tickets(cursor, conn, events, num_orders):
    # num_orders = 1000
    tickets = generate_ordertickets(events, num_orders)
    insert_ordertickets(tickets, cursor, conn)