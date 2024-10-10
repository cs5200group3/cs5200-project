import mysql.connector

def insert_genres(cursor):
    print("Inserting genres into the database...")
    insert_query = """
    INSERT INTO `Genre` (
        `genre_id`, `genre_name`
    ) VALUES (%s, %s)
    """
    
    genres = ['concert', 'sports', 'art, family & comedy', 'family']
    
    for i, genre in enumerate(genres, start=1):
        cursor.execute(insert_query, (i, genre))
    
    cursor._connection.commit()  # Use _connection to commit the transaction

def main(cursor):
    # Call the function to insert genres
    insert_genres(cursor)
    print("Genres inserted successfully.")

# Database connection configuration for Aiven MySQL
db_config = {
    'host': 'g3-sprint2-just4thedreamland-5e30.h.aivencloud.com',  # Replace with your Aiven hostname
    'port': 26740, 
    'user': 'avnadmin',  # Replace with your Aiven username
    'password': 'AVNS_k8-EKEKB0de1fhIa09w',  # Replace with your Aiven password
    'database': 'Sprint2'  # Replace with your database name
}

# Connect to the database
def connect_to_database():
    print("Connecting to the database...")
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("Database connection established.")
    return conn, cursor

if __name__ == "__main__":
    conn, cursor = None, None
    try:
        conn, cursor = connect_to_database()
        main(cursor)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()