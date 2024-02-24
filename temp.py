import pandas as pd
    
    
def tags():
    books_df = pd.read_csv('data/books.csv')
    # split authors
    books_df['authors'] = books_df['authors'].str.split(', ')
    # iterate over each row and create a dictionary over ratings_x col's

    books_df.rename(columns={'original_title': 'title'}, inplace=True)
    books_df = books_df.sort_values(by='work_id')

    book_tags_df = pd.read_csv('data/book_tags.csv')
    tags_df = pd.read_csv('data/tags.csv')

    # Merge book_tags with tags to get the tag names along with their IDs for each book
    book_tags_merged_df = pd.merge(book_tags_df, tags_df, on='tag_id')

    # Group tags by book_id and aggregate into a list of dictionaries
    book_tags_grouped = book_tags_merged_df.groupby('goodreads_book_id').apply(lambda x: x[['tag_id', 'tag_name']].apply(lambda row: {'tag_id': row['tag_id'], 'tag_name': row['tag_name']}, axis=1).tolist()).reset_index(name='tags')

    final_df = pd.merge(books_df, book_tags_grouped, on='goodreads_book_id')
    #print(final_df)
    return final_df

# write the data to a new csv file
tags().to_csv('books+tags.csv', index=False)