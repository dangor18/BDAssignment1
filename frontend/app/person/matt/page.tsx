import QueryBlock from "@/components/query-block"
import Image from "next/image"
import { Matt } from "@/server/actions"
import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"


export default async function MattPage() {
 const data = await Matt()

  return (
    <section className="container grid items-center gap-6 pb-8 pt-6 md:py-10">
      <div className="flex h-full max-w-[980px] items-center gap-2">
          <Image 
            src="/matt.png" 
            alt="Matt" 
            width="100" 
            height="100"
            style={{
                aspectRatio: "200/200",
                objectFit: "cover",
              }}
            className="mr-2 rounded-full" />
        <h1 className="text-3xl font-extrabold leading-tight tracking-tighter md:text-4xl">
          Matt&apos;s Query
        </h1>
        
      </div>
      <p className="max-w-[700px] text-lg text-muted-foreground">
        Aggregate user IDs alongside the total number of ratings that user has submitted. The result is sorted by the number of ratings they have submitted and the top 10 are shown
      </p>
      <div className="mt-2 max-w-prose rounded-sm text-lg outline outline-muted">
        <QueryBlock 
          query={`db.users.aggregate([{$project: {_id: 0, user_id: 1, numRatings: { $size: "$ratings" }}}, { $sort: { numRatings: -1 }}, { $limit: 10 }])`}
        />
      </div>
      <div className="flex min-h-[400px] flex-col items-center justify-center rounded-md border border-dashed p-8 animate-in fade-in-50">
        <Table>
                <TableCaption></TableCaption>
                <TableHeader>
                    <TableRow className="text-center">
                        <TableHead>User ID</TableHead>
                        <TableHead>Number of Ratings</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {data.map((user) => (
                        <TableRow key={user.user_id}>
                            <TableCell>{user.user_id}</TableCell>
                            <TableCell>{user.numRatings}</TableCell>
                        </TableRow>
                    ))
                    }
                </TableBody>
            </Table>
        </div>
    </section>
  )
}