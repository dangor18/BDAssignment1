import csv
import json
import re
import ast
import itertools

# Limit values
MAX_LINES_TO_READ = 10000000
MAX_RATINGS_PER_BOOK = 10
MAX_TAGS_PER_BOOK = 5  # Specify the maximum number of tags to list for each book

def clean_author_names(author_names):
    # Split author names by comma and space, then remove any non-alphabetic characters
    cleaned_authors = [re.sub(r'[^a-zA-Z\s]', '', author).strip() for author in author_names.split(',')]
    return [author for author in cleaned_authors if author]  # Remove empty strings

def parse_rating_counts(rating_counts_string):
    # Convert the string representation of dictionary into an actual dictionary
    return ast.literal_eval(rating_counts_string)

def parse_tags(tags_string):
    # Convert the string representation of list into an actual list
    tags = ast.literal_eval(tags_string)[:MAX_TAGS_PER_BOOK]  # Limit the number of tags
    return tags

def parse_ratings(ratings_string):
    # Convert the string representation of list into an actual list
    ratings = ast.literal_eval(ratings_string)[:MAX_RATINGS_PER_BOOK]  # Limit the number of ratings
    return ratings

def csv_to_json(csv_file, json_file, to_read_csv):
    print("Starting CSV to JSON conversion...")
    
    # Open the CSV file
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        # Read the CSV file as a dictionary
        reader = csv.DictReader(itertools.islice(csvfile, MAX_LINES_TO_READ))
        # Initialize an empty list to store the data
        data = []
        # Iterate over each row in the CSV file
        for row in reader:
            # Parse rating counts
            rating_counts = parse_rating_counts(row["rating_counts"])
            # Handle case where original publication year is represented as float
            original_publication_year = int(float(row["original_publication_year"])) if row["original_publication_year"] else None
            # Clean and split author names
            authors = clean_author_names(row["authors"])
            # Parse tags
            tags = parse_tags(row["tags"])
            # Get book ratings
            ratings = parse_ratings(row["ratings"])
            # Create a dictionary for each book
            book_data = {
                "book_id": row["work_id"],
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
                "tags": tags,
                "ratings": ratings
            }
            # Append the book data to the list
            data.append(book_data)
    print("CSV to JSON conversion completed.")
    
    # Write the data to a JSON file
    print("Writing JSON file...")
    with open(json_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4)
    print(f"JSON file '{json_file}' written successfully.")

# Specify the input CSV files and output JSON file
csv_file = 'data/merged.csv'
json_file = 'books.json'
to_read_csv = 'to_read_merged.csv'

# Convert CSV to JSON
csv_to_json(csv_file, json_file, to_read_csv)
