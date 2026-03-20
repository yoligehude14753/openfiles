import { useTranslation } from "react-i18next";
import { useStore } from "../../stores/useStore";
import { api } from "../../services/api";
import {
  MessageSquarePlus,
  MessageCircle,
  FolderOpen,
  Settings,
  Trash2,
  Globe,
} from "lucide-react";

export default function Sidebar() {
  const { t, i18n } = useTranslation();
  const {
    view,
    setView,
    conversations,
    setConversations,
    currentConversationId,
    setCurrentConversationId,
    setMessages,
    setStreamMessage,
  } = useStore();

  const startNewChat = () => {
    setCurrentConversationId(null);
    setMessages([]);
    setStreamMessage(null);
    setView("chat");
  };

  const loadConversation = async (id: number) => {
    setCurrentConversationId(id);
    setView("chat");
    try {
      const msgs = await api.getMessages(id);
      setMessages(msgs);
    } catch (err) {
      console.error(err);
    }
  };

  const deleteConversation = async (id: number, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await api.deleteConversation(id);
      setConversations(conversations.filter((c) => c.id !== id));
      if (currentConversationId === id) {
        startNewChat();
      }
    } catch (err) {
      console.error(err);
    }
  };

  const toggleLang = () => {
    const next = i18n.language === "en" ? "zh" : "en";
    i18n.changeLanguage(next);
    localStorage.setItem("chatfiles-lang", next);
  };

  return (
    <div className="flex flex-col h-full">
      {/* Logo */}
      <div className="p-4 flex items-center gap-2">
        <div className="w-8 h-8 rounded-lg bg-brand-600 flex items-center justify-center font-bold text-white text-sm">
          C
        </div>
        <div>
          <div className="font-semibold text-sm">ChatFiles</div>
          <div className="text-[10px] text-zinc-500">v0.1.0</div>
        </div>
      </div>

      {/* New Chat */}
      <div className="px-3 mb-2">
        <button
          onClick={startNewChat}
          className="w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg border border-zinc-700 hover:bg-zinc-800 transition-colors"
        >
          <MessageSquarePlus size={16} />
          {t("sidebar.newChat")}
        </button>
      </div>

      {/* Nav */}
      <nav className="px-3 space-y-0.5 mb-3">
        <button
          onClick={() => setView("chat")}
          className={`w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg transition-colors ${
            view === "chat"
              ? "bg-zinc-800 text-white"
              : "text-zinc-400 hover:text-white hover:bg-zinc-800/50"
          }`}
        >
          <MessageCircle size={16} />
          {t("sidebar.conversations")}
        </button>
        <button
          onClick={() => setView("files")}
          className={`w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg transition-colors ${
            view === "files"
              ? "bg-zinc-800 text-white"
              : "text-zinc-400 hover:text-white hover:bg-zinc-800/50"
          }`}
        >
          <FolderOpen size={16} />
          {t("sidebar.files")}
        </button>
        <button
          onClick={() => setView("settings")}
          className={`w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg transition-colors ${
            view === "settings"
              ? "bg-zinc-800 text-white"
              : "text-zinc-400 hover:text-white hover:bg-zinc-800/50"
          }`}
        >
          <Settings size={16} />
          {t("sidebar.settings")}
        </button>
      </nav>

      {/* Conversation list */}
      <div className="flex-1 overflow-y-auto px-3">
        <div className="text-[11px] font-medium text-zinc-500 uppercase tracking-wider px-2 mb-1">
          {t("sidebar.conversations")}
        </div>
        {conversations.length === 0 ? (
          <p className="text-xs text-zinc-600 px-2 py-4">
            {t("sidebar.noConversations")}
          </p>
        ) : (
          <div className="space-y-0.5">
            {conversations.map((c) => (
              <div
                key={c.id}
                onClick={() => loadConversation(c.id)}
                className={`group flex items-center gap-2 px-2 py-1.5 text-sm rounded-lg cursor-pointer transition-colors ${
                  currentConversationId === c.id
                    ? "bg-zinc-800 text-white"
                    : "text-zinc-400 hover:bg-zinc-800/50 hover:text-zinc-200"
                }`}
              >
                <span className="flex-1 truncate text-xs">{c.title}</span>
                <button
                  onClick={(e) => deleteConversation(c.id, e)}
                  className="opacity-0 group-hover:opacity-100 p-0.5 hover:text-red-400 transition-all"
                >
                  <Trash2 size={12} />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="p-3 border-t border-zinc-800">
        <button
          onClick={toggleLang}
          className="flex items-center gap-2 px-2 py-1.5 text-xs text-zinc-500 hover:text-zinc-300 transition-colors"
        >
          <Globe size={14} />
          {i18n.language === "en" ? "中文" : "English"}
        </button>
      </div>
    </div>
  );
}
