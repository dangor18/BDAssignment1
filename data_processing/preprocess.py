import pandas as pd
import csv
import json
import ast
import itertools
import re
import warnings

# Limit values
# Books Collection
MAX_LINES_TO_READ = 10000000
MAX_RATINGS_PER_BOOK = 50
MAX_TAGS_PER_BOOK = 50

# Users collections
MAX_TAGS = 5
MAX_TO_READ = 10
MAX_RATINGS_BOOK = 100

warnings.filterwarnings("ignore", category=DeprecationWarning)

def book_to_user_ratings():
    # read the original CSV file
    df = (pd.read_csv('data_processing/data/ratings.csv')).head(10000)
    user_names_df = pd.read_csv('data_processing/data/user_data.csv')
    df = pd.merge(df, user_names_df, on='user_id')
    #df.rename(columns={'book_id': 'work_id'}, inplace=True)
    # group by book_id and aggregate ratings for each book with user objects
    grouped = df.groupby('book_id').apply(lambda x: x.apply(lambda row: {
        "user": {
            "user_id": row['user_id'],
            "user_name": row['user_name']
        },
        "rating": row['rating']
    }, axis=1).tolist())

    # create a new DataFrame with book_id and ratings
    new_df = pd.DataFrame({'book_id': grouped.index, 'ratings': grouped.values})
    #print(new_df)
    return new_df

def book_to_tags():
    books_df = pd.read_csv('data_processing/data/books.csv')
    # split authors
    books_df['authors'] = books_df['authors'].str.split(', ')
    # iterate over each row and create a dictionary over ratings_x col's
    books_df['rating_counts'] = books_df.apply(lambda row: {
        'ratings_1': row['ratings_1'],
        'ratings_2': row['ratings_2'],
        'ratings_3': row['ratings_3'],
        'ratings_4': row['ratings_4'],
        'ratings_5': row['ratings_5']
    }, axis=1)
    # drop columms from books.csv
    books_df = books_df.drop(['ratings_1', 'ratings_2', 'ratings_3', 'ratings_4', 'ratings_5'], axis=1)
    books_df = books_df.drop(['best_book_id', 'title', 'work_ratings_count', 'work_text_reviews_count', 'small_image_url'], axis=1)
    # rename columns from books.csv
    books_df.rename(columns={'original_title': 'title'}, inplace=True)
    books_df = books_df.sort_values(by='work_id')

    book_tags_df = pd.read_csv('data_processing/data/book_tags.csv')
    tags_df = pd.read_csv('data_processing/data/tags.csv')

    # merge book_tags with tags to get the tag names along with their IDs for each book
    book_tags_merged_df = pd.merge(book_tags_df, tags_df, on='tag_id')

    # group tags by book_id and aggregate into a list of dictionaries
    book_tags_grouped = book_tags_merged_df.groupby('goodreads_book_id').apply(lambda x: x[['tag_id', 'tag_name']].apply(lambda row: {'tag_id': row['tag_id'], 'tag_name': row['tag_name']}, axis=1).tolist()[:MAX_TAGS]).reset_index(name='tags')
    
    final_df = pd.merge(books_df, book_tags_grouped, on='goodreads_book_id')
    final_df = final_df.dropna()
    #print(final_df)
    return final_df

def user_to_book_ratings():
    # read files
    ratings_df = pd.read_csv('data_processing/data/ratings.csv').head(10000)
    user_names_df = pd.read_csv('data_processing/data/user_data.csv')
    ratings_df = pd.merge(ratings_df, user_names_df, on='user_id')
    
    books_df = book_to_tags()
    merged_df = books_df.merge(ratings_df, on='book_id')
    #merged_df.to_csv("test.csv")
    
    grouped = merged_df.groupby(['user_id', 'user_name']).apply(lambda x: x.apply(lambda row: {
        "book": {
            "book_id": row['book_id'],
            "goodreads_book_id": row['goodreads_book_id'],
            "work_id": row['work_id'],
            "authors": row['authors'],
            "title": row['title'],
            "isbn": row['isbn'],
            "isbn13": row['isbn13'],
            "language_code": row['language_code'],
            "average_rating": row['average_rating'],
            "ratings_count": row['ratings_count'],
            "image_url": row['image_url'],
            "tags": row["tags"]
        },
        "rating": row['rating']
    }, axis=1).tolist()[:MAX_RATINGS_BOOK]).reset_index(name='ratings')

    grouped_df = grouped[['user_id', 'user_name', 'ratings']]
    #print(grouped_df)
    #grouped_df.to_csv("test.csv")
    return grouped_df

