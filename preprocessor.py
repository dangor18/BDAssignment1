import pandas as pd

ratings_df = pd.read_csv('data/ratings.csv')
books_df = pd.read_csv('data/books.csv')

merged_df = pd.merge(ratings_df, books_df, on='book_id')

# Initialize a new DataFrame to store the rows until user_id 50
filtered_df = pd.DataFrame()

# Step 3: Iterate through the DataFrame
for index, row in merged_df.iterrows():
    # Check if the user_id equals 50
    if row['user_id'] == 11:
        break  # Stop the loop
    else:
        # Append the row to the filtered_df DataFrame
        filtered_df = filtered_df._append(row)

# Optional: Display the filtered DataFrame
print(filtered_df)