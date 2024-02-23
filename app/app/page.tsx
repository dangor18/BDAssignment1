import Link from "next/link"


import { CardTitle, CardDescription, CardHeader, Card, CardContent } from "@/components/ui/card"
import { FaceCard } from "@/components/face-card"

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
      <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 gap-6 items-start">
        <FaceCard name="Daniel" image="/daniel.png" />
        <FaceCard name="Gabe" image="/gabe.png" />
        <FaceCard name="Joe" image="/joe.png" />
        <FaceCard name="Jordy" image="/jordy.png" />
        <FaceCard name="Matt" image="/matt.png" />
      </div>
    </section>
  )
}
