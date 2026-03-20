import { useRef, useEffect } from "react";
import { Search, Loader2, Mic } from "lucide-react";

interface Props {
  query: string;
  onChange: (q: string) => void;
  isSearching: boolean;
  voiceActive: boolean;
  onVoiceToggle: () => void;
}

export default function SearchInput({
  query,
  onChange,
  isSearching,
  voiceActive,
  onVoiceToggle,
}: Props) {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  return (
    <div className="flex items-center gap-3 px-4 py-3 border-b border-zinc-700/50">
      {isSearching ? (
        <Loader2 size={18} className="text-brand-400 animate-spin flex-shrink-0" />
      ) : (
        <Search size={18} className="text-zinc-500 flex-shrink-0" />
      )}
      <input
        ref={inputRef}
        type="text"
        value={query}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Search your files..."
        className="flex-1 bg-transparent text-zinc-100 text-base placeholder-zinc-500 outline-none"
        autoFocus
      />
      <button
        onClick={onVoiceToggle}
        className={`p-1.5 rounded-lg transition-colors ${
          voiceActive
            ? "bg-red-500/20 text-red-400"
            : "hover:bg-zinc-800 text-zinc-500 hover:text-zinc-300"
        }`}
        title="Voice mode (⌘⇧V)"
      >
        <Mic size={16} />
      </button>
    </div>
  );
}
