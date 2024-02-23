import Link from "next/link"


import { CardTitle, CardDescription, CardHeader, Card, CardContent } from "@/components/ui/card"

export default function IndexPage() {
  return (
    <section className="container grid items-center gap-6 pb-8 pt-6 md:py-10">
      <div className="flex max-w-[980px] flex-col items-start gap-2">
        <h1 className="text-3xl font-extrabold leading-tight tracking-tighter md:text-4xl">
          Queries
        </h1>
        <p className="max-w-[700px] text-lg text-muted-foreground">
        Explore our MongoDB queries from our CSC4019Z Big Data assignment
        </p>
      </div>
    </section>
  )
}
