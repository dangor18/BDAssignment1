import pandas as pd
from faker import Faker

# number of rows
n = 100000

# create dataframes
ratings_df = ((pd.read_csv('data/ratings.csv')).sort_values(by='user_id')).head(n)

# generate random names
fake = Faker()
names = [fake.first_name() for _ in range(n)]
surnames = [fake.last_name() for _ in range(n)]

ratings_df['Name'] = names
ratings_df['Surname'] = surnames
# rearange column order
cols = ratings_df.columns.tolist()

new_order = [cols[0]] + [cols[3], cols[4]] + cols[1:3] + cols[5:]
ratings_df = ratings_df[new_order]
# sort by user_id
# ratings_df = ratings_df.sort_values(by='user_id')
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
books_df = books_df.drop(['book_id', 'goodreads_book_id', 'best_book_id', 'title', 'work_ratings_count', 'work_text_reviews_count', 'small_image_url'], axis=1)
# rename columns from books.csv
books_df.rename(columns={'work_id': 'book_id'}, inplace=True)
books_df.rename(columns={'original_title': 'title'}, inplace=True)
books_df = books_df.sort_values(by='book_id')
# merge users to the book data
books_with_ratings_df = pd.merge(ratings_df, books_df, on='book_id')
print(books_with_ratings_df)

book_tags_df = pd.read_csv('data/book_tags.csv')
book_tags_df.rename(columns={'goodreads_book_id': 'book_id'}, inplace=True)
tags_df = pd.read_csv('data/tags.csv')

# merge book_tags with tags
book_tags_merged_df = pd.merge(book_tags_df, tags_df, on='tag_id')

# group tags by book_id
book_tags_grouped_df = book_tags_merged_df.groupby('book_id')['tag_name'].apply(list).reset_index()
print(book_tags_grouped_df)

books_with_ratings_and_tags_df = pd.merge(books_with_ratings_df, book_tags_grouped_df, on='book_id')
print(books_with_ratings_and_tags_df)

# Group by book_id and aggregate user details
# Assuming books_with_ratings_and_tags_df contains all needed details (ratings and tags included)
# Now, you should aggregate user ratings here, where book details and tags are already merged

# Correctly aggregate user ratings along with the book data that includes tags
user_ratings = books_with_ratings_and_tags_df.groupby('book_id').apply(lambda x: x[['user_id', 'rating', 'Name', 'Surname']].to_dict('records')).reset_index(name='ratings')

# Merge this with books_df if needed, but it seems you already have all book details in books_with_ratings_and_tags_df
# If books_df contains additional details not present in books_with_ratings_and_tags_df, merge those details now

# Since books_with_ratings_and_tags_df already contains book details and tags, you might just need to add the aggregated ratings:
final_df = pd.merge(books_with_ratings_and_tags_df.drop_duplicates(subset=['book_id']), user_ratings, on='book_id', how='left')

# Ensure to drop or select columns as needed to match your final structure, as it seems there might be redundant columns or missing steps in the shared code for the final merge.
final_df.dropna(subset=['ratings'], inplace=True)
print(final_df)
final_df.to_csv("test.csv")