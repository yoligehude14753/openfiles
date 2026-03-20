interface Props {
  resultsCount: number;
  query: string;
}

export default function StatusBar({ resultsCount, query }: Props) {
  return (
    <div className="flex items-center justify-between px-4 py-1.5 border-t border-zinc-700/50 text-[10px] text-zinc-600">
      <div className="flex items-center gap-3">
        <span>
          <kbd className="px-1 py-0.5 bg-zinc-800 rounded text-zinc-500">↑↓</kbd> Navigate
        </span>
        <span>
          <kbd className="px-1 py-0.5 bg-zinc-800 rounded text-zinc-500">⏎</kbd> Open
        </span>
        <span>
          <kbd className="px-1 py-0.5 bg-zinc-800 rounded text-zinc-500">⌘⏎</kbd> AI
        </span>
        <span>
          <kbd className="px-1 py-0.5 bg-zinc-800 rounded text-zinc-500">Esc</kbd> Close
        </span>
      </div>
      {query && (
        <span>{resultsCount} files</span>
      )}
    </div>
  );
}
