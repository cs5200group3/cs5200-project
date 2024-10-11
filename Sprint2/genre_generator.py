import mysql.connector
import random

# Function to generate random number combinations of random length (1 to 4)
def generate_random_combinations(NUM_USERS):
    combinations = []
    for i in range(1, NUM_USERS + 1):
        # Choose a random length for the combination (between 1 and 4)
        combination_length = random.randint(1, 4)
        random_combination = random.sample([1, 2, 3, 4], combination_length)
        for genre_id in random_combination:
            combinations.append((i, genre_id)) 
    return combinations

# Function to insert combinations into the database
def insert_combinations(combinations, cursor, conn, batch_size=50):
    print("Inserting combinations into the database...")
    insert_query = """
    INSERT INTO `UserGenre` (`user`, `genre_id`)
    VALUES (%s, %s)
    """
    for i in range(0, len(combinations), batch_size):
        batch = combinations[i:i + batch_size]
        cursor.executemany(insert_query, batch)
        conn.commit()  # Commit the transaction after each batch
