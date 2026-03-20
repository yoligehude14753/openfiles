import ReactMarkdown from "react-markdown";
import { Bot, Loader2, FileText } from "lucide-react";

interface Props {
  answer: string;
  sources: Array<{ path: string; type: string }>;
  isLoading: boolean;
}

export default function AIAnswer({ answer, sources, isLoading }: Props) {
  return (
    <div className="px-4 py-3">
      <div className="flex items-start gap-2.5">
        <div className="w-6 h-6 rounded-md bg-brand-600 flex items-center justify-center flex-shrink-0 mt-0.5">
          {isLoading ? (
            <Loader2 size={12} className="text-white animate-spin" />
          ) : (
            <Bot size={12} className="text-white" />
          )}
        </div>
        <div className="flex-1 min-w-0">
          {isLoading && !answer ? (
            <p className="text-sm text-zinc-400 animate-pulse">Thinking...</p>
          ) : (
            <div className="prose prose-invert prose-sm max-w-none prose-p:leading-relaxed prose-p:my-1 text-zinc-300">
              <ReactMarkdown>{answer}</ReactMarkdown>
            </div>
          )}

          {sources.length > 0 && (
            <div className="flex flex-wrap gap-1.5 mt-2">
              {sources.map((s, i) => (
                <span
                  key={i}
                  className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-zinc-800 text-[10px] text-zinc-400"
                >
                  <FileText size={10} />
                  {s.path.split("/").pop()}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
