import pandas as pd
from faker import Faker

def ratings():
    fake = Faker()
    # Read the original CSV file
    df = (pd.read_csv('data/ratings.csv')).head(100000)

    # Generate a unique name for each user_id
    user_ids = df['user_id'].unique()
    names = {user_id: fake.name() for user_id in user_ids}

    df.rename(columns={'book_id': 'work_id'}, inplace=True)
    # Group by book_id and aggregate ratings for each book with user objects
    grouped = df.groupby('work_id').apply(lambda x: x.apply(lambda row: {
        "user": {
            "user_id": row['user_id'],
            "user_name": names[row['user_id']]
        },
        "rating": row['rating']
    }, axis=1).tolist())

    # Create a new DataFrame with book_id and ratings
    new_df = pd.DataFrame({'work_id': grouped.index, 'ratings': grouped.values})
    print(new_df)
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
    print(final_df)
    return final_df

if __name__ == "__main__":
    book_ratings_df = ratings()
    book_tags_df = tags()

    final_df = pd.merge(book_ratings_df, book_tags_df, on='work_id')
    print(final_df)