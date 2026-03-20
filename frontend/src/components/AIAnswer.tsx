import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import ReactMarkdown from "react-markdown";
import { Bot, Loader2, FileText, RefreshCw, AlertCircle } from "lucide-react";

interface Props {
  answer: string;
  sources: Array<{ path: string; type: string }>;
  isLoading: boolean;
  error?: string;
  onRetry?: () => void;
}

function StreamingText({ text }: { text: string }) {
  const [displayed, setDisplayed] = useState("");

  useEffect(() => {
    if (!text) { setDisplayed(""); return; }
    let i = 0;
    setDisplayed("");
    const timer = setInterval(() => {
      i += 3;
      if (i >= text.length) {
        setDisplayed(text);
        clearInterval(timer);
      } else {
        setDisplayed(text.slice(0, i));
      }
    }, 10);
    return () => clearInterval(timer);
  }, [text]);

  return (
    <div className="prose prose-invert prose-sm max-w-none prose-p:leading-relaxed prose-p:my-1 text-zinc-300 prose-code:text-brand-300">
      <ReactMarkdown>{displayed}</ReactMarkdown>
      {displayed.length < text.length && (
        <span className="inline-block w-0.5 h-4 bg-brand-400 animate-pulse ml-0.5 align-text-bottom" />
      )}
    </div>
  );
}

export default function AIAnswer({ answer, sources, isLoading, error, onRetry }: Props) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2 }}
      className="px-4 py-3"
    >
      <div className="flex items-start gap-2.5">
        <motion.div
          animate={isLoading ? { rotate: [0, 360] } : {}}
          transition={isLoading ? { duration: 2, repeat: Infinity, ease: "linear" } : {}}
          className="w-6 h-6 rounded-md bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center flex-shrink-0 mt-0.5 shadow-sm"
        >
          {isLoading ? (
            <Loader2 size={12} className="text-white" />
          ) : error ? (
            <AlertCircle size={12} className="text-white" />
          ) : (
            <Bot size={12} className="text-white" />
          )}
        </motion.div>

        <div className="flex-1 min-w-0">
          {/* Error state */}
          {error && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex items-center gap-2 p-2 rounded-lg bg-red-500/10 border border-red-500/20"
            >
              <span className="text-sm text-red-400 flex-1">{error}</span>
              {onRetry && (
                <button
                  onClick={onRetry}
                  className="flex items-center gap-1 px-2 py-1 text-xs text-red-300 hover:text-white bg-red-500/10 hover:bg-red-500/20 rounded transition-colors"
                >
                  <RefreshCw size={10} /> Retry
                </button>
              )}
            </motion.div>
          )}

          {/* Loading */}
          {isLoading && !answer && !error && (
            <div className="flex items-center gap-2">
              <motion.div
                className="flex gap-1"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                {[0, 1, 2].map((i) => (
                  <motion.div
                    key={i}
                    animate={{ y: [-2, 2, -2] }}
                    transition={{ duration: 0.6, repeat: Infinity, delay: i * 0.15 }}
                    className="w-1.5 h-1.5 rounded-full bg-brand-400"
                  />
                ))}
              </motion.div>
              <span className="text-sm text-zinc-400">Thinking...</span>
            </div>
          )}

          {/* Answer with streaming effect */}
          {answer && <StreamingText text={answer} />}

          {/* Sources */}
          <AnimatePresence>
            {sources.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 4 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="flex flex-wrap gap-1.5 mt-2"
              >
                {sources.map((s, i) => (
                  <motion.span
                    key={s.path}
                    initial={{ opacity: 0, x: -8 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.4 + i * 0.08 }}
                    className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-zinc-800/80 border border-zinc-700/50 text-[10px] text-zinc-400 hover:text-zinc-300 hover:border-zinc-600 transition-colors cursor-default"
                  >
                    <FileText size={9} />
                    {s.path.split("/").pop()}
                  </motion.span>
                ))}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </motion.div>
  );
}
