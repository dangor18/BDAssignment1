#! /bin/bash

mongoimport --uri "mongodb+srv://admin:uGvwGdcT60QG75rs@cluster0.ce8456i.mongodb.net/goodbooks?retryWrites=true&w=majority" --collection books --type json --file /mongo-seed/books.json --jsonArray

mongoimport --uri "mongodb+srv://admin:uGvwGdcT60QG75rs@cluster0.ce8456i.mongodb.net/goodbooks?retryWrites=true&w=majority" --collection users --type json --file /mongo-seed/users.json --jsonArray