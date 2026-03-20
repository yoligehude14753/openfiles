import { create } from "zustand";
import type {
  View,
  Conversation,
  ChatMessage,
  Stats,
  SystemSettings,
  SourceRef,
} from "../types";

interface StreamMessage {
  role: "assistant";
  content: string;
  sources?: SourceRef[];
  isStreaming: boolean;
}

interface AppState {
  view: View;
  setView: (v: View) => void;

  // Conversations
  conversations: Conversation[];
  setConversations: (c: Conversation[]) => void;
  currentConversationId: number | null;
  setCurrentConversationId: (id: number | null) => void;

  // Messages
  messages: ChatMessage[];
  setMessages: (m: ChatMessage[]) => void;
  addMessage: (m: ChatMessage) => void;

  // Streaming
  streamMessage: StreamMessage | null;
  setStreamMessage: (m: StreamMessage | null) => void;
  appendStreamContent: (text: string) => void;

  // Loading
  isLoading: boolean;
  setIsLoading: (v: boolean) => void;

  // Stats
  stats: Stats | null;
  setStats: (s: Stats) => void;

  // Settings
  settings: SystemSettings | null;
  setSettings: (s: SystemSettings) => void;

  // Sidebar
  sidebarOpen: boolean;
  toggleSidebar: () => void;
}

export const useStore = create<AppState>((set) => ({
  view: "chat",
  setView: (v) => set({ view: v }),

  conversations: [],
  setConversations: (c) => set({ conversations: c }),
  currentConversationId: null,
  setCurrentConversationId: (id) => set({ currentConversationId: id }),

  messages: [],
  setMessages: (m) => set({ messages: m }),
  addMessage: (m) => set((s) => ({ messages: [...s.messages, m] })),

  streamMessage: null,
  setStreamMessage: (m) => set({ streamMessage: m }),
  appendStreamContent: (text) =>
    set((s) => ({
      streamMessage: s.streamMessage
        ? { ...s.streamMessage, content: s.streamMessage.content + text }
        : null,
    })),

  isLoading: false,
  setIsLoading: (v) => set({ isLoading: v }),

  stats: null,
  setStats: (s) => set({ stats: s }),

  settings: null,
  setSettings: (s) => set({ settings: s }),

  sidebarOpen: true,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
}));
