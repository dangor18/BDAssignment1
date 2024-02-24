const mongoose = require("mongoose")
const book = require("./Book")

const bookRatings = new mongoose.Schema({
  average_rating: Number,
  ratings_count: Number,
  ratings_1: Number,
  ratings_2: Number,
  ratings_3: Number,
  ratings_4: Number,
  ratings_5: Number
})

const nestedBookSchema = new mongoose.Schema({
  book_id: String,
  isbn: String,
  isbn14: String,
  authors: [String],
  original_publication_year: Number,
  title: String,
  language_code: String,
  book_ratings: bookRatings,
  ratings: [
    {
      //user_id: Number,
      user: mongoose.SchemaTypes.ObjectId,
      rating: Number
    }
  ],
  image_url: String,
  tags: [
    {
      tag_id: Number,
      tag_name: String
    }
  ]
})

const userSchema = new mongoose.Schema({
  user_id: Number,
  user_name: String,
  to_read: [nestedBookSchema],
  ratings: [nestedBookSchema]
})

module.exports = mongoose.model("User", userSchema)
