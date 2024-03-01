import QueryBlock from "@/components/query-block"
import Image from "next/image"
import { Joe } from "@/server/actions"
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
            className="mr-2 rounded-full" />
        <h1 className="text-3xl font-extrabold leading-tight tracking-tighter md:text-4xl">
          Joe&apos;s Query
        </h1>
        
      </div>
      <p className="max-w-[700px] text-lg text-muted-foreground">
        Find the names and ratings of the top 50 fiction books with at least 1000 ratings
      </p>
      <div className="mt-2 max-w-prose rounded-sm text-lg outline outline-muted">
        <QueryBlock 
          query={`db.books.aggregate([{ $match: { "total_ratings": { $gte: 1000 }, "tags.tag_name": "fiction" }}, {$sort: { "average_rating": -1 }}, {$limit: 50}, {$project: { _id: 0, title: 1, average_rating: 1 }}])`}
        />
      </div>
      <div className="flex min-h-[400px] flex-col items-center justify-center rounded-md border border-dashed p-8 animate-in fade-in-50">
        <Table>
                <TableCaption></TableCaption>
                <TableHeader>
                    <TableRow className="text-center">
                        <TableHead></TableHead>
                        <TableHead>Title</TableHead>
                        <TableHead>Average Rating</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {data.map((book, index) => (
                    <TableRow key={index}>
                    <TableCell>{index + 1}</TableCell>
                    <TableCell>
                <div className="flex items-center">
                    <Image 
                        src={book.image_url}
                        alt={book.title}
                        width="40"
                        height="60"
                        className="rounded-md"
                    />
                    <p className="ms-4">{book.title}</p>
                </div>
            </TableCell>
            <TableCell>
                <div className="flex items-center">
                    <svg className="me-1 size-4 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                        <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                    </svg>
                    <p className="ms-2 text-sm font-bold text-white">{book.average_rating}</p>
                </div>
            </TableCell>
        </TableRow>
    ))}
</TableBody>
            </Table>
        </div>
    </section>
  )
}