import { ReactNode } from "react";
import { useStore } from "../../stores/useStore";
import { Menu } from "lucide-react";

interface Props {
  sidebar: ReactNode;
  children: ReactNode;
}

export default function Layout({ sidebar, children }: Props) {
  const { sidebarOpen, toggleSidebar } = useStore();

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <aside
        className={`${
          sidebarOpen ? "w-64" : "w-0"
        } flex-shrink-0 border-r border-zinc-800 bg-zinc-900 transition-all duration-200 overflow-hidden`}
      >
        <div className="w-64 h-full flex flex-col">{sidebar}</div>
      </aside>

      {/* Main content */}
      <main className="flex-1 flex flex-col min-w-0">
        {/* Top bar */}
        <div className="h-12 flex items-center px-4 border-b border-zinc-800 bg-zinc-900/50 backdrop-blur flex-shrink-0">
          <button
            onClick={toggleSidebar}
            className="p-1.5 hover:bg-zinc-800 rounded-lg transition-colors mr-3"
          >
            <Menu size={18} className="text-zinc-400" />
          </button>
          <span className="text-sm font-semibold text-zinc-300">ChatFiles</span>
        </div>

        <div className="flex-1 overflow-hidden">{children}</div>
      </main>
    </div>
  );
}
