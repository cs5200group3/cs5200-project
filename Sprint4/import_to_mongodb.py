import json
from pymongo import MongoClient

# Load the JSON data from your file
with open('fake_events_concert_data.json', 'r') as file:
    data = json.load(file)

# MongoDB Atlas connection string
connection_string = "mongodb+srv://csycsy623:cs5200@cluster0.eenjl.mongodb.net/"
# Create a MongoClient to connect to the MongoDB Atlas cluster
client = MongoClient(connection_string)

# Specify the database and collection
db = client['Sprint4Database']  # Replace with your database name
collection = db['event_data']  # Replace with your collection name

# Insert the data into the collection
result = collection.insert_many(data)

# Print the result
print(f"Inserted {len(result.inserted_ids)} documents into the collection.")