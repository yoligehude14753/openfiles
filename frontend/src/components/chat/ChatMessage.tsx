import ReactMarkdown from "react-markdown";
import { User, Bot, Copy, Check } from "lucide-react";
import { useState } from "react";
import FileCard from "./FileCard";
import type { SourceRef } from "../../types";

interface Props {
  role: "user" | "assistant";
  content: string;
  sources?: SourceRef[] | null;
  isStreaming?: boolean;
}

export default function ChatMessage({
  role,
  content,
  sources,
  isStreaming,
}: Props) {
  const [copied, setCopied] = useState(false);
  const isUser = role === "user";

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div
      className={`animate-fade-in py-5 px-4 ${
        isUser ? "" : "bg-zinc-900/30"
      }`}
    >
      <div className="max-w-3xl mx-auto flex gap-4">
        {/* Avatar */}
        <div
          className={`w-7 h-7 rounded-lg flex-shrink-0 flex items-center justify-center ${
            isUser ? "bg-zinc-700" : "bg-brand-600"
          }`}
        >
          {isUser ? (
            <User size={14} className="text-zinc-300" />
          ) : (
            <Bot size={14} className="text-white" />
          )}
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          {/* Sources */}
          {sources && sources.length > 0 && (
            <div className="flex flex-wrap gap-1.5 mb-3">
              {sources.map((s, i) => (
                <FileCard key={i} source={s} />
              ))}
            </div>
          )}

          {/* Message body */}
          <div className="prose prose-invert prose-sm max-w-none prose-p:leading-relaxed prose-pre:bg-zinc-800 prose-pre:border prose-pre:border-zinc-700 prose-code:text-brand-400 prose-code:before:content-none prose-code:after:content-none">
            <ReactMarkdown>{content}</ReactMarkdown>
            {isStreaming && (
              <span className="inline-block w-2 h-4 bg-brand-400 animate-pulse ml-0.5" />
            )}
          </div>

          {/* Actions */}
          {!isUser && !isStreaming && content && (
            <div className="mt-2">
              <button
                onClick={handleCopy}
                className="p-1 text-zinc-600 hover:text-zinc-400 transition-colors"
                title="Copy"
              >
                {copied ? <Check size={14} /> : <Copy size={14} />}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
