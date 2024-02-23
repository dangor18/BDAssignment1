import pandas as pd
from faker import Faker

# number of rows
n = 10000

# create dataframes
ratings_df = (pd.read_csv('data/ratings.csv')).head(n)

# generate random names
fake = Faker()
names = [fake.first_name() for _ in range(n)]
surnames = [fake.last_name() for _ in range(n)]

ratings_df['Name'] = names
ratings_df['Surname'] = surnames
# sort by user_id
ratings_df = ratings_df.sort_values(by='user_id')
books_df = pd.read_csv('data/books.csv')
# split authors
books_df['authors'] = books_df['authors'].str.split(', ')

# drop columms from books.csv
books_df = books_df.drop(['book_id', 'goodreads_book_id', 'best_book_id', 'title', 'work_ratings_count', 'work_text_reviews_count', 'small_image_url'], axis=1)
# rename columns from books.csv
books_df.rename(columns={'work_id': 'book_id'}, inplace=True)
books_df.rename(columns={'original_title': 'title'}, inplace=True)

# merge users to the book data
merged_df = pd.merge(ratings_df, books_df, on='book_id')

book_tags_df = pd.read_csv('data/book_tags.csv')
book_tags_df.rename(columns={'goodreads_book_id': 'book_id'}, inplace=True)
tags_df = pd.read_csv('data/tags.csv')

# merge book_tags with tags
book_tags_merged_df = pd.merge(book_tags_df, tags_df, on='tag_id')

# group tags by book_id
book_tags_grouped_df = book_tags_merged_df.groupby('book_id')['tag_name'].apply(list).reset_index()

# display
print(book_tags_grouped_df)