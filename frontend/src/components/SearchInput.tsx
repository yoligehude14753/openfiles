import { useRef, useEffect } from "react";
import { motion } from "framer-motion";
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
  }, [voiceActive]);

  return (
    <div className="relative flex items-center gap-3 px-4 py-3.5 border-b border-zinc-700/50">
      <motion.div
        animate={isSearching ? { rotate: 360 } : { rotate: 0 }}
        transition={isSearching ? { duration: 0.8, repeat: Infinity, ease: "linear" } : {}}
      >
        {isSearching ? (
          <Loader2 size={18} className="text-brand-400 flex-shrink-0" />
        ) : (
          <Search size={18} className="text-zinc-500 flex-shrink-0" />
        )}
      </motion.div>

      <input
        ref={inputRef}
        type="text"
        value={query}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Search your files..."
        className="flex-1 bg-transparent text-zinc-100 text-[15px] placeholder-zinc-500 outline-none caret-brand-400"
        autoFocus
        spellCheck={false}
      />

      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        onClick={onVoiceToggle}
        className={`p-1.5 rounded-lg transition-colors ${
          voiceActive
            ? "bg-red-500/20 text-red-400"
            : "hover:bg-zinc-800 text-zinc-500 hover:text-zinc-300"
        }`}
        title="Voice mode (⌘⇧V)"
      >
        <Mic size={16} />
      </motion.button>

      {/* Focus glow effect */}
      <motion.div
        className="absolute inset-x-0 bottom-0 h-px bg-gradient-to-r from-transparent via-brand-500/50 to-transparent"
        initial={{ opacity: 0 }}
        animate={{ opacity: query ? 1 : 0 }}
        transition={{ duration: 0.3 }}
      />
    </div>
  );
}
