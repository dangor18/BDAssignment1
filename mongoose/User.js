const mongoose = require("mongoose")
const book = require("./Book")


const userSchema = new mongoose.Schema({
  user_id: Number,
  user_name: String,
  to_read: [book.bookSchema],
  ratings: [book.bookSchema]
})

module.exports = mongoose.model("User", userSchema)
