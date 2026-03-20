import { useState, useRef, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { ArrowUp } from "lucide-react";

interface Props {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export default function ChatInput({ onSend, disabled }: Props) {
  const { t } = useTranslation();
  const [input, setInput] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height =
        Math.min(textareaRef.current.scrollHeight, 200) + "px";
    }
  }, [input]);

  const handleSubmit = () => {
    const trimmed = input.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setInput("");
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="border-t border-zinc-800 bg-zinc-950 p-4">
      <div className="max-w-3xl mx-auto relative">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={t("chat.placeholder")}
          disabled={disabled}
          rows={1}
          className="w-full resize-none rounded-xl border border-zinc-700 bg-zinc-900 px-4 py-3 pr-12 text-sm text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500/50 disabled:opacity-50 transition-all"
        />
        <button
          onClick={handleSubmit}
          disabled={disabled || !input.trim()}
          className="absolute right-2.5 bottom-2.5 p-1.5 rounded-lg bg-brand-600 hover:bg-brand-700 text-white disabled:opacity-30 disabled:hover:bg-brand-600 transition-colors"
        >
          <ArrowUp size={16} />
        </button>
      </div>
      <p className="text-[10px] text-zinc-600 text-center mt-2">
        ChatFiles uses AI to search your local files. Responses may not always be accurate.
      </p>
    </div>
  );
}
