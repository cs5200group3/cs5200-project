import json
from pymongo import MongoClient


# Function to load JSON data from a file
def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


# Load the JSON data from multiple files
data1 = load_json_file('event-details-arts-theatre-comedy.json')
data2 = load_json_file('Event_family.json')
data3 = load_json_file('fake_events_concert_data.json')

# Combine all data into a single list
combined_data = data1 + data2 + data3

# MongoDB Atlas connection string
connection_string = "mongodb+srv://csycsy623:cs5200@cluster0.eenjl.mongodb.net/"
# Create a MongoClient to connect to the MongoDB Atlas cluster
client = MongoClient(connection_string)

# Specify the database and collection
db = client['Sprint4Database']  # Replace with your database name
collection = db['sprint4']  # Replace with your collection name

# Insert the combined data into the collection
result = collection.insert_many(combined_data)

# Print the result
print(f"Inserted {len(result.inserted_ids)} documents into the collection.")