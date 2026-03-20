import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import {
  FileText,
  Image,
  Code,
  Table,
  Presentation,
  File,
  Search,
  HardDriveDownload,
  Loader2,
} from "lucide-react";
import { api } from "../../services/api";
import type { FileResult, IndexStatus } from "../../types";

const TYPE_ICONS: Record<string, typeof File> = {
  pdf: FileText,
  docx: FileText,
  doc: FileText,
  xlsx: Table,
  xls: Table,
  csv: Table,
  pptx: Presentation,
  jpg: Image,
  jpeg: Image,
  png: Image,
  gif: Image,
  py: Code,
  js: Code,
  ts: Code,
  md: FileText,
  txt: FileText,
  html: Code,
};

function formatSize(bytes: number | null): string {
  if (!bytes) return "-";
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export default function FileBrowser() {
  const { t } = useTranslation();
  const [files, setFiles] = useState<FileResult[]>([]);
  const [total, setTotal] = useState(0);
  const [typeFilter, setTypeFilter] = useState<string>("");
  const [types, setTypes] = useState<Record<string, number>>({});
  const [searchQuery, setSearchQuery] = useState("");
  const [indexStatus, setIndexStatus] = useState<IndexStatus | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFiles();
    loadTypes();
    loadIndexStatus();
  }, [typeFilter]);

  const loadFiles = async () => {
    setLoading(true);
    try {
      const res = await api.getFiles({
        file_type: typeFilter || undefined,
        limit: 50,
      });
      setFiles(res.files);
      setTotal(res.total);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadTypes = async () => {
    try {
      setTypes(await api.getFileTypes());
    } catch (err) {
      console.error(err);
    }
  };

  const loadIndexStatus = async () => {
    try {
      setIndexStatus(await api.getIndexStatus());
    } catch (err) {
      console.error(err);
    }
  };

  const startIndexing = async () => {
    try {
      await api.startIndexing();
      setIndexStatus((prev) => (prev ? { ...prev, in_progress: true } : null));
      const interval = setInterval(async () => {
        const status = await api.getIndexStatus();
        setIndexStatus(status);
        if (!status.in_progress) {
          clearInterval(interval);
          loadFiles();
          loadTypes();
        }
      }, 3000);
    } catch (err) {
      console.error(err);
    }
  };

  const filteredFiles = searchQuery
    ? files.filter(
        (f) =>
          f.path.toLowerCase().includes(searchQuery.toLowerCase()) ||
          (f.summary || "").toLowerCase().includes(searchQuery.toLowerCase())
      )
    : files;

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-zinc-800 space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">{t("files.title")}</h2>
          <div className="flex items-center gap-3">
            {indexStatus && (
              <span className="text-xs text-zinc-500">
                {indexStatus.completed}/{indexStatus.total} {t("files.indexed")}
              </span>
            )}
            <button
              onClick={startIndexing}
              disabled={indexStatus?.in_progress}
              className="btn-primary text-sm flex items-center gap-2"
            >
              {indexStatus?.in_progress ? (
                <>
                  <Loader2 size={14} className="animate-spin" />
                  {t("files.indexing")}
                </>
              ) : (
                <>
                  <HardDriveDownload size={14} />
                  {t("files.startIndexing")}
                </>
              )}
            </button>
          </div>
        </div>

        <div className="flex gap-2">
          <div className="relative flex-1">
            <Search
              size={14}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500"
            />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Filter files..."
              className="w-full pl-9 pr-3 py-2 text-sm bg-zinc-900 border border-zinc-700 rounded-lg focus:outline-none focus:border-brand-500"
            />
          </div>
          <select
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
            className="px-3 py-2 text-sm bg-zinc-900 border border-zinc-700 rounded-lg focus:outline-none focus:border-brand-500"
          >
            <option value="">{t("files.allTypes")}</option>
            {Object.entries(types)
              .sort(([, a], [, b]) => b - a)
              .map(([type, count]) => (
                <option key={type} value={type}>
                  {type.toUpperCase()} ({count})
                </option>
              ))}
          </select>
        </div>
      </div>

      {/* File list */}
      <div className="flex-1 overflow-y-auto">
        {loading ? (
          <div className="flex items-center justify-center h-32">
            <Loader2 size={24} className="animate-spin text-zinc-500" />
          </div>
        ) : filteredFiles.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-32 text-zinc-500 text-sm">
            {t("files.noFiles")}
          </div>
        ) : (
          <div className="divide-y divide-zinc-800/50">
            {filteredFiles.map((f) => {
              const Icon = TYPE_ICONS[f.type] || File;
              const filename = f.path.split("/").pop() || f.path;
              const dir = f.path.replace(filename, "");

              return (
                <div
                  key={f.file_id}
                  className="flex items-center gap-3 px-4 py-3 hover:bg-zinc-900/50 transition-colors"
                >
                  <Icon size={18} className="text-zinc-500 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium text-zinc-200 truncate">
                      {filename}
                    </div>
                    <div className="text-xs text-zinc-600 font-mono truncate">
                      {dir}
                    </div>
                    {f.summary && (
                      <div className="text-xs text-zinc-500 mt-0.5 truncate">
                        {f.summary}
                      </div>
                    )}
                  </div>
                  <div className="text-right flex-shrink-0">
                    <span className="badge bg-zinc-800 text-zinc-400">
                      {f.type}
                    </span>
                    <div className="text-[10px] text-zinc-600 mt-1">
                      {formatSize(f.size)}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
