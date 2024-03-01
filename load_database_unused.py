import json
from pymongo import MongoClient

def read_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def main():
    client = MongoClient('localhost', 27017)
    db = client['goodbooks']
    users_data = read_json('mongo-seed/users.json')
    books_data = read_json('mongo-seed/books.json')
    users_collection = db['users']
    books_collection = db['books']
    users_collection.insert_many(users_data)
    books_collection.insert_many(books_data)
    
    print("Data inserted successfully.")

if __name__ == "__main__":
    main()
