import pandas as pd
from faker import Faker
import csv


def ratings():
    # Read the original CSV file
    df = (pd.read_csv('data/ratings.csv')).head(100000)
    user_names_df = pd.read_csv('user_data.csv')
    df = pd.merge(df, user_names_df, on='user_id')
    
    df.rename(columns={'book_id': 'work_id'}, inplace=True)
    # Group by book_id and aggregate ratings for each book with user objects
    grouped = df.groupby('work_id').apply(lambda x: x.apply(lambda row: {
        "user": {
            "user_id": row['user_id'],
            "user_name": row['user_name']
        },
        "rating": row['rating']
    }, axis=1).tolist())

    # Create a new DataFrame with book_id and ratings
    new_df = pd.DataFrame({'work_id': grouped.index, 'ratings': grouped.values})
    #print(new_df)
    return new_df

def tags():
    books_df = pd.read_csv('data/books.csv')
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

    book_tags_df = pd.read_csv('data/book_tags.csv')
    tags_df = pd.read_csv('data/tags.csv')

    # Merge book_tags with tags to get the tag names along with their IDs for each book
    book_tags_merged_df = pd.merge(book_tags_df, tags_df, on='tag_id')

    # Group tags by book_id and aggregate into a list of dictionaries
    book_tags_grouped = book_tags_merged_df.groupby('goodreads_book_id').apply(lambda x: x[['tag_id', 'tag_name']].apply(lambda row: {'tag_id': row['tag_id'], 'tag_name': row['tag_name']}, axis=1).tolist()).reset_index(name='tags')

    final_df = pd.merge(books_df, book_tags_grouped, on='goodreads_book_id')
    #print(final_df)
    return final_df

def transform_csv(input_csv, output_csv):
    user_books = {}

    # Read input CSV and aggregate book IDs for each user
    with open(input_csv, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_id = row['user_id']
            book_id = row['book_id']
            if user_id in user_books:
                user_books[user_id].append(book_id)
            else:
                user_books[user_id] = [book_id]

    # Write aggregated data to output CSV
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['user_id', 'book_ids'])
        for user_id, book_ids in user_books.items():
            writer.writerow([user_id, ','.join(book_ids)])



if __name__ == "__main__":
    book_ratings_df = ratings()
    book_tags_df = tags()

    final_df = pd.merge(book_ratings_df, book_tags_df, on='work_id')
    #print(final_df)
    # write data to a new csv file
    final_df.to_csv('data/merged.csv', index=False)
    # Specify input and output CSV file paths
    input_csv = 'data/to_read.csv'
    output_csv = 'to_read_merged.csv'

    # Transform CSV
    transform_csv(input_csv, output_csv)
    df = pd.read_csv('data/ratings.csv')

    # Group by user_id and aggregate book_id and rating as a list of dictionaries
    grouped = df.groupby('user_id').apply(lambda x: x[['book_id', 'rating']].apply(lambda y: {'book': y['book_id'], 'rating': y['rating']}, axis=1).tolist())

    # Create a new DataFrame with user_id and book_ratings
    new_df = pd.DataFrame({'user_id': grouped.index, 'book_ratings': grouped.values})

    # Save the new DataFrame to a CSV file
    new_df.to_csv('ratings_grouped_by_user.csv', index=False)
    
    print("Preprocessing completed.")


