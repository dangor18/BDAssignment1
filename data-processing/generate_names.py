import csv
from faker import Faker
import random

fake = Faker()

# generate and write to user_data.csv
with open('data/user_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['user_id', 'full_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i in range(100001):
        writer.writerow({'user_id': i, 'full_name': fake.name()})
