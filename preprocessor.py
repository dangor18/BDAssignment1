import pandas as pd

# create dataframes
ratings_df = pd.read_csv('data/ratings.csv')
books_df = pd.read_csv('data/books.csv')

# drop columms from books.csv
books_df = books_df.drop(['book_id', 'goodreads_book_id', 'best_book_id', 'title', 'work_ratings_count', 'work_text_reviews_count', 'small_image_url'], axis=1)
# rename columns from books.csv
books_df.rename(columns={'work_id': 'book_id'}, inplace=True)
books_df.rename(columns={'original_title': 'title'}, inplace=True)

merged_df = pd.merge(ratings_df, books_df, on='book_id')

# initialize a new DataFrame to store the rows until user_id 264 (arbitrary)
filtered_df = pd.DataFrame()

# iterate through merged dataframe
for index, row in merged_df.iterrows():
    # check if the user_id equals 264
    if row['user_id'] == 264:
        break
    else:
        # append the row to the filtered_df DataFrame
        filtered_df = filtered_df._append(row)

# display
print(filtered_df)