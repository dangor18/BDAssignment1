import dbConnect from "@/lib/db-connect"
import { Book, User } from "./models"

const Matt = async () => {
    await dbConnect()
    const data = await User.aggregate([
        {
            $project: {
                _id: 0,
                user_id: 1,
                numRatings: { $size: "$ratings" }
            }
        },
        { $sort: { numRatings: -1 }},
        { $limit: 10 }
    ])
    return data
}

const Joe = async () => {
    await dbConnect()
    const data = await Book.aggregate([
        { $match: { "total_ratings": { $gte: 1000 }, "tags.tag_name": "fiction" } },
        { $sort: { "average_rating": -1 } },
        { $limit: 50 },
        { $project: { _id: 0, title: 1, average_rating: 1, image_url: 1 } }
    ])
    return data
}

const Dan = async () => {
    await dbConnect()
    const data = await User.find(
        { ratings: { $exists: true, $not: { $size: 0 } }, to_read: { $size: 0 } },
        { _id: false, ratings: false }
    );
    return data
}

const Jordy = async () => {
    await dbConnect()
    const data = await User.aggregate([
        { $unwind: "$ratings" },
        { $lookup: { from: "books", localField: "ratings.book.title", foreignField: "title", as: "rated_books" } },
        { $unwind: "$rated_books" },
        { $unwind: "$rated_books.tags" },
        {
            $group: {
                _id: "$user_id",
                user_name: { $first: "$user_name" },
                genres: { $addToSet: "$rated_books.tags.tag_name" }
            }
        },
        { $addFields: { num_genres: { $size: "$genres" } } },
        { $sort: { num_genres: -1 } },
        { $limit: 10 }
    ]);
    
    return data
}

const Gabe = async () => {
    await dbConnect()
    const data = await User.find(
        { "to_read.book.title": "The Book Thief" },
        { "_id": 0, "user_name": 1 }
    )
    return data
}

export { Matt, Joe, Dan, Jordy, Gabe }
