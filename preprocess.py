import pandas as pd
import csv

# tags per book
MAX_TAGS = 5

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

""""
def book_to_read():
    # read files
    read_df = pd.read_csv('data/to_read.csv')
    ratings_df = pd.read_csv('data/ratings.csv').head(10000)
    
    # only get users to_read data who you're taking from ratings for consistency
    ratings_df = ratings_df.drop(['book_id', 'rating'], axis=1)
    read_df = pd.merge(ratings_df, read_df, on='user_id')
    
    # group by book_id and aggregate ratings for each book with user objects
    grouped = read_df.groupby('book_id').apply(lambda x: x.apply(lambda row: {
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
"""

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
    book_tags_grouped = book_tags_merged_df.groupby('goodreads_book_id').apply(lambda x: x[['tag_id', 'tag_name']].apply(lambda row: {'tag_id': row['tag_id'], 'tag_name': row['tag_name']}, axis=1).tolist()[:MAX_TAGS]).reset_index(name='tags')
    
    final_df = pd.merge(books_df, book_tags_grouped, on='goodreads_book_id')
    #print(final_df)
    return final_df

def user_to_book_ratings():
    # read files
    ratings_df = pd.read_csv('data/ratings.csv').head(10000)
    user_names_df = pd.read_csv('user_data.csv')
    ratings_df = pd.merge(ratings_df, user_names_df, on='user_id')
    
    books_df = book_to_tags()
    merged_df = ratings_df.merge(books_df, on='book_id')
    
    grouped = merged_df.groupby(['user_id', 'user_name']).apply(lambda x: x.apply(lambda row: {
        "book": {
            "book_id": row['book_id'],
            "goodreads_book_id": row['goodreads_book_id'],
            "work_id": row['work_id'],
            "authors": row['authors'],
            "title": row['title'],
            "isbn": row['isbn'],
            "isbn13": row['isbn13'],
            "language_code": row['language_code'],
            "average_rating": row['average_rating'],
            "ratings_count": row['ratings_count'],
            "image_url": row['image_url'],
            "tags": row["tags"]
        },
        "rating": row['rating']
    }, axis=1).tolist()).reset_index(name='ratings')

    grouped_df = grouped[['user_id', 'user_name', 'ratings']]
    #print(grouped_df)
    #grouped_df.to_csv("test.csv")
    return grouped_df

def user_to_read():
    # read files
    read_df = pd.read_csv('data/to_read.csv')
    ratings_df = pd.read_csv('data/ratings.csv').head(10000)
    
    # only get users to_read data who you're taking from ratings for consistency
    ratings_df = ratings_df.drop(['book_id', 'rating'], axis=1)
    read_df = pd.merge(ratings_df, read_df, on='user_id')
    
    # add user names
    user_names_df = pd.read_csv('user_data.csv')
    read_df = pd.merge(read_df, user_names_df, on='user_id')
    
    books_df = book_to_tags()
    merged_df = read_df.merge(books_df, on='book_id')
    
    grouped = merged_df.groupby('user_id').apply(lambda x: x.apply(lambda row: {
        "book": {
            "book_id": row['book_id'],
            "goodreads_book_id": row['goodreads_book_id'],
            "work_id": row['work_id'],
            "authors": row['authors'],
            "title": row['title'],
            "isbn": row['isbn'],
            "isbn13": row['isbn13'],
            "language_code": row['language_code'],
            "average_rating": row['average_rating'],
            "ratings_count": row['ratings_count'],
            "image_url": row['image_url'],
            "tags": row["tags"]
        }
    }, axis=1).tolist())

    grouped_df = pd.DataFrame({'user_id': grouped.index, 'to_read': grouped.values})
    #print(grouped_df)
    #grouped_df.to_csv("test.csv")
    return grouped_df

if __name__ == "__main__":
    # book to ratings objects dataframe
    book_ratings_df = book_to_user_ratings()
    
    # books to tags object dataframe
    book_tags_df = book_to_tags()

    # merge the two
    book_final_df = book_tags_df.merge(book_ratings_df, on='book_id')
    print(book_final_df)
    # write data to a new csv file
    book_final_df.to_csv('data/book_final.csv', index=False)

    # merge for user data
    user_final_df = user_to_book_ratings().merge(user_to_read(), on='user_id', how='left')
    print(user_final_df)

    user_final_df.to_csv('data/user_final.csv', index=False)
    
    print("Preprocessing completed.")