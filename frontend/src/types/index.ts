export interface FileResult {
  file_id: number;
  path: string;
  type: string;
  summary: string | null;
  keywords: string | null;
  category: string | null;
  confidence: number | null;
  similarity: number;
  size: number | null;
  mtime: string | null;
  status?: string;
  indexed_at?: string | null;
}

export interface SlideResult {
  slide_id: number;
  file_id: number;
  file_path: string;
  page_number: number;
  title: string | null;
  summary: string | null;
  keywords: string | null;
  notes: string | null;
  thumbnail_path: string | null;
  confidence: number | null;
  similarity: number;
}

export interface SourceRef {
  file_id: number;
  path: string;
  type: string;
}

export interface ChatMessage {
  id: number;
  role: "user" | "assistant";
  content: string;
  sources?: SourceRef[] | null;
  created_at: string;
}

export interface Conversation {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface Stats {
  total_files: number;
  indexed_files: number;
  total_slides: number;
  total_tokens: number;
  total_cost: number;
}

export interface SystemSettings {
  llm_provider: string;
  embedding_provider: string;
  ollama_host: string;
  ollama_model: string;
  ollama_available: boolean;
  scan_directories: string[];
  max_file_size_mb: number;
  daily_budget_usd: number;
  monthly_budget_usd: number;
  platform: string;
}

export interface IndexStatus {
  in_progress: boolean;
  total: number;
  completed: number;
  failed: number;
  pending: number;
}

export type View = "chat" | "files" | "settings";