def user_to_read():
    # read files
    read_df = pd.read_csv('data_processing/data/to_read.csv')
    ratings_df = pd.read_csv('data_processing/data/ratings.csv').head(10000)
    
    # only get users to_read data who you're taking from ratings for consistency
    ratings_df = ratings_df.drop(['book_id', 'rating'], axis=1)
    read_df = pd.merge(ratings_df, read_df, on='user_id')
    
    # add user names
    user_names_df = pd.read_csv('data_processing/data/user_data.csv')
    read_df = pd.merge(read_df, user_names_df, on='user_id')
    
    books_df = book_to_tags()
    merged_df = books_df.merge(read_df, on='book_id')
    
    grouped = merged_df.groupby('user_id').apply(lambda x: x.apply(lambda row: {
        "book": {
            "book_id": row['book_id'],
            "goodreads_book_id": row['goodreads_book_id'],
            "work_id": row['work_id'],
            "authors": row['authors'],
            "title": row['title'],
            "isbn": row['isbn'],
            "isbn13": row['isbn13'],
            "language_code": row['language_code'],
            "average_rating": row['average_rating'],
            "ratings_count": row['ratings_count'],
            "image_url": row['image_url'],
            "tags": row["tags"]
        }
    }, axis=1).tolist()[:MAX_TO_READ])

    grouped_df = pd.DataFrame({'user_id': grouped.index, 'to_read': grouped.values})
    #print(grouped_df)
    #grouped_df.to_csv("test.csv")
    return grouped_df

# User data parsing -----------------------------------------------------------
def user_dataframe_to_json(dataframe):
    # Initialize an empty list to store the final JSON objects
    json_data = []

    # Iterate over each row in the DataFrame
    for index, row in dataframe.iterrows():
        user_id = row['user_id']
        user_name = row['user_name']

        # Replace NaN values with "nan"
        ratings_str = str(row['ratings'])
        to_read_str = str(row['to_read'])

        # Initialize ratings and to_read as empty lists
        ratings = []
        to_read = []

        # Parse the ratings column
        if ratings_str != "":
           try:
               ratings = ast.literal_eval(ratings_str)
           except ValueError as e:
               pass
               #print(f"Error parsing ratings JSON for user {user_id}: {e}")

           # Parse the to_read column
           if to_read_str != "":
               try:
                   to_read = ast.literal_eval(to_read_str)
               except ValueError as e:
                   pass
                   #print(f"Error parsing to_read JSON for user {user_id}: {e}")

        # Create the JSON object for the user
        user_json = {
            "user_id": user_id,
            "user_name": user_name,
            "ratings": ratings,
            "to_read": to_read
        }

        json_data.append(user_json)
    return json_data

# Book data parsing -----------------------------------------------------------

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

def csv_to_json(csv_file, json_file):
    #print("Starting CSV to JSON conversion...")
    
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
    #print("CSV to JSON conversion completed.")
    
    # Write the data to a JSON file
    #print("Writing JSON file...")
    with open(json_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4)
    #print(f"JSON file '{json_file}' written successfully.")

if __name__ == "__main__":
    # book to ratings objects dataframe
    book_ratings_df = book_to_user_ratings()
    
    # books to tags object dataframe
    book_tags_df = book_to_tags()

    # merge the two
    book_final_df = book_tags_df.merge(book_ratings_df, on='book_id')
    #print(book_final_df)
    # write data to a new csv file
    book_final_df.to_csv('data_processing/data/book_final.csv', index=False)
    

    # merge for user data
    user_final_df = user_to_book_ratings().merge(user_to_read(), on='user_id', how='left')
    #print(user_final_df)

    #user_final_df.to_csv('data_processing/data/user_final.csv', index=False)
    
    # Specify the input CSV files and output JSON file
    csv_file = 'data_processing/data/book_final.csv'
    json_file = 'books.json'

    # Convert CSV to JSON
    csv_to_json(csv_file, json_file)
    
    with open('users.json', 'w', encoding='utf-8') as json_file:
        json.dump(user_dataframe_to_json(user_final_df), json_file, indent=4)

    