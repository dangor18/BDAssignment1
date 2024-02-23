import pandas as pd
from faker import Faker

# number of rows
n = 10000

# create dataframes
ratings_df = (pd.read_csv('data/ratings.csv')).head(n)

# generate random names
fake = Faker()
names = [fake.full_name() for _ in range(n)]
surnames = [fake.last_name() for _ in range(n)]

ratings_df['Name'] = names
ratings_df['Surname'] = surnames
# sort by user_id
ratings_df = ratings_df.sort_values(by='user_id')

books_df = pd.read_csv('data/books.csv')

# drop columms from books.csv
books_df = books_df.drop(['book_id', 'goodreads_book_id', 'best_book_id', 'title', 'work_ratings_count', 'work_text_reviews_count', 'small_image_url'], axis=1)
# rename columns from books.csv
books_df.rename(columns={'work_id': 'book_id'}, inplace=True)
books_df.rename(columns={'original_title': 'title'}, inplace=True)

# merge users to the book data
merged_df = pd.merge(ratings_df, books_df, on='book_id')

# display
print(merged_df)