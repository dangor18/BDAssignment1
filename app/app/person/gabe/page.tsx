import QueryBlock from "@/components/query-block"
import Image from "next/image"
import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Gabe } from "@/server/actions"

export default async function GabePage() {
    const data = await Gabe()
    
    return (
        <section className="container grid items-center gap-6 pb-8 pt-6 md:py-10">
        <div className="flex h-full max-w-[980px] items-center gap-2">
            <Image 
                src="/gabe.png" 
                alt="Gabe" 
                width="100" 
                height="100"
                style={{
                    aspectRatio: "200/200",
                    objectFit: "cover",
                }}
                className="rounded-full mr-2" />
            <h1 className="text-3xl font-extrabold leading-tight tracking-tighter md:text-4xl">
            Gabe's Query
            </h1>
        </div>
        <p className="max-w-[700px] text-lg text-muted-foreground">
            Find users who want to read “The Book Thief”
        </p>
        <div className="max-w-prose text-lg mt-2 outline outline-muted rounded-sm">
            <QueryBlock 
            query={`db.users.find({"to_read.book.title": "The Book Thief"},{"_id": 0, "user_name": 1})`}
            />
        </div>
        <div className="flex min-h-[400px] flex-col items-center justify-center rounded-md border border-dashed p-8 text-center animate-in fade-in-50">
            <Table>
                    <TableCaption></TableCaption>
                    <TableHeader>
                        <TableRow className="text-center">
                            <TableHead>Name</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {data.map((user) => (
                            <TableRow key={user.user_id}>
                                <TableCell>{user.user_name}</TableCell>
                            </TableRow>
                        ))
                        }
                    </TableBody>
                </Table>
            </div>
        </section>
  )
}