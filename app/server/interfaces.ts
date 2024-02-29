interface IBook {
    book_id: string;
    isbn: string;
    isbn13: string;
    authors: string[];
    original_publication_year: number;
    title: string;
    language_code: string;
    average_rating: number;
    ratings_count: number;
    total_ratings: {
        ratings_1: number;
        ratings_2: number;
        ratings_3: number;
        ratings_4: number;
        ratings_5: number;
    };
    image_url: string;
    tags: {
        tag_id: number;
        tag_name: string;
    }[];
    ratings: {
        user: {
            user_id: number;
            user_name: string;
        };
        rating: number;
    }[];
}

interface IUser {
    user_id: number;
    user_name: string;
    ratings: {
        book: {
            book_id: number;
            authors: string[];
            title: string;
            isbn: string;
            isbn13: number;
            language_code: string;
            average_rating: number;
            ratings_count: number;
            image_url: string;
            tags: {
                tag_id: number;
                tag_name: string;
            }[];
        };
        rating: number;
    }[];
    to_read: {
        book: {
            book_id: number;
            authors: string[];
            title: string;
            isbn: string;
            isbn13: number;
            language_code: string;
            average_rating: number;
            ratings_count: number;
            image_url: string;
            tags: {
                tag_id: number;
                tag_name: string;
            }[];
        };
    }[];
}


export type { IBook, IUser }