import mysql.connector
import random

# Function to generate random number combinations of random length (1 to 4)
def generate_random_combinations(NUM_USERS=450):
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

# # Database connection configuration (adjust these parameters)
# db_config = {
#     'host': 'g3-sprint2-just4thedreamland-5e30.h.aivencloud.com',  # Replace with your Aiven hostname
#     'port': 26740, 
#     'user': 'avnadmin',  # Replace with your Aiven username
#     'password': 'AVNS_k8-EKEKB0de1fhIa09w',  # Replace with your Aiven password
#     'database': 'sprint3'  # Replace with your database name
# }

# # Connect to the database
# def connect_to_database():
#     print("Connecting to the database...")
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()
#     print("Database connection established.")
#     return conn, cursor

# # Main function to generate and insert the combinations
# def generate_and_insert_combinations():
#     conn, cursor = connect_to_database()
#     try:
#         # Generate the random combinations
#         combinations = generate_random_combinations()
        
#         # Insert the combinations into the database
#         insert_combinations(combinations, cursor, conn)
        
#         print("Data insertion complete.")
#     finally:
#         cursor.close()
#         conn.close()
#         print("Database connection closed.")

# if __name__ == "__main__":
#     generate_and_insert_combinations()
