import pandas as pd
import csv

def book_to_user_ratings():
    # read the original CSV file
    df = (pd.read_csv('data/ratings.csv')).head(10000)
    user_names_df = pd.read_csv('user_data.csv')
    df = pd.merge(df, user_names_df, on='user_id')
    #df.rename(columns={'book_id': 'work_id'}, inplace=True)
    # group by book_id and aggregate ratings for each book with user objects
    grouped = df.groupby('book_id').apply(lambda x: x.apply(lambda row: {
        "user": {
            "user_id": row['user_id'],
            "user_name": row['user_name']
        },
        "rating": row['rating']
    }, axis=1).tolist())

    # create a new DataFrame with book_id and ratings
    new_df = pd.DataFrame({'book_id': grouped.index, 'ratings': grouped.values})
    #print(new_df)
    return new_df

def book_to_tags():
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

    # merge book_tags with tags to get the tag names along with their IDs for each book
    book_tags_merged_df = pd.merge(book_tags_df, tags_df, on='tag_id')

    # group tags by book_id and aggregate into a list of dictionaries
    book_tags_grouped = book_tags_merged_df.groupby('goodreads_book_id').apply(lambda x: x[['tag_id', 'tag_name']].apply(lambda row: {'tag_id': row['tag_id'], 'tag_name': row['tag_name']}, axis=1).tolist()).reset_index(name='tags')
    
    final_df = pd.merge(books_df, book_tags_grouped, on='goodreads_book_id')
    #print(final_df)
    return final_df

def user_to_book_ratings():
    # Assuming the necessary CSV files are located in the 'data' directory and named accordingly.
    ratings_df = pd.read_csv('data/ratings.csv').head(10000)
    user_names_df = pd.read_csv('user_data.csv')
    ratings_df = pd.merge(ratings_df, user_names_df, on='user_id')
    
    books_df = pd.read_csv('data/books.csv')
    books_df = books_df.drop(['ratings_1', 'ratings_2', 'ratings_3', 'ratings_4', 'ratings_5', 'best_book_id', 'title', 'work_ratings_count', 'work_text_reviews_count', 'small_image_url'], axis=1)
    books_df.rename(columns={'original_title': 'title'}, inplace=True)
    
    # Merge ratings_df with books_df on 'book_id'
    merged_df = ratings_df.merge(books_df, on='book_id')
    
    # Define a function to structure each book's data as a dictionary
    def book_data(row):
        return {
            'book_id': row['book_id'],
            'rating': row['rating'],
            'goodreads_book_id': row['goodreads_book_id'],
            'title': row['title'],
            'language_code': row['language_code'],
            'average_rating': row['average_rating'],
            'ratings_count': row['ratings_count'],
            'image_url': row['image_url']
        }
    
    # Group by user_id and user_name, then apply the function to each book in the group
    grouped = merged_df.groupby(['user_id', 'user_name']).apply(lambda x: x.apply(book_data, axis=1).tolist()).reset_index(name='books')
    
    # Convert the grouped object into a more friendly format, such as a list of dictionaries
    result = [{
        'user_id': row['user_id'],
        'user_name': row['user_name'],
        'books': row['books']
    } for index, row in grouped.iterrows()]
    result_df = pd.DataFrame(result)
    #print(result_df)
    #return result

def user_to_book_to_read():
    return

def transform_csv(input_csv, output_csv):
    user_books = {}

    # read input CSV and aggregate book IDs for each user
    with open(input_csv, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_id = row['user_id']
            book_id = row['book_id']
            if user_id in user_books:
                user_books[user_id].append(book_id)
            else:
                user_books[user_id] = [book_id]

    # write aggregated data to output CSV
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['user_id', 'book_ids'])
        for user_id, book_ids in user_books.items():
            writer.writerow([user_id, ','.join(book_ids)])

if __name__ == "__main__":
    user_to_book_ratings()
    # book to ratings objects dataframe
    book_ratings_df = book_to_user_ratings()
    #print(book_ratings_df)
    # books to tags object dataframe
    book_tags_df = book_to_tags()
    #print(book_tags_df)

    # merge the two
    final_df = book_tags_df.merge(book_ratings_df, on='book_id')
    #print(final_df)
    
    # write data to a new csv file
    final_df.to_csv('data/merged.csv', index=False)
    # specify input and output CSV file paths
    input_csv = 'data/to_read.csv'
    output_csv = 'to_read_merged.csv'

    # transform CSV
    transform_csv(input_csv, output_csv)
    df = pd.read_csv('data/ratings.csv')

    # group by user_id and aggregate book_id and rating as a list of dictionaries
    grouped = df.groupby('user_id').apply(lambda x: x[['book_id', 'rating']].apply(lambda y: {'book': y['book_id'], 'rating': y['rating']}, axis=1).tolist())

    # create a new DataFrame with user_id and book_ratings
    new_df = pd.DataFrame({'user_id': grouped.index, 'book_ratings': grouped.values})

    # save the new DataFrame to a CSV file
    new_df.to_csv('ratings_grouped_by_user.csv', index=False)
    
    print("Preprocessing completed.")