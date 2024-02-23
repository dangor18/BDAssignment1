import QueryBlock from "@/components/query-block"
import Image from "next/image"
import EmptyPlaceholder from "@/components/empty-placeholder"

export default function JordyPage() {
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
      <div className="max-w-prose text-lg mt-6 outline outline-muted rounded-sm">
        <QueryBlock 
          query={`db.books.find({ genre: "fiction", publishedYear: { $gte: 2000 }})`}
        />
      </div>
      < EmptyPlaceholder />
    </section>
  )
}