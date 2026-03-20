import { useEffect, useRef, useState } from "react";
import { Mic, MicOff, Loader2 } from "lucide-react";

const YUNWU_WS = "wss://yunwu.ai/v1/realtime?model=gpt-4o-realtime-preview";
const API_KEY = ""; // Will be fetched from backend settings

interface Props {
  active: boolean;
  onClose: () => void;
  onTranscript: (text: string) => void;
}

export default function VoiceButton({ active, onClose, onTranscript }: Props) {
  const [status, setStatus] = useState<"connecting" | "listening" | "thinking" | "speaking" | "error">("connecting");
  const [transcript, setTranscript] = useState("");
  const [aiText, setAiText] = useState("");
  const wsRef = useRef<WebSocket | null>(null);
  const audioCtxRef = useRef<AudioContext | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const processorRef = useRef<ScriptProcessorNode | null>(null);

  useEffect(() => {
    if (!active) return;
    let cancelled = false;

    (async () => {
      try {
        // Get API key from backend settings
        const base = (window as any).__TAURI__ ? "" : "http://localhost:8000";
        const settingsRes = await fetch(`${base}/api/v1/settings`);
        const settings = await settingsRes.json();

        const apiKey = settings.yunwu_api_key || API_KEY;
        if (!apiKey) {
          setStatus("error");
          setAiText("No API key configured for voice. Set YUNWU_API_KEY in .env");
          return;
        }

        // Get microphone
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        if (cancelled) { stream.getTracks().forEach(t => t.stop()); return; }
        streamRef.current = stream;

        // Connect WebSocket
        const ws = new WebSocket(YUNWU_WS);
        ws.binaryType = "arraybuffer";
        wsRef.current = ws;

        ws.onopen = () => {
          // Configure session with tools
          ws.send(JSON.stringify({
            type: "session.update",
            session: {
              modalities: ["text", "audio"],
              instructions: "You are ChatFiles, a helpful local file assistant. Answer concisely. When the user asks about files, use the search_files function to find relevant files first.",
              voice: "alloy",
              input_audio_transcription: { model: "whisper-1" },
              tools: [{
                type: "function",
                name: "search_files",
                description: "Search the user's local indexed files by semantic query",
                parameters: {
                  type: "object",
                  properties: {
                    query: { type: "string", description: "Search query" }
                  },
                  required: ["query"]
                }
              }]
            }
          }));

          // Start audio capture
          const audioCtx = new AudioContext({ sampleRate: 24000 });
          audioCtxRef.current = audioCtx;

          const source = audioCtx.createMediaStreamSource(stream);
          const processor = audioCtx.createScriptProcessor(4096, 1, 1);
          processorRef.current = processor;

          processor.onaudioprocess = (e) => {
            const input = e.inputBuffer.getChannelData(0);
            const pcm16 = new Int16Array(input.length);
            for (let i = 0; i < input.length; i++) {
              pcm16[i] = Math.max(-32768, Math.min(32767, Math.round(input[i] * 32767)));
            }
            const b64 = btoa(String.fromCharCode(...new Uint8Array(pcm16.buffer)));
            ws.send(JSON.stringify({
              type: "input_audio_buffer.append",
              audio: b64,
            }));
          };

          source.connect(processor);
          processor.connect(audioCtx.destination);
          setStatus("listening");
        };

        ws.onmessage = async (event) => {
          const data = JSON.parse(event.data);

          switch (data.type) {
            case "conversation.item.input_audio_transcription.completed":
              setTranscript(data.transcript || "");
              onTranscript(data.transcript || "");
              break;

            case "response.audio_transcript.delta":
              setAiText(prev => prev + (data.delta || ""));
              setStatus("speaking");
              break;

            case "response.audio.delta":
              playAudioChunk(data.delta);
              break;

            case "response.function_call_arguments.done":
              if (data.name === "search_files") {
                setStatus("thinking");
                try {
                  const args = JSON.parse(data.arguments);
                  const searchRes = await fetch(`${base}/api/v1/search`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ query: args.query, type: "files", limit: 5 }),
                  });
                  const searchData = await searchRes.json();
                  const resultSummary = (searchData.results || [])
                    .map((r: any) => `${r.path.split("/").pop()}: ${r.summary || ""}`.slice(0, 200))
                    .join("\n");

                  ws.send(JSON.stringify({
                    type: "conversation.item.create",
                    item: {
                      type: "function_call_output",
                      call_id: data.call_id,
                      output: resultSummary || "No matching files found.",
                    }
                  }));
                  ws.send(JSON.stringify({ type: "response.create" }));
                } catch {
                  ws.send(JSON.stringify({
                    type: "conversation.item.create",
                    item: {
                      type: "function_call_output",
                      call_id: data.call_id,
                      output: "Search failed.",
                    }
                  }));
                  ws.send(JSON.stringify({ type: "response.create" }));
                }
              }
              break;

            case "response.done":
              setStatus("listening");
              setAiText("");
              break;

            case "error":
              setStatus("error");
              setAiText(data.error?.message || "Voice connection error");
              break;
          }
        };

        ws.onerror = () => setStatus("error");
        ws.onclose = () => { if (!cancelled) onClose(); };

      } catch (err: any) {
        setStatus("error");
        setAiText(err.message || "Failed to start voice");
      }
    })();

    return () => {
      cancelled = true;
      processorRef.current?.disconnect();
      audioCtxRef.current?.close();
      streamRef.current?.getTracks().forEach(t => t.stop());
      wsRef.current?.close();
    };
  }, [active]);

  const playAudioChunk = (b64: string) => {
    if (!audioCtxRef.current) return;
    try {
      const binary = atob(b64);
      const bytes = new Uint8Array(binary.length);
      for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
      const pcm16 = new Int16Array(bytes.buffer);
      const float32 = new Float32Array(pcm16.length);
      for (let i = 0; i < pcm16.length; i++) float32[i] = pcm16[i] / 32768;

      const buffer = audioCtxRef.current.createBuffer(1, float32.length, 24000);
      buffer.getChannelData(0).set(float32);
      const source = audioCtxRef.current.createBufferSource();
      source.buffer = buffer;
      source.connect(audioCtxRef.current.destination);
      source.start();
    } catch {}
  };

  const statusConfig = {
    connecting: { icon: Loader2, text: "Connecting...", color: "text-zinc-400", animate: true },
    listening: { icon: Mic, text: "Listening...", color: "text-red-400", animate: false },
    thinking: { icon: Loader2, text: "Searching files...", color: "text-brand-400", animate: true },
    speaking: { icon: Mic, text: "Speaking...", color: "text-green-400", animate: false },
    error: { icon: MicOff, text: "Error", color: "text-red-500", animate: false },
  };

  const cfg = statusConfig[status];
  const Icon = cfg.icon;

  return (
    <div className="flex flex-col items-center py-6 px-4 border-b border-zinc-700/50">
      <div className={`w-16 h-16 rounded-full flex items-center justify-center mb-3 ${
        status === "listening" ? "bg-red-500/20 animate-pulse" : "bg-zinc-800"
      }`}>
        <Icon size={28} className={`${cfg.color} ${cfg.animate ? "animate-spin" : ""}`} />
      </div>
      <p className={`text-sm ${cfg.color} mb-1`}>{cfg.text}</p>

      {transcript && (
        <p className="text-xs text-zinc-400 text-center max-w-md">"{transcript}"</p>
      )}
      {aiText && (
        <p className="text-xs text-zinc-300 text-center max-w-md mt-1">{aiText}</p>
      )}

      <button
        onClick={onClose}
        className="mt-3 text-xs text-zinc-600 hover:text-zinc-400 transition-colors"
      >
        Press Esc to close voice
      </button>
    </div>
  );
}
