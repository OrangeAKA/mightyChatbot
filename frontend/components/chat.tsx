"use client";

import { useEffect, useRef, useState } from "react";
import { checkHealth, sendMessage, type ChatResponse } from "@/lib/api";

type BackendStatus = "checking" | "ok" | "error";

interface Message {
  role: "user" | "assistant";
  text: string;
  meta?: Pick<ChatResponse, "intent" | "confidence" | "low_confidence">;
}

export default function Chat() {
  const [status, setStatus] = useState<BackendStatus>("checking");
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    checkHealth()
      .then(() => setStatus("ok"))
      .catch(() => setStatus("error"));
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend() {
    const text = input.trim();
    if (!text || loading) return;

    setMessages((prev) => [...prev, { role: "user", text }]);
    setInput("");
    setLoading(true);

    try {
      const res = await sendMessage(text);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: res.reply,
          meta: { intent: res.intent, confidence: res.confidence, low_confidence: res.low_confidence },
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: "Sorry, I couldn't reach the backend. Please try again." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter" && !e.shiftKey) handleSend();
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <header className="bg-white border-b px-6 py-4 flex items-center justify-between">
        <h1 className="text-lg font-semibold text-gray-900">Mighty Chatbot</h1>
        <BackendBadge status={status} />
      </header>

      <main className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {messages.length === 0 && (
          <p className="text-center text-gray-400 text-sm mt-16">
            Try: &quot;Where is my order ORD-001?&quot; or &quot;Can I get a refund?&quot;
          </p>
        )}
        {messages.map((msg, i) => (
          <MessageBubble key={i} msg={msg} />
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white border rounded-2xl px-4 py-2 text-sm text-gray-400">
              thinking…
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </main>

      <footer className="bg-white border-t px-6 py-4">
        <div className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={status !== "ok" || loading}
            placeholder={status === "ok" ? "Type a message…" : "Connecting…"}
            className="flex-1 rounded-lg border border-gray-200 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50 disabled:text-gray-400"
          />
          <button
            onClick={handleSend}
            disabled={status !== "ok" || loading || !input.trim()}
            className="rounded-lg bg-blue-600 px-5 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            Send
          </button>
        </div>
      </footer>
    </div>
  );
}

function MessageBubble({ msg }: { msg: Message }) {
  const isUser = msg.role === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div className="max-w-[75%] space-y-1">
        <div
          className={`rounded-2xl px-4 py-2 text-sm ${
            isUser
              ? "bg-blue-600 text-white rounded-br-sm"
              : "bg-white border text-gray-800 rounded-bl-sm"
          }`}
        >
          {msg.text}
        </div>
        {msg.meta && <IntentBadge meta={msg.meta} />}
      </div>
    </div>
  );
}

function IntentBadge({
  meta,
}: {
  meta: Pick<ChatResponse, "intent" | "confidence" | "low_confidence">;
}) {
  return (
    <p className="text-xs text-gray-400 px-1">
      {meta.intent} · {(meta.confidence * 100).toFixed(0)}%
      {meta.low_confidence && (
        <span className="ml-1 text-amber-500 font-medium">low confidence</span>
      )}
    </p>
  );
}

function BackendBadge({ status }: { status: BackendStatus }) {
  const styles: Record<BackendStatus, string> = {
    checking: "bg-yellow-100 text-yellow-700",
    ok: "bg-green-100 text-green-700",
    error: "bg-red-100 text-red-700",
  };
  const labels: Record<BackendStatus, string> = {
    checking: "connecting…",
    ok: "backend ok",
    error: "backend error",
  };
  return (
    <span className={`rounded-full px-3 py-1 text-xs font-medium ${styles[status]}`}>
      {labels[status]}
    </span>
  );
}
