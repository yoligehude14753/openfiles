import { useState, useRef, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import SearchInput from "../components/SearchInput";
import ResultList from "../components/ResultList";
import AIAnswer from "../components/AIAnswer";
import VoiceOverlay from "../components/VoiceOverlay";
import StatusBar from "../components/StatusBar";
import Onboarding from "../components/Onboarding";
import type { FileResult } from "../types";

const API = (window as any).__TAURI__
  ? "/api/v1"
  : "http://localhost:8000/api/v1";

type Mode = "idle" | "searching" | "results" | "ai" | "voice" | "onboarding";

export default function SpotlightWindow() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<FileResult[]>([]);
  const [selectedIdx, setSelectedIdx] = useState(0);
  const [aiAnswer, setAiAnswer] = useState("");
  const [aiSources, setAiSources] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [isAsking, setIsAsking] = useState(false);
  const [aiError, setAiError] = useState("");
  const [voiceActive, setVoiceActive] = useState(false);
  const [needsOnboarding, setNeedsOnboarding] = useState(false);
  const [checkingSetup, setCheckingSetup] = useState(true);
  const debounceRef = useRef<ReturnType<typeof setTimeout>>();
  const resultsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetch(`${API}/stats`)
      .then((r) => r.json())
      .then((d) => {
        setNeedsOnboarding(d.indexed_files === 0);
        setCheckingSetup(false);
      })
      .catch(() => setCheckingSetup(false));
  }, []);

  const search = useCallback(async (q: string) => {
    if (!q.trim()) {
      setResults([]);
      setAiAnswer("");
      setAiError("");
      return;
    }
    setIsSearching(true);
    try {
      const res = await fetch(`${API}/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q, type: "files", limit: 6 }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setResults(data.results || []);
      setSelectedIdx(0);
    } catch {
      setResults([]);
    } finally {
      setIsSearching(false);
    }
  }, []);

  const askAI = useCallback(async (q: string) => {
    if (!q.trim()) return;
    setIsAsking(true);
    setAiAnswer("");
    setAiSources([]);
    setAiError("");
    try {
      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: q }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setAiAnswer(data.message || "");
      setAiSources(data.sources || []);
    } catch (e: any) {
      setAiError(e.message || "Failed to get AI response");
    } finally {
      setIsAsking(false);
    }
  }, []);

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => search(query), 200);
    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
    };
  }, [query, search]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Escape") {
      if (voiceActive) {
        e.preventDefault();
        setVoiceActive(false);
        return;
      }
    }
    if (voiceActive) return;

    if (e.key === "ArrowDown") {
      e.preventDefault();
      setSelectedIdx((i) => Math.min(i + 1, results.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setSelectedIdx((i) => Math.max(i - 1, 0));
    } else if (e.key === "Enter" && e.metaKey) {
      e.preventDefault();
      askAI(query);
    } else if (e.key === "Enter" && results[selectedIdx]) {
      e.preventDefault();
      openFile(results[selectedIdx].path);
    } else if (e.key === "v" && e.metaKey && e.shiftKey) {
      e.preventDefault();
      setVoiceActive(true);
    }
  };

  const openFile = async (path: string) => {
    try {
      const { open } = await import("@tauri-apps/plugin-shell");
      await open(path);
    } catch {
      window.open(`file://${path}`, "_blank");
    }
  };

  const mode: Mode = voiceActive
    ? "voice"
    : needsOnboarding
    ? "onboarding"
    : isAsking || aiAnswer || aiError
    ? "ai"
    : results.length > 0
    ? "results"
    : isSearching
    ? "searching"
    : "idle";

  if (checkingSetup) {
    return (
      <div className="h-screen w-screen bg-zinc-900/95 backdrop-blur-xl rounded-2xl border border-zinc-700/50 shadow-2xl flex items-center justify-center">
        <motion.div
          animate={{ opacity: [0.3, 1, 0.3] }}
          transition={{ duration: 1.5, repeat: Infinity }}
          className="text-zinc-500 text-sm"
        >
          Loading...
        </motion.div>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ scale: 0.96, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.2, ease: [0.23, 1, 0.32, 1] }}
      className="h-screen w-screen bg-zinc-900/95 backdrop-blur-xl rounded-2xl border border-zinc-700/50 shadow-2xl flex flex-col overflow-hidden"
      onKeyDown={handleKeyDown}
    >
      {/* Search bar */}
      {!needsOnboarding && (
        <SearchInput
          query={query}
          onChange={setQuery}
          isSearching={isSearching}
          voiceActive={voiceActive}
          onVoiceToggle={() => setVoiceActive(!voiceActive)}
        />
      )}

      {/* Main content area */}
      <div ref={resultsRef} className="flex-1 overflow-y-auto min-h-0">
        <AnimatePresence mode="wait">
          {needsOnboarding ? (
            <motion.div
              key="onboarding"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <Onboarding
                apiBase={API}
                onComplete={() => setNeedsOnboarding(false)}
              />
            </motion.div>
          ) : voiceActive ? (
            <motion.div
              key="voice"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
            >
              <VoiceOverlay
                apiBase={API}
                onClose={() => setVoiceActive(false)}
                onTranscript={(text) => {
                  setQuery(text);
                  setVoiceActive(false);
                  askAI(text);
                }}
              />
            </motion.div>
          ) : (
            <motion.div key="content" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              {results.length > 0 && (
                <ResultList
                  results={results}
                  selectedIdx={selectedIdx}
                  onSelect={setSelectedIdx}
                  onOpen={openFile}
                  containerRef={resultsRef}
                />
              )}

              {(aiAnswer || isAsking || aiError) && (
                <AIAnswer
                  answer={aiAnswer}
                  sources={aiSources}
                  isLoading={isAsking}
                  error={aiError}
                  onRetry={() => askAI(query)}
                />
              )}

              {mode === "idle" && (
                <motion.div
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 }}
                  className="flex flex-col items-center justify-center h-full text-zinc-500 text-sm py-12"
                >
                  <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center text-white font-bold text-xl mb-4 shadow-lg shadow-brand-500/20">
                    O
                  </div>
                  <p className="text-zinc-300 font-medium mb-1">
                    What are you looking for?
                  </p>
                  <p className="text-xs text-zinc-600">
                    <kbd className="px-1.5 py-0.5 bg-zinc-800 rounded text-zinc-400 text-[10px]">
                      ⌘⏎
                    </kbd>{" "}
                    AI answer
                    <span className="mx-2 text-zinc-700">|</span>
                    <kbd className="px-1.5 py-0.5 bg-zinc-800 rounded text-zinc-400 text-[10px]">
                      ⌘⇧V
                    </kbd>{" "}
                    Voice
                  </p>
                </motion.div>
              )}

              {mode === "searching" && (
                <div className="flex items-center justify-center py-8">
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    className="w-5 h-5 border-2 border-zinc-700 border-t-brand-400 rounded-full"
                  />
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Status bar */}
      {!needsOnboarding && (
        <StatusBar mode={mode} resultsCount={results.length} />
      )}
    </motion.div>
  );
}
