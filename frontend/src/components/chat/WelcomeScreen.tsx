import { useTranslation } from "react-i18next";
import { FileText, Image, Code, Table } from "lucide-react";

interface Props {
  onSuggestionClick: (text: string) => void;
}

const ICONS = [FileText, Image, Code, Table];

export default function WelcomeScreen({ onSuggestionClick }: Props) {
  const { t } = useTranslation();
  const suggestions = t("chat.welcome.suggestions", {
    returnObjects: true,
  }) as string[];

  return (
    <div className="flex flex-col items-center justify-center h-full px-4 animate-fade-in">
      <div className="w-16 h-16 rounded-2xl bg-brand-600/20 flex items-center justify-center mb-6">
        <div className="w-10 h-10 rounded-xl bg-brand-600 flex items-center justify-center text-white font-bold text-xl">
          C
        </div>
      </div>

      <h1 className="text-2xl font-semibold text-zinc-100 mb-2">
        {t("chat.welcome.title")}
      </h1>
      <p className="text-sm text-zinc-500 mb-10 text-center max-w-md">
        {t("chat.welcome.subtitle")}
      </p>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-lg">
        {suggestions.map((text, i) => {
          const Icon = ICONS[i % ICONS.length];
          return (
            <button
              key={i}
              onClick={() => onSuggestionClick(text)}
              className="flex items-start gap-3 p-4 rounded-xl border border-zinc-800 hover:border-zinc-700 hover:bg-zinc-900 transition-all text-left group"
            >
              <Icon
                size={18}
                className="text-zinc-500 group-hover:text-brand-400 mt-0.5 flex-shrink-0"
              />
              <span className="text-sm text-zinc-400 group-hover:text-zinc-200">
                {text}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
