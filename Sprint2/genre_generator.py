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

# Connect to the databas