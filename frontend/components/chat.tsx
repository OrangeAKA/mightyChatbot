"use client";

import { useEffect, useState } from "react";
import { checkHealth } from "@/lib/api";

type BackendStatus = "checking" | "ok" | "error";

export default function Chat() {
  const [status, setStatus] = useState<BackendStatus>("checking");

  useEffect(() => {
    checkHealth()
      .then(() => setStatus("ok"))
      .catch(() => setStatus("error"));
  }, []);

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b px-6 py-4 flex items-center justify-between">
        <h1 className="text-lg font-semibold text-gray-900">Mighty Chatbot</h1>
        <BackendBadge status={status} />
      </header>

      {/* Chat area — empty on Day 1, messages land here Day 2+ */}
      <main className="flex-1 overflow-y-auto px-6 py-4 flex items-center justify-center">
        <p className="text-gray-400 text-sm">
          {status === "checking" && "Connecting to backend…"}
          {status === "ok" && "Backend connected. Type a message to start. (Day 2)"}
          {status === "error" && "Could not reach backend. Is it deployed?"}
        </p>
      </main>

      {/* Input — stubbed, wired to LLM on Day 2 */}
      {/* STUB: input does nothing yet — chat logic lands Day 2 */}
      <footer className="bg-white border-t px-6 py-4">
        <div className="flex gap-3">
          <input
            type="text"
            disabled
            placeholder="Chat coming Day 2…"
            className="flex-1 rounded-lg border border-gray-200 px-4 py-2 text-sm bg-gray-50 text-gray-400 cursor-not-allowed"
          />
          <button
            disabled
            className="rounded-lg bg-blue-600 px-5 py-2 text-sm font-medium text-white opacity-40 cursor-not-allowed"
          >
            Send
          </button>
        </div>
      </footer>
    </div>
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
