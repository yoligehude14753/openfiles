import {
  FileText,
  Image,
  Code,
  Table,
  Presentation,
  File,
} from "lucide-react";
import type { SourceRef } from "../../types";

const TYPE_CONFIG: Record<string, { icon: typeof File; color: string; bg: string }> = {
  pdf: { icon: FileText, color: "text-red-400", bg: "bg-red-400/10" },
  docx: { icon: FileText, color: "text-blue-400", bg: "bg-blue-400/10" },
  doc: { icon: FileText, color: "text-blue-400", bg: "bg-blue-400/10" },
  xlsx: { icon: Table, color: "text-green-400", bg: "bg-green-400/10" },
  xls: { icon: Table, color: "text-green-400", bg: "bg-green-400/10" },
  csv: { icon: Table, color: "text-green-400", bg: "bg-green-400/10" },
  pptx: { icon: Presentation, color: "text-orange-400", bg: "bg-orange-400/10" },
  jpg: { icon: Image, color: "text-purple-400", bg: "bg-purple-400/10" },
  jpeg: { icon: Image, color: "text-purple-400", bg: "bg-purple-400/10" },
  png: { icon: Image, color: "text-purple-400", bg: "bg-purple-400/10" },
  py: { icon: Code, color: "text-yellow-400", bg: "bg-yellow-400/10" },
  js: { icon: Code, color: "text-yellow-400", bg: "bg-yellow-400/10" },
  ts: { icon: Code, color: "text-blue-400", bg: "bg-blue-400/10" },
  md: { icon: FileText, color: "text-zinc-400", bg: "bg-zinc-400/10" },
  txt: { icon: FileText, color: "text-zinc-400", bg: "bg-zinc-400/10" },
};

export default function FileCard({ source }: { source: SourceRef }) {
  const config = TYPE_CONFIG[source.type] || {
    icon: File,
    color: "text-zinc-400",
    bg: "bg-zinc-400/10",
  };
  const Icon = config.icon;
  const filename = source.path.split("/").pop() || source.path;

  return (
    <div className="inline-flex items-center gap-2 px-2.5 py-1.5 rounded-lg bg-zinc-800/50 border border-zinc-700/50 text-xs hover:bg-zinc-800 transition-colors">
      <div className={`p-1 rounded ${config.bg}`}>
        <Icon size={12} className={config.color} />
      </div>
      <span className="text-zinc-300 font-mono truncate max-w-[200px]">
        {filename}
      </span>
      <span className="badge bg-zinc-700 text-zinc-400">{source.type}</span>
    </div>
  );
}
