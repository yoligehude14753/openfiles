import { useEffect } from "react";
import { useStore } from "./stores/useStore";
import { api } from "./services/api";
import Layout from "./components/layout/Layout";
import Sidebar from "./components/layout/Sidebar";
import ChatView from "./components/chat/ChatView";
import FileBrowser from "./components/files/FileBrowser";
import SettingsPanel from "./components/settings/SettingsPanel";

export default function App() {
  const { view, setStats, setSettings, setConversations } = useStore();

  useEffect(() => {
    api.getStats().then(setStats).catch(console.error);
    api.getSettings().then(setSettings).catch(console.error);
    api.getConversations().then(setConversations).catch(console.error);
  }, []);

  return (
    <Layout sidebar={<Sidebar />}>
      {view === "chat" && <ChatView />}
      {view === "files" && <FileBrowser />}
      {view === "settings" && <SettingsPanel />}
    </Layout>
  );
}
