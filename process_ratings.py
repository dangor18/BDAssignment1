import pandas as pd
from faker import Faker
fake = Faker()

# Read the original CSV file
df = pd.read_csv('data/ratings.csv').head(10000)

# Generate a unique name for each user_id
user_ids = df['user_id'].unique()
names = {user_id: fake.name() for user_id in user_ids}

# Group by book_id and aggregate ratings for each book with user objects
grouped = df.groupby('book_id').apply(lambda x: x.apply(lambda row: {
    "user": {
        "user_id": row['user_id'],
        "user_name": names[row['user_id']]
    },
    "rating": row['rating']
}, axis=1).tolist())

# Create a new DataFrame with book_id and ratings
new_df = pd.DataFrame({'book_id': grouped.index, 'ratings': grouped.values})

# Save the new DataFrame to a CSV file
new_df.to_csv('grouped_ratings_with_user_objects.csv', index=False)

print(new_df)