import mysql.connector
import random
from faker import Faker
from datetime import timedelta

def generate_ordertickets(orders, tickets):
    print(f"Generating orderticket...")
    # fake = Faker()
    ordertickets = []
    # orderticket_id = 1
    
    # for order in orders:
    #     ticket = random.choice(tickets)  # Randomly associate a ticket with the order
    #     order_ticket = {
    #         'order_id': order['order_id'],
    #         'ticket_id': ticket['ticket_id'],
    #         'quantity': random.randint(1, 30)  # Random quantity for each order-ticket link
    #     }
    #     ordertickets.append(order_ticket)

    # print(f"Generated {len(ordertickets)} orders.")
    # return ordertickets

    # Group tickets by event_id to ensure we only associate tickets from the same event
    tickets_by_event = {}
    for ticket in tickets:
        event_id = ticket['event_id']
        if event_id not in tickets_by_event:
            tickets_by_event[event_id] = []
        tickets_by_event[event_id].append(ticket)

    # For each order, associate both ticket types (VIP and General Admission) from the same event
    for order in orders:
        # Randomly choose an event from available tickets
        event_id = random.choice(list(tickets_by_event.keys()))
        event_tickets = tickets_by_event[event_id]
        
        # Filter out the tickets by their type (VIP and General Admission)
        vip_tickets = [ticket for ticket in event_tickets if ticket['ticket_type'] == 'VIP']
        general_tickets = [ticket for ticket in event_tickets if ticket['ticket_type'] == 'General Admission']
        
        if vip_tickets and general_tickets:
            # Pick the first VIP and General Admission ticket for this event
            vip_ticket = vip_tickets[0]
            general_ticket = general_tickets[0]
            
            # Add both tickets to the orderticket list
            ordertickets.append({
                'order_id': order['order_id'],
                'ticket_id': vip_ticket['ticket_id'],
                'quantity': random.randint(1, 15)  # Random quantity for VIP
            })
            
            ordertickets.append({
                'order_id': order['order_id'],
                'ticket_id': general_ticket['ticket_id'],
                'quantity': random.randint(1, 35)  # Random quantity for General Admission
            })

    print(f"Generated {len(ordertickets)} ordertickets.")
    return ordertickets


def insert_ordertickets(ordertickets, cursor, conn, batch_size=50):
    print("Inserting orderticket into the database...")
    insert_query = """
    INSERT INTO `OrderTicket` (
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