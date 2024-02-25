import pandas as pd
import json
import ast  # Import ast module to safely evaluate literal strings
import os

# Read the CSV file from the data folder
user_final = pd.read_csv(os.path.join('data', 'user_final.csv'))

# Initialize an empty list to store the final JSON objects
json_data = []

# Iterate over each row in the user_final data
for index, row in user_final.iterrows():
    user_id = row['user_id']
    user_name = row['user_name']
    
    # Replace NaN values with "nan"
    ratings_str = str(row['ratings']).replace("nan", '"nan"')
    to_read_str = str(row['to_read']).replace("nan", '"nan"')
    
    print(user_id, "bruhhuhhuhuhhhhhhhhhhhhhhh")
    # Parse the ratings column
    print(ratings_str, "ratings_str")
    if ratings_str != "":
        try:
            ratings = ast.literal_eval(ratings_str)
        except ValueError as e:
            #print(f"Error parsing ratings JSON for user {user_id}: {e}")
            ratings = []
    
    if to_read_str != "":
        # Parse the to_read column
        try:
            print(to_read_str, "to_read_str")
            to_read = ast.literal_eval(to_read_str)
        except ValueError as e:
            #print(f"Error parsing to_read JSON for user {user_id}: {e}")
            to_read = []
    
    # Create the JSON object for the user
    user_json = {
        "user_id": user_id,
        "user_name": user_name,
        "ratings": ratings,
        "to_read": to_read
    }
    
    # Append the user JSON object to the list
    json_data.append(user_json)

# Write the JSON data to the users.json file using the specified format
with open('users.json', 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, indent=4)
