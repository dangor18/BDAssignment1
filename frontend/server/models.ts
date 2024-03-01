import mongoose, { Schema, Model, model } from "mongoose"
import { IBook, IUser } from "./interfaces"


const BookSchema = new Schema<IBook>({
    book_id: {
        type: String,
        required: true
    },
    isbn: {
        type: String,
        required: true
    },
    isbn13: {
        type: String,
        required: true
    },
    authors: {
        type: [String],
        required: true
    },
    original_publication_year: {
        type: Number,
        required: true
    },
    title: {
        type: String,
        required: true
    },
    language_code: {
        type: String,
        required: true
    },
    average_rating: {
        type: Number,
        required: true
    },
    ratings_count: {
        type: Number,
        required: true
    },
    total_ratings: {
        type: {
            ratings_1: Number,
            ratings_2: Number,
            ratings_3: Number,
            ratings_4: Number,
            ratings_5: Number
        },
        required: true
    },
    image_url: {
        type: String,
        required: true
    },
    tags: {
        type: [{
            tag_id: Number,
            tag_name: String
        }],
        required: true
    },
    ratings: {
        type: [{
            user: {
                user_id: Number,
                user_name: String
            },
            rating: Number
        }],
        required: true
    }
})

const UserSchema = new Schema<IUser>({
    user_id: {
        type: Number,
        required: true
    },
    user_name: {
        type: String,
        required: true
    },
    ratings: [{
        book: BookSchema,
        rating: Number
    }],
    to_read: [{
        book: BookSchema
    }]
})

const Book: Model<IBook> =  mongoose.models.Book || model<IBook>('Book', BookSchema)
const User: Model<IUser> = mongoose.models.User || model<IUser>('User', UserSchema)

export { Book, User }