import mysql.connector
import random
from faker import Faker
import order_generator
REFUND_REASON = ['Not able to go to the event due to personal reasons',
                 'Not able to go to the event due to medical situation', 
                 'No specific reasons', 'Other']


def generate_refunds(orders, num_items=10):
    print(f"Generating {num_items} refunds...")
    fake = Faker()
    refunds = []

    # retrieve the payment_id from the orders list where order_status is 'Refunded'
    payment_ids = [order['payment_id'] for order in orders if order['order_status'] == 'Refunded']

    for payment_id in payment_ids:
        refund = {
            'payment_id': payment_id,
            'refund_status': 'Approved',
            'refund_reason': random.choice(REFUND_REASON),
            'admin': 501
        }
        refunds.append(refund)
    print(f"Generated {len(refunds)} refunds.")
    return refunds


def insert_refunds(refunds, cursor, conn, batch_size=50):
    print("Inserting refunds into the database...")
    insert_query = """
    INSERT INTO `Refund` (
        `payment_id`, `refund_status`, `refund_reason`, `admin`
    ) VALUES (%s, %s, %s, %s)
    """
    
    for i in range(0, len(refunds), batch_size):
        batch = refunds[i:i + batch_size]
        cursor.executemany(insert_query, [
            (
                refund['payment_id'],
                refund['refund_status'],
                refund['refund_reason'],
                refund['admin']
            ) for refund in batch
        ])
        conn.commit()  # Commit after each batch
        print(f"Inserted batch {i // batch_size + 1} successfully.")

    print("All refunds inserted successfully.")