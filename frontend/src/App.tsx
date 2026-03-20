import { useEffect } from "react";
import SpotlightWindow from "./windows/Spotlight";

export default function App() {
  useEffect(() => {
    const handler = async (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        try {
          const { getCurrentWindow } = await import("@tauri-apps/api/window");
          getCurrentWindow().hide();
        } catch {
          // not in Tauri context
        }
      }
    };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, []);

  return <SpotlightWindow />;
}
