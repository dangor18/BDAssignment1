import { Icons } from "@/components/icons"
import { Button } from "@/components/ui/button"

export default function EmptyPlaceholder() {
  return (
    <div className="flex min-h-[400px] flex-col items-center justify-center rounded-md border border-dashed p-8 text-center animate-in fade-in-50">
        <div className="mx-auto flex max-w-[420px] flex-col items-center justify-center text-center">
            <div className="flex size-20 items-center justify-center rounded-full bg-muted">
                <Icons.logo className="size-10" />
            </div>
            <h2 className="mt-6 text-xl font-semibold">No data</h2>
            <p className="mb-8 mt-2 text-center text-sm font-normal leading-6 text-muted-foreground">You don&apos;t have any data yet. Run the query to fetch the data from MongoDB.</p>
            <Button variant={"outline"}>Run query</Button>
        </div>
      </div>
  )
}