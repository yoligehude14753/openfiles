import { useRef, useEffect } from "react";
import { useStore } from "../../stores/useStore";
import { api } from "../../services/api";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";
import WelcomeScreen from "./WelcomeScreen";

export default function ChatView() {
  const {
    messages,
    setMessages,
    addMessage,
    streamMessage,
    setStreamMessage,
    appendStreamContent,
    currentConversationId,
    setCurrentConversationId,
    isLoading,
    setIsLoading,
    conversations,
    setConversations,
  } = useStore();

  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, streamMessage?.content]);

  const handleSend = async (text: string) => {
    const userMsg = {
      id: Date.now(),
      role: "user" as const,
      content: text,
      created_at: new Date().toISOString(),
    };
    addMessage(userMsg);
    setIsLoading(true);
    setStreamMessage({ role: "assistant", content: "", isStreaming: true });

    try {
      const resp = await api.sendMessage(text, currentConversationId ?? undefined);

      if (!currentConversationId) {
        setCurrentConversationId(resp.conversation_id);
        const convs = await api.getConversations();
        setConversations(convs);
      }

      const assistantMsg = {
        id: Date.now() + 1,
        role: "assistant" as const,
        content: resp.message,
        sources: resp.sources,
        created_at: new Date().toISOString(),
      };
      addMessage(assistantMsg);
      setStreamMessage(null);
    } catch (err: any) {
      setStreamMessage(null);
      addMessage({
        id: Date.now() + 1,
        role: "assistant",
        content: `Error: ${err.message || "Failed to get response"}`,
        created_at: new Date().toISOString(),
      });
    } finally {
      setIsLoading(false);
    }
  };

  const isEmpty = messages.length === 0 && !streamMessage;

  return (
    <div className="flex flex-col h-full">
      <div ref={scrollRef} className="flex-1 overflow-y-auto">
        {isEmpty ? (
          <WelcomeScreen onSuggestionClick={handleSend} />
        ) : (
          <div className="pb-4">
            {messages.map((msg) => (
              <ChatMessage
                key={msg.id}
                role={msg.role}
                content={msg.content}
                sources={msg.sources}
              />
            ))}
            {streamMessage && (
              <ChatMessage
                role="assistant"
                content={streamMessage.content || "Thinking..."}
                sources={streamMessage.sources}
                isStreaming={streamMessage.isStreaming}
              />
            )}
          </div>
        )}
      </div>
      <ChatInput onSend={handleSend} disabled={isLoading} />
    </div>
  );
}
