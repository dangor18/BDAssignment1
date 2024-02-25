import json
from pymongo import MongoClient

# Function to read data from JSON file
def read_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

# Function to insert data into MongoDB
def insert_data(collection, data):
    collection.insert_many(data)

# Main function
def main():
    # Connect to MongoDB
    client = MongoClient('localhost', 27017)
    db = client['bookstore']
    
    # Read data from JSON files
    users_data = read_json('mongo-seed/users.json')
    books_data = read_json('mongo-seed/books.json')
    
    # Get collections
    users_collection = db['users']
    books_collection = db['books']
    
    # Insert data into respective collections
    insert_data(users_collection, users_data)
    insert_data(books_collection, books_data)
    
    print("Data inserted successfully.")

if __name__ == "__main__":
    main()
