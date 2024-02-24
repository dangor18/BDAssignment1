import pandas as pd
from faker import Faker

# number of rows
n = 100000

# create dataframes
# ratings_df = ((pd.read_csv('data/ratings.csv')).sort_values(by='user_id')).head(n)

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
books_df = books_df.drop(['work_id', 'goodreads_book_id', 'best_book_id', 'title', 'work_ratings_count', 'work_text_reviews_count', 'small_image_url'], axis=1)
# rename columns from books.csv
#books_df.rename(columns={'work_id': 'book_id'}, inplace=True)
books_df.rename(columns={'original_title': 'title'}, inplace=True)
books_df = books_df.sort_values(by='book_id')
# merge users to the book data
#books_with_ratings_df = pd.merge(ratings_df, books_df, on='book_id')
#print(books_with_ratings_df)

book_tags_df = pd.read_csv('data/book_tags.csv')
book_tags_df.rename(columns={'goodreads_book_id': 'book_id'}, inplace=True)
tags_df = pd.read_csv('data/tags.csv')

# Merge book_tags with tags to get the tag names along with their IDs for each book
book_tags_merged_df = pd.merge(book_tags_df, tags_df, on='tag_id')

# Group tags by book_id and aggregate into a list of dictionaries
book_tags_grouped = book_tags_merged_df.groupby('book_id').apply(lambda x: x[['tag_id', 'tag_name']].apply(lambda row: {'tag_id': row['tag_id'], 'tag_name': row['tag_name']}, axis=1).tolist()).reset_index(name='tags')
print(book_tags_grouped)
print(books_df)
final_df = pd.merge(books_df, book_tags_grouped, on='book_id')

print(final_df)