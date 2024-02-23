"use client"

import { CodeBlock, dracula } from 'react-code-blocks'

interface QueryBlockProps {
  query: string;
}

export default function QueryBlock({ query }: QueryBlockProps) {
  return (
    <div className="font-mono">
      <CodeBlock
      text={query}
      language={'javascript'}
      showLineNumbers={false}
      theme={dracula}
      wrapLongLines={true}
    />
  </div>
    
  )
}