# Mighty Chatbot

Production-grade customer-service chatbot built on FastAPI + Claude + Next.js.

**Live:**
- Frontend: https://frontend-ten-zeta-37.vercel.app
- Backend: https://mighty-chatbot.fly.dev/health

---

## Architecture

```
Browser (Next.js / Vercel)
         │
         │  HTTPS
         ▼
  ┌──────────────────┐
  │  FastAPI backend │   fly.io  (region: iad, US-East)
  │  ─────────────── │
  │  /health         │   Day 1 — scaffold only
  │  /chat  (Day 2)  │ ◄── Claude Haiku (routing)
  │  /resolve (Day2) │ ◄── Claude Sonnet (resolution)
  │                  │
  │  ChromaDB        │   Day 3 — vector store (in-process)
  │  Supabase client │   Day 3 — Postgres + Auth
  └──────────────────┘
         │
         ▼
   Supabase Postgres   (managed, Day 3+)
```

**Day 1 state:** skeleton only — `/health` returns `{"status":"ok"}`. No LLM calls, no auth, no vector store.

---

## Stack

| Layer | Choice | Why |
|---|---|---|
| Backend | FastAPI (Python) | Async, type-safe, production-ready |
| Python tooling | `uv` | Modern, fast; replaces pip/venv |
| LLM routing | Claude Haiku (`claude-haiku-4-5-20251001`) | Low-latency, cheap intent classification |
| LLM resolution | Claude Sonnet (`claude-sonnet-4-6`) | Quality responses for complex queries |
| Vector DB | ChromaDB (in-process) | Zero-infra RAG, Day 3+ |
| Auth + Postgres | Supabase | Auth + DB bundle; customer_id from JWT |
| Frontend | Next.js 16 + TypeScript + Tailwind | App Router, type-safe, production-ready |
| Backend deploy | Fly.io (`iad`) | US-East minimises Anthropic API latency |
| Frontend deploy | Vercel | GitHub-connected, instant previews |
| Logging | structlog → JSON stdout | Fly streams stdout; grep-friendly |
| Evals | pytest (Day 4+) | 50-100 golden-set queries |

---

## Local Development

### Prerequisites

- Python ≥ 3.12
- Node.js ≥ 20
- [`uv`](https://docs.astral.sh/uv/) — `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [`flyctl`](https://fly.io/docs/hands-on/install-flyctl/) (optional, for deploy)

### Backend

```bash
cd backend
uv sync                              # install deps + create .venv
cp .env.example .env                 # fill in secrets
uv run uvicorn app.main:app --reload --port 8080
# → http://localhost:8080/health
```

Run tests:

```bash
uv run pytest -v
```

### Frontend

```bash
cd frontend
cp .env.local.example .env.local     # sets NEXT_PUBLIC_BACKEND_URL=http://localhost:8080
npm install
npm run dev
# → http://localhost:3000
```

---

## Build Plan (9-item checklist)

- [x] Day 1 — Skeleton: FastAPI + Next.js deployed, `/health` live
- [ ] Day 2 — Intent routing: order status (deterministic)
- [ ] Day 2 — LLM integration: Claude Haiku for classification
- [ ] Day 3 — RAG: ChromaDB + refund policy intent
- [ ] Day 3 — Auth: Supabase JWT, real `customer_id`
- [ ] Day 4 — Handoff intent: talk-to-agent flow
- [ ] Day 4 — Ambiguity: low-confidence fallback
- [ ] Day 5 — Evals: pytest golden-set 50-100 queries
- [ ] Day 5 — Polish: CORS tightened, Better Stack logs, README final

---

## Project Structure

```
chatbot/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app, CORS, structlog
│   │   ├── config.py        # pydantic-settings
│   │   └── routes/
│   │       └── health.py    # GET /health
│   ├── tests/
│   │   └── test_health.py
│   ├── pyproject.toml       # uv + hatchling
│   ├── Dockerfile
│   └── fly.toml
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   └── chat.tsx         # chat shell (input stubbed Day 1)
│   ├── lib/
│   │   └── api.ts           # checkHealth(), future chat API
│   └── package.json
├── eval/                    # golden-set evals, Day 4+
├── LEARNING-LOG.md
└── README.md
```
