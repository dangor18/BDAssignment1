import pandas as pd
import csv
import json
import ast
import itertools
import re
import warnings

# books collection
MAX_LINES_TO_READ = 10000000
MAX_RATINGS_PER_BOOK = 50
MAX_TAGS_PER_BOOK = 50

# users collections
MAX_TAGS = 5
MAX_TO_READ = 10
MAX_RATINGS_BOOK = 100

warnings.filterwarnings("ignore", category=DeprecationWarning)

def book_to_user_ratings():
    df = (pd.read_csv('data_processing/data/ratings.csv')).head(10000)
    user_names_df = pd.read_csv('data_processing/data/user_data.csv')
    df = pd.merge(df, user_names_df, on='user_id')
    grouped = df.groupby('book_id').apply(lambda x: x.apply(lambda row: {
        "user": {
            "user_id": row['user_id'],
            "user_name": row['user_name']
        },
        "rating": row['rating']
    }, axis=1).tolist())
    new_df = pd.DataFrame({'book_id': grouped.index, 'ratings': grouped.values})
    return new_df

def book_to_tags():
    books_df = pd.read_csv('data_processing/data/books.csv')
    books_df['authors'] = books_df['authors'].str.split(', ')    
    books_df['total_ratings'] = books_df.apply(lambda row: {
        'ratings_1': row['ratings_1'],
        'ratings_2': row['ratings_2'],
        'ratings_3': row['ratings_3'],
        'ratings_4': row['ratings_4'],
        'ratings_5': row['ratings_5']
    }, axis=1)
    books_df = books_df.drop(['ratings_1', 'ratings_2', 'ratings_3', 'ratings_4', 'ratings_5'], axis=1)
    books_df = books_df.drop(['best_book_id', 'title', 'work_ratings_count', 'work_text_reviews_count', 'small_image_url'], axis=1)
    
    books_df.rename(columns={'original_title': 'title'}, inplace=True)
    books_df = books_df.sort_values(by='work_id')
    book_tags_df = pd.read_csv('data_processing/data/book_tags.csv')
    tags_df = pd.read_csv('data_processing/data/tags.csv')

    book_tags_merged_df = pd.merge(book_tags_df, tags_df, on='tag_id')
    book_tags_grouped = book_tags_merged_df.groupby('goodreads_book_id').apply(lambda x: x[['tag_id', 'tag_name']].apply(lambda row: {'tag_id': row['tag_id'], 'tag_name': row['tag_name']}, axis=1).tolist()[:MAX_TAGS]).reset_index(name='tags')
    final_df = pd.merge(books_df, book_tags_grouped, on='goodreads_book_id')
    final_df = final_df.dropna()
    return final_df

def user_to_book_ratings():
    ratings_df = pd.read_csv('data_processing/data/ratings.csv').head(10000)
    user_names_df = pd.read_csv('data_processing/data/user_data.csv')
    ratings_df = pd.merge(ratings_df, user_names_df, on='user_id')
    books_df = book_to_tags()
    merged_df = books_df.merge(ratings_df, on='book_id')
    
    grouped = merged_df.groupby(['user_id', 'user_name']).apply(lambda x: x.apply(lambda row: {
        "book": {
            "book_id": row['book_id'],
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
    return grouped_df

def user_to_read():
    read_df = pd.read_csv('data_processing/data/to_read.csv')
    ratings_df = pd.read_csv('data_processing/data/ratings.csv').head(10000)
    ratings_df = ratings_df.drop(['book_id', 'rating'], axis=1)
    read_df = pd.merge(ratings_df, read_df, on='user_id')
    user_names_df = pd.read_csv('data_processing/data/user_data.csv')
    read_df = pd.merge(read_df, user_names_df, on='user_id')    
    books_df = book_to_tags()
    merged_df = books_df.merge(read_df, on='book_id')
    
    grouped = merged_df.groupby('user_id').apply(lambda x: x.apply(lambda row: {
        "book": {
            "book_id": row['book_id'],
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
    return grouped_df

# User data parsing -----------------------------------------------------------

def user_dataframe_to_json(dataframe):
    json_data = []

    for index, row in dataframe.iterrows():
        user_id = row['user_id']
        user_name = row['user_name']
        ratings_str = str(row['ratings'])
        to_read_str = str(row['to_read'])
        ratings = []
        to_read = []

        if ratings_str != "":
           try:
               ratings = ast.literal_eval(ratings_str)
           except ValueError as e:
               pass

           if to_read_str != "":
               try:
                   to_read = ast.literal_eval(to_read_str)
               except ValueError as e:
                   pass
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
    cleaned_authors = [re.sub(r'[^a-zA-Z\s]', '', author).strip() for author in author_names.split(',')]
    return [author for author in cleaned_authors if author]

def parse_rating_counts(rating_counts_string):
    return ast.literal_eval(rating_counts_string)

def parse_tags(tags_string):
    tags = ast.literal_eval(tags_string)[:MAX_TAGS_PER_BOOK]
    return tags

def parse_ratings(ratings_string):
    ratings = ast.literal_eval(ratings_string)[:MAX_RATINGS_PER_BOOK] 
    return ratings

def csv_to_json(csv_file, json_file):
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(itertools.islice(csvfile, MAX_LINES_TO_READ))
        data = []
        for row in reader:
            rating_counts = parse_rating_counts(row["total_ratings"])
            original_publication_year = int(float(row["original_publication_year"])) if row["original_publication_year"] else None
            authors = clean_author_names(row["authors"])
            tags = parse_tags(row["tags"])
            ratings = parse_ratings(row["ratings"])
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
                "total_ratings": rating_counts,
                "image_url": row["image_url"],
                "tags": tags,
                "ratings": ratings
            }
            data.append(book_data)

    with open(json_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4)

if __name__ == "__main__":
    book_ratings_df = book_to_user_ratings()
    
    book_tags_df = book_to_tags()
    book_final_df = book_tags_df.merge(book_ratings_df, on='book_id')
    
    book_final_df.to_csv('data_processing/data/book_final.csv', index=False)
    user_final_df = user_to_book_ratings().merge(user_to_read(), on='user_id', how='left')

    csv_file = 'data_processing/data/book_final.csv'
    json_file = 'books.json'

    csv_to_json(csv_file, json_file)
    
    with open('users.json', 'w', encoding='utf-8') as json_file:
        json.dump(user_dataframe_to_json(user_final_df), json_file, indent=4)