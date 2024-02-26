#! /bin/bash

mongoimport --host mongodb --port 27017 --db goodbooks --mode upsert --collection books --type json --file /mongo-seed/books.json --jsonArray
mongoimport --host mongodb --port 27017 --db goodbooks --mode upsert --collection users --type json --file /mongo-seed/users.json --jsonArray