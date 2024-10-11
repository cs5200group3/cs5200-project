import mysql.connector

def insert_notificationType(cursor):
    print("Inserting notificationType into the database...")
    insert_query = """
    INSERT INTO `NotificationType` (
        `notification_type_id`, `notification_type`
    ) VALUES (%s, %s)
    """
    
    notificationType = ['System', 'Promotion', 'Order', 'Event', 'Review']
    
    for i, notificationType in enumerate(notificationType, start=1):
        cursor.execute(insert_query, (i, notificationType))
    
    cursor._connection.commit()  # Use _connection to commit the transaction
