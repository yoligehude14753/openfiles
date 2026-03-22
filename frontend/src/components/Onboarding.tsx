import { useState } from "react";
import { motion } from "framer-motion";
import { FolderOpen, Key, Loader2, CheckCircle2, ArrowRight } from "lucide-react";

interface Props {
  apiBase: string;
  onComplete: () => void;
}

export default function Onboarding({ apiBase, onComplete }: Props) {
  const [step, setStep] = useState<1 | 2 | 3>(1);
  const [isIndexing, setIsIndexing] = useState(false);
  const [indexProgress, setIndexProgress] = useState({ completed: 0, total: 0 });
  const [error, setError] = useState("");

  const startIndexing = async () => {
    setIsIndexing(true);
    setError("");
    try {
      await fetch(`${apiBase}/index`, { method: "POST" });

      const poll = setInterval(async () => {
        try {
          const res = await fetch(`${apiBase}/index/status`);
          const data = await res.json();
          setIndexProgress({ completed: data.completed, total: data.total || data.completed });
          if (!data.in_progress && data.completed > 0) {
            clearInterval(poll);
            setStep(3);
            setTimeout(onComplete, 2000);
          }
        } catch {}
      }, 2000);
    } catch (e: any) {
      setError(e.message || "Failed to start indexing");
      setIsIndexing(false);
    }
  };

  return (
    <div className="flex flex-col items-center px-8 py-6">
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center text-white font-bold text-2xl mb-4 shadow-lg shadow-brand-500/20">
          O
        </div>
      </motion.div>

      <h1 className="text-lg font-semibold text-zinc-100 mb-1">Welcome to OpenFiles</h1>
      <p className="text-sm text-zinc-500 mb-6">Let's set up your local file assistant</p>

      {/* Step indicators */}
      <div className="flex items-center gap-2 mb-6">
        {[1, 2, 3].map((s) => (
          <div key={s} className="flex items-center gap-2">
            <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium ${
              s < step ? "bg-brand-600 text-white" :
              s === step ? "bg-brand-500/20 text-brand-400 border border-brand-500" :
              "bg-zinc-800 text-zinc-500"
            }`}>
              {s < step ? <CheckCircle2 size={14} /> : s}
            </div>
            {s < 3 && <div className={`w-8 h-px ${s < step ? "bg-brand-500" : "bg-zinc-700"}`} />}
          </div>
        ))}
      </div>

      {/* Step 1: Info */}
      {step === 1 && (
        <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-sm space-y-3">
          <div className="flex items-start gap-3 p-3 rounded-lg bg-zinc-800/50 border border-zinc-700/50">
            <FolderOpen size={18} className="text-brand-400 mt-0.5 flex-shrink-0" />
            <div>
              <p className="text-sm text-zinc-200">Your files stay local</p>
              <p className="text-xs text-zinc-500">We index ~/Documents, ~/Desktop, ~/Downloads by default</p>
            </div>
          </div>
          <div className="flex items-start gap-3 p-3 rounded-lg bg-zinc-800/50 border border-zinc-700/50">
            <Key size={18} className="text-brand-400 mt-0.5 flex-shrink-0" />
            <div>
              <p className="text-sm text-zinc-200">AI-powered search</p>
              <p className="text-xs text-zinc-500">Uses your configured LLM to understand and search files</p>
            </div>
          </div>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => setStep(2)}
            className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-brand-600 hover:bg-brand-700 text-white text-sm font-medium rounded-lg transition-colors"
          >
            Start Indexing <ArrowRight size={14} />
          </motion.button>
        </motion.div>
      )}

      {/* Step 2: Indexing */}
      {step === 2 && (
        <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-sm">
          {!isIndexing ? (
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={startIndexing}
              className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-brand-600 hover:bg-brand-700 text-white text-sm font-medium rounded-lg transition-colors"
            >
              Index My Files <ArrowRight size={14} />
            </motion.button>
          ) : (
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <Loader2 size={16} className="text-brand-400 animate-spin" />
                <span className="text-sm text-zinc-300">Indexing files...</span>
              </div>
              <div className="w-full h-2 bg-zinc-800 rounded-full overflow-hidden">
                <motion.div
                  className="h-full bg-gradient-to-r from-brand-500 to-brand-400 rounded-full"
                  initial={{ width: "5%" }}
                  animate={{
                    width: indexProgress.total > 0
                      ? `${Math.max(5, (indexProgress.completed / indexProgress.total) * 100)}%`
                      : "15%",
                  }}
                  transition={{ duration: 0.5 }}
                />
              </div>
              <p className="text-xs text-zinc-500 text-center">
                {indexProgress.completed > 0
                  ? `${indexProgress.completed.toLocaleString()} files indexed`
                  : "Scanning directories..."}
              </p>
            </div>
          )}
          {error && <p className="text-xs text-red-400 mt-2">{error}</p>}
        </motion.div>
      )}

      {/* Step 3: Done */}
      {step === 3 && (
        <motion.div initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="text-center">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 200, damping: 15 }}
          >
            <CheckCircle2 size={48} className="text-green-400 mx-auto mb-3" />
          </motion.div>
          <p className="text-sm text-zinc-200 font-medium">You're all set!</p>
          <p className="text-xs text-zinc-500">{indexProgress.completed.toLocaleString()} files indexed. Start searching...</p>
        </motion.div>
      )}
    </div>
  );
}
