const mongoose = require("mongoose")
const User = require("./User")
//const Book = require("./Book")

mongoose.connect("mongodb://localhost/testdb")

example()
async function example() {
  const user = await User.create(
    {
      user_id: 1,
      user_name: "NameNameson",
      to_read: [
        {
          book_id: "2792775",
          isbn: "439554934",
          isbn13: "9.78043902348e+12",
          authors: [
            "Suzanne Collins"
          ],
          original_publication_year: 2008,
          title: "The Hunger Games",
          language_code: "eng",
          rating_counts: {
            average_rating: 4.34,
            ratings_total: 4780653,
            ratings_1: 66715,
            ratings_2: 127936,
            ratings_3: 560092,
            ratings_4: 1481305,
            ratings_5: 2706317
          },
          ratings: [
          ],
          image_url: "https://images.gr-assets.com/books/1447303603m/2767052.jpg",
          tags: [
            {
              tag_id: 98,
              tag_name: "02-fantasy"
            },
            {
              tag_id: 2772,
              tag_name: "apocalyptic-dystopian"
            }
          ]
        }
      ],
      ratings: [
        {
          book_id: "2792775",
          isbn: "439554934",
          isbn13: "9.78043902348e+12",
          authors: [
            "Suzanne Collins"
          ],
          original_publication_year: 2008,
          title: "The Hunger Games",
          language_code: "eng",
          rating_counts: {
            average_rating: 4.34,
            ratings_total: 4780653,
            ratings_1: 66715,
            ratings_2: 127936,
            ratings_3: 560092,
            ratings_4: 1481305,
            ratings_5: 2706317
          },
          ratings: [
          ],
          image_url: "https://images.gr-assets.com/books/1447303603m/2767052.jpg",
          tags: [
            {
              tag_id: 98,
              tag_name: "02-fantasy"
            },
            {
              tag_id: 2772,
              tag_name: "apocalyptic-dystopian"
            }
          ]
        }
      ]
    }
  )
  console.log(user)
}
