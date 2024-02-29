#!/bin/bash
mongosh bookstore --eval "db.dropDatabase();"
./mongo-seed/import.sh
