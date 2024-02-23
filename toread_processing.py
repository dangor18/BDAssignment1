import csv

def transform_csv(input_csv, output_csv):
    user_books = {}

    # Read input CSV and aggregate book IDs for each user
    with open(input_csv, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_id = row['user_id']
            book_id = row['book_id']
            if user_id in user_books:
                user_books[user_id].append(book_id)
            else:
                user_books[user_id] = [book_id]

    # Write aggregated data to output CSV
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['user_id', 'book_ids'])
        for user_id, book_ids in user_books.items():
            writer.writerow([user_id, ','.join(book_ids)])


# Specify input and output CSV file paths
input_csv = 'data/to_read.csv'
output_csv = 'to_read_merged.csv'

# Transform CSV
transform_csv(input_csv, output_csv)
