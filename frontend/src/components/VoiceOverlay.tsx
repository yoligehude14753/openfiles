import { useEffect, useRef, useState, useCallback } from "react";
import { motion } from "framer-motion";
import { Mic, MicOff, Loader2, X } from "lucide-react";

const WS_URL = "wss://yunwu.ai/v1/realtime?model=gpt-4o-realtime-preview";

interface Props {
  apiBase: string;
  onClose: () => void;
  onTranscript: (text: string) => void;
}

type Status = "connecting" | "listening" | "thinking" | "speaking" | "error";

export default function VoiceOverlay({ apiBase, onClose, onTranscript }: Props) {
  const [status, setStatus] = useState<Status>("connecting");
  const [transcript, setTranscript] = useState("");
  const [aiText, setAiText] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const wsRef = useRef<WebSocket | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const audioCtxRef = useRef<AudioContext | null>(null);
  const audioQueueRef = useRef<AudioBufferSourceNode[]>([]);

  const cleanup = useCallback(() => {
    audioQueueRef.current.forEach((s) => { try { s.stop(); } catch {} });
    audioQueueRef.current = [];
    streamRef.current?.getTracks().forEach((t) => t.stop());
    audioCtxRef.current?.close().catch(() => {});
    wsRef.current?.close();
  }, []);

  useEffect(() => {
    let cancelled = false;

    (async () => {
      try {
        const settingsRes = await fetch(`${apiBase}/settings`);
        const settings = await settingsRes.json();
        const apiKey = settings.yunwu_api_key;
        if (!apiKey) {
          setStatus("error");
          setErrorMsg("No API key configured. Set YUNWU_API_KEY in .env");
          return;
        }

        const stream = await navigator.mediaDevices.getUserMedia({ audio: { sampleRate: 24000, channelCount: 1, echoCancellation: true } });
        if (cancelled) { stream.getTracks().forEach((t) => t.stop()); return; }
        streamRef.current = stream;

        const ws = new WebSocket(WS_URL);
        wsRef.current = ws;

        ws.onopen = () => {
          ws.send(JSON.stringify({
            type: "session.update",
            session: {
              modalities: ["text", "audio"],
              instructions: "You are ChatFiles, a local file search assistant. Be concise. Use the search_files tool when the user asks about their files.",
              voice: "alloy",
              input_audio_transcription: { model: "whisper-1" },
              tools: [{
                type: "function",
                name: "search_files",
                description: "Search user's indexed local files",
                parameters: { type: "object", properties: { query: { type: "string" } }, required: ["query"] },
              }],
            },
          }));

          const audioCtx = new AudioContext({ sampleRate: 24000 });
          audioCtxRef.current = audioCtx;

          const source = audioCtx.createMediaStreamSource(stream);
          const processor = audioCtx.createScriptProcessor(4096, 1, 1);
          processor.onaudioprocess = (e) => {
            const input = e.inputBuffer.getChannelData(0);
            const pcm16 = new Int16Array(input.length);
            for (let i = 0; i < input.length; i++) {
              pcm16[i] = Math.max(-32768, Math.min(32767, Math.round(input[i] * 32767)));
            }
            const b64 = btoa(String.fromCharCode(...new Uint8Array(pcm16.buffer)));
            ws.send(JSON.stringify({ type: "input_audio_buffer.append", audio: b64 }));
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
              break;
            case "response.audio_transcript.delta":
              setAiText((prev) => prev + (data.delta || ""));
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
                  const res = await fetch(`${apiBase}/search`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ query: args.query, type: "files", limit: 5 }),
                  });
                  const sData = await res.json();
                  const summary = (sData.results || [])
                    .map((r: any) => `${r.path.split("/").pop()}: ${(r.summary || "").slice(0, 200)}`)
                    .join("\n");
                  ws.send(JSON.stringify({ type: "conversation.item.create", item: { type: "function_call_output", call_id: data.call_id, output: summary || "No files found." } }));
                  ws.send(JSON.stringify({ type: "response.create" }));
                } catch {
                  ws.send(JSON.stringify({ type: "conversation.item.create", item: { type: "function_call_output", call_id: data.call_id, output: "Search error." } }));
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
              setErrorMsg(data.error?.message || "Voice connection error");
              break;
          }
        };

        ws.onerror = () => { setStatus("error"); setErrorMsg("WebSocket connection failed"); };
        ws.onclose = () => { if (!cancelled) onClose(); };
      } catch (err: any) {
        setStatus("error");
        setErrorMsg(err.message || "Failed to start voice");
      }
    })();

    return () => { cancelled = true; cleanup(); };
  }, [apiBase, cleanup, onClose]);

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
      audioQueueRef.current.push(source);
      source.onended = () => {
        audioQueueRef.current = audioQueueRef.current.filter((s) => s !== source);
      };
    } catch {}
  };

  const ringVariants = {
    listening: { scale: [1, 1.4, 1], opacity: [0.4, 0, 0.4] },
    speaking: { scale: [1, 1.2, 1], opacity: [0.3, 0.1, 0.3] },
  };

  return (
    <div className="flex flex-col items-center py-8 px-4">
      {/* Pulsing rings */}
      <div className="relative w-20 h-20 mb-4">
        {status === "listening" || status === "speaking" ? (
          <>
            <motion.div
              className={`absolute inset-0 rounded-full ${status === "listening" ? "bg-red-500/20" : "bg-green-500/20"}`}
              animate={ringVariants[status]}
              transition={{ duration: 1.5, repeat: Infinity }}
            />
            <motion.div
              className={`absolute inset-2 rounded-full ${status === "listening" ? "bg-red-500/15" : "bg-green-500/15"}`}
              animate={ringVariants[status]}
              transition={{ duration: 1.5, repeat: Infinity, delay: 0.3 }}
            />
          </>
        ) : null}

        <div className={`absolute inset-0 m-auto w-14 h-14 rounded-full flex items-center justify-center ${
          status === "listening" ? "bg-red-500/30" :
          status === "speaking" ? "bg-green-500/30" :
          status === "error" ? "bg-red-900/30" : "bg-zinc-800"
        }`}>
          {status === "connecting" || status === "thinking" ? (
            <Loader2 size={24} className="text-brand-400 animate-spin" />
          ) : status === "error" ? (
            <MicOff size={24} className="text-red-400" />
          ) : (
            <Mic size={24} className={status === "listening" ? "text-red-400" : "text-green-400"} />
          )}
        </div>
      </div>

      {/* Status text */}
      <motion.p
        key={status}
        initial={{ opacity: 0, y: 4 }}
        animate={{ opacity: 1, y: 0 }}
        className={`text-sm mb-2 ${
          status === "error" ? "text-red-400" :
          status === "listening" ? "text-red-300" :
          status === "speaking" ? "text-green-300" : "text-zinc-400"
        }`}
      >
        {status === "connecting" && "Connecting..."}
        {status === "listening" && "Listening..."}
        {status === "thinking" && "Searching files..."}
        {status === "speaking" && "Speaking..."}
        {status === "error" && (errorMsg || "Error")}
      </motion.p>

      {transcript && (
        <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-xs text-zinc-500 text-center max-w-sm mb-1">
          &ldquo;{transcript}&rdquo;
        </motion.p>
      )}
      {aiText && (
        <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-xs text-zinc-300 text-center max-w-sm">
          {aiText}
        </motion.p>
      )}

      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => { cleanup(); onClose(); }}
        className="mt-4 flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800 transition-colors"
      >
        <X size={12} /> Press Esc to close
      </motion.button>
    </div>
  );
}
