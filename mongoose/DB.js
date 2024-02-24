const mongoose = require("mongoose")
const User = require("./User")
const Book = require("./Book")

mongoose.connect("mongodb://localhost/testdb")

run()
async function run() {
  const user = await User.create({name: "MatthewCraig", age: 22})
  console.log(user)
}
