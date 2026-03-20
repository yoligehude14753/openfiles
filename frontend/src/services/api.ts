import type {
  FileResult,
  SlideResult,
  Conversation,
  ChatMessage,
  Stats,
  SystemSettings,
  IndexStatus,
} from "../types";

const BASE = "/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

export const api = {
  // Search
  searchFiles: (query: string, limit = 10, fileType?: string) =>
    request<{ results: FileResult[] }>("/search", {
      method: "POST",
      body: JSON.stringify({ query, type: "files", limit, file_type: fileType }),
    }),

  searchSlides: (query: string, limit = 20) =>
    request<{ results: SlideResult[] }>("/search", {
      method: "POST",
      body: JSON.stringify({ query, type: "slides", limit }),
    }),

  // Chat
  sendMessage: (message: string, conversationId?: number) =>
    request<{ conversation_id: number; message: string; sources: any[] }>(
      "/chat",
      {
        method: "POST",
        body: JSON.stringify({ message, conversation_id: conversationId }),
      }
    ),

  // Conversations
  getConversations: () => request<Conversation[]>("/conversations"),

  getMessages: (conversationId: number) =>
    request<ChatMessage[]>(`/conversations/${conversationId}/messages`),

  deleteConversation: (conversationId: number) =>
    request<{ status: string }>(`/conversations/${conversationId}`, {
      method: "DELETE",
    }),

  // Files
  getFiles: (params?: {
    file_type?: string;
    status?: string;
    limit?: number;
    offset?: number;
  }) => {
    const qs = new URLSearchParams();
    if (params?.file_type) qs.set("file_type", params.file_type);
    if (params?.status) qs.set("status", params.status);
    if (params?.limit) qs.set("limit", String(params.limit));
    if (params?.offset) qs.set("offset", String(params.offset));
    return request<{ total: number; files: FileResult[] }>(
      `/files?${qs.toString()}`
    );
  },

  getFileTypes: () => request<Record<string, number>>("/files/types"),

  // Indexing
  startIndexing: () =>
    request<{ status: string; message: string }>("/index", { method: "POST" }),

  getIndexStatus: () => request<IndexStatus>("/index/status"),

  // System
  getStats: () => request<Stats>("/stats"),
  getSettings: () => request<SystemSettings>("/settings"),
};

export function createChatWebSocket(
  onMessage: (data: any) => void,
  onError?: (err: Event) => void
) {
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const ws = new WebSocket(`${protocol}//${window.location.host}/api/v1/chat/stream`);

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      onMessage(data);
    } catch {
      // ignore
    }
  };

  ws.onerror = (err) => onError?.(err);

  return ws;
}
