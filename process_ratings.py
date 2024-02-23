import pandas as pd

# Read the original CSV file
df = pd.read_csv('data/ratings.csv')

# Group by book_id and aggregate ratings for each book
grouped = df.groupby('book_id').apply(lambda x: x[['user_id', 'rating']].values.tolist())

# Create a new DataFrame with book_id and ratings
new_df = pd.DataFrame({'book_id': grouped.index, 'ratings': grouped.values})

# Replace NaN values with an empty list
new_df['ratings'].fillna(value=pd.Series([[]] * len(new_df)), inplace=True)

# Save the new DataFrame to a CSV file
new_df.to_csv('grouped_ratings.csv', index=False)
