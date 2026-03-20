import { useState, useRef, useEffect, useCallback } from "react";
import SearchInput from "../components/SearchInput";
import ResultList from "../components/ResultList";
import AIAnswer from "../components/AIAnswer";
import VoiceButton from "../components/VoiceButton";
import StatusBar from "../components/StatusBar";
import type { FileResult } from "../types";

const API_BASE = (window as any).__TAURI__ ? "/api/v1" : "http://localhost:8000/api/v1";

export default function SpotlightWindow() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<FileResult[]>([]);
  const [selectedIdx, setSelectedIdx] = useState(0);
  const [aiAnswer, setAiAnswer] = useState("");
  const [aiSources, setAiSources] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [isAsking, setIsAsking] = useState(false);
  const [voiceActive, setVoiceActive] = useState(false);
  const debounceRef = useRef<ReturnType<typeof setTimeout>>();

  const search = useCallback(async (q: string) => {
    if (!q.trim()) {
      setResults([]);
      setAiAnswer("");
      return;
    }
    setIsSearching(true);
    try {
      const res = await fetch(`${API_BASE}/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q, type: "files", limit: 6 }),
      });
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
    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: q }),
      });
      const data = await res.json();
      setAiAnswer(data.message || "");
      setAiSources(data.sources || []);
    } catch (e: any) {
      setAiAnswer(`Error: ${e.message}`);
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

  return (
    <div
      className="h-screen w-screen bg-zinc-900/95 backdrop-blur-xl rounded-2xl border border-zinc-700/50 shadow-2xl flex flex-col overflow-hidden"
      onKeyDown={handleKeyDown}
      data-tauri-drag-region
    >
      {/* Search bar */}
      <SearchInput
        query={query}
        onChange={setQuery}
        isSearching={isSearching}
        voiceActive={voiceActive}
        onVoiceToggle={() => setVoiceActive(!voiceActive)}
      />

      {/* Voice mode overlay */}
      {voiceActive && (
        <VoiceButton
          active={voiceActive}
          onClose={() => setVoiceActive(false)}
          onTranscript={(text) => {
            setQuery(text);
            setVoiceActive(false);
            askAI(text);
          }}
        />
      )}

      {/* Results + AI answer */}
      <div className="flex-1 overflow-y-auto min-h-0">
        {results.length > 0 && (
          <ResultList
            results={results}
            selectedIdx={selectedIdx}
            onSelect={setSelectedIdx}
            onOpen={openFile}
          />
        )}

        {(aiAnswer || isAsking) && (
          <AIAnswer
            answer={aiAnswer}
            sources={aiSources}
            isLoading={isAsking}
          />
        )}

        {!query && !voiceActive && (
          <div className="flex flex-col items-center justify-center h-full text-zinc-500 text-sm py-12">
            <div className="w-10 h-10 rounded-xl bg-brand-600 flex items-center justify-center text-white font-bold text-lg mb-3">
              C
            </div>
            <p className="mb-1">Type to search your files</p>
            <p className="text-xs text-zinc-600">
              <kbd className="px-1.5 py-0.5 bg-zinc-800 rounded text-zinc-400">
                ⌘⏎
              </kbd>{" "}
              AI answer{" "}
              <kbd className="px-1.5 py-0.5 bg-zinc-800 rounded text-zinc-400 ml-2">
                ⌘⇧V
              </kbd>{" "}
              Voice
            </p>
          </div>
        )}
      </div>

      {/* Status bar */}
      <StatusBar resultsCount={results.length} query={query} />
    </div>
  );
}
