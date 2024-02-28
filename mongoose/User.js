const mongoose = require("mongoose")
const Book = require("./Book")


const userSchema = new mongoose.Schema({
  user_id: Number,
  user_name: String,
  to_read: [Book.schema],
  ratings: [Book.schema]
})

module.exports = mongoose.model("User", userSchema)
