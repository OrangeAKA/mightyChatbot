# Chatbot Build — Claude Code Context

## What This Is

A production-grade customer-service chatbot built end-to-end for interview defensibility.
Owner: Akhil (PM at Reward360, interviewing for Sr. PM AI Agents at Eltropy).
Goal: Close the prototype-to-production perception gap — build and deploy a real system
so every technical probe from Sai Bhaskar (interviewer) can be answered from hands-on knowledge.

**Success metric: interview defensibility, not features or users.**

---

## Spec Files (source of truth)

- Architecture, stack, scoping rules, 9-item checklist:
  `/Users/krishnaakhil/Library/CloudStorage/GoogleDrive-allumoluakhil@gmail.com/My Drive/Akhil's Claudia/Interview/Interview Prep/companies/eltropy/chatbot-build-kickoff.md`

- Workflow rules (how Akhil and Claude Code work together):
  `/Users/krishnaakhil/Library/CloudStorage/GoogleDrive-allumoluakhil@gmail.com/My Drive/Akhil's Claudia/Interview/Interview Prep/companies/eltropy/build-learning-loop.md`

Read these only if directed to. The decisions below are already canonicalized here.

---

## Stack (LOCKED — do not substitute without raising it explicitly)

| Layer | Choice |
|---|---|
| Backend | FastAPI (Python), managed with `uv` |
| LLM routing | Claude Haiku (`claude-haiku-4-5-20251001`) |
| LLM resolution | Claude Sonnet (`claude-sonnet-4-6`) |
| Vector DB | ChromaDB (in-process, Day 3+) |
| Relational DB + Auth | Supabase (Postgres + Supabase Auth) |
| Frontend | Next.js (App Router) + TypeScript + Tailwind |
| Backend deploy | Fly.io, region `iad` (US-East) |
| Frontend deploy | Vercel (connected to GitHub) |
| Python tooling | `uv` (not pip/venv) |
| Logging | `structlog` → structured JSON to stdout from Day 1 |
| Eval | pytest-based, 50-100 golden-set queries |

---

## Approved Decisions (from pre-build discussion)

- **`uv` over pip/venv** — modern Python toolchain, defensible in interview
- **Tailwind on Day 1** — faster than hand-rolling CSS; UI is allowed ugly
- **Fly.io region `iad`** — US-East minimizes Anthropic API round-trip latency
- **structlog to stdout Day 1** — Fly streams stdout; Better Stack deferred to polish phase
- **Supabase** — auth+DB bundle means customer_id is a real JWT claim, not a hardcoded string
- **Deferred deps** — install `anthropic`, `supabase`, `chromadb` only when the layer that needs them lands; no pre-installing

---

## Day 1 Plan (not yet started)

Goal: skeleton deployed. No LLM. No intents. Just the scaffold.

1. Scaffold repo (structure below)
2. Wire `/health` endpoint on FastAPI
3. Frontend renders a minimal chat UI that calls `/health` on load
4. Deploy backend to Fly.io, frontend to Vercel
5. Push to private GitHub repo
6. Write README with architecture diagram, stack, run locally, deployed URLs

**Success criterion:** public URL in browser → chat UI → type "hello" → response from deployed backend.

### Proposed File Structure

```
chatbot/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app, CORS
│   │   ├── config.py            # pydantic-settings
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── health.py        # GET /health → {"status": "ok"}
│   ├── tests/
│   │   └── test_health.py
│   ├── pyproject.toml
│   ├── Dockerfile
│   ├── fly.toml
│   └── .env.example
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   │   └── chat.tsx
│   ├── lib/
│   │   └── api.ts
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.ts
│   └── .env.local.example
├── eval/
│   └── README.md
├── infra/
│   └── README.md
├── .gitignore
├── README.md
└── LEARNING-LOG.md
```

---

## How We Work Together (from build-learning-loop.md)

These rules change Claude's default behavior. Follow them exactly:

1. **Explain-why-first before any code.** Before writing code that involves a choice, explain:
   (1) what other options exist, (2) why this one, (3) tradeoffs, (4) what Akhil should be able
   to defend in interview. Then wait for approval.

2. **One vertical slice at a time.** Don't pre-build for the next intent. Build order:
   - Intent 1: Order status (deterministic path)
   - Intent 2: Refund policy (LLM + RAG)
   - Intent 3: Talk to agent (handoff)
   - Intent 4: Account help with low-confidence ambiguity

3. **Commit often.** Every meaningful change is its own commit with a descriptive message.

4. **Honest gap reporting.** If something is mocked or stubbed, say so in the code comment
   AND flag it to Akhil. Mocks are fine — pretending they're real is not.

5. **No feature creep.** If Akhil proposes something outside the 4-intent scope, push back.

6. **Cost awareness from Day 1.** Every LLM call logs token usage and latency.

7. **LEARNING-LOG.md** — At the end of each session, Akhil writes in his own words what
   was built, decisions made, and what he'd struggle to explain. Never skip this step.

---

## Things Still Pending Before Day 1 Execution Starts

- [ ] Confirm Fly.io app name (suggestion: `chatbot-backend-akhil`)
- [ ] Confirm GitHub repo name (suggestion: `chatbot`)
- [ ] `flyctl` installed and `fly auth login` done (run: `! fly auth login`)
- [ ] Vercel account connected to GitHub, OR Vercel CLI authed
- [ ] `gh` CLI authenticated (`gh auth status` should pass)
- [ ] Anthropic API key ready in password manager (not used Day 1, needed Day 2)
- [ ] Supabase project created (not used Day 1, needed Day 3)
