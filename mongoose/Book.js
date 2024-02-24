const mongoose = require("mongoose")

const ratingCounts = new mongoose.Schema({
  average_rating: Number,
  ratings_total: Number,
  ratings_1: Number,
  ratings_2: Number,
  ratings_3: Number,
  ratings_4: Number,
  ratings_5: Number
})

const bookSchema = new mongoose.Schema({
  isbn: String,
  isbn13: String,
  authors: [String],
  original_publication_year: Number,
  title: String,
  language_code: String,
  rating_counts: ratingCounts,
  ratings: [
    {
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

module.exports = {
  model: mongoose.model("Book", bookSchema),
  schema: bookSchema
}
