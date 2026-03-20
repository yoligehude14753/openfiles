import { motion, AnimatePresence } from "framer-motion";

interface Props {
  mode: string;
  resultsCount: number;
}

const HINTS: Record<string, Array<[string, string]>> = {
  idle: [
    ["↑↓", "Navigate"],
    ["⏎", "Open"],
    ["⌘⏎", "AI"],
    ["⌘⇧V", "Voice"],
    ["Esc", "Close"],
  ],
  results: [
    ["↑↓", "Navigate"],
    ["⏎", "Open file"],
    ["⌘⏎", "Ask AI"],
    ["Esc", "Close"],
  ],
  ai: [
    ["↑↓", "Navigate"],
    ["⏎", "Open file"],
    ["Esc", "Close"],
  ],
  voice: [
    ["Esc", "Stop voice"],
  ],
  searching: [
    ["Esc", "Cancel"],
  ],
};

export default function StatusBar({ mode, resultsCount }: Props) {
  const hints = HINTS[mode] || HINTS.idle;

  return (
    <div className="flex items-center justify-between px-4 py-1.5 border-t border-zinc-700/30 text-[10px] text-zinc-600 select-none">
      <AnimatePresence mode="wait">
        <motion.div
          key={mode}
          initial={{ opacity: 0, y: 4 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -4 }}
          transition={{ duration: 0.15 }}
          className="flex items-center gap-3"
        >
          {hints.map(([key, label]) => (
            <span key={key} className="flex items-center gap-1">
              <kbd className="px-1 py-px bg-zinc-800/80 rounded text-zinc-500 font-mono">
                {key}
              </kbd>
              <span>{label}</span>
            </span>
          ))}
        </motion.div>
      </AnimatePresence>

      <AnimatePresence>
        {resultsCount > 0 && (
          <motion.span
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="tabular-nums"
          >
            {resultsCount} file{resultsCount !== 1 ? "s" : ""}
          </motion.span>
        )}
      </AnimatePresence>
    </div>
  );
}
