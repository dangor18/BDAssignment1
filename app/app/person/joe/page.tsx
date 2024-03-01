import QueryBlock from "@/components/query-block"
import Image from "next/image"
import { Dan, Joe } from "@/server/actions"
import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"


export default async function JoePage() {
 const data = await Joe()

  return (
    <section className="container grid items-center gap-6 pb-8 pt-6 md:py-10">
      <div className="flex h-full max-w-[980px] items-center gap-2">
          <Image 
            src="/joe.png" 
            alt="Joe" 
            width="100" 
            height="100"
            style={{
                aspectRatio: "200/200",
                objectFit: "cover",
              }}
            className="rounded-full mr-2" />
        <h1 className="text-3xl font-extrabold leading-tight tracking-tighter md:text-4xl">
          Joe's Query
        </h1>
        
      </div>
      <p className="max-w-[700px] text-lg text-muted-foreground">
        Find the names and ratings of the top 50 fiction books with at least 1000 ratings
      </p>
      <div className="max-w-prose text-lg mt-2 outline outline-muted rounded-sm">
        <QueryBlock 
          query={`db.books.aggregate([{ $match: { "total_ratings": { $gte: 1000 }, "tags.tag_name": "fiction" }}, {$sort: { "average_rating": -1 }}, {$limit: 50}, {$project: { _id: 0, title: 1, average_rating: 1 }}])`}
        />
      </div>
      <div className="flex min-h-[400px] flex-col items-center justify-center rounded-md border border-dashed p-8 animate-in fade-in-50">
        <Table>
                <TableCaption></TableCaption>
                <TableHeader>
                    <TableRow className="text-center">
                        <TableHead>Title</TableHead>
                        <TableHead>Average Rating</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {data.map((book, index) => (
                        <TableRow key={index}>
                            <TableCell>{book.title}</TableCell>
                            <TableCell>{book.average_rating}</TableCell>
                        </TableRow>
                    ))
                    }
                </TableBody>
            </Table>
        </div>
    </section>
  )
}