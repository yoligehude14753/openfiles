import { useEffect } from "react";
import { useTranslation } from "react-i18next";
import {
  CheckCircle2,
  XCircle,
  Cpu,
  FolderOpen,
  DollarSign,
  BarChart3,
} from "lucide-react";
import { useStore } from "../../stores/useStore";
import { api } from "../../services/api";

export default function SettingsPanel() {
  const { t } = useTranslation();
  const { settings, setSettings, stats, setStats } = useStore();

  useEffect(() => {
    api.getSettings().then(setSettings).catch(console.error);
    api.getStats().then(setStats).catch(console.error);
  }, []);

  if (!settings) {
    return (
      <div className="flex items-center justify-center h-full text-zinc-500">
        Loading...
      </div>
    );
  }

  return (
    <div className="h-full overflow-y-auto">
      <div className="max-w-2xl mx-auto p-6 space-y-6">
        <h2 className="text-xl font-semibold">{t("settings.title")}</h2>

        {/* LLM Provider */}
        <section className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-5">
          <div className="flex items-center gap-2 mb-4">
            <Cpu size={18} className="text-brand-400" />
            <h3 className="font-medium">{t("settings.provider")}</h3>
          </div>

          <div className="grid grid-cols-2 gap-3">
            {["yunwu", "ollama", "openai", "claude"].map((p) => {
              const desc: Record<string, string> = {
                yunwu: "OpenAI-compatible proxy (GPT, Gemini, Claude)",
                ollama: "Local LLM, no API key needed",
                openai: "Direct OpenAI API",
                claude: "Anthropic Claude API",
              };
              return (
              <div
                key={p}
                className={`p-3 rounded-lg border transition-colors ${
                  settings.llm_provider === p
                    ? "border-brand-500 bg-brand-500/10"
                    : "border-zinc-700 hover:border-zinc-600"
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium capitalize">{p}</span>
                  {settings.llm_provider === p && (
                    <span className="badge bg-brand-500/20 text-brand-400">
                      Active
                    </span>
                  )}
                </div>
                <div className="text-xs text-zinc-500 mt-1">
                  {desc[p]}
                </div>
              </div>
              );
            })}
          </div>

          {/* Ollama Status */}
          <div className="mt-4 flex items-center gap-2 text-sm">
            <span className="text-zinc-400">{t("settings.ollamaStatus")}:</span>
            {settings.ollama_available ? (
              <span className="flex items-center gap-1 text-green-400">
                <CheckCircle2 size={14} /> {t("settings.connected")}
              </span>
            ) : (
              <span className="flex items-center gap-1 text-red-400">
                <XCircle size={14} /> {t("settings.disconnected")}
              </span>
            )}
          </div>
        </section>

        {/* Scan Directories */}
        <section className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-5">
          <div className="flex items-center gap-2 mb-4">
            <FolderOpen size={18} className="text-brand-400" />
            <h3 className="font-medium">{t("settings.directories")}</h3>
          </div>
          <div className="space-y-2">
            {settings.scan_directories.map((dir, i) => (
              <div
                key={i}
                className="flex items-center gap-2 px-3 py-2 bg-zinc-800 rounded-lg text-sm font-mono text-zinc-300"
              >
                <FolderOpen size={14} className="text-zinc-500" />
                {dir}
              </div>
            ))}
          </div>
        </section>

        {/* Statistics */}
        {stats && (
          <section className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-5">
            <div className="flex items-center gap-2 mb-4">
              <BarChart3 size={18} className="text-brand-400" />
              <h3 className="font-medium">{t("settings.stats")}</h3>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
              {[
                { label: "Files", value: stats.indexed_files },
                { label: "Slides", value: stats.total_slides },
                { label: "Tokens", value: stats.total_tokens.toLocaleString() },
              ].map(({ label, value }) => (
                <div key={label} className="text-center p-3 bg-zinc-800 rounded-lg">
                  <div className="text-2xl font-semibold text-zinc-100">
                    {value}
                  </div>
                  <div className="text-xs text-zinc-500 mt-1">{label}</div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Budget */}
        <section className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-5">
          <div className="flex items-center gap-2 mb-4">
            <DollarSign size={18} className="text-brand-400" />
            <h3 className="font-medium">{t("settings.budget")}</h3>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="p-3 bg-zinc-800 rounded-lg">
              <div className="text-sm text-zinc-400">Daily</div>
              <div className="text-lg font-semibold">
                ${stats?.total_cost?.toFixed(2) || "0.00"}{" "}
                <span className="text-xs text-zinc-500">
                  / ${settings.daily_budget_usd}
                </span>
              </div>
            </div>
            <div className="p-3 bg-zinc-800 rounded-lg">
              <div className="text-sm text-zinc-400">Monthly</div>
              <div className="text-lg font-semibold">
                ${settings.monthly_budget_usd}
                <span className="text-xs text-zinc-500 ml-1">limit</span>
              </div>
            </div>
          </div>
        </section>

        {/* Info */}
        <div className="text-center text-xs text-zinc-600 py-4">
          ChatFiles v0.1.0 &middot; Platform: {settings.platform}
        </div>
      </div>
    </div>
  );
}
