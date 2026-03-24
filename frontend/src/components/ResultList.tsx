import { useEffect, useRef } from "react";
import { motion } from "framer-motion";
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

const TYPE_COLORS: Record<string, string> = {
  pdf: "bg-red-500/15 text-red-400",
  docx: "bg-blue-500/15 text-blue-400",
  xlsx: "bg-green-500/15 text-green-400",
  csv: "bg-green-500/15 text-green-400",
  pptx: "bg-orange-500/15 text-orange-400",
  jpg: "bg-purple-500/15 text-purple-400",
  png: "bg-purple-500/15 text-purple-400",
  py: "bg-yellow-500/15 text-yellow-400",
  js: "bg-yellow-500/15 text-yellow-400",
  ts: "bg-blue-500/15 text-blue-400",
  md: "bg-zinc-500/15 text-zinc-400",
};

interface Props {
  results: FileResult[];
  selectedIdx: number;
  onSelect: (i: number) => void;
  onOpen: (path: string) => void;
  containerRef: React.RefObject<HTMLDivElement>;
}

export default function ResultList({
  results, selectedIdx, onSelect, onOpen, containerRef,
}: Props) {
  const itemRefs = useRef<(HTMLDivElement | null)[]>([]);

  useEffect(() => {
    const el = itemRefs.current[selectedIdx];
    if (el) {
      el.scrollIntoView({ block: "nearest", behavior: "smooth" });
    }
  }, [selectedIdx]);

  return (
    <div className="border-b border-zinc-700/30 py-1">
      {results.map((r, i) => {
        const Icon = ICONS[r.type] || File;
        const typeColor = TYPE_COLORS[r.type] || "bg-zinc-500/15 text-zinc-400";
        const filename = r.path.split("/").pop() || r.path;
        const lastSlash = r.path.lastIndexOf("/");
        const dir = lastSlash > 0 ? r.path.substring(0, lastSlash) : "";
        const score = Math.round((r.similarity || 0) * 100);
        const isSelected = i === selectedIdx;

        return (
          <motion.div
            key={r.file_id}
            ref={(el) => { itemRefs.current[i] = el; }}
            initial={{ opacity: 0, x: -8 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.15, delay: i * 0.03 }}
            onClick={() => onOpen(r.path)}
            onMouseEnter={() => onSelect(i)}
            className={`relative flex items-center gap-3 px-4 py-2 cursor-pointer transition-colors duration-100 ${
              isSelected ? "bg-brand-500/10" : "hover:bg-zinc-800/40"
            }`}
          >
            {/* Selection indicator */}
            {isSelected && (
              <motion.div
                layoutId="selection"
                className="absolute left-0 top-1 bottom-1 w-0.5 bg-brand-400 rounded-full"
                transition={{ type: "spring", stiffness: 500, damping: 30 }}
              />
            )}

            <Icon size={16} className="text-zinc-500 flex-shrink-0 ml-1" />

            <div className="flex-1 min-w-0">
              <div className={`text-sm truncate ${isSelected ? "text-zinc-100" : "text-zinc-300"}`}>
                {filename}
              </div>
              {dir && (
                <div className="text-[11px] text-zinc-600 font-mono truncate">
                  {dir}
                </div>
              )}
            </div>

            <div className="flex items-center gap-2 flex-shrink-0">
              <span className={`text-[10px] px-1.5 py-0.5 rounded-md font-medium uppercase ${typeColor}`}>
                {r.type}
              </span>
              {score > 0 && (
                <span className="text-[11px] text-zinc-500 tabular-nums w-7 text-right">
                  {score}%
                </span>
              )}
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}
