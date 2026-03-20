import {
  FileText, Image, Code, Table, Presentation, File,
} from "lucide-react";
import type { FileResult } from "../types";

const ICONS: Record<string, typeof File> = {
  pdf: FileText, docx: FileText, doc: FileText, txt: FileText, md: FileText,
  xlsx: Table, xls: Table, csv: Table,
  pptx: Presentation,
  jpg: Image, jpeg: Image, png: Image, gif: Image, webp: Image, svg: Image,
  py: Code, js: Code, ts: Code, java: Code, c: Code, cpp: Code, html: Code,
};

const COLORS: Record<string, string> = {
  pdf: "text-red-400", docx: "text-blue-400", xlsx: "text-green-400",
  csv: "text-green-400", pptx: "text-orange-400",
  jpg: "text-purple-400", png: "text-purple-400",
  py: "text-yellow-400", js: "text-yellow-400", ts: "text-blue-400",
};

interface Props {
  results: FileResult[];
  selectedIdx: number;
  onSelect: (i: number) => void;
  onOpen: (path: string) => void;
}

export default function ResultList({ results, selectedIdx, onSelect, onOpen }: Props) {
  return (
    <div className="border-b border-zinc-700/50">
      {results.map((r, i) => {
        const Icon = ICONS[r.type] || File;
        const color = COLORS[r.type] || "text-zinc-400";
        const filename = r.path.split("/").pop() || r.path;
        const dir = r.path.substring(0, r.path.lastIndexOf("/"));
        const score = Math.round((r.similarity || 0) * 100);

        return (
          <div
            key={r.file_id}
            className={`flex items-center gap-3 px-4 py-2.5 cursor-pointer transition-colors ${
              i === selectedIdx ? "bg-brand-600/20" : "hover:bg-zinc-800/50"
            }`}
            onClick={() => onOpen(r.path)}
            onMouseEnter={() => onSelect(i)}
          >
            <Icon size={18} className={`${color} flex-shrink-0`} />
            <div className="flex-1 min-w-0">
              <div className="text-sm text-zinc-200 truncate">{filename}</div>
              <div className="text-xs text-zinc-600 font-mono truncate">{dir}</div>
            </div>
            <div className="flex items-center gap-2 flex-shrink-0">
              <span className="text-[10px] px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-400 uppercase">
                {r.type}
              </span>
              {score > 0 && (
                <span className="text-xs text-zinc-500 w-8 text-right">{score}%</span>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
