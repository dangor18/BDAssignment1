import csv
from faker import Faker
import random

# Initialize Faker to generate random data
fake = Faker()

# Generate data and write to CSV
with open('user_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['user_id', 'full_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i in range(100001):
        writer.writerow({'user_id': i, 'full_name': fake.name()})
