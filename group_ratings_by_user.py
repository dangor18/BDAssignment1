import pandas as pd
import json

# Read the original CSV file
df = pd.read_csv('data/ratings.csv')

# Group by user_id and aggregate book_id and rating as a list of dictionaries
grouped = df.groupby('user_id').apply(lambda x: x[['book_id', 'rating']].apply(lambda y: {'book': y['book_id'], 'rating': y['rating']}, axis=1).tolist())

# Create a new DataFrame with user_id and book_ratings
new_df = pd.DataFrame({'user_id': grouped.index, 'book_ratings': grouped.values})

# Save the new DataFrame to a CSV file
new_df.to_csv('ratings_grouped_by_user.csv', index=False)
