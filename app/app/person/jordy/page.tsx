import QueryBlock from "@/components/query-block"
import Image from "next/image"
import { Jordy } from "@/server/actions"
import { Card, CardTitle, CardHeader, CardDescription, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

export default async function JordyPage() {
    const data = await Jordy()

    return (
        <section className="container grid items-center gap-6 pb-8 pt-6 md:py-10">
        <div className="flex h-full max-w-[980px] items-center gap-2">
            <Image 
                src="/jordy.png" 
                alt="Jordy" 
                width="100" 
                height="100"
                style={{
                    aspectRatio: "200/200",
                    objectFit: "cover",
                }}
                className="rounded-full mr-2" />
            <h1 className="text-3xl font-extrabold leading-tight tracking-tighter md:text-4xl">
            Jordy's Query
            </h1>
        </div>
        <p className="max-w-[700px] text-lg text-muted-foreground">
            Find the top 10 users who have rated the most diverse range of genres
        </p>
        <div className="max-w-prose text-lg mt-2 outline outline-muted rounded-sm">
            <QueryBlock 
            query={`db.users.aggregate([{ $unwind: "$ratings" }, { $lookup: { from: "books", localField: "ratings.book.title", foreignField: "title", as: "rated_books" } }, { $unwind: "$rated_books" },{ $unwind: "$rated_books.tags" },{ $group: { _id: "$user_id", user_name: { $first: "$user_name" }, genres: { $addToSet: "$rated_books.tags.tag_name" } } },{ $addFields: { num_genres: { $size: "$genres" } } },{ $sort: { num_genres: -1 } },{ $limit: 10 }])`}
            />
        </div>
        <div className="flex min-h-[400px] flex-col items-center justify-center rounded-md border border-dashed p-8 text-center animate-in fade-in-50">
            {
                data.map((user) => (
                    <Card key={user._id} className={"mb-4"}>
                        <CardHeader>
                            <CardTitle>{user.user_name}</CardTitle>
                            <CardDescription>{user.num_genres + " "}genres</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="flex flex-wrap gap-2">
                                {user.genres.map((genre: any) => (
                                    <Badge key={genre} variant={"outline"} className="text-muted-foreground text-md">{genre}</Badge>
                                ))}
                            </div>
                        </CardContent>
                    </Card>
                ))
            }
        </div>
        </section>
    )
}