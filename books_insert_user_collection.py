import csv
import json
import re
import ast

def clean_author_names(author_names):
    # Split author names by comma and space, then remove any non-alphabetic characters
    cleaned_authors = [re.sub(r'[^a-zA-Z\s]', '', author).strip() for author in author_names.split(',')]
    return [author for author in cleaned_authors if author]  # Remove empty strings

def parse_tags(tags_string):
    # Convert the string representation of list into an actual list
    return ast.literal_eval(tags_string)[:3]  # Limit to 3 tags

def csv_to_json(csv_file, json_file):
    # Open the CSV file
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        # Read the CSV file as a dictionary
        reader = csv.DictReader(csvfile)
        # Initialize an empty list to store the data
        data = []
        # Iterate over each row in the CSV file
        for row in reader:
            # Convert ratings counts to dictionary
            rating_counts = {
                f"ratings_{i}": int(row[f"ratings_{i}"]) for i in range(1, 6)
            }
            # Handle case where original publication year is represented as float
            original_publication_year = int(float(row["original_publication_year"])) if row["original_publication_year"] else None
            # Clean and split author names
            authors = clean_author_names(row["authors"])
            # Parse tags
            tags = parse_tags(row["tags"])
            # Create a dictionary for each book
            book_data = {
                "book_id": row["book_id"],
                "isbn": row["isbn"],
                "isbn13": row["isbn13"],
                "authors": authors,
                "original_publication_year": original_publication_year,
                "title": row["title"],
                "language_code": row["language_code"],
                "average_rating": float(row["average_rating"]) if row["average_rating"] else None,
                "ratings_count": int(row["ratings_count"]) if row["ratings_count"] else None,
                "rating_counts": rating_counts,
                "image_url": row["image_url"],
                "tags": tags
            }
            # Append the book data to the list
            data.append(book_data)
    
    # Write the data to a JSON file
    with open(json_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4)

# Specify the input CSV file and output JSON file
csv_file = 'books+tags.csv'
json_file = 'inset_books.json'

# Convert CSV to JSON
csv_to_json(csv_file, json_file)
