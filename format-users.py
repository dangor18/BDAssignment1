import pandas as pd
import json
import ast
import os

# Define the limit values
MAX_LINES_READ = 100000
MAX_ITEMS_NESTED = 2
MAX_RATINGS_PER_USER = 2  # Limit the number of ratings per user
MAX_USERS = 10000

# Read the CSV files with limits
user_data = pd.read_csv('user_data.csv', nrows=MAX_LINES_READ)
ratings_grouped_by_user = pd.read_csv('ratings_grouped_by_user.csv', nrows=MAX_LINES_READ)
to_read_merged = pd.read_csv('to_read_merged.csv', nrows=MAX_LINES_READ)

# Merge user_data and ratings_grouped_by_user on user_id
merged_data = pd.merge(user_data, ratings_grouped_by_user, on='user_id')

# Initialize an empty list to store the final JSON objects
json_data = []

## Iterate over each row in the merged data with limit for number of lines
for index, row in merged_data.iterrows():
    if index >= MAX_USERS:
        break  # Break loop if we've reached the limit of 10 items
    
    user_id = row['user_id']
    user_name = row['user_name']
    book_ratings_str = row['book_ratings']
    
    # Convert string representation of list of dictionaries to actual list of dictionaries
    book_ratings = ast.literal_eval(book_ratings_str)
    
    # Apply the nested limit to the number of ratings per user
    book_ratings = book_ratings[:MAX_RATINGS_PER_USER]
    
    # Extract book IDs to be read if available
    to_read_books_ids = []
    to_read_row = to_read_merged[to_read_merged['user_id'] == user_id]
    if not to_read_row.empty:
        to_read_books_ids = [int(book_id) for book_id in to_read_row['book_ids'].iloc[0].split(',') if book_id]
    
    # Create the to_read section in the same format as ratings
    to_read_books = [{"book_id": str(book_id)} for book_id in to_read_books_ids]
    
    # Create the JSON object
    user_json = {
        "user_id": user_id,
        "user_name": user_name,
        "to_read": to_read_books[:MAX_ITEMS_NESTED],
        "ratings": [{"book_id": str(book['book']), "rating": book['rating']} for book in book_ratings]
    }
    
    # Append the JSON object to the list
    json_data.append(user_json)

# Write the JSON data to the users.json file using the specified format
with open('users-collection.json', 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, indent=4)
