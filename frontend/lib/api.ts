const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8080";

export async function checkHealth(): Promise<{ status: string }> {
  const res = await fetch(`${BACKEND_URL}/health`);
  if (!res.ok) throw new Error(`Health check failed: ${res.status}`);
  return res.json();
}

export interface ChatResponse {
  reply: string;
  intent: string;
  confidence: number;
  low_confidence: boolean;
}

export async function sendMessage(message: string): Promise<ChatResponse> {
  const res = await fetch(`${BACKEND_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) throw new Error(`Chat request failed: ${res.status}`);
  return res.json();
}
