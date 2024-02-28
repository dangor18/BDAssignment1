#!/bin/bash
mongosh bookstore --eval "db.dropDatabase();"
python3 ./load_database.py
