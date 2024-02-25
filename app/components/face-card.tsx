import Link from "next/link"
import { Card, CardContent } from "@/components/ui/card"
import Image from "next/image"

interface FaceCardProps {
  name: string;
  image: string;
}

export function FaceCard({ name, image }: FaceCardProps) {
  return (
    <div className="aspect-card transition-all duration-500 hover:scale-105">
      <Card>
        <Link href={`person/${name.toLowerCase()}`} passHref>
          <CardContent className="flex flex-col items-center gap-2 p-4 rounded">
            <Image
              alt={`Photo of ${name}`}
              className="rounded-full cursor-pointer"
              height="200"
              src={image}
              style={{
                aspectRatio: "200/200",
                objectFit: "cover",
              }}
              width="200"
            />
            <p className="text-lg font-semibold cursor-pointer">{name}</p>
          </CardContent>
        </Link>
      </Card>
    </div>
  )
}
